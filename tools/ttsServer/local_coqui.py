import os
import torch
from pydub import AudioSegment
import base64
import tempfile
import subprocess
from TTS.api import TTS


# Effect constants matching the game code
SOUND_EFFECT_NONE = 0
SOUND_EFFECT_RADIO = 1
SOUND_EFFECT_ROBOT = 2
SOUND_EFFECT_RADIO_ROBOT = 3
SOUND_EFFECT_MEGAPHONE = 4
SOUND_EFFECT_MEGAPHONE_ROBOT = 5
SOUND_EFFECT_HIVEMIND = 6

# FFmpeg filter definitions for each effect
FFMPEG_FILTERS = {
    SOUND_EFFECT_RADIO: "highpass=f=1000, lowpass=f=3000, acrusher=1:1:50:0:log",
    SOUND_EFFECT_ROBOT: "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.5, deesser=i=0.4, volume=volume=1.5",
    SOUND_EFFECT_RADIO_ROBOT: "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.5, deesser=i=0.4, volume=volume=1.5, highpass=f=1000, lowpass=f=3000, acrusher=1:1:50:0:log",
    SOUND_EFFECT_MEGAPHONE: "highpass=f=500, lowpass=f=4000, volume=volume=10, acrusher=1:1:45:0:log",
    SOUND_EFFECT_MEGAPHONE_ROBOT: "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.5, deesser=i=0.4, highpass=f=500, lowpass=f=4000, volume=volume=10, acrusher=1:1:45:0:log",
    SOUND_EFFECT_HIVEMIND: "chorus=0.5:0.9:50|60|70:0.3|0.22|0.3:0.25|0.4|0.3:2|2.3|1.3",
}


class tts_creator:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        # Initialize Coqui TTS with XTTS v2 model
        # The model should be installed in the ttsServer directory
        self.model_path = os.path.join(os.path.dirname(__file__), "tts_models")

        # Use XTTS v2 - multilingual model with voice cloning support
        # If model is not downloaded, TTS will download it automatically
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)

        # Default speaker for Russian (can be overridden)
        self.default_speaker = "Claribel Dervla"
        self.language = "ru"

    def apply_effect(self, input_path, output_path, effect):
        """Apply audio effect using ffmpeg."""
        if effect not in FFMPEG_FILTERS:
            return False

        filter_str = FFMPEG_FILTERS[effect]
        cmd = [
            'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
            '-i', input_path,
            '-filter:a', filter_str,
            output_path
        ]

        try:
            # Run ffmpeg with hidden window on Windows
            startupinfo = None
            if os.name == 'nt':  # Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            subprocess.run(cmd, check=True, startupinfo=startupinfo,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
            return False

    def make_ogg_base64(self, text, speaker, sample_rate, effect=SOUND_EFFECT_NONE):
        """
        Generate TTS audio and return as base64-encoded OGG.

        Args:
            text: Text to synthesize
            speaker: Speaker ID/name (from XTTS v2 speaker list)
            sample_rate: Sample rate (note: XTTS v2 uses 24000Hz internally)
            effect: Sound effect to apply (0=none, 1=radio, 2=robot, etc.)

        Returns:
            Base64-encoded OGG audio string
        """
        # Create temporary files for wav and ogg
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_file:
            wav_path = wav_file.name

        try:
            # Use the speaker if provided, otherwise use default
            speaker_to_use = speaker if speaker else self.default_speaker

            # Generate speech with XTTS v2
            # XTTS v2 uses speaker embeddings from its internal speaker list
            self.tts.tts_to_file(
                text=text,
                speaker=speaker_to_use,
                language=self.language,
                file_path=wav_path
            )

            # Convert WAV to OGG
            ogg_path = wav_path.replace('.wav', '.ogg')
            AudioSegment.from_wav(wav_path).export(ogg_path, format='ogg')

            # Apply effect if requested
            final_ogg_path = ogg_path
            if effect and effect != SOUND_EFFECT_NONE:
                effect_ogg_path = wav_path.replace('.wav', '_effect.ogg')
                if self.apply_effect(ogg_path, effect_ogg_path, effect):
                    final_ogg_path = effect_ogg_path
                else:
                    print(f"Warning: Failed to apply effect {effect}, using original audio")

            # Read and encode to base64
            with open(final_ogg_path, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode()

            # Cleanup temp files
            for path in [ogg_path, wav_path.replace('.wav', '_effect.ogg')]:
                if os.path.exists(path) and path != final_ogg_path:
                    try:
                        os.remove(path)
                    except:
                        pass

            if os.path.exists(final_ogg_path):
                os.remove(final_ogg_path)

            return audio_base64

        finally:
            # Cleanup temp wav file
            if os.path.exists(wav_path):
                os.remove(wav_path)

    def get_available_speakers(self):
        """Return list of available speakers from the model."""
        if hasattr(self.tts, 'speakers') and self.tts.speakers:
            return self.tts.speakers
        return []
