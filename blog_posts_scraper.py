import requests
from bs4 import BeautifulSoup
import json

urls = ["https://devyuminkim.github.io/lifelog/", "https://devyuminkim.github.io/devlog/"]

output_data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.select("div.grid-item div.post-card.content a")[:3]:
        title = article.find("figcaption").text.strip()
        link = url.rstrip("/") + article["href"]

        post_data = {
            "title": title,
            "link": link
        }

        output_data.append(post_data)

with open("output.json", "w") as json_file:
    json.dump(output_data, json_file)
