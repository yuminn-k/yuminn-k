# Python 3.8イメージをベースにDockerイメージを生成
FROM python:3.8-slim-buster

# 作業ディレクトリを/appに設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y git

# 必要なPythonライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Gitユーザー名とメールアドレスを設定
RUN git config --global user.name "yuminnk"
RUN git config --global user.email "gimyumin40@gmail.com"

# アプリケーションコードをDockerコンテナにコピー
COPY . .

# スクリプト実行
CMD ["sh", "-c", "python blog_posts_scraper.py && python update_readme.py && cp README.md /app/ && git add README.md && git commit -m 'Updated README.md with recent blog posts'"]