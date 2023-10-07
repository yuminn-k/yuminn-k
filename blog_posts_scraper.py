import requests
from bs4 import BeautifulSoup
import json
import os
import random
from pathlib import Path

def is_absolute(url):
    return bool(requests.utils.urlparse(url).netloc)

def get_random_blog_posts(url, css_selector):
    output_data = []

    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select(css_selector)
        all_links = []

        for article in articles:
            links = article.find_all("a")
            all_links.extend(links)

        selected_links = random.sample(all_links, min(3, len(all_links)))

        for link in selected_links:
            title = link.text.strip()

            if '202' in title:
                index_202 = title.index('202')
                title = title[:index_202]

            href = link["href"]
        
            if not is_absolute(href):
                href = url.rstrip("/") + href.lstrip(".")
        
            post_data = {
                "title": title,
                "url": href,
            }

            output_data.append(post_data)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while scraping {url}: {e}")

    return output_data

def save_output_to_json(sample_output_data, output_file):
    output_path = Path(output_file)
    try:
        with output_path.open("w") as json_file:
            json.dump(sample_output_data, json_file)
        print(f"{output_path}에 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"{output_path}에 저장하는 동안 오류가 발생했습니다: {e}")

    return str(output_path)

def main():
    url = os.getenv("URL")
    css_selector = os.getenv("CSS_SELECTOR")
    output_file = "output.json"

    output_data = get_random_blog_posts(url, css_selector)
    sample_output_data = random.sample(output_data, min(len(output_data), 3))
    save_output_to_json(sample_output_data, output_file)

if __name__ == "__main__":
    main()
