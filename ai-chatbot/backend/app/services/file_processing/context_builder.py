import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UploadedFile

logger = logging.getLogger(__name__)

MAX_CONTEXT_LENGTH = 8000


async def build_file_context(
    db: AsyncSession, conversation_id: int, user_id: int
) -> str:
    result = await db.execute(
        select(UploadedFile).where(
            UploadedFile.conversation_id == conversation_id,
            UploadedFile.user_id == user_id,
            UploadedFile.is_processed == True,
        )
    )
    files = result.scalars().all()

    if not files:
        return ""

    context_parts = []
    total_length = 0

    for file in files:
        if not file.extracted_text:
            continue
        header = f"--- File: {file.filename} ({file.file_type}) ---\n"
        remaining = MAX_CONTEXT_LENGTH - total_length
        if remaining <= 0:
            break

        text = file.extracted_text[:remaining]
        part = header + text
        context_parts.append(part)
        total_length += len(part)

    return "\n\n".join(context_parts)
