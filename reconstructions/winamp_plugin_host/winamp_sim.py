"""
Winamp Modular Plugin Host, Audio Pipeline, Skinning & Media Library Simulator.
Demonstrates C-ABI plugin jump-tables, decoupled audio pipelines, declarative skin UI binding,
and local media indexing abstractions.
"""

import math
import os
from typing import Dict, List, Optional, Tuple, Any, Callable


# ============================================================================
# 1. Audio Data Representation
# ============================================================================

class AudioChunk:
    """Represents a discrete block of PCM audio samples in the pipeline."""
    def __init__(self, samples: List[float], sample_rate: int = 44100, channels: int = 2, bits_per_sample: int = 16):
        self.samples = samples  # Interleaved float PCM samples in [-1.0, 1.0]
        self.sample_rate = sample_rate
        self.channels = channels
        self.bits_per_sample = bits_per_sample

    def duration_ms(self) -> int:
        num_frames = len(self.samples) // self.channels
        if self.sample_rate == 0:
            return 0
        return int((num_frames / self.sample_rate) * 1000)


# ============================================================================
# 2. Plugin C-ABI Abstract Interface Contracts
# ============================================================================

class OutputPlugin:
    """Interface for Winamp Output Modules (out_*.dll)."""
    def __init__(self, plugin_id: str, description: str):
        self.plugin_id = plugin_id
        self.description = description
        self.version = 0x100
        self.is_open = False
        self.volume = 255  # 0 to 255
        self.pan = 0        # -128 to 128
        self.buffer: List[float] = []

    def init(self) -> None:
        pass

    def quit(self) -> None:
        pass

    def open(self, sample_rate: int, channels: int, bits_per_sample: int, buffer_len_ms: int) -> int:
        self.is_open = True
        self.buffer.clear()
        return 0  # 0 = success

    def close(self) -> None:
        self.is_open = False

    def write(self, chunk: AudioChunk) -> int:
        if not self.is_open:
            return -1
        # Apply output volume and panning
        vol_scale = self.volume / 255.0
        pan_left = min(1.0, 1.0 - (self.pan / 128.0)) if self.pan > 0 else 1.0
        pan_right = min(1.0, 1.0 + (self.pan / 128.0)) if self.pan < 0 else 1.0

        for i, sample in enumerate(chunk.samples):
            ch_scale = pan_left if (i % chunk.channels == 0) else pan_right
            processed = sample * vol_scale * ch_scale
            self.buffer.append(processed)
        return len(chunk.samples)

    def can_write(self) -> int:
        return 65536 - len(self.buffer)  # Remaining buffer capacity

    def is_playing(self) -> bool:
        return self.is_open and len(self.buffer) > 0

    def get_written_time(self) -> int:
        # Dummy time estimation in ms
        return len(self.buffer) // 2 // 44  # 44.1 kHz stereo approximation

    def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(255, volume))

    def set_pan(self, pan: int) -> None:
        self.pan = max(-128, min(128, pan))


class DSPPlugin:
    """Interface for Winamp DSP Modules (dsp_*.dll)."""
    def __init__(self, plugin_id: str, description: str):
        self.plugin_id = plugin_id
        self.description = description
        self.version = 0x100
        self.enabled = True

    def init(self) -> None:
        pass

    def quit(self) -> None:
        pass

    def modify_samples(self, chunk: AudioChunk) -> AudioChunk:
        """Transforms PCM samples in place or returns modified AudioChunk."""
        return chunk


