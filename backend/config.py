"""
Backend configuration using environment variables
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Groq API Keys (3 with automatic fallback)
    groq_api_key_1: str = Field(..., env="GROQ_API_KEY_1")
    groq_api_key_2: str = Field(..., env="GROQ_API_KEY_2")
    groq_api_key_3: str = Field(..., env="GROQ_API_KEY_3")

    # RapidAPI for Instagram data
    rapidapi_key: str = Field(..., env="RAPIDAPI_KEY")

    # Server settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # CORS settings - allow React dev server by default
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )

    # API settings
    api_prefix: str = Field(default="/api")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


# Global settings instance
settings = Settings()


def get_groq_api_keys() -> List[str]:
    """Get list of all Groq API keys for fallback"""
    return [
        settings.groq_api_key_1,
        settings.groq_api_key_2,
        settings.groq_api_key_3,
    ]
