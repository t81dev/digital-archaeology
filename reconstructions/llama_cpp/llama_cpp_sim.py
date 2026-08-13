#!/usr/bin/env python3
"""
llama.cpp Lineage Reconstruction Simulator.
Demonstrates the core architectural and numerical abstractions of:
1. GGUF unified single-file binary container format (metadata + aligned tensors).
2. Q4_0 block-wise integer quantization (grouping elements into blocks sharing scale factors).
3. Dequantization-on-the-fly inside low-precision matrix multiplication (GEMV/GEMM).
4. KV-cache capacity and memory overhead projection across varying context sequences.
"""

import struct
from typing import List, Dict, Any, Tuple, Optional

# =====================================================================
# 1. GGUF Container Specification Simulator
# =====================================================================

class GGUFContainer:
    """
    Simulates GGUF binary container serialization and deserialization.
    Allows packing metadata key-value pairs and raw aligned tensors into a single continuous byte stream.
    To allow dynamic zero-copy execution via mmap, GGUF enforces strict alignment (usually 32 bytes).
    """
    GGUF_MAGIC = b"GGUF"
    GGUF_VERSION = 3

    # GGUF Metadata Value Types
    TYPE_UINT32 = 0
    TYPE_INT32 = 1
    TYPE_FLOAT32 = 2
    TYPE_STRING = 3

    @classmethod
    def get_tensor_size(cls, shape: List[int], qtype: str) -> int:
        """Computes the exact unpadded byte size of a tensor based on shape and quant type."""
        elements = 1
        for dim in shape:
            elements *= dim

        if qtype == "q4_0":
            # 18 bytes per block of 32 elements
            blocks = (elements + 31) // 32
            return blocks * 18
        elif qtype == "fp32":
            return elements * 4
        else:
            return elements

    @classmethod
    def serialize(cls, metadata: Dict[str, Tuple[int, Any]], tensors: Dict[str, Tuple[List[int], str, bytes]], alignment: int = 32) -> bytes:
        """
        Serializes metadata and tensors into a single GGUF binary payload.

        Args:
            metadata: Dict of { key_string: (value_type_id, value_payload) }
            tensors: Dict of { tensor_name: (shape_list, quant_type_string, raw_bytes) }
            alignment: Byte-boundary alignment for raw tensor segments.
        """
        # Pack Header: Magic (4B) + Version (4B) + Tensor Count (8B) + Metadata Count (8B)
        payload = bytearray()
        payload.extend(cls.GGUF_MAGIC)
        payload.extend(struct.pack("<I", cls.GGUF_VERSION))
        payload.extend(struct.pack("<Q", len(tensors)))
        payload.extend(struct.pack("<Q", len(metadata)))

        # Pack Metadata Key-Value pairs
        for key, (val_type, val) in metadata.items():
            # Key string representation: length (8B) + key bytes
            key_bytes = key.encode("utf-8")
            payload.extend(struct.pack("<Q", len(key_bytes)))
            payload.extend(key_bytes)

            # Value type (4B)
            payload.extend(struct.pack("<I", val_type))

            # Value encoding
            if val_type == cls.TYPE_UINT32:
                payload.extend(struct.pack("<I", val))
            elif val_type == cls.TYPE_INT32:
                payload.extend(struct.pack("<i", val))
            elif val_type == cls.TYPE_FLOAT32:
                payload.extend(struct.pack("<f", val))
            elif val_type == cls.TYPE_STRING:
                val_bytes = val.encode("utf-8")
                payload.extend(struct.pack("<Q", len(val_bytes)))
                payload.extend(val_bytes)
            else:
                raise ValueError(f"Unsupported metadata value type ID: {val_type}")

        # Pack Tensor Information Records (Index block)
        # GGUF writes tensor directory info BEFORE the aligned tensor binaries
        tensor_data_offsets = {}
        current_offset = 0

        # Pre-calculate aligned offsets
        header_index_len = 0  # We will track where raw tensors start

        # We temporarily serialize tensor headers to compute their binary size
        tensor_headers = bytearray()
        for name, (shape, qtype, raw_data) in tensors.items():
            name_bytes = name.encode("utf-8")
            tensor_headers.extend(struct.pack("<Q", len(name_bytes)))
            tensor_headers.extend(name_bytes)

            # Dimensions count (4B) + Dimensions (8B each)
            tensor_headers.extend(struct.pack("<I", len(shape)))
            for dim in shape:
                tensor_headers.extend(struct.pack("<Q", dim))

            # Quantization type string: length (8B) + string bytes
            qtype_bytes = qtype.encode("utf-8")
            tensor_headers.extend(struct.pack("<Q", len(qtype_bytes)))
            tensor_headers.extend(qtype_bytes)

            # Offset inside the binary segment (8B) - to be filled
            # We record placeholder offset
            tensor_headers.extend(struct.pack("<Q", 0))

        # Re-serialize header index correctly calculating aligned offsets
        # Start of raw tensor blocks starts immediately after: Header + Metadata + Tensor Headers
        raw_tensor_start_pos = len(payload) + len(tensor_headers)

        # We need to make sure the first tensor starts at an aligned offset
        padding_to_align = (alignment - (raw_tensor_start_pos % alignment)) % alignment
        raw_tensor_start_pos += padding_to_align

        # Write actual tensor catalog records with real absolute/relative offsets
        running_tensor_offset = 0
        for name, (shape, qtype, raw_data) in tensors.items():
            name_bytes = name.encode("utf-8")
            payload.extend(struct.pack("<Q", len(name_bytes)))
            payload.extend(name_bytes)

            payload.extend(struct.pack("<I", len(shape)))
            for dim in shape:
                payload.extend(struct.pack("<Q", dim))

            qtype_bytes = qtype.encode("utf-8")
            payload.extend(struct.pack("<Q", len(qtype_bytes)))
            payload.extend(qtype_bytes)

            # Record offset relative to the raw tensor block start
            # Align the offset for each tensor within the block
            padding_t = (alignment - (running_tensor_offset % alignment)) % alignment
            running_tensor_offset += padding_t

            payload.extend(struct.pack("<Q", running_tensor_offset))
            tensor_data_offsets[name] = running_tensor_offset

            running_tensor_offset += len(raw_data)

        # Pad payload to meet the alignment block
        current_len = len(payload)
        pad_len = (alignment - (current_len % alignment)) % alignment
        payload.extend(b"\x00" * pad_len)

        # Write aligned raw tensor payloads
        for name, (shape, qtype, raw_data) in tensors.items():
            # Align current binary offset
            curr_pos = len(payload) - (current_len + pad_len)
            t_offset = tensor_data_offsets[name]
            # Write padding if offset doesn't match current relative position
            if curr_pos < t_offset:
                payload.extend(b"\x00" * (t_offset - curr_pos))
            payload.extend(raw_data)

        return bytes(payload)

    @classmethod
    def deserialize(cls, gguf_data: bytes) -> Tuple[Dict[str, Any], Dict[str, Tuple[List[int], str, bytes]]]:
        """
        Deserializes a GGUF binary payload back into metadata and raw aligned tensors.
        """
        if len(gguf_data) < 24:
            raise ValueError("GGUF payload too small to parse.")

        magic = gguf_data[0:4]
        if magic != cls.GGUF_MAGIC:
            raise ValueError(f"Invalid GGUF Magic header: {magic}")

        version = struct.unpack("<I", gguf_data[4:8])[0]
        if version != cls.GGUF_VERSION:
            raise ValueError(f"Unsupported GGUF version: {version}")

        tensor_count = struct.unpack("<Q", gguf_data[8:16])[0]
        metadata_count = struct.unpack("<Q", gguf_data[16:24])[0]

        idx = 24
        metadata = {}

        # Parse Metadata Key-Value pairs
        for _ in range(metadata_count):
            # Parse Key
            key_len = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
            idx += 8
            key = gguf_data[idx:idx+key_len].decode("utf-8")
            idx += key_len

            # Parse Value Type
            val_type = struct.unpack("<I", gguf_data[idx:idx+4])[0]
            idx += 4

            # Parse Value
            if val_type == cls.TYPE_UINT32:
                val = struct.unpack("<I", gguf_data[idx:idx+4])[0]
                idx += 4
            elif val_type == cls.TYPE_INT32:
                val = struct.unpack("<i", gguf_data[idx:idx+4])[0]
                idx += 4
            elif val_type == cls.TYPE_FLOAT32:
                val = struct.unpack("<f", gguf_data[idx:idx+4])[0]
                idx += 4
            elif val_type == cls.TYPE_STRING:
                val_len = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
                idx += 8
                val = gguf_data[idx:idx+val_len].decode("utf-8")
                idx += val_len
            else:
                raise ValueError(f"Unknown metadata type ID during deserialization: {val_type}")

            metadata[key] = val

        # Parse Tensor Catalog
        tensor_catalog = []
        for _ in range(tensor_count):
            name_len = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
            idx += 8
            name = gguf_data[idx:idx+name_len].decode("utf-8")
            idx += name_len

            dims_count = struct.unpack("<I", gguf_data[idx:idx+4])[0]
            idx += 4

            shape = []
            for _ in range(dims_count):
                dim = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
                idx += 8
                shape.append(dim)

            qtype_len = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
            idx += 8
            qtype = gguf_data[idx:idx+qtype_len].decode("utf-8")
            idx += qtype_len

            offset = struct.unpack("<Q", gguf_data[idx:idx+8])[0]
            idx += 8

            tensor_catalog.append((name, shape, qtype, offset))

        # Resolve aligned raw tensor binary segments
        # To find the relative start of the raw tensor block, we align idx
        # Standard GGUF alignment is 32 bytes
        alignment = 32
        pad_offset = (alignment - (idx % alignment)) % alignment
        raw_tensor_block_start = idx + pad_offset

        tensors = {}
        for i, (name, shape, qtype, offset) in enumerate(tensor_catalog):
            # Calculate actual unpadded tensor length
            tensor_size = cls.get_tensor_size(shape, qtype)
            start_pos = raw_tensor_block_start + offset
            end_pos = start_pos + tensor_size

            tensor_bytes = gguf_data[start_pos:end_pos]
            tensors[name] = (shape, qtype, tensor_bytes)

        return metadata, tensors


