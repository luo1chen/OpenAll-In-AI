"""
Tests for model registry
"""
import pytest
from backend.model_manager.registry import ModelRegistry


def test_list_models():
    """Test listing available models"""
    registry = ModelRegistry()
    models = registry.list_models()

    assert len(models) > 0
    assert any(m.name == "Qwen 2.5 7B" for m in models)


def test_get_model_info():
    """Test getting model information"""
    registry = ModelRegistry()
    model = registry.get_model_info("qwen2.5-7b")

    assert model is not None
    assert model.name == "Qwen 2.5 7B"
    assert model.size == 7_000_000_000


def test_get_repo_id():
    """Test getting model repo ID"""
    registry = ModelRegistry()

    repo_id = registry.get_repo_id("qwen2.5-7b")
    assert repo_id == "Qwen/Qwen2.5-7B-Instruct"

    repo_id = registry.get_repo_id("llama3-8b")
    assert repo_id == "meta-llama/Meta-Llama-3-8B-Instruct"


def test_is_downloaded():
    """Test checking if model is downloaded"""
    registry = ModelRegistry()

    # Initially no models are downloaded
    assert registry.is_downloaded("qwen2.5-7b") is False


def test_get_downloaded_models():
    """Test getting list of downloaded models"""
    registry = ModelRegistry()
    downloaded = registry.get_downloaded_models()

    assert isinstance(downloaded, list)
