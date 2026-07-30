"""
Media service for multimedia processing
"""
import uuid
from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import MediaTask


class MediaService:
    """Service for media processing (TTS, ASR, OCR, etc.)"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._tasks: Dict[str, Dict[str, Any]] = {}

    async def text_to_speech(
        self,
        text: str,
        lang: str = "zh",
        speed: float = 1.0
    ) -> Dict[str, Any]:
        """Convert text to speech"""
        task_id = str(uuid.uuid4())

        # Create task record
        task = MediaTask(
            id=task_id,
            task_type="tts",
            status="pending",
            input_data=text
        )
        self.db.add(task)
        await self.db.commit()

        # Process (simplified - actual implementation would use TTS engine)
        task.status = "running"
        await self.db.commit()

        # Return task info for frontend to poll
        return {
            "task_id": task_id,
            "status": "started",
            "message": "TTS task queued"
        }

    async def speech_to_text(
        self,
        audio_data: bytes,
        filename: str,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """Convert speech to text"""
        task_id = str(uuid.uuid4())

        task = MediaTask(
            id=task_id,
            task_type="asr",
            status="pending",
            input_data=filename
        )
        self.db.add(task)
        await self.db.commit()

        return {
            "task_id": task_id,
            "status": "started",
            "message": "ASR task queued"
        }

    async def ocr_recognize(
        self,
        image_data: bytes,
        filename: str,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """OCR text recognition"""
        task_id = str(uuid.uuid4())

        task = MediaTask(
            id=task_id,
            task_type="ocr",
            status="pending",
            input_data=filename
        )
        self.db.add(task)
        await self.db.commit()

        return {
            "task_id": task_id,
            "status": "started",
            "message": "OCR task queued"
        }

    async def audio_denoise(
        self,
        audio_data: bytes,
        filename: str
    ) -> Dict[str, Any]:
        """Audio noise reduction"""
        task_id = str(uuid.uuid4())

        task = MediaTask(
            id=task_id,
            task_type="denoise",
            status="pending",
            input_data=filename
        )
        self.db.add(task)
        await self.db.commit()

        return {
            "task_id": task_id,
            "status": "started",
            "message": "Denoise task queued"
        }

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 512,
        height: int = 512,
        steps: int = 20
    ) -> Dict[str, Any]:
        """Generate image from text prompt"""
        task_id = str(uuid.uuid4())

        task = MediaTask(
            id=task_id,
            task_type="image",
            status="pending",
            input_data=prompt
        )
        self.db.add(task)
        await self.db.commit()

        return {
            "task_id": task_id,
            "status": "started",
            "message": "Image generation task queued"
        }

    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        result = await self.db.execute(
            select(MediaTask).where(MediaTask.id == task_id)
        )
        task = result.scalar_one_or_none()

        if not task:
            return None

        return {
            "task_id": task.id,
            "status": task.status,
            "progress": task.progress,
            "result": task.output_data,
            "error": task.error
        }