# =====================================================================
# 2. Q4_0 Block Quantizer & Core Mathematics
# =====================================================================

class Q4_0Quantizer:
    """
    Implements Q4_0 block quantization.
    Segments raw float32 streams into contiguous chunks of block size B (typically 32).
    For each block:
      - Finds the maximum absolute weight value.
      - Calculates a 16-bit float scale factor: d = max(abs(min) / 8, abs(max) / 7).
      - Fits floats into 4-bit unsigned integers: q = round(x / d).
      - Constrains 4-bit integers to interval [-8, 7] represented as [0, 15] offset-centered.
    """
    BLOCK_SIZE = 32

    @classmethod
    def quantize(cls, floats: List[float]) -> bytes:
        """
        Compresses standard FP32 weight arrays into 4-bit block-quantized Q4_0 binary stream.
        Each block yields:
          - Scale factor d: float16 (2 bytes)
          - 32 nibbles (4-bit chunks) packed into 16 bytes.
          Total size per 32 weights = 18 bytes (saving 86% memory footprint).
        """
        # Pad list of floats if not multiples of BLOCK_SIZE
        remainder = len(floats) % cls.BLOCK_SIZE
        if remainder > 0:
            floats = floats + [0.0] * (cls.BLOCK_SIZE - remainder)

        payload = bytearray()
        for b in range(0, len(floats), cls.BLOCK_SIZE):
            block = floats[b : b + cls.BLOCK_SIZE]

            # Find scale d to perfectly prevent positive or negative saturation
            min_val = min(block)
            max_val = max(block)
            max_abs = max(abs(min_val), abs(max_val))

            if max_abs == 0.0:
                d = 0.0
            else:
                # Center around 8: negative goes down to -8, positive goes up to +7
                d = max(abs(min_val) / 8.0, abs(max_val) / 7.0)

            # Convert d to float16 binary (simulated via standard float32 unpack/pack)
            # We store as 16-bit half-precision float format 'e'
            d_half_bytes = struct.pack("<e", d)
            payload.extend(d_half_bytes)

            # Quantize values to 4-bit unsigned nibbles [0, 15] centered around 8
            # Formula: q = round(x / d) + 8
            nibbles = []
            for x in block:
                if d == 0.0:
                    q = 8
                else:
                    q = int(round(x / d)) + 8
                    q = max(0, min(15, q)) # saturate to 4 bits
                nibbles.append(q)

            # Pack 32 nibbles into 16 bytes (two 4-bit nibbles per byte)
            for i in range(0, cls.BLOCK_SIZE, 2):
                low_nibble = nibbles[i] & 0x0F
                high_nibble = nibbles[i+1] & 0x0F
                byte_val = low_nibble | (high_nibble << 4)
                payload.append(byte_val)

        return bytes(payload)

    @classmethod
    def dequantize(cls, q4_bytes: bytes, count: int) -> List[float]:
        """
        Decompresses Q4_0 binary bytes back into a float32 array.
        """
        floats = []
        idx = 0
        blocks_needed = (count + cls.BLOCK_SIZE - 1) // cls.BLOCK_SIZE

        for _ in range(blocks_needed):
            if idx >= len(q4_bytes):
                break

            # Extract 2-byte float16 scale factor d
            d = struct.unpack("<e", q4_bytes[idx : idx+2])[0]
            idx += 2

            # Extract 16 bytes containing 32 nibbles
            nibbles_bytes = q4_bytes[idx : idx+16]
            idx += 16

            for byte_val in nibbles_bytes:
                # Retrieve two 4-bit nibbles
                low_q = byte_val & 0x0F
                high_q = (byte_val >> 4) & 0x0F

                # Dequantize: x = d * (q - 8)
                floats.append(d * (low_q - 8))
                floats.append(d * (high_q - 8))

        return floats[:count]


