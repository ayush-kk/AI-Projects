import logging
import os
from datetime import datetime
from pathlib import Path

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

HF_SD_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


async def generate_image(prompt: str, user_id: int) -> str:
    output_dir = Path(settings.generated_dir) / str(user_id) / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = str(output_dir / filename)

    if settings.huggingface_token:
        try:
            result = await _generate_via_huggingface(prompt)
            if result:
                with open(filepath, "wb") as f:
                    f.write(result)
                return filepath
        except Exception as e:
            logger.warning(f"HuggingFace image gen failed: {e}")

    try:
        result = await _generate_via_ollama(prompt)
        if result:
            with open(filepath, "wb") as f:
                f.write(result)
            return filepath
    except Exception as e:
        logger.warning(f"Ollama image gen failed: {e}")

    return ""


async def _generate_via_huggingface(prompt: str) -> bytes:
    headers = {"Authorization": f"Bearer {settings.huggingface_token}"}
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            HF_SD_URL,
            headers=headers,
            json={"inputs": prompt},
        )
        response.raise_for_status()
        return response.content


async def _generate_via_ollama(prompt: str) -> bytes:
    import json

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.ollama_base_url}/api/generate",
            json={
                "model": "sdxl",
                "prompt": prompt,
            },
        )
        if response.status_code == 200:
            data = response.json()
            import base64

            images = data.get("images", [])
            if images:
                return base64.b64decode(images[0])
    return None
