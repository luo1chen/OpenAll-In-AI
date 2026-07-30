"""
Model registry for managing available models
"""
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.core.config import settings


class ModelInfo:
    """Model information"""

    def __init__(
        self,
        name: str,
        size: int,
        dtype: str,
        quantized: bool,
        local_path: Optional[str] = None,
        status: str = "available"
    ):
        self.name = name
        self.size = size
        self.dtype = dtype
        self.quantized = quantized
        self.local_path = local_path
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "size": self.size,
            "dtype": self.dtype,
            "quantized": self.quantized,
            "local_path": self.local_path,
            "status": self.status
        }


class ModelRegistry:
    """Registry for available models"""

    # Predefined model catalog
    MODEL_CATALOG = {
        "qwen2.5-7b": {
            "name": "Qwen 2.5 7B",
            "size": 7_000_000_000,
            "dtype": "FP16",
            "quantized": False,
            "repo_id": "Qwen/Qwen2.5-7B-Instruct"
        },
        "qwen2.5-3b": {
            "name": "Qwen 2.5 3B",
            "size": 3_000_000_000,
            "dtype": "FP16",
            "quantized": False,
            "repo_id": "Qwen/Qwen2.5-3B-Instruct"
        },
        "llama3-8b": {
            "name": "Llama 3 8B",
            "size": 8_000_000_000,
            "dtype": "FP16",
            "quantized": False,
            "repo_id": "meta-llama/Meta-Llama-3-8B-Instruct"
        },
        "gemma-2b": {
            "name": "Gemma 2B",
            "size": 2_000_000_000,
            "dtype": "FP16",
            "quantized": False,
            "repo_id": "google/gemma-2b-it"
        },
        "phi-2": {
            "name": "Phi-2",
            "size": 2_000_000_000,
            "dtype": "FP16",
            "quantized": False,
            "repo_id": "microsoft/phi-2"
        }
    }

    def __init__(self):
        self.cache_dir = Path(settings.models.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._downloaded_models: Dict[str, str] = {}

    def list_models(self) -> List[ModelInfo]:
        """List all available models"""
        models = []

        for model_id, info in self.MODEL_CATALOG.items():
            local_path = self._get_local_path(model_id)
            status = "downloaded" if local_path.exists() else "available"

            models.append(ModelInfo(
                name=info["name"],
                size=info["size"],
                dtype=info["dtype"],
                quantized=info["quantized"],
                local_path=str(local_path) if local_path.exists() else None,
                status=status
            ))

        return models

    def get_model_info(self, model_id: str) -> Optional[ModelInfo]:
        """Get information about a specific model"""
        if model_id not in self.MODEL_CATALOG:
            return None

        info = self.MODEL_CATALOG[model_id]
        local_path = self._get_local_path(model_id)
        status = "downloaded" if local_path.exists() else "available"

        return ModelInfo(
            name=info["name"],
            size=info["size"],
            dtype=info["dtype"],
            quantized=info["quantized"],
            local_path=str(local_path) if local_path.exists() else None,
            status=status
        )

    def get_repo_id(self, model_id: str) -> Optional[str]:
        """Get HuggingFace repo ID for a model"""
        if model_id in self.MODEL_CATALOG:
            return self.MODEL_CATALOG[model_id]["repo_id"]
        return None

    def _get_local_path(self, model_id: str) -> Path:
        """Get local path for a model"""
        return self.cache_dir / model_id

    def is_downloaded(self, model_id: str) -> bool:
        """Check if a model is already downloaded"""
        return self._get_local_path(model_id).exists()

    def get_downloaded_models(self) -> List[str]:
        """Get list of downloaded model IDs"""
        return [
            model_id for model_id in self.MODEL_CATALOG.keys()
            if self.is_downloaded(model_id)
        ]
