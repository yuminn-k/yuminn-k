import requests
from bs4 import BeautifulSoup
import json

urls = ["https://devyuminkim.github.io/lifelog/", "https://devyuminkim.github.io/devlog/"]

output_data = []

for url in urls:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for article in soup.select("div.post-list--item"):
            title = article.select_one("div.post-list--item--title").text.strip()
            link = url.rstrip("/") + article.select_one("a")["href"]
            timestamp = article.select_one("div.post-list--item--date").text.strip()

            post_data = {
                "title": title,
                "link": link,
                "timestamp": timestamp
            }

            output_data.append(post_data)
    except Exception as e:
        print(f"Error while scraping {url}: {e}")

output_data.sort(key=lambda x: x["timestamp"], reverse=True)
output_data = output_data[:3]


output_data = sorted(output_data, key=lambda x: x['link'], reverse=True)[:3]

with open("output.json", "w") as json_file:
    json.dump(output_data, json_file)
