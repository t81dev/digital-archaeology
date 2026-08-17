"""
Unit tests for FFmpeg Multimedia Pipeline Simulator.
Verifies reference-counted buffer management, codec/container discovery,
5-stage transcode dataflow loop, filter graph transformations, and CLI translation.
"""

import pytest
from reconstructions.ffmpeg_pipeline.ffmpeg_sim import (
    AVBufferRef,
    AVPacket,
    AVFrame,
    CodecDescriptor,
    ContainerDescriptor,
    CodecContainerRegistry,
    Demuxer,
    Decoder,
    FilterGraph,
    Encoder,
    Muxer,
    FFmpegPipeline,
    FFmpegCLITranslator
)


def test_buffer_reference_counting():
    buf = AVBufferRef(1024)
    assert buf.ref_count == 1

    ref1 = buf.ref()
    assert buf.ref_count == 2

    assert not buf.unref()
    assert buf.ref_count == 1

    assert buf.unref()
    assert buf.ref_count == 0


def test_packet_frame_cloning():
    pkt = AVPacket(stream_index=0, pts=100, dts=100, data=b"TEST_BITSTREAM", is_keyframe=True)
    assert pkt.size == 14
    assert pkt.buffer_ref.ref_count == 1

    pkt_clone = pkt.clone()
    assert pkt_clone.pts == 100
    assert pkt.buffer_ref.ref_count == 2

    frame = AVFrame(width=1280, height=720, pixel_format="yuv420p", pts=500)
    assert frame.width == 1280
    assert frame.media_type == "video"
    assert frame.buffer_ref.ref_count == 1

    frame_clone = frame.clone()
    assert frame_clone.height == 720
    assert frame.buffer_ref.ref_count == 2


def test_codec_container_registry():
    registry = CodecContainerRegistry()

    demuxer = registry.probe_format_by_extension("video.mp4")
    assert demuxer is not None
    assert "mp4" in demuxer.extensions

    decoder = registry.find_decoder("h264")
    assert decoder is not None
    assert decoder.media_type == "video"

    encoder = registry.find_encoder("libx264")
    assert encoder is not None
    assert encoder.codec_id == "h264"


def test_filter_graph_execution():
    frame = AVFrame(width=1920, height=1080, pts=0)
    graph = FilterGraph("scale=1280:720")

    filtered = graph.process_frame(frame)
    assert filtered.width == 1280
    assert filtered.height == 720

    crop_graph = FilterGraph("crop=640:480")
    cropped = crop_graph.process_frame(frame)
    assert cropped.width == 640
    assert cropped.height == 480


def test_ffmpeg_pipeline_5_stage_loop():
    pipeline = FFmpegPipeline(
        input_filename="input_sample.mp4",
        output_filename="output_sample.mkv",
        video_codec="libx264",
        filter_spec="scale=1280:720"
    )

    processed = pipeline.run()
    assert processed == 5
    assert len(pipeline.muxer.written_packets) == 5

    written_pkt = pipeline.muxer.written_packets[0]
    assert written_pkt.pts == 0
    assert b"1280x720" in written_pkt.data


def test_cli_translator():
    translator = FFmpegCLITranslator()
    cmd = "ffmpeg -i sample.mp4 -vf scale=1280:720 -c:v libx264 output.mkv"

    pipeline, count = translator.parse_and_execute(cmd)
    assert count == 5
    assert len(pipeline.muxer.written_packets) == 5
    assert pipeline.encoder.encoder_desc.name == "libx264"


def test_invalid_cli_command():
    translator = FFmpegCLITranslator()

    with pytest.raises(ValueError, match="Command must start with 'ffmpeg'"):
        translator.parse_and_execute("invalid_cmd -i test.mp4 out.mp4")

    with pytest.raises(ValueError, match="missing input or output file"):
        translator.parse_and_execute("ffmpeg -i test.mp4")
