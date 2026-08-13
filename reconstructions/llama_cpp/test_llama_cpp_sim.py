#!/usr/bin/env python3
"""
Unit tests for the llama.cpp Lineage Reconstruction Simulator.
Verifies GGUF container packing/unpacking, Q4_0 block quantization accuracy,
dequantization-on-the-fly matrix-vector multiplication (GEMV), and KV-Cache calculations.
"""

import pytest
import struct
from reconstructions.llama_cpp.llama_cpp_sim import GGUFContainer, Q4_0Quantizer, QuantizedLinearMath, KVCacheTracker

def test_q4_0_quantization_cycle():
    """Checks that quantizing and then dequantizing maintains basic accuracy metrics."""
    # Generate 64 values ranging from -1.5 to 3.5
    raw_data = [float(i) * 0.1 - 1.0 for i in range(64)]

    # Compress to Q4_0
    compressed_bytes = Q4_0Quantizer.quantize(raw_data)

    # 64 elements with block size 32 means exactly 2 blocks.
    # Each block is 18 bytes (2B scale + 16B payload) -> 36 bytes total.
    assert len(compressed_bytes) == 36

    # Decompress back
    decompressed = Q4_0Quantizer.dequantize(compressed_bytes, 64)
    assert len(decompressed) == 64

    # Verify delta is bounded by quantization precision bins
    for orig, deq in zip(raw_data, decompressed):
        # Scale for each block is approx max_abs / 8. Max absolute val is ~5.4.
        # Max quantization error should be bounded by scale_factor / 2.
        assert abs(orig - deq) < 0.5


def test_gguf_container_serialization():
    """Verifies that GGUF metadata packing and tensor memory alignments survive serialization cycles."""
    metadata = {
        "architecture": (GGUFContainer.TYPE_STRING, "gemma"),
        "layers": (GGUFContainer.TYPE_UINT32, 28),
        "embedding_dim": (GGUFContainer.TYPE_INT32, 2048),
        "learning_rate": (GGUFContainer.TYPE_FLOAT32, 1e-4)
    }

    # Prepare mock quantized tensors
    tensor_data_1 = Q4_0Quantizer.quantize([0.25] * 32)
    tensor_data_2 = Q4_0Quantizer.quantize([-0.75] * 64)

    tensors = {
        "attn_w": ([32], "q4_0", tensor_data_1),
        "mlp_w": ([2, 32], "q4_0", tensor_data_2)
    }

    # Pack to GGUF byte payload
    payload = GGUFContainer.serialize(metadata, tensors, alignment=32)
    assert payload.startswith(b"GGUF")

    # Unpack and verify integrity
    parsed_meta, parsed_tensors = GGUFContainer.deserialize(payload)

    assert parsed_meta["architecture"] == "gemma"
    assert parsed_meta["layers"] == 28
    assert parsed_meta["embedding_dim"] == 2048
    assert abs(parsed_meta["learning_rate"] - 1e-4) < 1e-6

    # Verify tensor shapes and payload lengths
    shape_1, qtype_1, bytes_1 = parsed_tensors["attn_w"]
    assert shape_1 == [32]
    assert qtype_1 == "q4_0"
    assert len(bytes_1) == 18

    shape_2, qtype_2, bytes_2 = parsed_tensors["mlp_w"]
    assert shape_2 == [2, 32]
    assert qtype_2 == "q4_0"
    assert len(bytes_2) == 36


def test_quantized_linear_gemv():
    """Tests dot-product matrix multiplication computed directly over low-bit weights on-the-fly."""
    # Let's create W = [3, 32] weight matrix filled with structured values
    matrix_weights = [float(i % 16) * 0.1 for i in range(96)]
    x_vec = [1.0] * 32

    # FP32 reference result:
    ref_out = [0.0] * 3
    for r in range(3):
        ref_out[r] = sum(matrix_weights[r * 32 + c] * x_vec[c] for c in range(32))

    # Compress weights to Q4_0
    q_weights = Q4_0Quantizer.quantize(matrix_weights)

    # Run quantized GEMV on-the-fly
    quant_out = QuantizedLinearMath.gemv_q4_0(x_vec, q_weights, [3, 32])

    assert len(quant_out) == 3
    # Check that output values are close to FP32 reference (allowing minor block quantization delta)
    for ref, quant in zip(ref_out, quant_out):
        assert abs(ref - quant) < 1.0


def test_kv_cache_tracker():
    """Validates math formulas governing KV-cache tracking metrics."""
    # 1 layer, 1 head, 64 head-dim, 1024 sequence, FP16 (2B)
    stats = KVCacheTracker.calculate_kv_cache_bytes(
        sequence_length=1024,
        batch_size=1,
        num_layers=1,
        num_heads=1,
        head_dimension=64,
        precision_bytes=2
    )

    # elements_per_token = 2 * layers * heads * head_dim = 2 * 1 * 1 * 64 = 128
    assert stats["elements_per_token"] == 128

    # total elements = 128 * 1024 = 131,072
    assert stats["total_elements"] == 131072

    # total bytes = 131072 * 2 = 262,144 bytes = 0.25 MB
    assert stats["bytes_allocated"] == 262144
    assert stats["megabytes_allocated"] == 0.25
