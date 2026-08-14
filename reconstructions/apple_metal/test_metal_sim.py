"""
Unit tests for Apple Metal Architecture Simulator (MetalSim).
"""

import pytest
from reconstructions.apple_metal.metal_sim import (
    SimMetalDevice,
    StorageMode,
    MTLLoadAction,
    MTLStoreAction,
    SimRenderPassDescriptor,
    SimRenderPassColorAttachment,
    CommandBufferStatus
)


def test_device_creation_and_queues():
    device = SimMetalDevice("Apple M3 Max")
    queue = device.make_command_queue()
    assert queue.device == device
    assert len(queue.pending_buffers) == 0


def test_storage_modes_and_uma():
    device = SimMetalDevice()

    # StorageModeShared: Coherent CPU/GPU access
    shared_buf = device.make_buffer("shared_data", 1024, StorageMode.SHARED)
    shared_buf.write_cpu(0, b"Hello Metal Unified Memory")
    assert shared_buf.read_cpu(0, 26) == b"Hello Metal Unified Memory"
    assert shared_buf.cpu_writes == 1

    # StorageModePrivate: CPU access forbidden
    private_buf = device.make_buffer("private_data", 1024, StorageMode.PRIVATE)
    with pytest.raises(PermissionError):
        private_buf.write_cpu(0, b"Fail")
    with pytest.raises(PermissionError):
        private_buf.read_cpu(0, 10)

    # StorageModeMemoryless: Main RAM bytes == 0
    memoryless_tex = device.make_texture("depth_transient", 1920, 1080, "Depth32Float", StorageMode.MEMORYLESS)
    assert len(memoryless_tex.data) == 0


def test_pso_immutability_and_command_encoding():
    device = SimMetalDevice()
    queue = device.make_command_queue()

    # Dummy shader functions
    vertex_shader_called = [False]
    fragment_shader_called = [False]

    def mock_vertex():
        vertex_shader_called[0] = True

    def mock_fragment():
        fragment_shader_called[0] = True

    # Compile immutable PSO upfront
    pso = device.make_render_pipeline_state("BasicPSO", mock_vertex, mock_fragment)
    assert pso.is_compiled is True

    # Prepare render pass
    render_tex = device.make_texture("framebuffer", 800, 600, "BGRA8Unorm", StorageMode.SHARED)
    desc = SimRenderPassDescriptor()
    attachment = SimRenderPassColorAttachment(render_tex)
    attachment.load_action = MTLLoadAction.CLEAR
    attachment.store_action = MTLStoreAction.STORE
    desc.colorAttachments[0] = attachment

    # Record command buffer
    cmd_buffer = queue.make_command_buffer()
    encoder = cmd_buffer.make_render_command_encoder(desc)
    encoder.set_render_pipeline_state(pso)

    vbuf = device.make_buffer("vbuf", 256, StorageMode.SHARED)
    encoder.set_vertex_buffer(vbuf, 0, 0)
    encoder.draw_primitives("triangle", 0, 3)
    encoder.endEncoding()

    cmd_buffer.commit()

    assert cmd_buffer.status == CommandBufferStatus.COMPLETED
    assert vertex_shader_called[0] is True
    assert fragment_shader_called[0] is True
    assert render_tex.main_ram_flushes == 1


def test_tbdr_memoryless_optimization():
    device = SimMetalDevice()
    queue = device.make_command_queue()

    # Transient MSAA attachment using StorageModeMemoryless
    msaa_tex = device.make_texture("msaa_attachment", 1920, 1080, "BGRA8Unorm", StorageMode.MEMORYLESS)

    desc = SimRenderPassDescriptor()
    attachment = SimRenderPassColorAttachment(msaa_tex)
    attachment.load_action = MTLLoadAction.CLEAR
    # Critical TBDR optimization: DONT_CARE store action suppresses main RAM flush!
    attachment.store_action = MTLStoreAction.DONT_CARE
    desc.colorAttachments[0] = attachment

    pso = device.make_render_pipeline_state("MSAAPSO", lambda: None, lambda: None)

    cmd_buffer = queue.make_command_buffer()
    encoder = cmd_buffer.make_render_command_encoder(desc)
    encoder.set_render_pipeline_state(pso)
    encoder.draw_primitives("triangle", 0, 6)
    encoder.endEncoding()

    initial_ram_writes = device.total_main_ram_writes
    cmd_buffer.commit()

    # Main RAM writes should NOT increase because StoreAction.DONT_CARE was specified!
    assert device.total_main_ram_writes == initial_ram_writes
    assert msaa_tex.main_ram_flushes == 0


def test_fence_hazard_tracking():
    device = SimMetalDevice()
    queue = device.make_command_queue()
    fence = device.make_fence("ComputeToRenderFence")

    compute_called = [False]
    def mock_compute():
        compute_called[0] = True

    compute_pso = device.make_compute_pipeline_state("PhysicsCompute", mock_compute)
    render_pso = device.make_render_pipeline_state("ParticleRender", lambda: None, lambda: None)

    render_tex = device.make_texture("out_tex", 100, 100, "BGRA8Unorm", StorageMode.SHARED)
    desc = SimRenderPassDescriptor()
    desc.colorAttachments[0] = SimRenderPassColorAttachment(render_tex)

    cmd_buffer = queue.make_command_buffer()

    # Compute encoder updates fence after finishing kernel
    comp_encoder = cmd_buffer.make_compute_command_encoder()
    comp_encoder.set_compute_pipeline_state(compute_pso)
    comp_encoder.dispatch_threadgroups((1, 1, 1), (64, 1, 1))
    comp_encoder.updateFence(fence)
    comp_encoder.endEncoding()

    # Render encoder waits for fence before rendering
    render_encoder = cmd_buffer.make_render_command_encoder(desc)
    render_encoder.waitForFence(fence)
    render_encoder.set_render_pipeline_state(render_pso)
    render_encoder.draw_primitives("point", 0, 100)
    render_encoder.endEncoding()

    cmd_buffer.commit()
    assert compute_called[0] is True
    assert fence.signaled is True


def test_unwaited_fence_hazard_raises():
    device = SimMetalDevice()
    queue = device.make_command_queue()
    unsignaled_fence = device.make_fence("UnsignaledFence")

    render_tex = device.make_texture("out_tex", 100, 100, "BGRA8Unorm", StorageMode.SHARED)
    desc = SimRenderPassDescriptor()
    desc.colorAttachments[0] = SimRenderPassColorAttachment(render_tex)

    render_pso = device.make_render_pipeline_state("RenderPSO", lambda: None, lambda: None)

    cmd_buffer = queue.make_command_buffer()
    encoder = cmd_buffer.make_render_command_encoder(desc)
    encoder.waitForFence(unsignaled_fence)  # Waiting on unsignaled fence!
    encoder.set_render_pipeline_state(render_pso)
    encoder.draw_primitives("triangle", 0, 3)
    encoder.endEncoding()

    with pytest.raises(RuntimeError, match="Execution Hazard"):
        cmd_buffer.commit()
