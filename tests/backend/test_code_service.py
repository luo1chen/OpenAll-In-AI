"""
Tests for code service
"""
import pytest
from backend.services.code_service import CodeService


@pytest.mark.asyncio
async def test_generate_code(test_db):
    """Test code generation"""
    service = CodeService(test_db)

    result = await service.generate_code(
        prompt="Write a hello world function",
        language="python"
    )

    assert "code" in result
    assert result["language"] == "python"


@pytest.mark.asyncio
async def test_fix_code(test_db):
    """Test code fixing"""
    service = CodeService(test_db)

    result = await service.fix_code(
        code="print('hello'",
        language="python"
    )

    assert "fixed_code" in result


@pytest.mark.asyncio
async def test_add_comment(test_db):
    """Test adding comments to code"""
    service = CodeService(test_db)

    result = await service.add_comment(
        code="def hello():\n    print('hello')",
        language="python"
    )

    assert "commented_code" in result
    assert result["original_code"] != result["commented_code"]


@pytest.mark.asyncio
async def test_optimize_code(test_db):
    """Test code optimization"""
    service = CodeService(test_db)

    result = await service.optimize_code(
        code="for i in range(len(items)):\n    print(items[i])",
        language="python"
    )

    assert "optimized_code" in result
    assert "suggestions" in result


@pytest.mark.asyncio
async def test_generate_scaffold(test_db):
    """Test project scaffold generation"""
    service = CodeService(test_db)

    result = await service.generate_scaffold(
        project_type="vue-fastapi",
        project_name="my-project"
    )

    assert result["project_name"] == "my-project"
    assert result["project_type"] == "vue-fastapi"
    assert "files" in result


@pytest.mark.asyncio
async def test_debug_api(test_db):
    """Test API debugging"""
    service = CodeService(test_db)

    result = await service.debug_api(
        method="GET",
        url="https://api.example.com/test"
    )

    assert result["method"] == "GET"
    assert result["url"] == "https://api.example.com/test"
