# Cloud Functions移行タスクリスト

FastAPIからCloud Functionsへの移行作業

## 参考プロジェクト
- https://github.com/Adan-AI-Solutions/ai-interview

## タスク一覧

### フェーズ1: 準備と構造変更

- [x] ブランチ作成: `fujiwara/cloud-functions-migration`
- [ ] サンプルプロジェクト（ai-interview）の構造分析
- [ ] 既存のbackendディレクトリをバックアップ
- [ ] 既存のbackendディレクトリを削除
- [ ] Cloud Functions用のbackend構造を作成
  - `backend/functions/` ディレクトリ作成
  - `backend/firebase.json` 作成

### フェーズ2: Cloud Functions設定

- [ ] `backend/functions/requirements.txt` 作成
  - firebase-admin
  - firebase-functions
  - functions-framework
  - SQLModel/SQLAlchemy（既存の依存関係を維持）
  - psycopg2-binary（Cloud SQL接続用）
  - Alembic
- [ ] `backend/functions/main.py` 作成（Cloud Functionsエントリポイント）
- [ ] `backend/firebase.json` 設定
  - Python 3.11 runtime
  - functions source設定

### フェーズ3: コード移行

- [ ] `app/core/config.py` を `functions/core/config.py` に移動・調整
  - Cloud Functions用の環境変数設定
- [ ] `app/db/session.py` を `functions/db/session.py` に移動・調整
  - Cloud SQL接続設定（Private IP対応）
  - SQLModel/SQLAlchemy設定
- [ ] `app/models/` を `functions/models/` に移動
- [ ] `app/api/` を `functions/api/` に移動
  - FastAPIルーターからCloud Functions HTTP関数に変換
- [ ] `migrations/` を `functions/migrations/` に移動
  - Alembic設定の調整

### フェーズ4: APIエンドポイント変換

- [ ] `/healthz` エンドポイントをCloud Functions HTTP関数に変換
- [ ] `/api/v1/todos` エンドポイントをCloud Functions HTTP関数に変換
  - GET /todos
  - POST /todos
  - GET /todos/{id}
  - PATCH /todos/{id}
  - DELETE /todos/{id}
- [ ] CORS設定をCloud Functions用に調整

### フェーズ5: インフラ設定

- [ ] `docker-compose.yaml` 更新
  - backendサービスを削除
  - Firebase Emulatorサービスを追加（オプション）
- [ ] `.gitignore` 更新
  - Cloud Functions関連の除外設定
- [ ] 環境変数設定
  - `.env.example` 更新
  - Cloud Functions用の環境変数定義

### フェーズ6: ローカル開発環境

- [ ] Firebase Emulator設定
  - `firebase.json` のemulators設定
- [ ] ローカル開発用スクリプト作成
- [ ] README更新（Cloud Functions用の手順）

### フェーズ7: デプロイ設定

- [ ] Firebaseプロジェクト設定確認（wb-dev-480009）
- [ ] Cloud SQL接続設定（Private IP）
- [ ] デプロイスクリプト作成
- [ ] 動作確認

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

