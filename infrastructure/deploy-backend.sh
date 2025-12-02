#!/bin/bash
# Backend を Cloud Run にデプロイするスクリプト

set -e

PROJECT_ID="wb-dev-480009"
REGION="asia-northeast1"
SERVICE_NAME="wb-backend-dev"
ARTIFACT_REPO_NAME="wb-backend-dev"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO_NAME}/wb-backend"
VPC_CONNECTOR_NAME="wb-dev-vpc-connector"

echo "=== Backend デプロイ開始 ==="
echo "プロジェクト: ${PROJECT_ID}"
echo "サービス名: ${SERVICE_NAME}"
echo ""

# デフォルトプロジェクトの設定確認
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
if [ "${CURRENT_PROJECT}" != "${PROJECT_ID}" ]; then
  echo "デフォルトプロジェクトを ${PROJECT_ID} に設定します..."
  gcloud config set project ${PROJECT_ID}
fi

# イメージをビルドしてプッシュ
echo "1. Docker イメージをビルドしてプッシュ中..."
cd "$(dirname "$0")/../backend"
gcloud builds submit --tag ${IMAGE_NAME}:latest --project=${PROJECT_ID}

# Cloud Run サービスをデプロイ
echo "2. Cloud Run サービスをデプロイ中..."

# 環境変数の設定（実際の値に置き換える必要があります）
# DATABASE_URL は Cloud SQL の Private IP を使用
read -p "Cloud SQL の Private IP を入力してください: " DB_PRIVATE_IP
read -p "データベースパスワードを入力してください: " -s DB_PASSWORD
echo ""

DATABASE_URL="postgresql+psycopg2://wb_dev_user:${DB_PASSWORD}@${DB_PRIVATE_IP}:5432/wb_dev"

gcloud run deploy ${SERVICE_NAME} \
  --project=${PROJECT_ID} \
  --image=${IMAGE_NAME}:latest \
  --region=${REGION} \
  --platform=managed \
  --allow-unauthenticated \
  --vpc-connector=${VPC_CONNECTOR_NAME} \
  --vpc-egress=private-ranges-only \
  --set-env-vars="DATABASE_URL=${DATABASE_URL},API_V1_PREFIX=/api/v1,APP_NAME=WB Backend,APP_VERSION=0.1.0,DEBUG=false" \
  --memory=512Mi \
  --cpu=1 \
  --timeout=300 \
  --max-instances=10 \
  --min-instances=0

echo ""
echo "=== デプロイ完了 ==="
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --project=${PROJECT_ID} --format='value(status.url)')
echo "サービスURL: ${SERVICE_URL}"
echo "ヘルスチェック: ${SERVICE_URL}/healthz"

