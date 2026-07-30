"""
Database models for OpenAll-In-AI
"""
from sqlalchemy import Boolean, Column, DateTime, Float, String, Text
from sqlalchemy.sql import func

from backend.core.database import Base


class ChatSession(Base):
    """Chat session model"""
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), default="新对话")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    model = Column(String(100), default="qwen2.5-7b")
    system_prompt = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "model": self.model,
            "system_prompt": self.system_prompt
        }


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), index=True)
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class MediaTask(Base):
    """Media processing task model"""
    __tablename__ = "media_tasks"

    id = Column(String(36), primary_key=True)
    task_type = Column(String(50))  # tts, asr, ocr, denoise, image
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    progress = Column(Float, default=0.0)
    input_data = Column(Text, nullable=True)
    output_data = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "status": self.status,
            "progress": self.progress,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class Plugin(Base):
    """Plugin model"""
    __tablename__ = "plugins"

    id = Column(String(100), primary_key=True)
    name = Column(String(255))
    version = Column(String(20))
    description = Column(Text)
    author = Column(String(100))
    enabled = Column(Boolean, default=True)
    config = Column(Text, nullable=True)
    installed_at = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "installed_at": self.installed_at.isoformat() if self.installed_at else None
        }
