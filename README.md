# WB Project

開発環境と本番環境を分離したGCPベースのアプリケーション。

## プロジェクト構成

- **Frontend**: Vue.js + Firebase Hosting
- **Backend**: FastAPI + SQLModel + Cloud Run
- **Database**: Cloud SQL for PostgreSQL 15
- **Infrastructure**: GCP (dev/prod プロジェクト分離)

## ディレクトリ構造

```
wb/
├── frontend/              # Vue.js フロントエンド
│   ├── README.md
│   └── .gitignore
├── backend/               # FastAPI バックエンド
│   ├── app/               # アプリケーションコード
│   │   ├── api/           # APIルーティング
│   │   ├── models/        # SQLModelモデル
│   │   ├── db/            # データベースセッション
│   │   ├── core/          # 設定・共通定数
│   │   ├── auth/          # 認証関連
│   │   └── main.py        # FastAPIエントリポイント
│   ├── migrations/        # Alembicマイグレーション
│   ├── requirements.txt   # Python依存関係
│   ├── Dockerfile         # Cloud Run用Dockerfile
│   ├── alembic.ini        # Alembic設定
│   └── README.md
├── infrastructure/         # GCPインフラ構築スクリプト
│   ├── setup-dev.sh       # dev環境セットアップスクリプト
│   ├── deploy-backend.sh  # バックエンドデプロイスクリプト
│   ├── README.md          # インフラ構築手順
│   └── PROD_SETUP.md      # prod環境セットアップメモ
├── docker-compose.yaml     # ローカル開発環境
├── .gitignore
└── README.md
```

## 開発環境セットアップ

### 前提条件

以下のツールがインストールされている必要があります:

- Python 3.11
- Node.js / npm or pnpm
- Docker & Docker Compose
- gcloud CLI
- Firebase CLI（後で使用）

### GCPプロジェクト設定

```bash
# GCP認証
gcloud auth login

# デフォルトプロジェクトを設定
gcloud config set project wb-dev-480009
```

### ローカル開発

#### 1. バックエンドのセットアップ

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# または .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 2. 環境変数の設定

```bash
# .env.local ファイルを作成（docker-compose用）
# DATABASE_URLはdocker-compose.yamlで自動設定されます
```

#### 3. Docker Composeで起動

```bash
# プロジェクトルートから
docker compose up -d
```

#### 4. マイグレーション実行

```bash
# 初回のみ: マイグレーションファイル作成
docker compose run backend alembic revision --autogenerate -m "Initial migration"

# マイグレーション適用
docker compose run backend alembic upgrade head
```

#### 5. 動作確認

```bash
# ヘルスチェック
curl http://localhost:8000/healthz
```

#### 6. フロントエンドのセットアップ（後で実装）

```bash
cd frontend
npm install  # or pnpm install
npm run dev  # or pnpm dev
```

## GCP プロジェクト

- **Dev**: wb-dev-480009
- **Prod**: (後で作成)

## リージョン

- **Region**: asia-northeast1 (東京)

## 技術スタック

- **Backend**: FastAPI, SQLModel, SQLAlchemy, Alembic, Gunicorn
- **Database**: PostgreSQL 15 (Cloud SQL)
- **Frontend**: Vue.js, Vite
- **Infrastructure**: Cloud Run, Cloud SQL, VPC, Private Service Connect, Artifact Registry

## GCPインフラ構築

詳細は `infrastructure/README.md` を参照してください。

### クイックスタート

```bash
# 1. インフラ構築（初回のみ）
cd infrastructure
./setup-dev.sh

# 2. バックエンドデプロイ
./deploy-backend.sh
```

## 注意事項

- **DB タイムゾーン**: UTC
- **主キー**: UUID
- **ORM**: SQLModel (手動SQL原則禁止)
- **シークレット管理**: 当面は環境変数直書き（Secret Managerなし）
- **CI/CD**: なし（手動デプロイ）
- **ログ**: デフォルトのみ（追加整備なし）

## 次のステップ

1. ✅ ローカル準備・ディレクトリ構造作成
2. ✅ Backend雛形作成
3. ✅ Frontend雛形作成
4. ⏳ GCPインフラ構築（`infrastructure/setup-dev.sh`を実行）
5. ⏳ バックエンドデプロイ（`infrastructure/deploy-backend.sh`を実行）
6. ⏳ Frontendプロジェクト作成（Vue.js）
7. ⏳ Firebase Hosting設定
8. ⏳ Firebase Authentication設定

