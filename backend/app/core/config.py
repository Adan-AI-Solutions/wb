"""アプリケーション設定管理"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # Database
    DATABASE_URL: str
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # App
    APP_NAME: str = "WB Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True


settings = Settings()

