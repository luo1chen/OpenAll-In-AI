"""
Model downloader for downloading models from HuggingFace
"""
import asyncio
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

from backend.model_manager.registry import ModelRegistry


@dataclass
class DownloadTask:
    """Download task information"""
    task_id: str
    model_id: str
    status: str  # pending, downloading, completed, failed
    progress: float
    error: Optional[str] = None


class ModelDownloader:
    """Downloader for AI models from HuggingFace"""

    def __init__(self):
        self.registry = ModelRegistry()
        self._tasks: Dict[str, DownloadTask] = {}

    async def download(self, model_id: str) -> str:
        """Start downloading a model"""
        task_id = str(uuid.uuid4())

        # Check if model exists in catalog
        if not self.registry.get_repo_id(model_id):
            raise ValueError(f"Unknown model: {model_id}")

        # Check if already downloaded
        if self.registry.is_downloaded(model_id):
            return task_id

        # Create task
        task = DownloadTask(
            task_id=task_id,
            model_id=model_id,
            status="pending",
            progress=0.0
        )
        self._tasks[task_id] = task

        # Start download in background
        asyncio.create_task(self._download_model(task_id, model_id))

        return task_id

    async def _download_model(self, task_id: str, model_id: str):
        """Download model in background"""
        task = self._tasks.get(task_id)
        if not task:
            return

        try:
            task.status = "downloading"

            repo_id = self.registry.get_repo_id(model_id)
            local_path = self.registry._get_local_path(model_id)

            # Import huggingface hub
            from huggingface_hub import snapshot_download

            # Download with progress
            await asyncio.to_thread(
                snapshot_download,
                repo_id=repo_id,
                local_dir=str(local_path),
                resume_download=True
            )

            task.status = "completed"
            task.progress = 1.0

        except Exception as e:
            task.status = "failed"
            task.error = str(e)

    def get_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get download status"""
        task = self._tasks.get(task_id)
        if not task:
            return None

        return {
            "task_id": task.task_id,
            "model_id": task.model_id,
            "status": task.status,
            "progress": task.progress,
            "error": task.error
        }

    def cancel(self, task_id: str) -> bool:
        """Cancel a download task"""
        task = self._tasks.get(task_id)
        if not task:
            return False

        if task.status in ["pending", "downloading"]:
            task.status = "cancelled"
            return True
        return False
