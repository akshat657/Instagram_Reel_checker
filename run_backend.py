"""
Run script for FastAPI backend

This script ensures the Python path is set correctly so that
the backend package can be imported properly.

Usage:
    python run_backend.py
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now we can import from backend
if __name__ == "__main__":
    import uvicorn
    from backend.main import app
    from backend.config import settings

    print("=" * 60)
    print("Starting MedReel Analyzer FastAPI Backend")
    print(f"API Docs: http://{settings.host}:{settings.port}/docs")
    print(f"Health Check: http://{settings.host}:{settings.port}/api/health")
    print("=" * 60)

    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )
