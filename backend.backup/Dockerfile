# Backend Dockerfile for Cloud Run
FROM python:3.11-slim

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# gunicornのインストール（Cloud Run用）
RUN pip install --no-cache-dir gunicorn

# アプリケーションコードのコピー
COPY . .

# ポート設定（Cloud RunはPORT環境変数を使用）
ENV PORT=8080

# ヘルスチェック用のエンドポイント
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT}/healthz')" || exit 1

# Cloud Run用のコマンド
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 --worker-class uvicorn.workers.UvicornWorker app.main:app

