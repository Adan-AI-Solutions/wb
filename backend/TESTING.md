# ローカルテスト手順

## 前提条件

1. Docker Desktopが起動していること
2. ポート4000, 5001, 5432が使用可能であること

## テスト手順

### 1. Docker Composeでコンテナを起動

```bash
cd /Users/mini/adan/wb
docker compose up -d --build
```

### 2. コンテナの状態確認

```bash
docker compose ps
```

### 3. コンテナに入る

```bash
docker compose exec backend bash
```

### 4. Python仮想環境のセットアップ（初回のみ）

```bash
cd functions
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Firebase Emulatorの起動

```bash
cd /backend
source functions/venv/bin/activate  # venvをactivate
firebase emulators:start --only functions
```

**重要**: `firebase emulators:start`を実行する前に、必ず`source functions/venv/bin/activate`でvenvをactivateしてください。

**注意**: 初回起動時は、エミュレーターが関数を読み込むまで30-40秒程度かかることがあります。

### 6. 別のターミナルでAPIをテスト

#### ヘルスチェック

```bash
curl http://localhost:5001/wb-dev-480009/asia-northeast1/healthz_endpoint
```

期待されるレスポンス:
```json
{
  "status": "ok",
  "timestamp": "2024-12-04T...",
  "service": "wb-backend"
}
```

#### Todo一覧取得

```bash
curl http://localhost:5001/wb-dev-480009/asia-northeast1/list_todos
```

#### Todo作成

```bash
curl -X POST http://localhost:5001/wb-dev-480009/asia-northeast1/create_todo \
  -H "Content-Type: application/json" \
  -d '{"title": "テストTodo", "description": "これはテストです"}'
```

#### Todo取得

```bash
# 作成したTodoのIDを使用
curl http://localhost:5001/wb-dev-480009/asia-northeast1/get_todo?todo_id=<TODO_ID>
```

#### Todo更新

```bash
curl -X PATCH http://localhost:5001/wb-dev-480009/asia-northeast1/update_todo?todo_id=<TODO_ID> \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

#### Todo削除

```bash
curl -X DELETE http://localhost:5001/wb-dev-480009/asia-northeast1/delete_todo?todo_id=<TODO_ID>
```

## トラブルシューティング

### ポートが既に使用されている場合

```bash
# ポート4000を確認
lsof -ti:4000

# ポート5001を確認
lsof -ti:5001

# プロセスを停止
lsof -ti:4000 | xargs kill -9
lsof -ti:5001 | xargs kill -9
```

### Dockerコンテナのログ確認

```bash
docker compose logs backend --tail 50
docker compose logs db --tail 50
```

### コンテナの再起動

```bash
docker compose restart backend
docker compose restart db
```

### コンテナの完全リセット

```bash
docker compose down
docker compose up -d --build
```


