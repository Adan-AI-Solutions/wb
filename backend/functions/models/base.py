"""ベースモデル定義"""
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from typing import Optional


class BaseModel(SQLModel):
    """全モデルの基底クラス"""
    
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="主キー（UUID）"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        description="作成日時（UTC）"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="更新日時（UTC）"
    )
    
    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }

