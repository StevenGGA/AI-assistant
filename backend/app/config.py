"""
Application configuration and settings
"""
from pydantic_settings import BaseSettings
from typing import List
import secrets

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "AI Workflow Assistant"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://workflow_user:workflow_password@localhost:5432/workflow_db"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    # OAuth credentials (optional for now)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    SLACK_CLIENT_ID: str = ""
    SLACK_CLIENT_SECRET: str = ""
    CANVAS_CLIENT_ID: str = ""
    CANVAS_CLIENT_SECRET: str = ""
    CANVAS_BASE_URL: str = ""
    
    # AI Model settings
    AI_MODEL_NAME: str = "Qwen/Qwen2.5-3B-Instruct"
    AI_MAX_TOKENS: int = 2048
    AI_TEMPERATURE: float = 0.7
    
    # Redis (for background tasks)
    REDIS_URL: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()