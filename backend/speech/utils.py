"""
Speech processing utilities (STT and TTS).
"""
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """Mock STT transcription (requires whisper)."""
    logger.info(f"Transcribing {audio_path} in {language}")
    return "This is a transcribed sample text from the audio."

def synthesize_speech(text: str, language: str = "en", output_path: str = None) -> str:
    """Mock TTS synthesis (requires coqui TTS)."""
    logger.info(f"Synthesizing speech for: {text[:20]}... in {language}")
    if not output_path:
        output_path = os.path.join(settings.MEDIA_ROOT, "audio", "sample_speech.wav")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # create empty file for mock
    with open(output_path, "wb") as f:
        f.write(b"MOCK AUDIO DATA")
    return output_path
