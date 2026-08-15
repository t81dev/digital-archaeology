"""
Tests for Winamp Modular Plugin Host, Audio Pipeline, Skinning & Media Library Simulator.
"""

import pytest
from reconstructions.winamp_plugin_host.winamp_sim import (
    AudioChunk,
    WinampHost,
    MP3InputPlugin,
    WAVInputPlugin,
    DirectSoundOutputPlugin,
    GainSpatializerDSPPlugin,
    GlobalHotkeysGeneralPlugin,
    ClassicSkinEngine,
    PlaylistManager,
    TrackMetadata
)


def test_audio_chunk_properties():
    samples = [0.1, -0.1, 0.5, -0.5]
    chunk = AudioChunk(samples=samples, sample_rate=44100, channels=2)
    assert len(chunk.samples) == 4
    # 2 stereo frames at 44100Hz = ~0.045 ms
    assert chunk.duration_ms() >= 0


def test_plugin_registration_and_discovery():
    host = WinampHost()
    in_mp3 = MP3InputPlugin()
    in_wav = WAVInputPlugin()
    out_ds = DirectSoundOutputPlugin()
    dsp_gain = GainSpatializerDSPPlugin(gain_db=6.0)
    gen_hotkeys = GlobalHotkeysGeneralPlugin()

    host.register_input_plugin(in_mp3)
    host.register_input_plugin(in_wav)
    host.register_output_plugin(out_ds)
    host.register_dsp_plugin(dsp_gain)
    host.register_general_plugin(gen_hotkeys)

    assert len(host.input_plugins) == 2
    assert len(host.output_plugins) == 1
    assert len(host.dsp_plugins) == 1
    assert len(host.general_plugins) == 1

    # File format matching
    matched_mp3 = host.find_input_plugin_for_file("song.mp3")
    assert matched_mp3 == in_mp3

    matched_wav = host.find_input_plugin_for_file("track.wav")
    assert matched_wav == in_wav

    matched_none = host.find_input_plugin_for_file("video.avi")
    assert matched_none is None


def test_decoupled_audio_pipeline_execution():
    host = WinampHost()
    in_mp3 = MP3InputPlugin()
    out_ds = DirectSoundOutputPlugin()
    dsp_gain = GainSpatializerDSPPlugin(gain_db=3.0)

    host.register_input_plugin(in_mp3)
    host.register_output_plugin(out_ds)
    host.register_dsp_plugin(dsp_gain)

    # Start playback
    success = host.play_file("test_audio.mp3")
    assert success is True
    assert host.is_playing is True

    # Step pipeline
    chunk = host.step_audio_pipeline()
    assert chunk is not None
    assert len(chunk.samples) > 0
    assert out_ds.is_playing() is True

    # Test pause and unpause
    host.pause()
    assert in_mp3.is_paused() is True
    assert host.step_audio_pipeline() is None

    host.pause()
    assert in_mp3.is_paused() is False

    # Test stop
    host.stop()
    assert host.is_playing is False


def test_equalizer_filter_effects():
    host = WinampHost()
    in_mp3 = MP3InputPlugin()
    out_ds = DirectSoundOutputPlugin()

    host.register_input_plugin(in_mp3)
    host.register_output_plugin(out_ds)

    host.play_file("song.mp3")

    # Step baseline without EQ
    chunk1 = host.step_audio_pipeline()
    val_normal = chunk1.samples[0]

    # Enable Equalizer with boost
    host.set_equalizer(enabled=True, preamp=6, bands=[6] * 10)
    chunk2 = host.step_audio_pipeline()
    val_boosted = chunk2.samples[0]

    assert abs(val_boosted) > abs(val_normal)


def test_general_plugin_hotkeys():
    host = WinampHost()
    gen_hotkeys = GlobalHotkeysGeneralPlugin()
    host.register_general_plugin(gen_hotkeys)

    gen_hotkeys.register_hotkey("CTRL+ALT+Z", "PLAY")
    gen_hotkeys.register_hotkey("CTRL+ALT+X", "PAUSE")

    host.playlist = ["song1.mp3", "song2.mp3"]
    in_mp3 = MP3InputPlugin()
    out_ds = DirectSoundOutputPlugin()
    host.register_input_plugin(in_mp3)
    host.register_output_plugin(out_ds)

    action = gen_hotkeys.trigger_hotkey("CTRL+ALT+Z", host)
    assert action == "PLAY"
    assert host.is_playing is True


def test_classic_skin_ui_engine():
    skin_engine = ClassicSkinEngine()
    host = WinampHost()
    in_mp3 = MP3InputPlugin()
    out_ds = DirectSoundOutputPlugin()
    host.register_input_plugin(in_mp3)
    host.register_output_plugin(out_ds)

    host.playlist = ["song.mp3"]

    # Verify sprite offset lookup
    play_offset = skin_engine.get_sprite_offset("PLAY_BUTTON")
    assert play_offset == (0, 135, 23, 18)

    # Test UI click dispatch
    res_play = skin_engine.dispatch_ui_click("PLAY_BUTTON", host)
    assert res_play == "PLAYED"
    assert host.is_playing is True

    res_pause = skin_engine.dispatch_ui_click("PAUSE_BUTTON", host)
    assert res_pause == "PAUSED"
    assert in_mp3.is_paused() is True

    res_stop = skin_engine.dispatch_ui_click("STOP_BUTTON", host)
    assert res_stop == "STOPPED"
    assert host.is_playing is False


def test_playlist_parsing_and_media_library_search():
    pm = PlaylistManager()

    # M3U parsing
    m3u_sample = """#EXTM3U
#EXTINF:235,Daft Punk - Around the World
/Music/daft_punk.mp3
#EXTINF:180,Kraftwerk - Computer World
/Music/kraftwerk.mp3
"""
    m3u_files = pm.parse_m3u_content(m3u_sample)
    assert len(m3u_files) == 2
    assert m3u_files[0] == "/Music/daft_punk.mp3"

    # PLS parsing
    pls_sample = """[playlist]
File1=/Music/track1.mp3
Title1=Track 1
Length1=200
File2=/Music/track2.mp3
Title2=Track 2
Length2=150
NumberOfEntries=2
Version=2
"""
    pls_files = pm.parse_pls_content(pls_sample)
    assert len(pls_files) == 2
    assert pls_files[1] == "/Music/track2.mp3"

    # Media library search
    t1 = TrackMetadata("/Music/daft_punk.mp3", "Around the World", "Daft Punk", "Homework", 235, "Electronic")
    t2 = TrackMetadata("/Music/kraftwerk.mp3", "Computer World", "Kraftwerk", "Computer World", 180, "Synthpop")
    pm.add_track_to_library(t1)
    pm.add_track_to_library(t2)

    res_daft = pm.search_library("daft world")
    assert len(res_daft) == 1
    assert res_daft[0].title == "Around the World"

    res_all = pm.search_library("")
    assert len(res_all) == 2
