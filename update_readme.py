import json
from pathlib import Path

# README.md 파일을 업데이트하는 함수
def update_readme(posts):
    template_path = Path("README_template.md")
    readme_path = Path("README.md")
    try:
        with template_path.open("r") as template_file:
            template_content = template_file.read()

        # 포스트 목록을 기반으로 새 섹션 생성
        new_section = ''.join([f"- [{post['title']}]({post['link']})\n" for post in posts])
        readme_content = template_content.replace("{blog_posts}", new_section)

        # 변경된 내용으로 README.md 파일 작성
        with readme_path.open("w") as readme_file:
            readme_file.write(readme_content)
        print(f"{readme_path} 업데이트 성공!")
    except Exception as e:
        print(f"{readme_path} 업데이트 동안 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    output_path = Path("output.json")
    try:
        with output_path.open("r") as json_file:
            sample_output_data = json.load(json_file)
        update_readme(sample_output_data)
    except Exception as e:
        print(f"{output_path} 읽기 동안 오류가 발생했습니다: {e}")
