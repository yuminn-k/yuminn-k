import requests
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse

urls = [
    "https://devyuminkim.github.io/lifelog/",
    "https://devyuminkim.github.io/devlog/",
]

output_data = []

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select("#_main > div.post > ul.post-list > li")

        for article in articles[:3]:
            title = article.select_one("a").text.strip()
            link = url.rstrip("/") + article.select_one("a")["href"]
            timestamp = article.select_one("span.post-meta").text.strip()

            # 추가할 로그 출력 코드
            print(f"title: {title}, link: {link}, timestamp: {timestamp}")

            post_data = {
                "title": title,
                "link": link,
                "timestamp": parse(timestamp),
            }

            output_data.append(post_data)
    except Exception as e:
        print(f"Error while scraping {url}: {e}")

output_data.sort(key=lambda x: x["timestamp"], reverse=True)
output_data = output_data[:3]

# Convert datetime objects back to strings
for post in output_data:
    post["timestamp"] = post["timestamp"].strftime("%Y-%m-%d")

with open("output.json", "w") as json_file:
    json.dump(output_data, json_file)
