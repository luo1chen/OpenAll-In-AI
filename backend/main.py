"""
OpenAll-In-AI Backend Application
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.core.config import settings
from backend.api import chat, media, office, code, plugins
from backend.core.database import engine, Base
from backend.models import ChatSession, ChatMessage, MediaTask, Plugin  # Import models to register with Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="OpenAll-In-AI API",
    description="一站式本地部署AI聚合工具箱 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - restrict in production
import os
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat.router, prefix="/api/chat", tags=["AI对话"])
app.include_router(media.router, prefix="/api/media", tags=["多媒体处理"])
app.include_router(office.router, prefix="/api/office", tags=["办公工具"])
app.include_router(code.router, prefix="/api/code", tags=["代码助手"])
app.include_router(plugins.router, prefix="/api/plugins", tags=["插件系统"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "OpenAll-In-AI",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload
    )
