"""Todo APIエンドポイント（Cloud Functions用）"""
from typing import List
from uuid import UUID
from firebase_functions import https_fn
from flask import jsonify, request
from db.session import get_db
from models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from sqlmodel import Session, select


def cors_response(data, status_code=200):
    """CORSヘッダー付きレスポンスを作成"""
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PATCH,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Max-Age': '3600'
    }
    response = jsonify(data)
    for key, value in cors_headers.items():
        response.headers[key] = value
    response.status_code = status_code
    return response


def list_todos(req: https_fn.Request) -> https_fn.Response:
    """Todo一覧を取得"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    if req.method != 'GET':
        return cors_response({"error": "Method not allowed"}, 405)
    
    data = request.get_json(silent=True) or {}
    skip = int(req.args.get('skip', data.get('skip', 0)))
    limit = int(req.args.get('limit', data.get('limit', 100)))
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        statement = select(Todo).offset(skip).limit(limit)
        todos = db.exec(statement).all()
        
        result = [
            TodoRead(
                id=str(todo.id),
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                created_at=todo.created_at.isoformat(),
                updated_at=todo.updated_at.isoformat() if todo.updated_at else None
            ).model_dump()
            for todo in todos
        ]
        return cors_response(result)
    finally:
        db.close()


def get_todo(req: https_fn.Request) -> https_fn.Response:
    """Todoを取得"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    if req.method != 'GET':
        return cors_response({"error": "Method not allowed"}, 405)
    
    data = request.get_json(silent=True) or {}
    path_parts = req.path.strip('/').split('/')
    todo_id = data.get('id') or (path_parts[-1] if path_parts else None)
    
    if not todo_id:
        return cors_response({"error": "Todo ID is required"}, 400)
    
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        return cors_response({"error": "Invalid todo ID"}, 400)
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        todo = db.get(Todo, todo_uuid)
        if not todo:
            return cors_response({"error": f"Todo with id {todo_id} not found"}, 404)
        
        result = TodoRead(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at.isoformat(),
            updated_at=todo.updated_at.isoformat() if todo.updated_at else None
        )
        return cors_response(result.model_dump())
    finally:
        db.close()


def create_todo(req: https_fn.Request) -> https_fn.Response:
    """Todoを作成"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    if req.method != 'POST':
        return cors_response({"error": "Method not allowed"}, 405)
    
    data = request.get_json()
    if not data:
        return cors_response({"error": "Request body is required"}, 400)
    
    try:
        todo_create = TodoCreate(**data)
    except Exception as e:
        return cors_response({"error": str(e)}, 400)
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        db_todo = Todo(**todo_create.model_dump())
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        
        result = TodoRead(
            id=str(db_todo.id),
            title=db_todo.title,
            description=db_todo.description,
            completed=db_todo.completed,
            created_at=db_todo.created_at.isoformat(),
            updated_at=db_todo.updated_at.isoformat() if db_todo.updated_at else None
        )
        return cors_response(result.model_dump(), 201)
    finally:
        db.close()


def update_todo(req: https_fn.Request) -> https_fn.Response:
    """Todoを更新"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    if req.method != 'PATCH':
        return cors_response({"error": "Method not allowed"}, 405)
    
    data = request.get_json(silent=True) or {}
    path_parts = req.path.strip('/').split('/')
    todo_id = data.get('id') or (path_parts[-1] if path_parts else None)
    
    if not todo_id:
        return cors_response({"error": "Todo ID is required"}, 400)
    
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        return cors_response({"error": "Invalid todo ID"}, 400)
    
    try:
        todo_update = TodoUpdate(**data)
    except Exception as e:
        return cors_response({"error": str(e)}, 400)
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        todo = db.get(Todo, todo_uuid)
        if not todo:
            return cors_response({"error": f"Todo with id {todo_id} not found"}, 404)
        
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        
        db.add(todo)
        db.commit()
        db.refresh(todo)
        
        result = TodoRead(
            id=str(todo.id),
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at.isoformat(),
            updated_at=todo.updated_at.isoformat() if todo.updated_at else None
        )
        return cors_response(result.model_dump())
    finally:
        db.close()


def delete_todo(req: https_fn.Request) -> https_fn.Response:
    """Todoを削除"""
    if req.method == 'OPTIONS':
        return cors_response({}, 204)
    
    if req.method != 'DELETE':
        return cors_response({"error": "Method not allowed"}, 405)
    
    data = request.get_json(silent=True) or {}
    path_parts = req.path.strip('/').split('/')
    todo_id = data.get('id') or (path_parts[-1] if path_parts else None)
    
    if not todo_id:
        return cors_response({"error": "Todo ID is required"}, 400)
    
    try:
        todo_uuid = UUID(todo_id)
    except ValueError:
        return cors_response({"error": "Invalid todo ID"}, 400)
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        todo = db.get(Todo, todo_uuid)
        if not todo:
            return cors_response({"error": f"Todo with id {todo_id} not found"}, 404)
        
        db.delete(todo)
        db.commit()
        return cors_response({}, 204)
    finally:
        db.close()
