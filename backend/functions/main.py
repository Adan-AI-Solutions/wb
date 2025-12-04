"""Cloud Functions for Firebase - Pythonエントリポイント"""
import os
from firebase_functions import https_fn
from firebase_admin import initialize_app

# Firebase Admin初期化
# 本番環境では自動的にデフォルトプロジェクトを使用
# エミュレーター環境では環境変数からプロジェクトIDを取得
try:
    # 既に初期化されている場合はスキップ
    app = initialize_app()
except ValueError:
    # 既に初期化されている場合は何もしない
    pass

# APIモジュールをインポート
from api import healthz, todos


@https_fn.on_request(region="asia-northeast1")
def healthz_endpoint(req: https_fn.Request) -> https_fn.Response:
    """ヘルスチェックエンドポイント"""
    return healthz.handle_healthz(req)


@https_fn.on_request(region="asia-northeast1")
def list_todos(req: https_fn.Request) -> https_fn.Response:
    """Todo一覧取得エンドポイント"""
    return todos.list_todos(req)


@https_fn.on_request(region="asia-northeast1")
def get_todo(req: https_fn.Request) -> https_fn.Response:
    """Todo取得エンドポイント"""
    return todos.get_todo(req)


@https_fn.on_request(region="asia-northeast1")
def create_todo(req: https_fn.Request) -> https_fn.Response:
    """Todo作成エンドポイント"""
    return todos.create_todo(req)


@https_fn.on_request(region="asia-northeast1")
def update_todo(req: https_fn.Request) -> https_fn.Response:
    """Todo更新エンドポイント"""
    return todos.update_todo(req)


@https_fn.on_request(region="asia-northeast1")
def delete_todo(req: https_fn.Request) -> https_fn.Response:
    """Todo削除エンドポイント"""
    return todos.delete_todo(req)
