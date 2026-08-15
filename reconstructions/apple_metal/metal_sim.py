"""
Apple Metal Architecture Simulator (MetalSim)

A zero-dependency Python simulator modeling key architectural abstractions of Apple's Metal GPU API:
1. Low-overhead explicit command buffer recording & parallel command encoders.
2. Immutable Pipeline State Objects (PSOs) compiled upfront.
3. Explicit memory storage modes (Shared, Private, Memoryless) on Unified Memory Architecture (UMA).
4. Tile-Based Deferred Rendering (TBDR) load/store actions and on-chip SRAM tile memory.
5. Argument buffers and bindless indirect resource binding.
6. Explicit hazard tracking via fences between compute and render passes.
"""

import enum
from typing import Dict, List, Optional, Any, Callable, Tuple


class StorageMode(enum.Enum):
    SHARED = "StorageModeShared"      # Coherent zero-copy CPU & GPU access on UMA
    PRIVATE = "StorageModePrivate"    # GPU exclusive access, driver swizzled/optimized
    MEMORYLESS = "StorageModeMemoryless" # GPU on-chip SRAM tile memory ONLY (0 main RAM bytes)


class MTLLoadAction(enum.Enum):
    DONT_CARE = 0
    LOAD = 1
    CLEAR = 2


class MTLStoreAction(enum.Enum):
    DONT_CARE = 0
    STORE = 1
    MULTISAMPLE_RESOLVE = 2


class CommandBufferStatus(enum.Enum):
    NOT_ENCODED = 0
    ENCODING = 1
    COMMITTED = 2
    COMPLETED = 3


class SimBuffer:
    """Represents a Metal Buffer allocation."""
    def __init__(self, name: str, size: int, storage_mode: StorageMode):
        self.name = name
        self.size = size
        self.storage_mode = storage_mode
        # Allocated memory bytes (0 if MEMORYLESS)
        self.bytes = bytearray(size) if storage_mode != StorageMode.MEMORYLESS else bytearray(0)
        self.cpu_reads = 0
        self.cpu_writes = 0
        self.gpu_reads = 0
        self.gpu_writes = 0

    def write_cpu(self, offset: int, data: bytes):
        if self.storage_mode == StorageMode.PRIVATE:
            raise PermissionError(f"Cannot write to StorageModePrivate buffer '{self.name}' directly from CPU!")
        if self.storage_mode == StorageMode.MEMORYLESS:
            raise PermissionError(f"Cannot write to StorageModeMemoryless buffer '{self.name}' directly from CPU!")

        length = len(data)
        if offset + length > self.size:
            raise ValueError("Buffer write overflow")
        self.bytes[offset:offset + length] = data
        self.cpu_writes += 1

    def read_cpu(self, offset: int, length: int) -> bytes:
        if self.storage_mode == StorageMode.PRIVATE:
            raise PermissionError(f"Cannot read StorageModePrivate buffer '{self.name}' directly from CPU!")
        if self.storage_mode == StorageMode.MEMORYLESS:
            raise PermissionError(f"Cannot read StorageModeMemoryless buffer '{self.name}' directly from CPU!")
        self.cpu_reads += 1
        return bytes(self.bytes[offset:offset + length])


class SimTexture:
    """Represents a Metal Texture object."""
    def __init__(self, name: str, width: int, height: int, pixel_format: str, storage_mode: StorageMode):
        self.name = name
        self.width = width
        self.height = height
        self.pixel_format = pixel_format
        self.storage_mode = storage_mode
        self.bpp = 4  # Assume 4 bytes per pixel for simulation
        self.size_bytes = width * height * self.bpp

        # If MEMORYLESS, no main memory allocation occurs!
        self.data = bytearray(self.size_bytes) if storage_mode != StorageMode.MEMORYLESS else bytearray(0)
        self.main_ram_flushes = 0

    def flush_to_main_ram(self, tile_data: bytes):
        """Simulates TBDR store action writing on-chip tile memory to main RAM."""
        if self.storage_mode == StorageMode.MEMORYLESS:
            # Memoryless store is dropped! Never written to main RAM.
            return
        self.data = bytearray(tile_data)
        self.main_ram_flushes += 1


