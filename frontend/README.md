# WB Frontend

Vue.js 3 + Vite + TypeScript のフロントエンドアプリケーション

## セットアップ

### 依存関係のインストール

```bash
npm install
# または
pnpm install
```

### 環境変数の設定

Cloud Functionsは関数名ごとのエンドポイントを直接叩くため、環境ごとにフルURLを持つ`.env`を用意しています（値は編集可）。

- `.env.local` : ローカル Functions Emulator 用（例: `http://localhost:5001/wb-dev-480009/asia-northeast1/*`）
- `.env.dev`   : 開発環境 Functions 用
- `.env.prod`  : 本番環境 Functions 用（プロジェクトIDに合わせて変更してください）

各ファイルのデフォルト値（例）:

```env
VITE_API_HEALTH_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/healthz_endpoint
VITE_API_TODOS_LIST_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/list_todos
VITE_API_TODOS_GET_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/get_todo
VITE_API_TODOS_CREATE_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/create_todo
VITE_API_TODOS_UPDATE_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/update_todo
VITE_API_TODOS_DELETE_ENDPOINT=http://localhost:5001/wb-dev-480009/asia-northeast1/delete_todo
```

`--mode`オプションで読み込む`.env`を切り替えられます。

```bash
# ローカル（Functions Emulator）
npm run dev -- --mode local

# 開発環境（wb-dev-480009）
npm run dev -- --mode dev

# 本番環境（プロジェクトIDに合わせて.env.prodを更新）
npm run build -- --mode prod
```

### 開発サーバーの起動

```bash
npm run dev
# または
pnpm dev
```

開発サーバーは `http://localhost:3000` で起動します。

### ビルド

```bash
npm run build
# または
pnpm build
```

## ディレクトリ構造

```
frontend/
├── src/
│   ├── components/    # Vueコンポーネント
│   ├── views/         # ページビュー
│   │   ├── HomeView.vue
│   │   └── AboutView.vue
│   ├── stores/        # Piniaストア
│   │   └── counter.ts
│   ├── router/        # Vue Router設定
│   │   └── index.ts
│   ├── api/           # APIクライアント
│   │   └── health.ts
│   ├── assets/        # 静的アセット
│   ├── App.vue        # ルートコンポーネント
│   └── main.ts        # エントリポイント
├── public/            # 静的ファイル
├── index.html         # HTMLエントリポイント
├── vite.config.ts     # Vite設定
├── tsconfig.json      # TypeScript設定
└── package.json
```

## 技術スタック

- **Framework**: Vue.js 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Router**: Vue Router 4
- **TypeScript**: 完全対応
- **HTTP Client**: Axios

## 機能

- ✅ バックエンドヘルスチェックAPI連携
- ✅ Vue Routerによるルーティング
- ✅ Piniaによる状態管理
- ✅ TypeScriptによる型安全性

## Firebase Hosting

Firebase Hostingへのデプロイは後続タスクで実装予定。
