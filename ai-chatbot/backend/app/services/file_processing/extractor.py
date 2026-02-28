import logging
import os
from pathlib import Path

import pdfplumber
from docx import Document as DocxDocument

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    try:
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""


def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = DocxDocument(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return ""


def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        logger.error(f"TXT extraction error: {e}")
        return ""


def extract_text_from_csv(file_path: str) -> str:
    try:
        import pandas as pd

        df = pd.read_csv(file_path)
        summary = f"CSV file with {len(df)} rows and {len(df.columns)} columns.\n"
        summary += f"Columns: {', '.join(df.columns.tolist())}\n\n"
        summary += "First 20 rows:\n"
        summary += df.head(20).to_string(index=False)
        return summary
    except Exception as e:
        logger.error(f"CSV extraction error: {e}")
        return ""


def extract_text_from_image(file_path: str) -> str:
    try:
        import easyocr

        reader = easyocr.Reader(["en"], gpu=False)
        results = reader.readtext(file_path)
        text_parts = [result[1] for result in results]
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"Image OCR error: {e}")
        return ""


EXTRACTORS = {
    "pdf": extract_text_from_pdf,
    "docx": extract_text_from_docx,
    "doc": extract_text_from_docx,
    "txt": extract_text_from_txt,
    "csv": extract_text_from_csv,
    "png": extract_text_from_image,
    "jpg": extract_text_from_image,
    "jpeg": extract_text_from_image,
}


def extract_text(file_path: str, file_type: str) -> str:
    ext = file_type.lower().lstrip(".")
    extractor = EXTRACTORS.get(ext)
    if extractor:
        return extractor(file_path)
    return f"Unsupported file type: {file_type}"