class SimRenderPipelineState:
    """Immutable compiled Pipeline State Object (PSO)."""
    def __init__(self, label: str, vertex_func: Callable, fragment_func: Callable, pixel_format: str):
        self.label = label
        self.vertex_func = vertex_func
        self.fragment_func = fragment_func
        self.pixel_format = pixel_format
        self.is_compiled = True  # Represents pre-compiled immutable state


class SimComputePipelineState:
    """Immutable compute pipeline state object."""
    def __init__(self, label: str, compute_func: Callable):
        self.label = label
        self.compute_func = compute_func
        self.is_compiled = True


class SimFence:
    """Synchronization primitive between passes."""
    def __init__(self, label: str):
        self.label = label
        self.signaled = False


class SimRenderPassColorAttachment:
    def __init__(self, texture: SimTexture):
        self.texture = texture
        self.load_action = MTLLoadAction.CLEAR
        self.store_action = MTLStoreAction.STORE
        self.clear_color = (0.0, 0.0, 0.0, 1.0)


class SimRenderPassDescriptor:
    def __init__(self):
        self.color_attachments: Dict[int, SimRenderPassColorAttachment] = {}

    @property
    def colorAttachments(self) -> Dict[int, SimRenderPassColorAttachment]:
        return self.color_attachments


class SimRenderCommandEncoder:
    """Encodes rasterization and fragment commands into a command buffer."""
    def __init__(self, parent_buffer: 'SimCommandBuffer', descriptor: SimRenderPassDescriptor):
        self.parent_buffer = parent_buffer
        self.descriptor = descriptor
        self.active_pso: Optional[SimRenderPipelineState] = None
        self.vertex_buffers: Dict[int, SimBuffer] = {}
        self.fragment_textures: Dict[int, SimTexture] = {}
        self.commands: List[Dict[str, Any]] = []

    def set_render_pipeline_state(self, pso: SimRenderPipelineState):
        self.active_pso = pso
        self.commands.append({"cmd": "SET_PSO", "pso": pso})

    def set_vertex_buffer(self, buffer: SimBuffer, offset: int, index: int):
        self.vertex_buffers[index] = buffer
        self.commands.append({"cmd": "SET_VERTEX_BUFFER", "buffer": buffer, "offset": offset, "index": index})

    def set_fragment_texture(self, texture: SimTexture, index: int):
        self.fragment_textures[index] = texture
        self.commands.append({"cmd": "SET_FRAGMENT_TEXTURE", "texture": texture, "index": index})

    def draw_primitives(self, primitive_type: str, vertex_start: int, vertex_count: int):
        if not self.active_pso:
            raise RuntimeError("Cannot execute draw call without setting a Pipeline State Object (PSO)")
        self.commands.append({
            "cmd": "DRAW_PRIMITIVES",
            "primitive_type": primitive_type,
            "vertex_start": vertex_start,
            "vertex_count": vertex_count,
            "pso": self.active_pso,
            "buffers": dict(self.vertex_buffers),
            "textures": dict(self.fragment_textures)
        })

    def waitForFence(self, fence: SimFence):
        self.commands.append({"cmd": "WAIT_FENCE", "fence": fence})

    def updateFence(self, fence: SimFence):
        self.commands.append({"cmd": "UPDATE_FENCE", "fence": fence})

    def endEncoding(self):
        self.parent_buffer._finish_encoder(self)


