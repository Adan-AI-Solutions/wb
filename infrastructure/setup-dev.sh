#!/bin/bash
# GCP dev環境インフラ構築スクリプト
# プロジェクト: wb-dev-480009
# リージョン: asia-northeast1

set -e

PROJECT_ID="wb-dev-480009"
REGION="asia-northeast1"
VPC_NAME="wb-vpc"
SUBNET_NAME="wb-subnet-main"
SUBNET_RANGE="10.1.0.0/24"
VPC_CONNECTOR_NAME="wb-dev-vpc-connector"
DB_INSTANCE_NAME="wb-dev-db"
DB_NAME="wb_dev"
DB_USER="wb_dev_user"
ARTIFACT_REPO_NAME="wb-backend-dev"

echo "=== GCP Dev環境インフラ構築開始 ==="
echo "プロジェクト: ${PROJECT_ID}"
echo "リージョン: ${REGION}"
echo ""

# デフォルトプロジェクトの設定確認
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
if [ "${CURRENT_PROJECT}" != "${PROJECT_ID}" ]; then
  echo "デフォルトプロジェクトを ${PROJECT_ID} に設定します..."
  gcloud config set project ${PROJECT_ID}
fi

# 1. API有効化
echo "1. 必要なAPIを有効化中..."
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  vpcaccess.googleapis.com \
  artifactregistry.googleapis.com \
  compute.googleapis.com \
  servicenetworking.googleapis.com \
  --project=${PROJECT_ID}

# 2. VPC作成
echo "2. VPC作成中..."
if gcloud compute networks describe ${VPC_NAME} --project=${PROJECT_ID} &>/dev/null; then
  echo "  VPC ${VPC_NAME} は既に存在します。スキップします。"
else
  gcloud compute networks create ${VPC_NAME} \
    --project=${PROJECT_ID} \
    --subnet-mode=custom \
    --bgp-routing-mode=regional
  echo "  VPC ${VPC_NAME} を作成しました。"
fi

# 3. サブネット作成
echo "3. サブネット作成中..."
if gcloud compute networks subnets describe ${SUBNET_NAME} --region=${REGION} --project=${PROJECT_ID} &>/dev/null; then
  echo "  サブネット ${SUBNET_NAME} は既に存在します。スキップします。"
else
  gcloud compute networks subnets create ${SUBNET_NAME} \
    --project=${PROJECT_ID} \
    --network=${VPC_NAME} \
    --range=${SUBNET_RANGE} \
    --region=${REGION}
  echo "  サブネット ${SUBNET_NAME} を作成しました。"
fi

# 4. VPC Access コネクタ作成
echo "4. VPC Access コネクタ作成中..."
if gcloud compute networks vpc-access connectors describe ${VPC_CONNECTOR_NAME} --region=${REGION} --project=${PROJECT_ID} &>/dev/null; then
  echo "  VPC コネクタ ${VPC_CONNECTOR_NAME} は既に存在します。スキップします。"
else
  gcloud compute networks vpc-access connectors create ${VPC_CONNECTOR_NAME} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --subnet=${SUBNET_NAME} \
    --subnet-project=${PROJECT_ID} \
    --min-instances=2 \
    --max-instances=3 \
    --machine-type=e2-micro
  echo "  VPC コネクタ ${VPC_CONNECTOR_NAME} を作成しました。"
fi

# 5. Cloud SQL インスタンス作成
echo "5. Cloud SQL インスタンス作成中..."
if gcloud sql instances describe ${DB_INSTANCE_NAME} --project=${PROJECT_ID} &>/dev/null; then
  echo "  Cloud SQL インスタンス ${DB_INSTANCE_NAME} は既に存在します。スキップします。"
else
  echo "  Cloud SQL インスタンスを作成します（数分かかります）..."
  gcloud sql instances create ${DB_INSTANCE_NAME} \
    --project=${PROJECT_ID} \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=${REGION} \
    --network=projects/${PROJECT_ID}/global/networks/${VPC_NAME} \
    --no-assign-ip \
    --enable-google-private-path \
    --storage-type=SSD \
    --storage-size=10GB \
    --storage-auto-increase \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=3 \
    --maintenance-release-channel=production \
    --deletion-protection
  
  echo "  Cloud SQL インスタンス ${DB_INSTANCE_NAME} を作成しました。"
fi

# 6. データベース作成
echo "6. データベース作成中..."
if gcloud sql databases describe ${DB_NAME} --instance=${DB_INSTANCE_NAME} --project=${PROJECT_ID} &>/dev/null; then
  echo "  データベース ${DB_NAME} は既に存在します。スキップします。"
else
  gcloud sql databases create ${DB_NAME} \
    --instance=${DB_INSTANCE_NAME} \
    --project=${PROJECT_ID}
  echo "  データベース ${DB_NAME} を作成しました。"
fi

# 7. データベースユーザー作成（パスワードは環境変数から取得、なければプロンプト）
echo "7. データベースユーザー作成中..."
DB_PASSWORD="${DB_PASSWORD:-}"
if [ -z "${DB_PASSWORD}" ]; then
  echo "  データベースユーザーのパスワードを入力してください:"
  read -s DB_PASSWORD
  echo ""
fi

# ユーザーが既に存在するかチェック（エラーハンドリング）
if gcloud sql users list --instance=${DB_INSTANCE_NAME} --project=${PROJECT_ID} | grep -q "^${DB_USER}"; then
  echo "  ユーザー ${DB_USER} は既に存在します。スキップします。"
else
  gcloud sql users create ${DB_USER} \
    --instance=${DB_INSTANCE_NAME} \
    --password=${DB_PASSWORD} \
    --project=${PROJECT_ID}
  echo "  ユーザー ${DB_USER} を作成しました。"
fi

# 8. Artifact Registry リポジトリ作成
echo "8. Artifact Registry リポジトリ作成中..."
if gcloud artifacts repositories describe ${ARTIFACT_REPO_NAME} --location=${REGION} --project=${PROJECT_ID} &>/dev/null; then
  echo "  Artifact Registry リポジトリ ${ARTIFACT_REPO_NAME} は既に存在します。スキップします。"
else
  gcloud artifacts repositories create ${ARTIFACT_REPO_NAME} \
    --project=${PROJECT_ID} \
    --repository-format=docker \
    --location=${REGION} \
    --description="Backend Docker images for dev environment"
  echo "  Artifact Registry リポジトリ ${ARTIFACT_REPO_NAME} を作成しました。"
fi

echo ""
echo "=== インフラ構築完了 ==="
echo ""
echo "次のステップ:"
echo "1. Cloud SQL の Private IP を確認:"
echo "   gcloud sql instances describe ${DB_INSTANCE_NAME} --project=${PROJECT_ID} --format='value(ipAddresses[0].ipAddress)'"
echo ""
echo "2. バックエンドの環境変数に接続情報を設定"
echo ""
echo "3. バックエンドをビルドしてデプロイ（タスク5参照）"

