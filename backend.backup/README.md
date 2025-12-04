# WB Backend

FastAPI + SQLModel + PostgreSQL 15 のバックエンドアプリケーション

## セットアップ

### ローカル開発環境

1. 仮想環境の作成と有効化
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# または
.venv\Scripts\activate  # Windows
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env.local
# .env.local を編集して必要に応じて設定を変更
```

4. データベースマイグレーション
```bash
# 初回のみ: Alembicの初期化（既に作成済みの場合は不要）
# alembic init migrations

# マイグレーションの作成
alembic revision --autogenerate -m "Initial migration"

# マイグレーションの適用
alembic upgrade head
```

5. アプリケーションの起動
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Compose を使用した開発

プロジェクトルートから以下を実行:

```bash
docker compose up -d
docker compose run backend alembic upgrade head
```

## ディレクトリ構造

```
backend/
├── app/
│   ├── api/          # APIルーティング
│   ├── models/       # SQLModelモデル
│   ├── db/           # データベースセッション管理
│   ├── core/         # 設定・共通定数
│   ├── auth/         # 認証関連（Firebase Authは後で実装）
│   └── main.py       # FastAPIエントリポイント
├── migrations/       # Alembicマイグレーション
├── requirements.txt  # Python依存関係
├── Dockerfile        # Cloud Run用Dockerfile
└── alembic.ini       # Alembic設定
```

## API エンドポイント

- `GET /` - ルートエンドポイント
- `GET /healthz` - ヘルスチェック

## 技術スタック

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy)
- **Migration**: Alembic
- **Database**: PostgreSQL 15
- **Python**: 3.11

## 注意事項

- データベースタイムゾーン: UTC
- 主キー: UUID
- 手動SQLは原則禁止（SQLModel/SQLAlchemyを使用）