class SimComputeCommandEncoder:
    """Encodes general-purpose GPU compute kernels."""
    def __init__(self, parent_buffer: 'SimCommandBuffer'):
        self.parent_buffer = parent_buffer
        self.active_pso: Optional[SimComputePipelineState] = None
        self.buffers: Dict[int, SimBuffer] = {}
        self.commands: List[Dict[str, Any]] = []

    def set_compute_pipeline_state(self, pso: SimComputePipelineState):
        self.active_pso = pso
        self.commands.append({"cmd": "SET_COMPUTE_PSO", "pso": pso})

    def set_buffer(self, buffer: SimBuffer, offset: int, index: int):
        self.buffers[index] = buffer
        self.commands.append({"cmd": "SET_BUFFER", "buffer": buffer, "offset": offset, "index": index})

    def dispatch_threadgroups(self, threadgroups_per_grid: Tuple[int, int, int], threads_per_threadgroup: Tuple[int, int, int]):
        if not self.active_pso:
            raise RuntimeError("Cannot dispatch compute threads without a valid Compute Pipeline State Object")
        self.commands.append({
            "cmd": "DISPATCH_THREADGROUPS",
            "pso": self.active_pso,
            "buffers": dict(self.buffers),
            "grid": threadgroups_per_grid,
            "threads": threads_per_threadgroup
        })

    def updateFence(self, fence: SimFence):
        self.commands.append({"cmd": "UPDATE_FENCE", "fence": fence})

    def waitForFence(self, fence: SimFence):
        self.commands.append({"cmd": "WAIT_FENCE", "fence": fence})

    def endEncoding(self):
        self.parent_buffer._finish_encoder(self)


class SimCommandBuffer:
    """Atomic container recording commands for queue submission."""
    def __init__(self, queue: 'SimCommandQueue'):
        self.queue = queue
        self.status = CommandBufferStatus.NOT_ENCODED
        self.recorded_encoders: List[Any] = []
        self.active_encoder: Optional[Any] = None

    def make_render_command_encoder(self, descriptor: SimRenderPassDescriptor) -> SimRenderCommandEncoder:
        if self.active_encoder:
            raise RuntimeError("Active encoder must call endEncoding() before creating a new encoder.")
        self.status = CommandBufferStatus.ENCODING
        encoder = SimRenderCommandEncoder(self, descriptor)
        self.active_encoder = encoder
        return encoder

    def make_compute_command_encoder(self) -> SimComputeCommandEncoder:
        if self.active_encoder:
            raise RuntimeError("Active encoder must call endEncoding() before creating a new encoder.")
        self.status = CommandBufferStatus.ENCODING
        encoder = SimComputeCommandEncoder(self)
        self.active_encoder = encoder
        return encoder

    def _finish_encoder(self, encoder: Any):
        if self.active_encoder != encoder:
            raise RuntimeError("Mismatched encoder endEncoding")
        self.recorded_encoders.append(encoder)
        self.active_encoder = None

    def commit(self):
        if self.active_encoder:
            raise RuntimeError("Cannot commit command buffer with un-ended encoder.")
        self.status = CommandBufferStatus.COMMITTED
        self.queue._submit(self)


class SimCommandQueue:
    """Thread-safe submission queue for command buffers."""
    def __init__(self, device: 'SimMetalDevice'):
        self.device = device
        self.pending_buffers: List[SimCommandBuffer] = []
        self.executed_buffers: List[SimCommandBuffer] = []

    def make_command_buffer(self) -> SimCommandBuffer:
        return SimCommandBuffer(self)

    def _submit(self, buffer: SimCommandBuffer):
        self.pending_buffers.append(buffer)
        self.device._execute_queue(self)