class InputPlugin:
    """Interface for Winamp Input Modules (in_*.dll)."""
    def __init__(self, plugin_id: str, description: str, supported_extensions: List[str]):
        self.plugin_id = plugin_id
        self.description = description
        self.supported_extensions = [ext.lower() for ext in supported_extensions]
        self.version = 0x100
        self.out_mod: Optional[OutputPlugin] = None
        self.is_playing_file = False
        self.is_paused_file = False
        self.current_filename: Optional[str] = None
        self.position_ms = 0
        self.duration_ms = 180000  # Default 3 min synthetic

    def init(self) -> None:
        pass

    def quit(self) -> None:
        pass

    def is_our_file(self, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower().lstrip(".")
        return ext in self.supported_extensions

    def get_file_info(self, filename: str) -> Tuple[str, int]:
        title = os.path.basename(filename)
        return title, self.duration_ms

    def play(self, filename: str) -> int:
        self.current_filename = filename
        self.is_playing_file = True
        self.is_paused_file = False
        self.position_ms = 0
        return 0

    def pause(self) -> None:
        self.is_paused_file = True

    def unpause(self) -> None:
        self.is_paused_file = False

    def is_paused(self) -> bool:
        return self.is_paused_file

    def stop(self) -> None:
        self.is_playing_file = False
        self.is_paused_file = False

    def decode_frame(self) -> Optional[AudioChunk]:
        """Synthesizes or reads next PCM chunk."""
        if not self.is_playing_file or self.is_paused_file:
            return None
        if self.position_ms >= self.duration_ms:
            self.stop()
            return None

        # Generate 100ms synthetic sine wave chunk
        num_samples = 4410  # 100ms at 44.1kHz mono/stereo
        freq = 440.0
        samples = []
        for i in range(num_samples):
            t = (self.position_ms / 1000.0) + (i / 44100.0)
            val = math.sin(2.0 * math.pi * freq * t)
            samples.append(val)

        self.position_ms += 100
        return AudioChunk(samples=samples, sample_rate=44100, channels=2, bits_per_sample=16)

    def set_volume(self, volume: int) -> None:
        if self.out_mod:
            self.out_mod.set_volume(volume)

    def set_pan(self, pan: int) -> None:
        if self.out_mod:
            self.out_mod.set_pan(pan)

    def eq_set(self, on: int, bands: List[int], preamp: int) -> None:
        pass


class GeneralPlugin:
    """Interface for Winamp General Purpose Modules (gen_*.dll)."""
    def __init__(self, plugin_id: str, description: str):
        self.plugin_id = plugin_id
        self.description = description
        self.version = 0x100
        self.initialized = False

    def init(self, host: Any) -> int:
        self.initialized = True
        return 0

    def quit(self) -> None:
        self.initialized = False


# ============================================================================
# 3. Concrete Plugin Implementations
# ============================================================================

class MP3InputPlugin(InputPlugin):
    """MPEG Layer III audio decoding input module."""
    def __init__(self):
        super().__init__("in_mp3", "Nullsoft MPEG Audio Decoder v2.91", ["mp3", "mp2", "mp1"])


class WAVInputPlugin(InputPlugin):
    """Waveform audio decoding input module."""
    def __init__(self):
        super().__init__("in_wave", "Nullsoft Waveform Decoder v2.0", ["wav", "voc"])


class DirectSoundOutputPlugin(OutputPlugin):
    """DirectSound hardware output module."""
    def __init__(self):
        super().__init__("out_ds", "Nullsoft DirectSound Output v2.2")


class GainSpatializerDSPPlugin(DSPPlugin):
    """Simple DSP plugin adjusting gain and channel balance."""
    def __init__(self, gain_db: float = 0.0):
        super().__init__("dsp_gain", "Nullsoft Gain Spatializer DSP")
        self.gain_db = gain_db

    def modify_samples(self, chunk: AudioChunk) -> AudioChunk:
        if not self.enabled or self.gain_db == 0.0:
            return chunk
        scale = math.pow(10.0, self.gain_db / 20.0)
        modified_samples = [max(-1.0, min(1.0, s * scale)) for s in chunk.samples]
        return AudioChunk(
            samples=modified_samples,
            sample_rate=chunk.sample_rate,
            channels=chunk.channels,
            bits_per_sample=chunk.bits_per_sample
        )


class GlobalHotkeysGeneralPlugin(GeneralPlugin):
    """General purpose plugin registering global hotkeys."""
    def __init__(self):
        super().__init__("gen_hotkeys", "Winamp Global Hotkeys Handler")
        self.registered_keys: Dict[str, str] = {}

    def register_hotkey(self, key_combination: str, action: str) -> None:
        self.registered_keys[key_combination] = action

    def trigger_hotkey(self, key_combination: str, host: Any) -> Optional[str]:
        if key_combination in self.registered_keys:
            action = self.registered_keys[key_combination]
            if action == "PLAY":
                host.play()
            elif action == "PAUSE":
                host.pause()
            elif action == "STOP":
                host.stop()
            elif action == "NEXT":
                host.next_track()
            return action
        return None


# ============================================================================
# 4. Winamp Core Host Engine
# ============================================================================

class WinampHost:
    """
    Winamp Core Host Process (winamp.exe).
    Coordinates plugin registration, dynamic audio pipeline execution,
    equalizer filter states, volume/pan controls, and playlist orchestration.
    """
    def __init__(self):
        self.input_plugins: List[InputPlugin] = []
        self.output_plugins: List[OutputPlugin] = []
        self.dsp_plugins: List[DSPPlugin] = []
        self.general_plugins: List[GeneralPlugin] = []

        self.active_output_plugin: Optional[OutputPlugin] = None
        self.active_input_plugin: Optional[InputPlugin] = None

        self.volume = 255  # 0 to 255
        self.pan = 0        # -128 to 128
        self.eq_enabled = False
        self.eq_preamp = 0
        self.eq_bands = [0] * 10  # 10 bands: -12 to +12 dB

        self.playlist: List[str] = []
        self.current_playlist_index = -1
        self.is_playing = False

    def register_input_plugin(self, plugin: InputPlugin) -> None:
        plugin.init()
        self.input_plugins.append(plugin)

    def register_output_plugin(self, plugin: OutputPlugin) -> None:
        plugin.init()
        self.output_plugins.append(plugin)
        if not self.active_output_plugin:
            self.active_output_plugin = plugin

    def register_dsp_plugin(self, plugin: DSPPlugin) -> None:
        plugin.init()
        self.dsp_plugins.append(plugin)

    def register_general_plugin(self, plugin: GeneralPlugin) -> None:
        plugin.init(self)
        self.general_plugins.append(plugin)

    def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(255, volume))
        if self.active_output_plugin:
            self.active_output_plugin.set_volume(self.volume)

    def set_pan(self, pan: int) -> None:
        self.pan = max(-128, min(128, pan))
        if self.active_output_plugin:
            self.active_output_plugin.set_pan(self.pan)

    def set_equalizer(self, enabled: bool, preamp: int, bands: List[int]) -> None:
        self.eq_enabled = enabled
        self.eq_preamp = preamp
        self.eq_bands = list(bands)
        if self.active_input_plugin:
            self.active_input_plugin.eq_set(1 if enabled else 0, [chr(b & 0xFF) for b in bands], preamp)

    def find_input_plugin_for_file(self, filename: str) -> Optional[InputPlugin]:
        for plugin in self.input_plugins:
            if plugin.is_our_file(filename):
                return plugin
        return None

    def play(self, filename: Optional[str] = None) -> bool:
        if filename:
            return self.play_file(filename)
        elif self.playlist and self.current_playlist_index != -1:
            return self.play_file(self.playlist[self.current_playlist_index])
        elif self.playlist:
            self.current_playlist_index = 0
            return self.play_file(self.playlist[0])
        elif self.active_input_plugin and self.active_input_plugin.current_filename:
            return self.play_file(self.active_input_plugin.current_filename)
        return False

    def play_file(self, filename: str) -> bool:
        plugin = self.find_input_plugin_for_file(filename)
        if not plugin:
            return False

        if self.active_input_plugin:
            self.active_input_plugin.stop()

        if not self.active_output_plugin and self.output_plugins:
            self.active_output_plugin = self.output_plugins[0]

        if not self.active_output_plugin:
            return False

        self.active_input_plugin = plugin
        self.active_input_plugin.out_mod = self.active_output_plugin
        self.active_output_plugin.open(44100, 2, 16, 2000)

        self.active_input_plugin.set_volume(self.volume)
        self.active_input_plugin.set_pan(self.pan)
        self.active_input_plugin.play(filename)
        self.is_playing = True
        return True

    def step_audio_pipeline(self) -> Optional[AudioChunk]:
        """
        Executes one decoding step of the audio pipeline:
        Decode frame -> Apply Equalizer & DSP chain -> Output to Ring Buffer.
        """
        if not self.is_playing or not self.active_input_plugin:
            return None

        # 1. Decode raw chunk
        chunk = self.active_input_plugin.decode_frame()
        if not chunk:
            self.is_playing = False
            return None

        # 2. Equalizer Processing Stage
        if self.eq_enabled:
            # Simple global gain modification representing EQ profile
            avg_eq = (sum(self.eq_bands) / 10.0) + self.eq_preamp
            scale = math.pow(10.0, avg_eq / 20.0)
            chunk.samples = [max(-1.0, min(1.0, s * scale)) for s in chunk.samples]

        # 3. DSP Stage Chain
        for dsp in self.dsp_plugins:
            if dsp.enabled:
                chunk = dsp.modify_samples(chunk)

        # 4. Write to Output Module
        if self.active_output_plugin:
            self.active_output_plugin.write(chunk)

        return chunk

    def pause(self) -> None:
        if self.active_input_plugin:
            if self.active_input_plugin.is_paused():
                self.active_input_plugin.unpause()
            else:
                self.active_input_plugin.pause()

    def stop(self) -> None:
        if self.active_input_plugin:
            self.active_input_plugin.stop()
        if self.active_output_plugin:
            self.active_output_plugin.close()
        self.is_playing = False

    def next_track(self) -> bool:
        if not self.playlist:
            return False
        self.current_playlist_index = (self.current_playlist_index + 1) % len(self.playlist)
        return self.play_file(self.playlist[self.current_playlist_index])


