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

`.env.local` ファイルを作成（オプション）:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_V1_PREFIX=/api/v1
```

デフォルトでは `http://localhost:8000` に接続します。

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

