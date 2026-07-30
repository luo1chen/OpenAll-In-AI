"""
Configuration management using Pydantic Settings
"""
import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    log_level: str = "info"


class DatabaseConfig(BaseModel):
    url: str = "sqlite+aiosqlite:///./data/openall.db"
    echo: bool = False


class ModelConfig(BaseModel):
    cache_dir: str = "./models"
    default_model: str = "qwen2.5-7b"
    auto_download: bool = True
    max_memory: dict = {"cpu": "8GB", "gpu": "4GB"}


class APIConfig(BaseModel):
    enabled: bool = False
    base_url: str = ""
    api_key: str = ""
    default_model: str = ""


class APIsConfig(BaseModel):
    openai: APIConfig = APIConfig()
    dashscope: APIConfig = APIConfig()
    spark: APIConfig = APIConfig()
    deepseek: APIConfig = APIConfig()


class PluginsConfig(BaseModel):
    enabled: bool = True
    market_url: str = "https://plugins.openall.ai"
    auto_update: bool = False


class MediaConfig(BaseModel):
    temp_dir: str = "./data/temp"
    max_file_size: str = "100MB"
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".mp3", ".wav", ".mp4", ".avi", ".pdf"]


class SecurityConfig(BaseModel):
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 1440


class Settings(BaseSettings):
    server: ServerConfig = ServerConfig()
    database: DatabaseConfig = DatabaseConfig()
    models: ModelConfig = ModelConfig()
    apis: APIsConfig = APIsConfig()
    plugins: PluginsConfig = PluginsConfig()
    media: MediaConfig = MediaConfig()
    security: SecurityConfig = SecurityConfig()

    class Config:
        env_prefix = ""
        case_sensitive = False


def load_config_from_json(config_path: str = "./config.json") -> dict:
    """Load configuration from JSON file"""
    path = Path(config_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    config_data = load_config_from_json()
    return Settings(**config_data)


settings = get_settings()