# ============================================================================
# 5. Classic Skin Declarative UI Engine
# ============================================================================

class ClassicSkinEngine:
    """
    Simulates Classic Skin bitmap sprite sheet mapping and UI event binding.
    """
    def __init__(self):
        self.sprite_maps: Dict[str, Tuple[int, int, int, int]] = {
            # control_name -> (x, y, width, height) in MAIN.BMP
            "TITLE_BAR": (0, 0, 275, 14),
            "PLAY_BUTTON": (0, 135, 23, 18),
            "PAUSE_BUTTON": (23, 135, 23, 18),
            "STOP_BUTTON": (46, 135, 23, 18),
            "PREV_BUTTON": (69, 135, 23, 18),
            "NEXT_BUTTON": (92, 135, 23, 18),
            "VOLUME_SLIDER": (0, 200, 68, 13),
            "EQ_SLIDER": (0, 240, 14, 63)
        }
        self.transparent_mask_regions: List[Tuple[int, int, int, int]] = []

    def load_region_mask(self, region_lines: List[str]) -> None:
        """Parses REGION.TXT transparent bounding boxes."""
        for line in region_lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [int(p) for p in line.split(",") if p.strip().isdigit()]
            if len(parts) == 4:
                self.transparent_mask_regions.append((parts[0], parts[1], parts[2], parts[3]))

    def get_sprite_offset(self, control_name: str) -> Optional[Tuple[int, int, int, int]]:
        return self.sprite_maps.get(control_name)

    def dispatch_ui_click(self, control_name: str, host: WinampHost) -> str:
        """Simulates clicking a mapped control on the rendered window surface."""
        if control_name == "PLAY_BUTTON":
            if host.playlist and host.current_playlist_index == -1:
                host.current_playlist_index = 0
                host.play_file(host.playlist[0])
            elif host.active_input_plugin and host.active_input_plugin.current_filename:
                host.play_file(host.active_input_plugin.current_filename)
            return "PLAYED"
        elif control_name == "PAUSE_BUTTON":
            host.pause()
            return "PAUSED"
        elif control_name == "STOP_BUTTON":
            host.stop()
            return "STOPPED"
        elif control_name == "NEXT_BUTTON":
            host.next_track()
            return "NEXT_TRACK"
        return "UNKNOWN_CONTROL"


