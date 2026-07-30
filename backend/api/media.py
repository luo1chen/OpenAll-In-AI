"""
Media processing API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from backend.core.database import get_db
from backend.services.media_service import MediaService

router = APIRouter()


class TTSRequest(BaseModel):
    text: str
    lang: str = "zh"
    speed: float = 1.0


class ASRRequest(BaseModel):
    language: str = "zh"


class OCRRequest(BaseModel):
    language: str = "zh"
    document_type: Optional[str] = None


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: float
    result: Optional[dict] = None
    error: Optional[str] = None


def get_media_service(db: AsyncSession = Depends(get_db)) -> MediaService:
    return MediaService(db)


@router.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    service: MediaService = Depends(get_media_service)
):
    """Convert text to speech"""
    result = await service.text_to_speech(
        text=request.text,
        lang=request.lang,
        speed=request.speed
    )
    return result


@router.post("/asr")
async def speech_to_text(
    file: UploadFile = File(...),
    language: str = "zh",
    service: MediaService = Depends(get_media_service)
):
    """Convert speech to text"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.speech_to_text(
        audio_data=content,
        filename=file.filename,
        language=language
    )
    return result


@router.post("/ocr")
async def ocr_recognize(
    file: UploadFile = File(...),
    language: str = "zh",
    service: MediaService = Depends(get_media_service)
):
    """OCR text recognition"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.ocr_recognize(
        image_data=content,
        filename=file.filename,
        language=language
    )
    return result


@router.post("/denoise")
async def audio_denoise(
    file: UploadFile = File(...),
    service: MediaService = Depends(get_media_service)
):
    """Audio noise reduction"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.audio_denoise(
        audio_data=content,
        filename=file.filename
    )
    return result


@router.post("/image/generate")
async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 512,
    height: int = 512,
    steps: int = 20,
    service: MediaService = Depends(get_media_service)
):
    """Generate image from text prompt"""
    result = await service.generate_image(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        steps=steps
    )
    return result


@router.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    service: MediaService = Depends(get_media_service)
):
    """Get media processing task status"""
    task = await service.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