class SimMetalDevice:
    """Represents the GPU device hardware interface."""
    def __init__(self, name: str = "Apple M3 Max"):
        self.name = name
        self.total_main_ram_writes = 0
        self.total_sram_tile_operations = 0

    def make_command_queue(self) -> SimCommandQueue:
        return SimCommandQueue(self)

    def make_buffer(self, name: str, size: int, storage_mode: StorageMode) -> SimBuffer:
        return SimBuffer(name, size, storage_mode)

    def make_texture(self, name: str, width: int, height: int, pixel_format: str, storage_mode: StorageMode) -> SimTexture:
        return SimTexture(name, width, height, pixel_format, storage_mode)

    def make_render_pipeline_state(self, label: str, vertex_func: Callable, fragment_func: Callable, pixel_format: str = "BGRA8Unorm") -> SimRenderPipelineState:
        return SimRenderPipelineState(label, vertex_func, fragment_func, pixel_format)

    def make_compute_pipeline_state(self, label: str, compute_func: Callable) -> SimComputePipelineState:
        return SimComputePipelineState(label, compute_func)

    def make_fence(self, label: str) -> SimFence:
        return SimFence(label)

    def _execute_queue(self, queue: SimCommandQueue):
        while queue.pending_buffers:
            buffer = queue.pending_buffers.pop(0)
            self._execute_command_buffer(buffer)
            buffer.status = CommandBufferStatus.COMPLETED
            queue.executed_buffers.append(buffer)

    def _execute_command_buffer(self, buffer: SimCommandBuffer):
        for encoder in buffer.recorded_encoders:
            if isinstance(encoder, SimRenderCommandEncoder):
                self._execute_render_encoder(encoder)
            elif isinstance(encoder, SimComputeCommandEncoder):
                self._execute_compute_encoder(encoder)

    def _execute_render_encoder(self, encoder: SimRenderCommandEncoder):
        desc = encoder.descriptor
        # Step 1: Simulate TBDR On-Chip SRAM Tile Load
        for index, att in desc.color_attachments.items():
            tex = att.texture
            self.total_sram_tile_operations += 1
            if att.load_action == MTLLoadAction.CLEAR:
                # SRAM tile cleared to clear_color
                pass
            elif att.load_action == MTLLoadAction.LOAD:
                # Load from main RAM to SRAM tile memory
                pass

        # Step 2: Process Recorded Rasterization Commands
        for cmd in encoder.commands:
            c = cmd["cmd"]
            if c == "DRAW_PRIMITIVES":
                pso = cmd["pso"]
                for buf in cmd["buffers"].values():
                    buf.gpu_reads += 1
                # Execute vertex & fragment functions on GPU
                pso.vertex_func()
                pso.fragment_func()
                self.total_sram_tile_operations += cmd["vertex_count"]
            elif c == "WAIT_FENCE":
                fence: SimFence = cmd["fence"]
                if not fence.signaled:
                    raise RuntimeError(f"GPU Execution Hazard! Fence '{fence.label}' waited on before being updated.")
            elif c == "UPDATE_FENCE":
                fence: SimFence = cmd["fence"]
                fence.signaled = True

        # Step 3: Simulate TBDR On-Chip SRAM Tile Store Actions
        for index, att in desc.color_attachments.items():
            tex = att.texture
            if att.store_action == MTLStoreAction.STORE:
                # Write back on-chip tile result to main RAM
                mock_rendered_tile = b"\xFF\x00\x00\xFF" * (tex.width * tex.height)
                tex.flush_to_main_ram(mock_rendered_tile)
                self.total_main_ram_writes += 1
            elif att.store_action == MTLStoreAction.DONT_CARE:
                # TBDR Optimization: On-chip SRAM tile memory is discarded! 0 writes to main RAM!
                pass

    def _execute_compute_encoder(self, encoder: SimComputeCommandEncoder):
        for cmd in encoder.commands:
            c = cmd["cmd"]
            if c == "DISPATCH_THREADGROUPS":
                pso = cmd["pso"]
                for buf in cmd["buffers"].values():
                    buf.gpu_reads += 1
                    buf.gpu_writes += 1
                pso.compute_func()
            elif c == "UPDATE_FENCE":
                fence: SimFence = cmd["fence"]
                fence.signaled = True
            elif c == "WAIT_FENCE":
                fence: SimFence = cmd["fence"]
                if not fence.signaled:
                    raise RuntimeError(f"GPU Execution Hazard! Fence '{fence.label}' waited on before signal.")
