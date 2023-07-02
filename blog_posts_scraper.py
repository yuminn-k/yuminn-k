import requests
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse
import os
import re
import random

def is_absolute(url):
    return bool(requests.utils.urlparse(url).netloc)

urls = [
    "https://devyuminkim.github.io/lifelog/",
    "https://devyuminkim.github.io/devlog/",
]

output_data = []

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select("#_main > article > ul:not(:first-child) > li.h4 > a")

        for article in articles:
            title = article.find("span").text.strip()
            link = article["href"]

            time_element = article.parent.find("time")
            if time_element:
                timestamp = time_element.text.strip()
            else:
                print(f"Timestamp not found for article: {title}")
                continue

            if not is_absolute(link):
                link = url.rstrip("/") + link.lstrip(".")
                # 중복되는 부분 제거
                link = re.sub(r"/(?:devlog|lifelog)/", "/", link, count=1)

            print(f"title: {title}, link: {link}, timestamp: {timestamp}")

            post_data = {
                "title": title,
                "link": link,
                "timestamp": parse(timestamp),
            }

            output_data.append(post_data)
    except Exception as e:
        print(f"Error while scraping {url}: {e}")

# 랜덤한 3개의 포스트를 가져옵니다.
sample_output_data = random.sample(output_data, min(len(output_data), 3))
sample_output_data.sort(key=lambda x: x["timestamp"], reverse=True)

for post in sample_output_data:
    post["timestamp"] = post["timestamp"].strftime("%Y-%m-%d")

try:
    output_file = "output.json"
    with open(output_file, "w") as json_file:
        json.dump(sample_output_data, json_file)
    print(f"output.json에 성공적으로 저장되었습니다. 작업 디렉토리: {os.getcwd()}")
except Exception as e:
    print(f"output.json에 저장하는 동안 오류가 발생했습니다: {e}")

# output.json이 있는지 확인하는 코드 추가
print(f"\n저장된 output.json 파일의 경로: {os.path.abspath(output_file)}")

# output.json 파일 내용 확인 코드 추가
print("\noutput.json 파일 내용 확인:")
with open(output_file, "r") as json_file:
    loaded_data = json.load(json_file)
    print(json.dumps(loaded_data, indent=4))
