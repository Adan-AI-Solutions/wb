"""Cloud Functions用アプリケーション設定管理"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # Database (Cloud SQL)
    DATABASE_URL: str
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # App
    APP_NAME: str = "WB Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # GCP Project
    GCP_PROJECT: Optional[str] = os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT")
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True


# Cloud Functions環境変数から設定を読み込む
def get_settings() -> Settings:
    """設定を取得（環境変数から優先的に読み込む）"""
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL", ""),
        API_V1_PREFIX=os.getenv("API_V1_PREFIX", "/api/v1"),
        APP_NAME=os.getenv("APP_NAME", "WB Backend"),
        APP_VERSION=os.getenv("APP_VERSION", "0.1.0"),
        DEBUG=os.getenv("DEBUG", "false").lower() == "true",
        GCP_PROJECT=os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT")
    )


settings = get_settings()

