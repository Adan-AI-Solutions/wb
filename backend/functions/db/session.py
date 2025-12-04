"""Cloud Functions用データベースセッション管理"""
import os
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlmodel import SQLModel, Session
from models.base import BaseModel

# 環境変数から直接DATABASE_URLを取得（エミュレーター環境対応）
# 優先順位: 環境変数 > デフォルト値（ローカル開発環境用）
database_url = os.getenv("DATABASE_URL", "")

# DATABASE_URLが空の場合はデフォルト値を使用（ローカル開発環境）
if not database_url:
    database_url = "postgresql+psycopg2://wb_dev_user:wb_dev_password@db:5432/wb_dev"

# DEBUG設定（環境変数から取得、デフォルトはFalse）
debug_mode = os.getenv("DEBUG", "false").lower() == "true"

# SQLAlchemyエンジン作成（Cloud SQL接続用）
engine = create_engine(
    database_url,
    echo=debug_mode,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    # Cloud SQL接続のための設定
    connect_args={
        "connect_timeout": 10,
    }
)


@event.listens_for(SQLAlchemySession, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    """更新前にupdated_atを自動設定"""
    if isinstance(target, BaseModel):
        target.updated_at = datetime.utcnow()


def get_db():
    """データベースセッションを取得する関数（Cloud Functions用）"""
    with Session(engine) as session:
        yield session


def init_db():
    """データベーステーブルを初期化"""
    SQLModel.metadata.create_all(engine)

