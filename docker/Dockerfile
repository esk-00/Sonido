FROM python:3.12-slim

# システムパッケージのインストール（必要に応じて追加）
RUN apt-get update && apt-get install -y git curl

# エラー防止のために Git を Dockerfile に入れておく
RUN apt-get update && apt-get install -y git

# 作業ディレクトリ
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# pre-commitなど開発用ツールも入れる
RUN pip install pre-commit

# ソースコードを追加
COPY . .

CMD ["bash"]
