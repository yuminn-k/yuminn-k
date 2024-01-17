FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python blog_posts_scraper.py && python update_readme.py"]