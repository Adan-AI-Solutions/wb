# Python 3.11をベースイメージとして使用
FROM python:3.11-alpine as base

# システムパッケージのアップデートと必要なパッケージのインストール
RUN apk update && \
    apk add --no-cache \
    git \
    bash \
    curl \
    nodejs \
    npm \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    openssl-dev \
    make \
    postgresql-dev \
    openjdk11

# npmのバージョンを固定してインストールし、firebase-toolsもインストール
RUN npm install -g firebase-tools

# Google Cloud CLI のダウンロードとインストール
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-470.0.0-linux-x86_64.tar.gz && \
    tar -xf google-cloud-cli-470.0.0-linux-x86_64.tar.gz && \
    rm google-cloud-cli-470.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh --quiet --path-update true

# 環境変数の設定
ENV PATH $PATH:/google-cloud-sdk/bin

# 作業ディレクトリの設定
WORKDIR /backend

