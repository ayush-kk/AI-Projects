import logging

from app.services.llm.model_router import model_router
from app.services.search.web_search import search_web

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are NexusAI, a helpful AI assistant. You can:
- Answer questions and have conversations
- Generate code snippets with syntax highlighting
- Help analyze uploaded files and documents
- Generate Excel, Word, and PDF documents when asked
- Generate images when asked
- Search the internet for current information when enabled

Be helpful, concise, and accurate. Format code in markdown code blocks with language tags."""


async def build_chat_messages(
    conversation_messages: list[dict],
    user_message: str,
    file_context: str = None,
    search_results: str = None,
) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if file_context:
        messages.append(
            {
                "role": "system",
                "content": f"The user has uploaded files. Here is the extracted content:\n\n{file_context}",
            }
        )

    if search_results:
        messages.append(
            {
                "role": "system",
                "content": f"Here are relevant web search results:\n\n{search_results}",
            }
        )

    for msg in conversation_messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})
    return messages


async def generate_response(
    conversation_messages: list[dict],
    user_message: str,
    model: str,
    file_context: str = None,
    search_enabled: bool = False,
):
    search_results = None
    if search_enabled:
        try:
            results = await search_web(user_message, max_results=3)
            if results:
                search_results = "\n".join(
                    [f"- {r['title']}: {r['snippet']} (Source: {r['url']})" for r in results]
                )
        except Exception as e:
            logger.warning(f"Search failed: {e}")

    messages = await build_chat_messages(
        conversation_messages, user_message, file_context, search_results
    )
    return await model_router.generate(messages, model)


async def generate_response_stream(
    conversation_messages: list[dict],
    user_message: str,
    model: str,
    file_context: str = None,
    search_enabled: bool = False,
):
    search_results = None
    if search_enabled:
        try:
            results = await search_web(user_message, max_results=3)
            if results:
                search_results = "\n".join(
                    [f"- {r['title']}: {r['snippet']} (Source: {r['url']})" for r in results]
                )
        except Exception as e:
            logger.warning(f"Search failed: {e}")

    messages = await build_chat_messages(
        conversation_messages, user_message, file_context, search_results
    )
    async for token in model_router.generate_stream(messages, model):
        yield token
