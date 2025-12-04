# ローカル開発環境セットアップタスクリスト

## 目的

Docker + Firebase Emulatorを使用したローカル開発環境を構築し、Cloud Functionsの動作を確認する。

## 前提条件

- Docker Desktopがインストール・起動されていること
- ポート4000, 4500, 5001, 5432が使用可能であること

---

## タスク一覧

### フェーズ1: Docker環境のセットアップ ✅

- [x] `docker-compose.yaml` 作成
  - PostgreSQL 15サービス
  - Backend Cloud Functions開発環境サービス
- [x] `backend/Dockerfile` 作成
  - Python 3.11 + Firebase CLI + Google Cloud CLI
- [x] 環境変数設定（`docker-compose.yaml`）
  - `DATABASE_URL`: PostgreSQL接続文字列
  - `DEBUG`: デバッグモード

### フェーズ2: Python環境のセットアップ ✅

- [x] `backend/functions/requirements.txt` 作成
  - firebase-admin, firebase-functions
  - SQLModel, SQLAlchemy
  - psycopg2-binary
- [x] Python仮想環境（venv）のセットアップ手順
- [x] 依存関係のインストール手順

### フェーズ3: Firebase Emulator設定 ✅

- [x] `backend/firebase.json` 設定
  - Functions Emulator設定（ポート5001）
  - UI Emulator設定（ポート4000）
  - Logging Emulator設定（ポート4500）
- [x] `.firebaserc` 設定
  - プロジェクトID: `wb-dev-480009`

### フェーズ4: データベース接続設定 🔄

- [x] `backend/functions/db/session.py` 作成
  - SQLAlchemyエンジン設定
  - 環境変数からDATABASE_URLを読み込み
- [ ] **DATABASE_URL読み込み問題の解決**
  - [ ] エミュレーター起動時の環境変数読み込み確認
  - [ ] `.env.local`ファイルの読み込み確認
  - [ ] デフォルト値の設定（ローカル開発用）

### フェーズ5: ローカル開発環境の動作確認 ⏳

- [ ] **Docker Composeでコンテナ起動**
  - [ ] `docker compose up -d` でコンテナ起動
  - [ ] PostgreSQLコンテナのヘルスチェック確認
  - [ ] Backendコンテナの起動確認

- [ ] **Python仮想環境のセットアップ**
  - [ ] コンテナ内でvenv作成
  - [ ] 依存関係のインストール
  - [ ] `main.py`のインポート確認

- [ ] **Firebase Emulatorの起動**
  - [ ] エミュレーター起動コマンド実行
  - [ ] 関数の読み込み確認
  - [ ] エラーログの確認・修正

- [ ] **APIエンドポイントの動作テスト**
  - [ ] `/healthz` エンドポイントのテスト
  - [ ] `/list_todos` エンドポイントのテスト
  - [ ] `/create_todo` エンドポイントのテスト
  - [ ] `/get_todo` エンドポイントのテスト
  - [ ] `/update_todo` エンドポイントのテスト
  - [ ] `/delete_todo` エンドポイントのテスト

### フェーズ6: トラブルシューティング ⏳

- [ ] **ポート競合の解決**
  - [ ] ポート4000, 4500, 5001, 5432の使用状況確認
  - [ ] 既存プロセスの停止方法

- [ ] **環境変数の読み込み問題**
  - [ ] Docker Composeの環境変数設定確認
  - [ ] エミュレーター起動時の環境変数引き継ぎ確認
  - [ ] `.env.local`ファイルの読み込み確認

- [ ] **関数の読み込みエラー**
  - [ ] `main.py`のインポートエラー確認
  - [ ] 依存関係の不足確認
  - [ ] インポートパスの修正

---

## 現在の状況

### 完了済み ✅
- Docker環境のセットアップ
- Python環境のセットアップ
- Firebase Emulator設定
- コード移行（APIエンドポイント変換）

### 進行中 🔄
- DATABASE_URL読み込み問題の解決
- ローカル開発環境の動作確認

### 課題
1. **DATABASE_URL環境変数の読み込み**
   - エミュレーター起動時に環境変数が空になる問題
   - 解決策: `db/session.py`でデフォルト値を設定

2. **Firebase Emulatorの関数読み込み**
   - 関数が見つからないエラー
   - 原因: DATABASE_URLが空でエンジン作成時にエラー

---

## 実行手順（まとめ）

### 1. Docker Composeでコンテナ起動

```bash
cd /Users/mini/adan/wb
docker compose up -d --build
```

### 2. コンテナに入る

```bash
docker compose exec backend bash
```

### 3. Python仮想環境のセットアップ（初回のみ）

```bash
cd functions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Firebase Emulatorの起動

```bash
cd /backend
export DATABASE_URL=postgresql+psycopg2://wb_dev_user:wb_dev_password@db:5432/wb_dev
export DEBUG=true
source functions/venv/bin/activate
firebase emulators:start --only functions
```

### 5. APIテスト（別ターミナル）

```bash
# ヘルスチェック
curl http://localhost:5001/wb-dev-480009/asia-northeast1/healthz_endpoint

# Todo一覧取得
curl http://localhost:5001/wb-dev-480009/asia-northeast1/list_todos

# Todo作成
curl -X POST http://localhost:5001/wb-dev-480009/asia-northeast1/create_todo \
  -H "Content-Type: application/json" \
  -d '{"title": "テストTodo", "description": "これはテストです"}'
```

---

## 参考ドキュメント

- `backend/README.md` - セットアップ手順
- `backend/TESTING.md` - テスト手順
- `MIGRATION_TASKS.md` - 全体の移行タスク

