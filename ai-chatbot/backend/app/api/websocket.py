import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import verify_token
from app.db.base import AsyncSessionLocal
from app.db.models import Conversation, Message, User
from app.services.chat_service import generate_response_stream
from app.services.file_processing.context_builder import build_file_context

router = APIRouter(tags=["WebSocket"])
logger = logging.getLogger(__name__)


async def authenticate_ws(token: str) -> int | None:
    payload = verify_token(token)
    if payload is None or payload.get("type") != "access":
        return None
    return int(payload.get("sub"))


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        init_data = await websocket.receive_text()
        init_msg = json.loads(init_data)
        token = init_msg.get("token")
        if not token:
            await websocket.send_json({"type": "error", "message": "Token required"})
            await websocket.close()
            return

        user_id = await authenticate_ws(token)
        if not user_id:
            await websocket.send_json({"type": "error", "message": "Invalid token"})
            await websocket.close()
            return

        await websocket.send_json({"type": "connected", "message": "Authenticated"})

        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            msg_type = msg.get("type", "chat_message")
            if msg_type != "chat_message":
                continue

            conversation_id = msg.get("conversation_id")
            user_message = msg.get("message", "")
            model = msg.get("model", "llama-3.1-8b-instant")
            search_enabled = msg.get("search_enabled", False)

            if not user_message.strip():
                continue

            async with AsyncSessionLocal() as db:
                if conversation_id:
                    result = await db.execute(
                        select(Conversation)
                        .options(selectinload(Conversation.messages))
                        .where(
                            Conversation.id == conversation_id,
                            Conversation.user_id == user_id,
                        )
                    )
                    conversation = result.scalar_one_or_none()
                else:
                    conversation = Conversation(
                        user_id=user_id,
                        title=user_message[:50],
                        model_name=model,
                    )
                    db.add(conversation)
                    await db.flush()
                    await db.refresh(conversation)

                if not conversation:
                    await websocket.send_json(
                        {"type": "error", "message": "Conversation not found"}
                    )
                    continue

                user_msg = Message(
                    conversation_id=conversation.id,
                    role="user",
                    content=user_message,
                )
                db.add(user_msg)
                await db.flush()

                history = []
                if hasattr(conversation, "messages") and conversation.messages:
                    history = [
                        {"role": m.role, "content": m.content}
                        for m in conversation.messages
                    ]

                file_context = await build_file_context(db, conversation.id, user_id)

                await websocket.send_json({
                    "type": "start",
                    "conversation_id": conversation.id,
                })

                full_response = ""
                try:
                    async for token in generate_response_stream(
                        history,
                        user_message,
                        model,
                        file_context=file_context if file_context else None,
                        search_enabled=search_enabled,
                    ):
                        full_response += token
                        await websocket.send_json({"type": "token", "content": token})
                except Exception as e:
                    logger.error(f"LLM streaming error: {e}")
                    full_response = f"Sorry, an error occurred: {str(e)}"
                    await websocket.send_json(
                        {"type": "error", "message": str(e)}
                    )

                assistant_msg = Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=full_response,
                )
                db.add(assistant_msg)
                conversation.updated_at = datetime.now(timezone.utc)
                conversation.model_name = model
                await db.commit()

                await websocket.send_json({
                    "type": "complete",
                    "conversation_id": conversation.id,
                    "message_id": assistant_msg.id if assistant_msg.id else 0,
                })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": "Internal error"})
        except Exception:
            pass
