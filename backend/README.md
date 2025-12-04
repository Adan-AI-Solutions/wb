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

### ローカル開発環境

1. Firebase CLIのインストール（未インストールの場合）
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

2. Python仮想環境の作成
```bash
cd functions
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env.local
# .env.local を編集してDB接続情報を設定
```

4. Firebase Emulatorの起動
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

Firebase ConsoleまたはCLIで環境変数を設定：

```bash
firebase functions:config:set database.url="postgresql+psycopg2://..."
```

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

