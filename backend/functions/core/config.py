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
settings = Settings()
