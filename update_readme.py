import json

# README.md 파일을 업데이트하는 함수
def update_readme(posts):
    with open("README_template.md", "r") as template:
        template_content = template.read()

    # 포스트 목록을 기반으로 새 섹션 생성
    new_section = ''.join([f"- [{post['title']}]({post['link']})\n" for post in posts])
    readme_content = template_content.replace("{blog_posts}", new_section)

    # 변경된 내용으로 README.md 파일 작성
    with open("README.md", "w") as readme:
        readme.write(readme_content)
    print(f"README.md 업데이트 성공!")

if __name__ == "__main__":
    with open("output.json", "r") as json_file:
        sample_output_data = json.load(json_file)
    update_readme(sample_output_data)
