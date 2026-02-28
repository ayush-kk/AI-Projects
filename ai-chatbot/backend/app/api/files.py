import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.config import settings
from app.db.base import get_db
from app.db.models import UploadedFile, User
from app.services.file_processing.extractor import extract_text
from app.services.file_processing.video_processor import extract_text_from_video

router = APIRouter(prefix="/files", tags=["Files"])

ALLOWED_EXTENSIONS = {
    "pdf", "docx", "doc", "txt", "csv",
    "png", "jpg", "jpeg", "gif",
    "mp4", "avi", "mov", "mkv", "webm",
}
VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv", "webm"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    conversation_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type .{ext} not supported")

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > settings.max_upload_size_mb:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds {settings.max_upload_size_mb}MB limit",
        )

    upload_dir = Path(settings.upload_dir) / str(current_user.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = str(upload_dir / safe_filename)

    with open(filepath, "wb") as f:
        f.write(content)

    if ext in VIDEO_EXTENSIONS:
        extracted_text = extract_text_from_video(filepath)
    else:
        extracted_text = extract_text(filepath, ext)

    db_file = UploadedFile(
        user_id=current_user.id,
        conversation_id=conversation_id,
        filename=file.filename,
        file_path=filepath,
        file_type=ext,
        file_size=len(content),
        extracted_text=extracted_text,
        is_processed=bool(extracted_text),
    )
    db.add(db_file)
    await db.flush()
    await db.refresh(db_file)

    return {
        "id": db_file.id,
        "filename": db_file.filename,
        "file_type": db_file.file_type,
        "file_size": db_file.file_size,
        "is_processed": db_file.is_processed,
        "extracted_text_preview": (extracted_text[:200] + "...") if extracted_text and len(extracted_text) > 200 else extracted_text,
    }


@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UploadedFile).where(
            UploadedFile.id == file_id,
            UploadedFile.user_id == current_user.id,
        )
    )
    file_record = result.scalar_one_or_none()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(file_record.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        file_record.file_path,
        filename=file_record.filename,
        media_type="application/octet-stream",
    )
