def update_readme(posts):
    with open("README_template.md", "r") as template:
        template_content = template.read()

    new_section = ''.join([f"- [{post['title']}]({post['link']}) {post['timestamp']}\n" for post in posts])
    readme_content = template_content.replace("{blog_posts}", new_section)

    with open("README.md", "w") as readme:
        readme.write(readme_content)
    print(f"README.md 업데이트 성공!")

update_readme(sample_output_data)
