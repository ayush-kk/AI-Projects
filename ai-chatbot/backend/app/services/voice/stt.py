import logging
import tempfile

from app.config import settings

logger = logging.getLogger(__name__)


async def speech_to_text(audio_path: str) -> str:
    try:
        from faster_whisper import WhisperModel

        model = WhisperModel(
            settings.whisper_model_size, device="cpu", compute_type="int8"
        )
        segments, info = model.transcribe(audio_path, language=None)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    except Exception as e:
        logger.error(f"Speech-to-text error: {e}")
        return ""