# ============================================================================
# 6. Playlist & Media Library Substrate
# ============================================================================

class TrackMetadata:
    """Represents local file metadata parsed from ID3 tags or media database."""
    def __init__(self, filename: str, title: str, artist: str, album: str, duration_sec: int, genre: str = "Unknown"):
        self.filename = filename
        self.title = title
        self.artist = artist
        self.album = album
        self.duration_sec = duration_sec
        self.genre = genre


class PlaylistManager:
    """
    Parses M3U/PLS files and maintains a local Media Library index.
    """
    def __init__(self):
        self.media_library: Dict[str, TrackMetadata] = {}

    def add_track_to_library(self, track: TrackMetadata) -> None:
        self.media_library[track.filename] = track

    def parse_m3u_content(self, m3u_text: str) -> List[str]:
        """Parses plain or Extended M3U playlist format."""
        files = []
        for line in m3u_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            files.append(line)
        return files

    def parse_pls_content(self, pls_text: str) -> List[str]:
        """Parses INI-style PLS playlist format."""
        files = []
        for line in pls_text.splitlines():
            line = line.strip()
            if line.lower().startswith("file"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    files.append(parts[1].strip())
        return files

    def search_library(self, query: str) -> List[TrackMetadata]:
        """
        Executes instantaneous tokenized substring search over local catalog fields.
        """
        q_clean = query.lower().strip()
        if not q_clean:
            return list(self.media_library.values())

        tokens = q_clean.split()
        results = []

        for track in self.media_library.values():
            haystack = f"{track.title} {track.artist} {track.album} {track.genre} {track.filename}".lower()
            if all(token in haystack for token in tokens):
                results.append(track)

        return results
