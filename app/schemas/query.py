from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    """Schema for RAG query request"""
    question: str = Field(..., min_length=1, description="User question to answer")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "What is the main topic of the uploaded document?"
            }
        }
    }


class RetrievalChunk(BaseModel):
    """Schema for retrieved chunk information"""
    text: str = Field(..., description="Retrieved text chunk")
    similarity_score: float = Field(0.0, description="Similarity score (if available)")
    source: str = Field(..., description="Source document filename")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "This is a relevant chunk of text from the document.",
                "similarity_score": 0.85,
                "source": "document.pdf"
            }
        }
    }


class QueryData(BaseModel):
    """Query response data"""
    answer: str = Field(..., description="Generated answer")
    retrieved_chunks: List[RetrievalChunk] = Field(..., description="Retrieved context chunks")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "answer": "The main topic is artificial intelligence and machine learning.",
                "retrieved_chunks": [
                    {
                        "text": "Artificial intelligence is transforming industries...",
                        "similarity_score": 0.92,
                        "source": "ai_report.pdf"
                    }
                ]
            }
        }
    }


class QueryResponse(BaseModel):
    """Standard response schema for RAG query"""
    status: str = "success"
    message: str = "Query processed successfully"
    data: QueryData
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Query processed successfully",
                "data": {
                    "answer": "The document discusses the impact of AI on healthcare.",
                    "retrieved_chunks": [
                        {
                            "text": "AI in healthcare has shown promising results...",
                            "similarity_score": 0.89,
                            "source": "healthcare_ai.pdf"
                        }
                    ]
                }
            }
        }
    }


class ErrorResponse(BaseModel):
    """Standard error response schema"""
    status: str = "error"
    message: str
    details: Optional[dict] = None
