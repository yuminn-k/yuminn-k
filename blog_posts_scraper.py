import requests
from bs4 import BeautifulSoup
import json

urls = ["https://devyuminkim.github.io/lifelog/", "https://devyuminkim.github.io/devlog/"]

output_data = []

for url in urls:
    blog_posts = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.select("#_main > article > ul:nth-child(3) > li"):
        title = article.find("a").text.strip()
        link = url.rstrip("/") + article.find("a")["href"]

        post_data = {
            "title": title,
            "link": link
        }

        blog_posts.append(post_data)
    
    output_data.extend(sorted(blog_posts, key=lambda x: x['link'], reverse=True)[:3])

output_data = sorted(output_data, key=lambda x: x['link'], reverse=True)[:3]

with open("output.json", "w") as json_file:
    json.dump(output_data, json_file)
