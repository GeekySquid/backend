# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    APP_NAME: str = "Stock Prediction API"
    APP_VERSION: str = "2.1.0"
    DEBUG: bool = False
    
    # Alpha Vantage
    ALPHA_VANTAGE_API_KEY: str = "I7I80NHU76DZS60Q"
    
    # Model Configuration
    SEQUENCE_LENGTH: int = 30
    MODEL_VERSION: str = "v2.1"
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 600  # 10 minutes
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
