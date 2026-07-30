"""
Tests for chat service
"""
import pytest
from backend.services.chat_service import ChatService
from backend.models import ChatSession, ChatMessage


@pytest.mark.asyncio
async def test_create_session(test_db):
    """Test creating a new chat session"""
    service = ChatService(test_db)

    session = await service.create_session(
        title="Test Session",
        model="test-model"
    )

    assert session.id is not None
    assert session.title == "Test Session"
    assert session.model == "test-model"


@pytest.mark.asyncio
async def test_send_message(test_db):
    """Test sending a message"""
    service = ChatService(test_db)

    message, session = await service.send_message(
        content="Hello, AI!",
        model="test-model"
    )

    # send_message returns the assistant message and session
    assert message.id is not None
    assert message.role == "assistant"
    assert len(message.content) > 0  # AI should have some response
    assert session.id is not None
    assert session.model == "test-model"


@pytest.mark.asyncio
async def test_get_history(test_db):
    """Test getting chat history"""
    service = ChatService(test_db)

    # Create a session first
    session = await service.create_session(title="History Test", model="test-model")

    # Send messages in the same session
    await service.send_message(content="First message", session_id=session.id, model="test-model")
    await service.send_message(content="Second message", session_id=session.id, model="test-model")

    # Get history
    history = await service.get_history(session.id)

    assert len(history) == 4  # 2 user + 2 assistant messages
    assert history[0]["role"] in ["user", "assistant"]


@pytest.mark.asyncio
async def test_delete_session(test_db):
    """Test deleting a chat session"""
    service = ChatService(test_db)

    # Create a session
    await service.send_message(content="Test", model="test-model")
    sessions = await service.list_sessions()
    session_id = sessions[0]["id"]

    # Delete the session
    result = await service.delete_session(session_id)
    assert result is True

    # Verify it's deleted
    remaining = await service.list_sessions()
    assert len(remaining) == 0


@pytest.mark.asyncio
async def test_list_sessions(test_db):
    """Test listing all chat sessions"""
    service = ChatService(test_db)

    # Create multiple sessions
    await service.send_message(content="Session 1", model="test-model")
    await service.create_session(title="Session 2")
    await service.create_session(title="Session 3")

    sessions = await service.list_sessions()

    assert len(sessions) >= 3
