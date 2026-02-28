import logging
from typing import AsyncGenerator

from app.services.llm.base import LLMClient
from app.services.llm.groq_client import GroqClient
from app.services.llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

GROQ_MODEL_IDS = {
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
}


class ModelRouter:
    def __init__(self):
        self.ollama = OllamaClient()
        self.groq = GroqClient()

    def _get_client(self, model: str) -> LLMClient:
        if model in GROQ_MODEL_IDS or model.startswith("groq:"):
            return self.groq
        return self.ollama

    def _clean_model_name(self, model: str) -> str:
        if model.startswith("groq:"):
            return model[5:]
        if model.startswith("ollama:"):
            return model[7:]
        return model

    async def generate(self, messages: list[dict], model: str, **kwargs) -> str:
        client = self._get_client(model)
        clean_model = self._clean_model_name(model)
        return await client.generate(messages, clean_model, **kwargs)

    async def generate_stream(
        self, messages: list[dict], model: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        client = self._get_client(model)
        clean_model = self._clean_model_name(model)
        async for token in client.generate_stream(messages, clean_model, **kwargs):
            yield token

    async def list_all_models(self) -> list[dict]:
        models = []
        ollama_models = await self.ollama.list_models()
        models.extend(ollama_models)
        groq_models = await self.groq.list_models()
        models.extend(groq_models)
        return models


model_router = ModelRouter()
