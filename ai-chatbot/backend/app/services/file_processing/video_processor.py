import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def extract_text_from_video(video_path: str) -> str:
    try:
        import ffmpeg

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio_path = tmp.name

        try:
            (
                ffmpeg.input(video_path)
                .output(audio_path, acodec="pcm_s16le", ac=1, ar="16000")
                .overwrite_output()
                .run(quiet=True)
            )
        except Exception as e:
            logger.error(f"FFmpeg audio extraction error: {e}")
            return "Could not extract audio from video. Ensure FFmpeg is installed."

        try:
            from faster_whisper import WhisperModel

            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path, language=None)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            return "Could not transcribe video audio. Ensure faster-whisper is installed."
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

    except Exception as e:
        logger.error(f"Video processing error: {e}")
        return ""
