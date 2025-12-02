# Prod環境セットアップ（メモ）

本番環境用のGCPプロジェクトセットアップ手順（後で具体化）

## 概要

- プロジェクト名: wb-prod（仮）
- リージョン: asia-northeast1
- 構成: dev環境とほぼ同様だが、以下の点を検討

## 検討事項

### VPC構成

- **オプション1**: 各プロジェクトで独立したVPC
- **オプション2**: Shared VPCを使用（推奨）
  - ホストプロジェクト: wb-shared-vpc（新規作成）
  - サービスプロジェクト: wb-dev-480009, wb-prod

### Cloud SQL構成

- **オプション1**: prod環境で独立したCloud SQLインスタンスを作成
- **オプション2**: dev環境のCloud SQLをPSC経由で共有
  - Private Service Connectエンドポイントを作成
  - prodプロジェクトからdevプロジェクトのCloud SQLに接続

### セキュリティ

- Secret Managerの導入を検討
- 本番環境では環境変数直書きを避ける
- IAMロールの適切な設定
- ネットワークセキュリティポリシーの設定

### バックアップ・災害対策

- 本番環境では自動バックアップを有効化
- ポイントインタイムリカバリ（PITR）の設定
- クロスリージョンレプリカの検討

## 実装手順（後で具体化）

1. 新規GCPプロジェクト作成（wb-prod）
2. 必要なAPIの有効化
3. VPC/サブネット/VPCコネクタ作成
4. Cloud SQLインスタンス作成（またはPSC設定）
5. Artifact Registry作成
6. Cloud Runサービス作成
7. CI/CDパイプラインの構築（GitHub Actions等）

## 参考

- [Shared VPC](https://cloud.google.com/vpc/docs/shared-vpc)
- [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)

