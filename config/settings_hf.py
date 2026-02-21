"""
Configuration for Hugging Face Spaces deployment
Simplified version using SQLite instead of PostgreSQL
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BRD Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-in-production"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 7860
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Database - Use SQLite for Hugging Face
    DATABASE_URL: str = "sqlite+aiosqlite:///./brd_generator.db"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    
    # AI Configuration
    AI_PROVIDER: str = "gemini"  # or "openai"
    
    # Gemini
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-flash-latest"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # AI Processing
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Storage
    DOCUMENT_STORAGE_PATH: str = "./storage/documents"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Redis (optional - can be None for HF)
    REDIS_URL: Optional[str] = None
    REDIS_CACHE_TTL: int = 3600
    
    # Gmail API (optional)
    GMAIL_CLIENT_ID: Optional[str] = None
    GMAIL_CLIENT_SECRET: Optional[str] = None
    GMAIL_REDIRECT_URI: Optional[str] = None
    
    # Slack API (optional)
    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_APP_TOKEN: Optional[str] = None
    SLACK_SIGNING_SECRET: Optional[str] = None
    
    # Fireflies API (optional)
    FIREFLIES_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
