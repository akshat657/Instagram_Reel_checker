"""
Pydantic schemas for request/response validation
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl


class Citation(BaseModel):
    """Research paper citation"""
    title: str = Field(..., description="Paper title")
    url: str = Field(..., description="URL to full paper")
    source: str = Field(..., description="Source database (PubMed, PMC, Europe PMC)")
    year: str = Field(default="N/A", description="Publication year")
    abstract: str = Field(default="Abstract not available", description="Paper abstract")
    pmid: Optional[str] = Field(default=None, description="PubMed ID")
    doi: Optional[str] = Field(default=None, description="Digital Object Identifier")
    authors: Optional[str] = Field(default=None, description="Author names")
    journal: Optional[str] = Field(default=None, description="Journal name")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Effects of Turmeric on Health",
                "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
                "source": "PubMed",
                "year": "2023",
                "abstract": "This study examines the health benefits of turmeric...",
                "pmid": "12345678",
                "doi": "10.1234/example",
                "authors": "Smith J, Doe A",
                "journal": "Journal of Medicine"
            }
        }


class AnalyzeRequest(BaseModel):
    """Request to analyze an Instagram Reel"""
    url: HttpUrl = Field(..., description="Instagram Reel URL", examples=["https://www.instagram.com/reel/ABC123/"])
    language: str = Field(default="auto", description="Language for transcript ('auto' for automatic detection, 'English', 'Hindi')")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.instagram.com/reel/ABC123/",
                "language": "auto"
            }
        }


class AnalyzeResponse(BaseModel):
    """Response from analyzing an Instagram Reel"""
    caption: str = Field(..., description="Instagram Reel caption")
    transcript: str = Field(..., description="Original transcript from audio")
    corrected_transcript: str = Field(..., description="Grammar-corrected transcript")
    detected_language: str = Field(..., description="Detected language from audio (e.g., 'English', 'Hindi')")
    analysis: str = Field(..., description="HTML-formatted medical analysis with inline citations")
    citations: List[Citation] = Field(default_factory=list, description="List of research paper citations")
    audio_url: Optional[str] = Field(default=None, description="URL to downloaded audio file")

    class Config:
        json_schema_extra = {
            "example": {
                "caption": "Try this health hack for better sleep!",
                "transcript": "मुझे रात को सोने में दिक्कत होती है",
                "corrected_transcript": "मुझे रात को सोने में दिक्कत होती है",
                "detected_language": "Hindi",
                "analysis": "<p>This claim is partially true [1][2]...</p>",
                "citations": [
                    {
                        "title": "Sleep and Health",
                        "url": "https://pubmed.ncbi.nlm.nih.gov/12345/",
                        "source": "PubMed",
                        "year": "2023",
                        "abstract": "...",
                        "pmid": "12345"
                    }
                ],
                "audio_url": "/static/audio/abc123.mp3"
            }
        }


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What are the side effects?"
            }
        }


class ChatContext(BaseModel):
    """Context information for chat"""
    caption: str = Field(..., description="Instagram Reel caption")
    transcript: str = Field(..., description="Original transcript")
    corrected_transcript: Optional[str] = Field(default=None, description="Corrected transcript")
    analysis: str = Field(..., description="Medical analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "caption": "Health tip about sleep",
                "transcript": "मुझे नींद नहीं आती",
                "corrected_transcript": "मुझे नींद नहीं आती",
                "analysis": "<p>This claim is partially true...</p>"
            }
        }


class ChatRequest(BaseModel):
    """Request to chat with context"""
    message: str = Field(..., description="User's question", min_length=1)
    context: ChatContext = Field(..., description="Context from analyzed reel")
    citations: List[Citation] = Field(default_factory=list, description="Citations from analysis")
    history: List[ChatMessage] = Field(default_factory=list, description="Chat history (last 10 messages)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are the side effects?",
                "context": {
                    "caption": "Try this supplement!",
                    "transcript": "Take vitamin D daily",
                    "analysis": "Vitamin D is beneficial [1]..."
                },
                "citations": [],
                "history": [
                    {"role": "user", "content": "Is this safe?"},
                    {"role": "assistant", "content": "Yes, generally safe..."}
                ]
            }
        }


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    response: str = Field(..., description="Assistant's response")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "The side effects of vitamin D include nausea and headache when taken in excessive amounts..."
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(default=None, description="Error type/category")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid Instagram URL provided",
                "error_type": "validation_error"
            }
        }
