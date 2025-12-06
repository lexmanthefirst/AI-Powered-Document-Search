from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List


class DocumentUploadRequest(BaseModel):
    """Schema for uploading a document"""
    pass  # File upload handled by FastAPI's UploadFile


class DocumentData(BaseModel):
    """Document data schema"""
    id: UUID
    filename: str
    content_type: str
    file_size: int
    chunk_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class DocumentUploadResponse(BaseModel):
    """Response schema for document upload"""
    status: str = "success"
    message: str = "Document uploaded successfully"
    data: DocumentData


class DocumentListResponse(BaseModel):
    """Response schema for listing documents"""
    status: str = "success"
    message: str = "Documents retrieved successfully"
    data: List[DocumentData]


class DocumentDetailResponse(BaseModel):
    """Response schema for document details"""
    status: str = "success"
    message: str = "Document retrieved successfully"
    data: DocumentData


class ErrorResponse(BaseModel):
    """Standard error response schema"""
    status: str = "error"
    message: str
    details: Optional[dict] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "error",
                "message": "Document not found",
                "details": {"document_id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }
    }
