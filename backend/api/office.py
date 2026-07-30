"""
Office tools API endpoints
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.services.office_service import OfficeService

router = APIRouter()


class PDFOperationRequest(BaseModel):
    password: Optional[str] = None


class WordProcessRequest(BaseModel):
    operation: str  # summarize, proofread, rewrite
    language: str = "zh"


class ExcelProcessRequest(BaseModel):
    operation: str  # process, summarize


def get_office_service(db: AsyncSession = Depends(get_db)) -> OfficeService:
    return OfficeService(db)


@router.post("/pdf/split")
async def pdf_split(
    file: UploadFile = File(...),
    pages: str = "1-3",  # comma-separated page ranges
    service: OfficeService = Depends(get_office_service)
):
    """Split PDF into separate files"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.pdf_split(
        pdf_data=content,
        filename=file.filename,
        pages=pages
    )
    return result


@router.post("/pdf/merge")
async def pdf_merge(
    files: List[UploadFile] = File(...),
    service: OfficeService = Depends(get_office_service)
):
    """Merge multiple PDFs into one"""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="At least 2 files required")
    
    file_contents = []
    filenames = []
    for f in files:
        if f.filename:
            content = await f.read()
            file_contents.append(content)
            filenames.append(f.filename)
    
    result = await service.pdf_merge(
        pdf_data_list=file_contents,
        filenames=filenames
    )
    return result


@router.post("/pdf/encrypt")
async def pdf_encrypt(
    file: UploadFile = File(...),
    password: str = "",
    service: OfficeService = Depends(get_office_service)
):
    """Encrypt PDF with password"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.pdf_encrypt(
        pdf_data=content,
        filename=file.filename,
        password=password
    )
    return result


@router.post("/pdf/decrypt")
async def pdf_decrypt(
    file: UploadFile = File(...),
    password: str = "",
    service: OfficeService = Depends(get_office_service)
):
    """Decrypt PDF with password"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.pdf_decrypt(
        pdf_data=content,
        filename=file.filename,
        password=password
    )
    return result


@router.post("/pdf/convert")
async def pdf_convert(
    file: UploadFile = File(...),
    target_format: str = "images",  # images, word, excel
    service: OfficeService = Depends(get_office_service)
):
    """Convert PDF to other formats"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.pdf_convert(
        pdf_data=content,
        filename=file.filename,
        target_format=target_format
    )
    return result


@router.post("/pdf/summary")
async def pdf_summary(
    file: UploadFile = File(...),
    max_length: int = 500,
    service: OfficeService = Depends(get_office_service)
):
    """AI summarize PDF content"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.pdf_summary(
        pdf_data=content,
        filename=file.filename,
        max_length=max_length
    )
    return result


@router.post("/docx/process")
async def docx_process(
    file: UploadFile = File(...),
    operation: str = "summarize",
    service: OfficeService = Depends(get_office_service)
):
    """Process Word document"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.docx_process(
        docx_data=content,
        filename=file.filename,
        operation=operation
    )
    return result


@router.post("/excel/process")
async def excel_process(
    file: UploadFile = File(...),
    operation: str = "process",
    service: OfficeService = Depends(get_office_service)
):
    """Process Excel file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    result = await service.excel_process(
        excel_data=content,
        filename=file.filename,
        operation=operation
    )
    return result
