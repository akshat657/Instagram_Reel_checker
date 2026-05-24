"""
FastAPI backend for MedReel Analyzer

This is the main entry point for the API server.
Run with: uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.api.routes import router


# Create FastAPI app
app = FastAPI(
    title="MedReel Analyzer API",
    description="""
    Backend API for MedReel Analyzer - AI-powered fact-checking for medical claims in Instagram Reels.

    Features:
    - Instagram Reel download and audio extraction
    - Multi-language transcription with Groq Whisper (automatic language detection)
    - Grammar correction and keyword extraction
    - Research paper fetching from PubMed, PMC, and Europe PMC
    - LLM-powered medical analysis with inline citations
    - Chat interface for follow-up questions

    Tech Stack:
    - FastAPI (async Python web framework)
    - Groq API (Whisper transcription + LLaMA LLM)
    - RapidAPI (Instagram data)
    - PubMed/PMC/Europe PMC APIs (research papers)
    """,
    version="2.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # React dev server URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint

    Returns basic information about the API.
    For full documentation, visit /docs (Swagger) or /redoc (ReDoc).
    """
    return {
        "name": "MedReel Analyzer API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "analyze": "POST /api/analyze",
            "chat": "POST /api/chat",
            "health": "GET /api/health"
        }
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 60)
    print("MedReel Analyzer API starting up...")
    print(f"API Docs: http://{settings.host}:{settings.port}/docs")
    print(f"Health Check: http://{settings.host}:{settings.port}/api/health")
    print(f"CORS Origins: {', '.join(settings.cors_origins)}")
    print("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("=" * 60)
    print("MedReel Analyzer API shutting down...")
    print("=" * 60)


# Run with uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
