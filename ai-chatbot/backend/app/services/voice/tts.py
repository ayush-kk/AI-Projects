import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)


async def text_to_speech(text: str, user_id: int, voice: str = "en-US-AriaNeural") -> str:
    try:
        import edge_tts

        output_dir = Path(settings.generated_dir) / str(user_id) / "audio"
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        filepath = str(output_dir / filename)

        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
        return filepath
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        return ""
