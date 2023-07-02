import json
import re

with open("output.json", "r") as json_file:
    post_data = json.load(json_file)

new_section = "<h2>Blog Posts</h2>\n\n" + ''.join([f"- [{post['title']}]({post['link']}) {post['timestamp']}\n" for post in post_data])

with open("README.md", "r") as readme:
    readme_content = readme.read()

pattern = re.compile(r"(?<=<h2>Blog\sPosts<\/h2>)(\r?\n)([^\r^\n]*(\r?\n)*)", re.MULTILINE)
readme_content, result = re.subn(pattern, f"\\1{new_section}\n", readme_content)

if not result:
    readme_content = f"{new_section}\n{readme_content}\n"

with open("README.md", "w") as readme:
    readme.write(readme_content)
print(f"README.md 업데이트 성공!")
