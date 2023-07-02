import requests
from bs4 import BeautifulSoup
import json
from dateutil.parser import parse

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
        articles = soup.select("body > article > header > h1 > a")

        for article in articles[:3]:
            title = article.text.strip()
            link = article["href"]
            timestamp = article.find_previous_sibling("time").text.strip()
            if not is_absolute(link):
                link = url.rstrip("/") + "/" + link.lstrip("/")

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

for post in output_data:
    post["timestamp"] = post["timestamp"].strftime("%Y-%m-%d")

try:
    with open("output.json", "w") as json_file:
        json.dump(output_data, json_file)
    print("output.json에 성공적으로 저장되었습니다.")
except Exception as e:
    print(f"output.json에 저장하는 동안 오류가 발생했습니다: {e}")
