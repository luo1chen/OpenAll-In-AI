"""
Chat service for AI conversation
"""
import uuid
from datetime import datetime
from typing import Optional, List, Tuple

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import ChatSession, ChatMessage
from backend.core.config import settings
from backend.model_manager.inference import ModelInference


class ChatService:
    """Service for managing chat sessions and messages"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.inference = ModelInference()

    async def send_message(
        self,
        content: str,
        session_id: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> Tuple[ChatMessage, ChatSession]:
        """Send a message and get AI response"""
        # Get or create session
        if session_id:
            session = await self._get_session(session_id)
            if not session:
                session = await self.create_session(
                    title="新对话",
                    model=model,
                    system_prompt=system_prompt
                )
        else:
            session = await self.create_session(
                title=self._generate_title(content),
                model=model,
                system_prompt=system_prompt
            )

        # Save user message
        user_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session.id,
            role="user",
            content=content
        )
        self.db.add(user_message)
        await self.db.flush()

        # Get AI response
        model_name = session.model or settings.models.default_model
        response_content = await self.inference.generate(
            prompt=content,
            model=model_name,
            system_prompt=session.system_prompt
        )

        # Save assistant message
        assistant_message = ChatMessage(
            id=str(uuid.uuid4()),
            session_id=session.id,
            role="assistant",
            content=response_content
        )
        self.db.add(assistant_message)

        # Update session
        session.updated_at = datetime.now()

        await self.db.commit()
        await self.db.refresh(assistant_message)
        await self.db.refresh(session)

        return assistant_message, session

    async def create_session(
        self,
        title: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            id=str(uuid.uuid4()),
            title=title or "新对话",
            model=model or settings.models.default_model,
            system_prompt=system_prompt
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        return await self._get_session(session_id)

    async def _get_session(self, session_id: str) -> Optional[ChatSession]:
        """Internal method to get session"""
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        return result.scalar_one_or_none()

    async def delete_session(self, session_id: str) -> bool:
        """Delete a chat session and its messages"""
        # Delete messages first
        await self.db.execute(
            delete(ChatMessage).where(ChatMessage.session_id == session_id)
        )
        # Delete session
        result = await self.db.execute(
            delete(ChatSession).where(ChatSession.id == session_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def get_history(self, session_id: str) -> List[ChatMessage]:
        """Get chat history for a session"""
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
        )
        messages = result.scalars().all()
        return [msg.to_dict() for msg in messages]

    async def list_sessions(self) -> List[ChatSession]:
        """List all chat sessions"""
        result = await self.db.execute(
            select(ChatSession).order_by(ChatSession.updated_at.desc())
        )
        sessions = result.scalars().all()
        return [s.to_dict() for s in sessions]

    def _generate_title(self, content: str) -> str:
        """Generate a title from message content"""
        return content[:50] + "..." if len(content) > 50 else content
