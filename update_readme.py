import json

with open("output.json", "r") as json_file:
    post_data = json.load(json_file)

new_section = "<h2>Blog Posts</h2>\n\n"
for post in post_data:
    new_section += f"- [{post['title']}]({post['link']})\n"

split_readme = open("README.md").read().split("<h2>Blog Posts</h2>")
before_blog_posts = split_readme[0]
after_blog_posts = "".join(split_readme[1:])

with open("README.md", "w") as readme:
    readme.write(before_blog_posts + new_section + after_blog_posts)
