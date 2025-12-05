"""Todoモデル（サンプル）"""
from typing import Optional
from sqlmodel import Field, SQLModel
from models.base import BaseModel


class TodoBase(SQLModel):
    """Todoの基底モデル"""
    title: str = Field(max_length=200, description="タイトル")
    description: Optional[str] = Field(default=None, max_length=1000, description="説明")
    completed: bool = Field(default=False, description="完了フラグ")


class Todo(TodoBase, BaseModel, table=True):
    """Todoテーブルモデル"""
    __tablename__ = "todos"


class TodoCreate(TodoBase):
    """Todo作成用モデル"""
    pass


class TodoUpdate(SQLModel):
    """Todo更新用モデル"""
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TodoRead(TodoBase):
    """Todo読み取り用モデル"""
    id: str
    created_at: str
    updated_at: Optional[str] = None
