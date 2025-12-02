# GCP Infrastructure Setup

wb-dev-480009 プロジェクト用のインフラ構築手順

## 前提条件

- gcloud CLI がインストール済み
- wb-dev-480009 プロジェクトへのアクセス権限
- デフォルトプロジェクトが設定済み: `gcloud config set project wb-dev-480009`

## セットアップ手順

### 1. 必要なAPIの有効化

```bash
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  vpcaccess.googleapis.com \
  artifactregistry.googleapis.com \
  compute.googleapis.com \
  servicenetworking.googleapis.com
```

### 2. VPC / サブネット / VPCコネクタの作成

#### 2-1. VPC作成

```bash
gcloud compute networks create wb-vpc \
  --project=wb-dev-480009 \
  --subnet-mode=custom \
  --bgp-routing-mode=regional
```

#### 2-2. サブネット作成

```bash
gcloud compute networks subnets create wb-subnet-main \
  --project=wb-dev-480009 \
  --network=wb-vpc \
  --range=10.1.0.0/24 \
  --region=asia-northeast1
```

#### 2-3. Serverless VPC Access コネクタ作成

```bash
gcloud compute networks vpc-access connectors create wb-dev-vpc-connector \
  --project=wb-dev-480009 \
  --region=asia-northeast1 \
  --subnet=wb-subnet-main \
  --subnet-project=wb-dev-480009 \
  --min-instances=2 \
  --max-instances=3 \
  --machine-type=e2-micro
```

### 3. Cloud SQL (PostgreSQL 15) インスタンス作成

#### 3-1. インスタンス作成

```bash
gcloud sql instances create wb-dev-db \
  --project=wb-dev-480009 \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-northeast1 \
  --network=projects/wb-dev-480009/global/networks/wb-vpc \
  --no-assign-ip \
  --enable-google-private-path \
  --storage-type=SSD \
  --storage-size=10GB \
  --storage-auto-increase \
  --backup-start-time=00:00 \
  --enable-bin-log \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=3 \
  --maintenance-release-channel=production \
  --deletion-protection
```

**注意**: 上記コマンドは自動バックアップを有効にしていますが、要件では「バックアップなし」とあります。
バックアップを無効にする場合は、`--no-backup` フラグを使用するか、作成後にバックアップ設定を無効化してください。

#### 3-2. データベースとユーザー作成

```bash
# データベース作成
gcloud sql databases create wb_dev \
  --instance=wb-dev-db \
  --project=wb-dev-480009

# ユーザー作成（パスワードは適宜変更）
gcloud sql users create wb_dev_user \
  --instance=wb-dev-db \
  --password=YOUR_SECURE_PASSWORD \
  --project=wb-dev-480009
```

### 4. Cloud SQL の Private Service Connect 有効化

```bash
# Private Service Connect エンドポイント作成
gcloud compute addresses create wb-dev-db-psc \
  --project=wb-dev-480009 \
  --global \
  --purpose=VPC_PEERING \
  --prefix-length=16 \
  --network=projects/wb-dev-480009/global/networks/wb-vpc

# Private Service Connect 接続作成
gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --ranges=wb-dev-db-psc \
  --network=wb-vpc \
  --project=wb-dev-480009
```

### 5. Artifact Registry リポジトリ作成

```bash
gcloud artifacts repositories create wb-backend-dev \
  --project=wb-dev-480009 \
  --repository-format=docker \
  --location=asia-northeast1 \
  --description="Backend Docker images for dev environment"
```

### 6. Cloud Run サービス作成（初回デプロイ後）

```bash
# イメージをビルドしてプッシュ（後で実行）
# gcloud builds submit --tag asia-northeast1-docker.pkg.dev/wb-dev-480009/wb-backend-dev/wb-backend:latest

# Cloud Run サービス作成
gcloud run deploy wb-backend-dev \
  --project=wb-dev-480009 \
  --image=asia-northeast1-docker.pkg.dev/wb-dev-480009/wb-backend-dev/wb-backend:latest \
  --region=asia-northeast1 \
  --platform=managed \
  --allow-unauthenticated \
  --vpc-connector=wb-dev-vpc-connector \
  --vpc-egress=private-ranges-only \
  --set-env-vars="DATABASE_URL=postgresql+psycopg2://wb_dev_user:PASSWORD@PRIVATE_IP:5432/wb_dev" \
  --memory=512Mi \
  --cpu=1 \
  --timeout=300 \
  --max-instances=10 \
  --min-instances=0
```

**注意**: 
- `PRIVATE_IP` は Cloud SQL インスタンスの Private IP アドレスに置き換えてください
- `PASSWORD` は実際のパスワードに置き換えてください
- セキュリティのため、環境変数は Secret Manager を使用することを推奨します（今回は env 直書き）

## 接続情報の確認

### Cloud SQL Private IP の確認

```bash
gcloud sql instances describe wb-dev-db \
  --project=wb-dev-480009 \
  --format="value(ipAddresses[0].ipAddress)"
```

### VPC コネクタの確認

```bash
gcloud compute networks vpc-access connectors describe wb-dev-vpc-connector \
  --project=wb-dev-480009 \
  --region=asia-northeast1
```

## トラブルシューティング

### Cloud Run から Cloud SQL に接続できない場合

1. VPC コネクタが正しく設定されているか確認
2. Cloud SQL の Private IP が有効になっているか確認
3. Cloud Run の egress 設定が `private-ranges-only` になっているか確認
4. ファイアウォールルールを確認（必要に応じて追加）

## 次のステップ

- [ ] バックエンドのビルドとデプロイ（タスク5）
- [ ] フロントエンドの Firebase Hosting 設定
- [ ] Firebase Authentication の設定

