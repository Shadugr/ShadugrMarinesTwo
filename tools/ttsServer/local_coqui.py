import os
import torch
from pydub import AudioSegment
import base64
import tempfile
from TTS.api import TTS


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

    def make_ogg_base64(self, text, speaker, sample_rate):
        """
        Generate TTS audio and return as base64-encoded OGG.

        Args:
            text: Text to synthesize
            speaker: Speaker ID/name (from XTTS v2 speaker list)
            sample_rate: Sample rate (note: XTTS v2 uses 24000Hz internally)

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

            # Read and encode to base64
            with open(ogg_path, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode()

            # Cleanup temp ogg file
            if os.path.exists(ogg_path):
                os.remove(ogg_path)

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