# =====================================================================
# 3. Low-Bit Quantized Matrix Multiplication Engine
# =====================================================================

class QuantizedLinearMath:
    """
    Simulates memory-bandwidth-aware matrix multiplication (GEMV/GEMM).
    Performs matrix operations directly over the low-precision block weights,
    performing dequantization-on-the-fly directly within CPU execution loops,
    avoiding dynamic high-precision memory allocations.
    """

    @staticmethod
    def gemv_q4_0(x: List[float], q_weight: bytes, q_shape: List[int]) -> List[float]:
        """
        Performs matrix-vector multiplication Y = W * X.
        Where W is a Q4_0 quantized weight matrix.
        We stream the 4-bit nibbles of W, dequantize on-the-fly, and accumulate in FP32.

        Args:
            x: Input activations vector of length K (float32 list).
            q_weight: Raw quantized Q4_0 byte payload.
            q_shape: Shape of W matrix [Rows, Cols] (where Cols matches length of X, which is K).
        """
        rows, cols = q_shape
        if len(x) != cols:
            raise ValueError(f"Matrix column dimension {cols} does not match vector length {len(x)}.")

        block_size = Q4_0Quantizer.BLOCK_SIZE
        bytes_per_block = 18 # 2B scale + 16B payload

        y = [0.0] * rows

        # W rows represents matrix output dimensions
        for r in range(rows):
            row_sum = 0.0
            # Track binary offset of weight row W[r, :]
            row_bytes_offset = r * (cols // block_size) * bytes_per_block

            # Iterate columns in groups of block size B (32 elements)
            for b in range(0, cols, block_size):
                block_offset = row_bytes_offset + (b // block_size) * bytes_per_block

                # Retrieve scale factor d (FP16) from block start
                d = struct.unpack("<e", q_weight[block_offset : block_offset+2])[0]

                # Dequantize block and perform vector dot-product accumulation
                # Accumulate: sum_i( x_i * d * (q_i - 8) )
                for nibble_idx in range(16):
                    byte_val = q_weight[block_offset + 2 + nibble_idx]

                    # Unpack dual 4-bit nibbles
                    low_q = byte_val & 0x0F
                    high_q = (byte_val >> 4) & 0x0F

                    # Calculate physical index
                    idx_1 = b + nibble_idx * 2
                    idx_2 = idx_1 + 1

                    # Accumulate dot-product on-the-fly
                    row_sum += x[idx_1] * d * (low_q - 8)
                    row_sum += x[idx_2] * d * (high_q - 8)

            y[r] = row_sum

        return y


# =====================================================================
# 4. KV-Cache Memory Capacity & Overhead Tracker
# =====================================================================

class KVCacheTracker:
    """
    Models the context-window scaling limits of autoregressive transformer decoding.
    As context sequence length (N) increases, key-value storage grows linearly with batch size
    and quadratically inside attention matrix paths, presenting a severe local memory ceiling.
    """

    @staticmethod
    def calculate_kv_cache_bytes(
        sequence_length: int,
        batch_size: int,
        num_layers: int,
        num_heads: int,
        head_dimension: int,
        precision_bytes: int = 2 # FP16 defaults to 2 bytes
    ) -> Dict[str, Any]:
        """
        Calculates physical RAM capacity overhead of KV-cache memory blocks.
        Formula:
          Total Elements = 2 (Key + Value) * num_layers * sequence_length * batch_size * num_heads * head_dimension
          Total Bytes = Total Elements * precision_bytes
        """
        elements_per_token = 2 * num_layers * num_heads * head_dimension
        total_elements = elements_per_token * sequence_length * batch_size
        total_bytes = total_elements * precision_bytes

        return {
            "sequence_length": sequence_length,
            "batch_size": batch_size,
            "elements_per_token": elements_per_token,
            "total_elements": total_elements,
            "bytes_allocated": total_bytes,
            "megabytes_allocated": round(total_bytes / (1024 * 1024), 2),
            "gigabytes_allocated": round(total_bytes / (1024 * 1024 * 1024), 4)
        }


# =====================================================================
# Demonstration & Self-Verification Execution
# =====================================================================

def run_reconstruction_demo():
    print("===============================================================")
    print("      llama.cpp ARCHAEOLOGICAL RECONSTRUCTION SIMULATOR        ")
    print("===============================================================\n")

    # Step 1: Demonstrate Block-wise Q4_0 Quantization
    print("--- 1. Testing Q4_0 Block Quantization ---")
    # Generate mock FP32 weights (size: 32 elements to match block size B)
    raw_weights = [0.15 * i for i in range(32)]
    print(f"Original Weights (Sample 5): {raw_weights[:5]}")

    q4_bytes = Q4_0Quantizer.quantize(raw_weights)
    print(f"Quantized Q4_0 binary bytes length: {len(q4_bytes)} bytes (Raw FP32 was 128 bytes).")

    dequant_weights = Q4_0Quantizer.dequantize(q4_bytes, 32)
    print(f"Dequantized Weights (Sample 5): {dequant_weights[:5]}")

    # Calculate error margins
    abs_errors = [abs(orig - deq) for orig, deq in zip(raw_weights, dequant_weights)]
    print(f"Maximum absolute quantization error: {max(abs_errors):.4f}")

    # Step 2: GGUF Serialization
    print("\n--- 2. Testing GGUF Container Structuring ---")
    metadata = {
        "general.architecture": (GGUFContainer.TYPE_STRING, "llama"),
        "llama.attention.head_count": (GGUFContainer.TYPE_UINT32, 32),
        "llama.attention.layer_count": (GGUFContainer.TYPE_UINT32, 12),
        "llama.feed_forward_length": (GGUFContainer.TYPE_UINT32, 1024)
    }

    # Prepare quantized weights tensor
    tensors = {
        "token_embeddings.weight": ([32, 32], "q4_0", Q4_0Quantizer.quantize([0.5] * 1024))
    }

    # Serialize to single file-mapped payload
    payload = GGUFContainer.serialize(metadata, tensors)
    print(f"GGUF Packed payload size: {len(payload)} bytes.")

    # Deserialize back
    parsed_meta, parsed_tensors = GGUFContainer.deserialize(payload)
    print(f"Deserialized GGUF Metadata Name: '{parsed_meta['general.architecture']}'")
    print(f"Deserialized GGUF Attention Heads: {parsed_meta['llama.attention.head_count']}")
    print(f"Deserialized GGUF Embedded Tensor Shape: {parsed_tensors['token_embeddings.weight'][0]}")

    # Step 3: Quantized Linear GEMV On-the-fly execution
    print("\n--- 3. Testing Dequantization-on-the-fly GEMV ---")
    # Create rows=2, cols=32 weight matrix
    matrix_weights = [0.5 * (i % 8) for i in range(64)]
    x_activation = [1.0] * 32

    # Compute high-precision FP32 ground truth reference
    ref_y = [0.0, 0.0]
    for r in range(2):
        ref_y[r] = sum(matrix_weights[r * 32 + c] * x_activation[c] for c in range(32))
    print(f"FP32 Reference matrix dot-product result: {ref_y}")

    # Quantize weight matrix W to Q4_0
    q_weights_payload = Q4_0Quantizer.quantize(matrix_weights)

    # Compute dot product directly on the quantized bytes with dequantization on-the-fly!
    quant_y = QuantizedLinearMath.gemv_q4_0(x_activation, q_weights_payload, [2, 32])
    print(f"Quantized on-the-fly GEMV result:        {quant_y}")
    print(f"Error delta: {[abs(r - q) for r, q in zip(ref_y, quant_y)]}")

    # Step 4: KV-Cache scaling metrics
    print("\n--- 4. Projecting KV-Cache Context Boundaries ---")
    # Project cache growth for a standard LLaMA-7B configuration:
    # 32 layers, 32 attention heads, 128 head dimension, Batch size = 1
    for seq_len in [2048, 8192, 32768, 65536]:
        stats = KVCacheTracker.calculate_kv_cache_bytes(
            sequence_length=seq_len,
            batch_size=1,
            num_layers=32,
            num_heads=32,
            head_dimension=128,
            precision_bytes=2  # FP16
        )
        print(f"Context Length {seq_len:5d} tokens ──► RAM allocated: {stats['megabytes_allocated']:8.2f} MB ({stats['gigabytes_allocated']:.4f} GB)")


if __name__ == "__main__":
    run_reconstruction_demo()
