import logging
import os
import tempfile

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.db.models import User
from app.services.voice.stt import speech_to_text
from app.services.voice.tts import text_to_speech

router = APIRouter(prefix="/voice", tags=["Voice"])
logger = logging.getLogger(__name__)


class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"


@router.post("/stt")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    allowed = {"wav", "mp3", "ogg", "webm", "m4a", "flac"}
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Audio format .{ext} not supported")

    with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = await speech_to_text(tmp_path)
        if not text:
            raise HTTPException(status_code=422, detail="Could not transcribe audio")
        return {"text": text}
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@router.post("/tts")
async def synthesize_speech(
    request: TTSRequest,
    current_user: User = Depends(get_current_user),
):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    filepath = await text_to_speech(request.text, current_user.id, request.voice)
    if not filepath:
        raise HTTPException(status_code=500, detail="Failed to generate speech")

    filename = os.path.basename(filepath)
    return {
        "filename": filename,
        "download_url": f"/api/v1/documents/download/{filename}?user_id={current_user.id}",
    }
