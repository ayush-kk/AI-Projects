from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.models import User
from app.services.llm.model_router import model_router

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("")
async def list_models(current_user: User = Depends(get_current_user)):
    models = await model_router.list_all_models()
    return {"models": models}


@router.get("/ollama/refresh")
async def refresh_ollama_models(current_user: User = Depends(get_current_user)):
    models = await model_router.ollama.list_models()
    return {"models": models}
