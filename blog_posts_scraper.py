import requests
from bs4 import BeautifulSoup
import json
import os
import random
from dotenv import load_dotenv

# URL이 절대 경로인지 확인하는 함수
def is_absolute(url):
    return bool(requests.utils.urlparse(url).netloc)

# 블로그에서 포스트 목록을 가져오는 함수
def get_random_blog_posts(url, css_selector):
    output_data = []

    try:
        # 블로그의 HTML 코드 가져오기
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # 포스트 목록 가져오기
        articles = soup.select(css_selector)

        # 각 포스트의 a 태그들의 링크를 가져옵니다.
        for article in articles:
            links = article.find_all("a")

            # 각 링크의 제목과 링크 저장하기
            for link in links:
                title = link.text.strip()
                href = link["href"]

                if not is_absolute(href):
                    href = url.rstrip("/") + href.lstrip(".")

                post_data = {
                    "title": title,
                    "link": href,
                }

                output_data.append(post_data)
    except Exception as e:
        print(f"Error while scraping {url}: {e}")

    return output_data

# 출력 데이터를 JSON 파일에 저장하는 함수
def save_output_to_json(sample_output_data, output_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, output_file)
    try:
        with open(output_path, "w") as json_file:
            json.dump(sample_output_data, json_file)
        print(f"{output_path}에 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"{output_path}에 저장하는 동안 오류가 발생했습니다:e\n")
    return output_path

def main():
    load_dotenv()
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    url = os.getenv("URL")
    css_selector = os.getenv("CSS_SELECTOR")
    output_file = "output.json"

    output_data = get_random_blog_posts(url, css_selector)
    print(f"Output Data: {output_data}")
    sample_output_data = random.sample(output_data, min(len(output_data), 3)) # 기본 3개
    save_output_to_json(sample_output_data, output_file)

if __name__ == "__main__":
    main()
