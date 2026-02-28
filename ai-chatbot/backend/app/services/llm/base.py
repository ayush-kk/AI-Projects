from abc import ABC, abstractmethod
from typing import AsyncGenerator


class LLMClient(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict], model: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def generate_stream(
        self, messages: list[dict], model: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        pass

    @abstractmethod
    async def list_models(self) -> list[dict]:
        pass
