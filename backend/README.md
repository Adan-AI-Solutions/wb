# WB Backend (Cloud Functions)

Firebase Cloud Functions for Python を使用したバックエンドアプリケーション

## 構造

```
backend/
├── functions/           # Cloud Functionsのコード
│   ├── main.py         # エントリポイント
│   ├── api/            # APIエンドポイント
│   ├── models/         # SQLModelモデル
│   ├── db/             # データベースセッション管理
│   ├── core/           # 設定・共通定数
│   ├── migrations/     # Alembicマイグレーション
│   └── requirements.txt
├── firebase.json        # Firebase設定
└── README.md
```

## セットアップ

### Dockerを使用したローカル開発環境（推奨）

1. Docker Composeでコンテナを起動
```bash
# プロジェクトルートから
docker compose up -d --build
```

2. コンテナに入る
```bash
docker compose exec backend bash
```

3. コンテナ内でPython仮想環境をセットアップ（初回のみ）
```bash
cd functions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Firebase Emulatorの起動
```bash
# コンテナ内で
cd /backend
source functions/venv/bin/activate  # venvをactivate
firebase emulators:start --only functions
```

**重要**: `firebase emulators:start`を実行する前に、必ず`source functions/venv/bin/activate`でvenvをactivateしてください。

**注意**: Firebase Emulatorは環境変数`DATABASE_URL`を使ってローカルのPostgreSQL（`db`サービス）に接続します。
Docker環境では、`db`ホスト名でPostgreSQLに接続できます。

### ローカル環境でのセットアップ（Docker不使用）

1. Firebase CLIのインストール
```bash
npm install -g firebase-tools
```

2. Firebaseプロジェクトの初期化（初回のみ）
```bash
cd backend
firebase login
firebase init functions
# または既存の設定を使用する場合は、.firebasercが既に作成されています
```

3. Firebase Emulatorのセットアップ（Functionsのみ）
```bash
cd backend
firebase init emulators
# Functions Emulatorのみを選択
```

4. Python仮想環境の作成
```bash
cd functions
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. 環境変数の設定

環境に応じた`.env`ファイルが用意されています：

- `.env.local` - ローカル開発環境（Docker使用時）
- `.env.wb-dev` - 開発環境（wb-dev-480009）デプロイ用
- `.env.wb-prod` - 本番環境デプロイ用

ローカル環境でDockerを使用しない場合は、`.env.local`を編集してください：

```bash
# Database (Local PostgreSQL)
DATABASE_URL=postgresql+psycopg2://wb_dev_user:wb_dev_password@localhost:5432/wb_dev
```

6. Firebase Emulatorの起動
```bash
firebase emulators:start
```

## デプロイ

### Firebase Functionsへのデプロイ

```bash
cd backend
firebase deploy --only functions
```

### 環境変数の設定

本番環境のDB URLは、Firebase Functionsの環境変数として設定します。

#### 方法1: Firebase Console（推奨）

1. [Firebase Console](https://console.firebase.google.com/project/wb-dev-480009/functions/config) にアクセス
2. 「Functions」→「設定」→「環境変数」を選択
3. `DATABASE_URL`を追加：
   ```
   DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@PRIVATE_IP:5432/DB_NAME
   ```
   - `PRIVATE_IP`: Cloud SQLインスタンスのPrivate IPアドレス
   - `USER`, `PASSWORD`, `DB_NAME`: 実際の値に置き換え

#### 方法2: Firebase CLI

```bash
cd backend
firebase functions:secrets:set DATABASE_URL
# プロンプトでDB URLを入力（Secret Managerを使用）

# または直接環境変数として設定（非推奨、機密情報はSecret Managerを使用）
firebase functions:config:set database.url="postgresql+psycopg2://..."
```

**注意**: 
- Cloud SQLのPrivate IPを使用する場合は、VPCコネクタの設定が必要です
- 機密情報（パスワード等）はSecret Managerの使用を推奨します
- 環境変数はデプロイ後に反映されます

## 技術スタック

- **Runtime**: Python 3.11 (Cloud Functions)
- **Framework**: Firebase Functions for Python
- **ORM**: SQLModel (SQLAlchemy)
- **Migration**: Alembic
- **Database**: Cloud SQL for PostgreSQL 15

## 注意事項

- Cloud SQL接続にはPrivate IPを使用
- 環境変数はFirebase Functionsの設定から読み込む
- ローカル開発時はFirebase Emulatorを使用（Functionsのみ）
- Firestoreは使用しません（RDBのみ）

