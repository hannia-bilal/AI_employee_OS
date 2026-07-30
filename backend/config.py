"""
AI Employee OS - Configuration
Environment configuration using pydantic-settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Employee OS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./ai_employee_os.db"

    # AI Provider
    GROQ_API_KEY: Optional[str] = None
    AI_MODEL: str = "llama-3.3-70b-versatile"

    # JWT Auth
    SECRET_KEY: str = "ai-employee-os-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
