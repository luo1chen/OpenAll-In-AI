"""
Code helper API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List, Dict

from backend.core.database import get_db
from backend.services.code_service import CodeService

router = APIRouter()


class CodeGenerateRequest(BaseModel):
    prompt: str
    language: str = "python"
    context: Optional[str] = None


class CodeFixRequest(BaseModel):
    code: str
    language: str = "python"
    error_message: Optional[str] = None


class CodeCommentRequest(BaseModel):
    code: str
    language: str = "python"


class CodeOptimizeRequest(BaseModel):
    code: str
    language: str = "python"


class ScaffoldRequest(BaseModel):
    project_type: str  # vue-fastapi, react-nodejs, python-script
    project_name: str
    requirements: Optional[List[str]] = None


class APIRequest(BaseModel):
    method: str
    url: str
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, str]] = None
    body: Optional[dict] = None


def get_code_service(db: AsyncSession = Depends(get_db)) -> CodeService:
    return CodeService(db)


@router.post("/generate")
async def generate_code(
    request: CodeGenerateRequest,
    service: CodeService = Depends(get_code_service)
):
    """Generate code from prompt"""
    result = await service.generate_code(
        prompt=request.prompt,
        language=request.language,
        context=request.context
    )
    return result


@router.post("/fix")
async def fix_code(
    request: CodeFixRequest,
    service: CodeService = Depends(get_code_service)
):
    """Fix code errors"""
    result = await service.fix_code(
        code=request.code,
        language=request.language,
        error_message=request.error_message
    )
    return result


@router.post("/comment")
async def add_comment(
    request: CodeCommentRequest,
    service: CodeService = Depends(get_code_service)
):
    """Add code comments"""
    result = await service.add_comment(
        code=request.code,
        language=request.language
    )
    return result


@router.post("/optimize")
async def optimize_code(
    request: CodeOptimizeRequest,
    service: CodeService = Depends(get_code_service)
):
    """Optimize code"""
    result = await service.optimize_code(
        code=request.code,
        language=request.language
    )
    return result


@router.post("/scaffold")
async def generate_scaffold(
    request: ScaffoldRequest,
    service: CodeService = Depends(get_code_service)
):
    """Generate project scaffold"""
    result = await service.generate_scaffold(
        project_type=request.project_type,
        project_name=request.project_name,
        requirements=request.requirements
    )
    return result


@router.post("/debug")
async def debug_api(
    request: APIRequest,
    service: CodeService = Depends(get_code_service)
):
    """Debug/diagnose API endpoint"""
    result = await service.debug_api(
        method=request.method,
        url=request.url,
        headers=request.headers,
        params=request.params,
        body=request.body
    )
    return result
