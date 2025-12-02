"""Todo APIエンドポイント"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_db
from app.models.todo import Todo, TodoCreate, TodoUpdate, TodoRead

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> TodoRead:
    """Todoを作成"""
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return TodoRead(
        id=str(db_todo.id),
        title=db_todo.title,
        description=db_todo.description,
        completed=db_todo.completed,
        created_at=db_todo.created_at.isoformat(),
        updated_at=db_todo.updated_at.isoformat() if db_todo.updated_at else None
    )


@router.get("", response_model=List[TodoRead])
@router.get("/", response_model=List[TodoRead])
async def list_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[TodoRead]:
    """Todo一覧を取得"""
    statement = select(Todo).offset(skip).limit(limit)
    todos = db.exec(statement).all()
    return [
        TodoRead(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at.isoformat(),
            updated_at=todo.updated_at.isoformat() if todo.updated_at else None
        )
        for todo in todos
    ]


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(todo_id: UUID, db: Session = Depends(get_db)) -> TodoRead:
    """Todoを取得"""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return TodoRead(
        id=str(todo.id),
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at.isoformat(),
        updated_at=todo.updated_at.isoformat() if todo.updated_at else None
    )


@router.patch("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
) -> TodoRead:
    """Todoを更新"""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return TodoRead(
        id=str(todo.id),
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at.isoformat(),
        updated_at=todo.updated_at.isoformat() if todo.updated_at else None
    )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID, db: Session = Depends(get_db)):
    """Todoを削除"""
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    db.delete(todo)
    db.commit()
    return None

