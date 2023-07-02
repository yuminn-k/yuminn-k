import json
import re

with open("output.json", "r") as json_file:
    post_data = json.load(json_file)

new_section = "<h2>Blog Posts</h2>\n\n" + ''.join([f"- [{post['title']}]({post['link']}) {post['timestamp']}\n" for post in post_data])

with open("README.md", "r") as readme:
    readme_content = readme.read()

pattern = re.compile(r"<h2>Blog\sPosts<\/h2>[^\#\-\r\n]*(?:\r?\n-.*?)*(?=\r?\n\#)", re.MULTILINE | re.DOTALL)
readme_content = re.sub(pattern, new_section, readme_content)

with open("README.md", "w") as readme:
    readme.write(readme_content)
print(f"README.md 업데이트 성공!")
