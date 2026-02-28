import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.exceptions import register_exception_handlers
from app.db.init_db import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG)
    logger.info("Starting NexusAI API...")

    await init_db()
    logger.info("Database initialized")

    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.generated_dir).mkdir(parents=True, exist_ok=True)
    logger.info("Storage directories ready")

    yield

    # Shutdown
    logger.info("Shutting down NexusAI API...")


app = FastAPI(
    title="NexusAI API",
    description="AI-Powered Chatbot Backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
origins = [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Routers
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.documents import router as documents_router
from app.api.files import router as files_router
from app.api.models import router as models_router
from app.api.search import router as search_router
from app.api.voice import router as voice_router
from app.api.websocket import router as ws_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(models_router, prefix="/api/v1")
app.include_router(files_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/api/v1")


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
