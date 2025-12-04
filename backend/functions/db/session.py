"""Cloud Functions用データベースセッション管理"""
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlmodel import SQLModel, Session
from core.config import settings
from models.base import BaseModel

# SQLAlchemyエンジン作成（Cloud SQL接続用）
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
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

