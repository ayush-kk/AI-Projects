import logging
from typing import AsyncGenerator

from app.config import settings
from app.services.llm.base import LLMClient

logger = logging.getLogger(__name__)

GROQ_MODELS = [
    {"id": "llama-3.3-70b-versatile", "name": "Llama 3.3 70B", "provider": "groq"},
    {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B", "provider": "groq"},
    {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B", "provider": "groq"},
    {"id": "gemma2-9b-it", "name": "Gemma 2 9B", "provider": "groq"},
]


class GroqClient(LLMClient):
    def __init__(self):
        self.api_key = settings.groq_api_key

    def _get_client(self):
        from groq import AsyncGroq

        return AsyncGroq(api_key=self.api_key)

    async def generate(self, messages: list[dict], model: str, **kwargs) -> str:
        if not self.api_key:
            raise ValueError("Groq API key not configured")

        client = self._get_client()
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=False,
        )
        return response.choices[0].message.content or ""

    async def generate_stream(
        self, messages: list[dict], model: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        if not self.api_key:
            raise ValueError("Groq API key not configured")

        client = self._get_client()
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content

    async def list_models(self) -> list[dict]:
        if not self.api_key:
            return []
        return GROQ_MODELS.copy()
