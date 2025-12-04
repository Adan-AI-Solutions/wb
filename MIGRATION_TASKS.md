# Cloud Functions移行タスクリスト

## 目的

FastAPIベースのバックエンドをFirebase Cloud Functions（Python）に移行する。
- **アーキテクチャ**: FastAPI → Cloud Functions（1関数1エンドポイント形式）
- **データベース**: PostgreSQL 15（Cloud SQL）を継続使用（RDBのみ、Firestoreは使用しない）
- **デプロイ先**: Firebase Project `wb-dev-480009`

## 参考プロジェクト
- https://github.com/Adan-AI-Solutions/ai-interview

## タスク一覧

### フェーズ1: 準備と構造変更 ✅

- [x] ブランチ作成: `fujiwara/cloud-functions-migration`
- [x] サンプルプロジェクト（ai-interview）の構造分析
- [x] 既存のbackendディレクトリをバックアップ
- [x] 既存のbackendディレクトリを削除
- [x] Cloud Functions用のbackend構造を作成
  - `backend/functions/` ディレクトリ作成
  - `backend/firebase.json` 作成

### フェーズ2: Cloud Functions設定 ✅

- [x] `backend/functions/requirements.txt` 作成
  - firebase-admin
  - firebase-functions
  - functions-framework
  - SQLModel/SQLAlchemy（既存の依存関係を維持）
  - psycopg2-binary（Cloud SQL接続用）
  - Alembic
- [x] `backend/functions/main.py` 作成（Cloud Functionsエントリポイント）
  - 1関数1エンドポイント形式で実装
- [x] `backend/firebase.json` 設定
  - Python 3.11 runtime
  - functions source設定

### フェーズ3: コード移行 ✅

- [x] `app/core/config.py` を `functions/core/config.py` に移動・調整
  - Cloud Functions用の環境変数設定
- [x] `app/db/session.py` を `functions/db/session.py` に移動・調整
  - Cloud SQL接続設定（Private IP対応）
  - SQLModel/SQLAlchemy設定
  - 環境変数から直接DATABASE_URLを読み込むように修正
- [x] `app/models/` を `functions/models/` に移動
  - インポートパスを修正（`app.models` → `models`）
- [x] `app/api/` を `functions/api/` に移動
  - FastAPIルーターからCloud Functions HTTP関数に変換
  - 各エンドポイントを個別関数として実装
- [x] `migrations/` を `functions/migrations/` に移動
  - Alembic設定の調整

### フェーズ4: APIエンドポイント変換 ✅

- [x] `/healthz` エンドポイントをCloud Functions HTTP関数に変換
- [x] `/api/v1/todos` エンドポイントをCloud Functions HTTP関数に変換
  - GET /todos（list_todos）
  - POST /todos（create_todo）
  - GET /todos/{id}（get_todo）
  - PATCH /todos/{id}（update_todo）
  - DELETE /todos/{id}（delete_todo）
- [x] CORS設定をCloud Functions用に調整

### フェーズ5: インフラ設定 ✅

- [x] `docker-compose.yaml` 更新
  - backendサービスを追加（Cloud Functions開発環境）
  - PostgreSQL 15サービス設定
- [x] `.gitignore` 更新
  - Cloud Functions関連の除外設定
- [x] 環境変数設定
  - `.env.local` 作成（ローカル開発用）
  - `.env.wb-dev` 作成（開発環境用）
  - `.env.wb-prod` 作成（本番環境用）
  - Git管理対象に設定

### フェーズ6: ローカル開発環境 🔄

- [x] Firebase Emulator設定
  - `firebase.json` のemulators設定
- [x] Dockerfile作成（Python 3.11 + Firebase CLI + Google Cloud CLI）
- [x] README更新（Cloud Functions用の手順）
- [x] TESTING.md作成（ローカルテスト手順）
- [ ] **ローカル開発環境の動作確認**
  - [ ] Docker Composeでコンテナ起動確認
  - [ ] Firebase Emulator起動確認
  - [ ] DATABASE_URL環境変数の読み込み確認
  - [ ] APIエンドポイントの動作テスト

### フェーズ7: デプロイ設定 ⏳

- [ ] Firebaseプロジェクト設定確認（wb-dev-480009）
- [ ] Cloud SQL接続設定（Private IP）
- [ ] デプロイスクリプト作成
- [ ] 本番環境での動作確認

## 技術スタック

- **Runtime**: Python 3.11（Cloud Functions）
- **Framework**: Firebase Functions for Python
- **ORM**: SQLModel + SQLAlchemy（維持）
- **Database**: Cloud SQL for PostgreSQL 15（維持）
- **Migration**: Alembic（維持）

## 注意事項

- RDB（Cloud SQL）は引き続き使用
- FastAPIからCloud Functions HTTP関数への変換が必要
- Cloud SQL Private IP接続の設定が必要
- Firebase Functionsの環境変数設定が必要

