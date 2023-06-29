import json

with open("output.json", "r") as json_file:
    post_data = json.load(json_file)

new_section = "<h2>Blog Posts</h2>\n"
for post in post_data:
    new_section += f"- [{post['title']}]({post['link']})\n"

with open("README.md", "r") as readme:
    readme_content = readme.read()

readme_content = readme_content.split("<h2>Blog Posts</h2>")[0] + \
                 new_section + \
                 "".join(readme_content.split("<h2>Blog Posts</h2>")[1:])

with open("README.md", "w") as readme:
    readme.write(readme_content)
