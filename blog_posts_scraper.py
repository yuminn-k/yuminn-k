import requests
from bs4 import BeautifulSoup
import json
import os
import random
from dotenv import load_dotenv

def is_absolute(url):
    return bool(requests.utils.urlparse(url).netloc)

def get_random_blog_posts(url, css_selector):
    output_data = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select(css_selector + ' > a')

        for article in articles:
            title = article.text.strip()
            link = article["href"]

            if not is_absolute(link):
                link = url.rstrip("/") + link.lstrip(".")

            post_data = {
                "title": title,
                "link": link,
            }

            output_data.append(post_data)
    except Exception as e:
        print(f"Error while scraping {url}: {e}")

    return output_data

def save_output_to_json(sample_output_data, output_file):
    try:
        with open(output_file, "w") as json_file:
            json.dump(sample_output_data, json_file)
        print(f"{output_file}에 성공적으로 저장되었습니다. 작업 디렉토리: {os.getcwd()}")
    except Exception as e:
        print(f"{output_file}에 저장하는 동안 오류가 발생했습니다: {e}\n")
    
    return output_file

def main():
    load_dotenv()
    url = os.getenv("URL")
    css_selector = os.getenv("CSS_SELECTOR")
    output_file = "output.json"

    output_data = get_random_blog_posts(url, css_selector)
    sample_output_data = random.sample(output_data, min(len(output_data), 3))
    save_output_to_json(sample_output_data, output_file)

    print(f"\n저장된 {output_file} 파일의 경로: {os.path.abspath(output_file)}")

    print(f"\n{output_file} 파일 내용 확인:")
    with open(output_file, "r") as json_file:
        loaded_data = json.load(json_file)
        print(json.dumps(loaded_data, indent=4))

if __name__ == "__main__":
    main()
