"""データベースセッション管理"""
from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlmodel import SQLModel, Session
from app.core.config import settings
from app.models.base import BaseModel

# SQLAlchemyエンジン作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


@event.listens_for(SQLAlchemySession, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    """更新前にupdated_atを自動設定"""
    if isinstance(target, BaseModel):
        target.updated_at = datetime.utcnow()


def get_db():
    """データベースセッションを取得する依存性注入用関数"""
    # SQLModelのSessionを使う
    with Session(engine) as session:
        yield session


def init_db():
    """データベーステーブルを初期化"""
    SQLModel.metadata.create_all(engine)
