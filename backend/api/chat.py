"""
AI Chat API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from backend.core.database import get_db
from backend.services.chat_service import ChatService

router = APIRouter()


# Pydantic Models
class ChatMessageCreate(BaseModel):
    session_id: Optional[str] = None
    content: str = Field(..., min_length=1)
    model: Optional[str] = None
    system_prompt: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime


class ChatSessionCreate(BaseModel):
    title: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    model: str
    system_prompt: str


class ModelInfo(BaseModel):
    name: str
    size: int
    dtype: str
    quantized: bool
    local_path: Optional[str] = None
    status: str  # downloaded, downloading, available


class SendMessageResponse(BaseModel):
    message: ChatMessageResponse
    session: ChatSessionResponse


# Dependency
def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(db)


@router.post("/send")
async def send_message(
    message: ChatMessageCreate,
    service: ChatService = Depends(get_chat_service)
):
    """Send a chat message and get AI response"""
    assistant_message, session = await service.send_message(
        content=message.content,
        session_id=message.session_id,
        model=message.model,
        system_prompt=message.system_prompt
    )
    return {
        "message": assistant_message.to_dict(),
        "session": session.to_dict()
    }


@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    service: ChatService = Depends(get_chat_service)
):
    """Get chat history for a session"""
    messages = await service.get_history(session_id)
    return {"session_id": session_id, "messages": [m.to_dict() for m in messages]}


@router.post("/session")
async def create_session(
    session_data: ChatSessionCreate,
    service: ChatService = Depends(get_chat_service)
):
    """Create a new chat session"""
    session = await service.create_session(
        title=session_data.title,
        model=session_data.model,
        system_prompt=session_data.system_prompt
    )
    return session.to_dict()


@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    service: ChatService = Depends(get_chat_service)
):
    """Delete a chat session"""
    success = await service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}


@router.get("/sessions")
async def list_sessions(
    service: ChatService = Depends(get_chat_service)
):
    """List all chat sessions"""
    sessions = await service.list_sessions()
    return {"sessions": [s.to_dict() for s in sessions]}


@router.get("/models")
async def list_models():
    """List available models"""
    from backend.model_manager.registry import ModelRegistry
    registry = ModelRegistry()
    models = registry.list_models()
    return [m.to_dict() for m in models]


@router.post("/models/download")
async def download_model(
    model_name: str,
    service: ChatService = Depends(get_chat_service)
):
    """Download a model"""
    from backend.model_manager.downloader import ModelDownloader
    downloader = ModelDownloader()
    task_id = await downloader.download(model_name)
    return {"task_id": task_id, "status": "started"}


@router.get("/models/download/status/{task_id}")
async def get_download_status(task_id: str):
    """Get model download status"""
    from backend.model_manager.downloader import ModelDownloader
    downloader = ModelDownloader()
    status = downloader.get_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return status
