import json
import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.db.models import User
from app.services.doc_gen.excel_gen import generate_excel
from app.services.doc_gen.pdf_gen import generate_pdf
from app.services.doc_gen.word_gen import generate_word

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = logging.getLogger(__name__)


class ExcelRequest(BaseModel):
    title: str = None
    sheet_name: str = "Sheet1"
    headers: list[str] = []
    rows: list[list] = []


class WordRequest(BaseModel):
    title: str = "Document"
    subtitle: str = None
    sections: list[dict] = []


class PdfRequest(BaseModel):
    title: str = "Document"
    sections: list[dict] = []


@router.post("/excel")
async def create_excel(
    request: ExcelRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        filepath = generate_excel(request.model_dump(), current_user.id)
        filename = os.path.basename(filepath)
        return {
            "filename": filename,
            "download_url": f"/api/v1/documents/download/{filename}?user_id={current_user.id}",
        }
    except Exception as e:
        logger.error(f"Excel generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate Excel file")


@router.post("/word")
async def create_word(
    request: WordRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        filepath = generate_word(request.model_dump(), current_user.id)
        filename = os.path.basename(filepath)
        return {
            "filename": filename,
            "download_url": f"/api/v1/documents/download/{filename}?user_id={current_user.id}",
        }
    except Exception as e:
        logger.error(f"Word generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate Word document")


@router.post("/pdf")
async def create_pdf(
    request: PdfRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        filepath = generate_pdf(request.model_dump(), current_user.id)
        filename = os.path.basename(filepath)
        return {
            "filename": filename,
            "download_url": f"/api/v1/documents/download/{filename}?user_id={current_user.id}",
        }
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF document")


@router.get("/download/{filename}")
async def download_document(
    filename: str,
    user_id: int = None,
    current_user: User = Depends(get_current_user),
):
    from app.config import settings
    from pathlib import Path

    uid = user_id if user_id == current_user.id else current_user.id
    filepath = Path(settings.generated_dir) / str(uid) / filename

    if not filepath.exists():
        audio_path = Path(settings.generated_dir) / str(uid) / "audio" / filename
        image_path = Path(settings.generated_dir) / str(uid) / "images" / filename
        if audio_path.exists():
            filepath = audio_path
        elif image_path.exists():
            filepath = image_path
        else:
            raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(filepath), filename=filename)
