"""
Application settings and configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "BRD Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # AI Provider Configuration
    AI_PROVIDER: str = "gemini"  # Options: "openai" or "gemini"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"  # or "gemini-1.5-pro"
    
    # Common AI Settings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # Gmail API
    GMAIL_CLIENT_ID: Optional[str] = None
    GMAIL_CLIENT_SECRET: Optional[str] = None
    GMAIL_REDIRECT_URI: Optional[str] = None
    
    # Slack API
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_APP_TOKEN: Optional[str] = None
    SLACK_SIGNING_SECRET: Optional[str] = None
    
    # Fireflies API
    FIREFLIES_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Document Storage
    DOCUMENT_STORAGE_PATH: str = "./storage/documents"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    
    # AI Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # BRD Generation
    DEFAULT_BRD_TEMPLATE: str = "standard"
    ENABLE_AUTO_CITATION: bool = True
    ENABLE_CONFLICT_DETECTION: bool = True
    ENABLE_SENTIMENT_ANALYSIS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
