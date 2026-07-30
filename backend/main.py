"""
OpenAll-In-AI Backend Application
FastAPI application entry point with comprehensive API documentation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

from backend.core.config import settings
from backend.api import chat, media, office, code, plugins
from backend.core.database import engine, Base
import backend.models  # noqa: F401 - Import models to register with Base.metadata


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
    title="🚀 OpenAll-In-AI API",
    description="""
# OpenAll-In-AI API

**The Ultimate All-in-One Local AI Toolbox API**

OpenAll-In-AI provides a comprehensive set of AI-powered tools through a clean,
RESTful API. Combine the power of large language models, AI image generation,
OCR, document processing, code assistance, and more — all in one place.

## ✨ Key Features

- 💬 **AI Chat** — Multi-model conversation with local and cloud support
- 🎨 **AI Image Generation** — Text-to-image, image-to-image, outpainting
- 📄 **Document Processing** — PDF tools, OCR, document parsing
- 💻 **Code Assistance** — Generation, debugging, scaffolding
- 🎙️ **Media Processing** — Speech-to-text, voiceover, audio analysis
- 🔌 **Plugin System** — Extensible architecture for custom tools

## 🔒 Privacy First

All processing happens locally when using local models. Cloud APIs are optional
and can be configured in the settings page.

## 📚 Quick Start

```bash
# Chat with AI
POST /api/chat/send
{
    "content": "Hello, who are you?",
    "model": "qwen2.5-7b"
}

# List available models
GET /api/chat/models
```
""",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)

# CORS middleware
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with branding"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="🚀 OpenAll-In-AI API Documentation",
        swagger_favicon_url="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚀</text></svg>",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """ReDoc API documentation"""
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="🚀 OpenAll-In-AI API Documentation",
    )


# Include API routers
app.include_router(chat.router, prefix="/api/chat", tags=["💬 AI Chat"])
app.include_router(media.router, prefix="/api/media", tags=["🎬 Media Processing"])
app.include_router(office.router, prefix="/api/office", tags=["📄 Office Tools"])
app.include_router(code.router, prefix="/api/code", tags=["💻 Code Assistant"])
app.include_router(plugins.router, prefix="/api/plugins", tags=["🔌 Plugin System"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "🚀 OpenAll-In-AI",
        "version": "1.0.0",
        "description": "The Ultimate All-in-One Local AI Toolbox",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "media": "/api/media",
            "office": "/api/office",
            "code": "/api/code",
            "plugins": "/api/plugins",
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": "2026-07-30T00:00:00Z"
        }
    )


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    """Custom OpenAPI schema"""
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload
    )