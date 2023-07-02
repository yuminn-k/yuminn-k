import json
import re

with open("output.json", "r") as json_file:
    post_data = json.load(json_file)

new_section = "<h2>Blog Posts</h2>\n\n"
for post in post_data:
    new_section += f"- [{post['title']}]({post['link']}) {post['timestamp']}\n"

with open("README.md", "r") as readme:
    readme_content = readme.read()

pattern = re.compile(r"<h2>Blog Posts<\/h2>\n[\s\S]*?(?=!)(?:1|\s){0,2}\n", re.MULTILINE)
readme_content = re.sub(pattern, new_section + "\n", readme_content)

with open("README.md", "w") as readme:
    readme.write(readme_content)
