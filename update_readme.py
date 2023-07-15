import json
from pathlib import Path

def format_post(post):
    title = post["title"]
    url = post["url"]
    return f"- [{title}]({url})"

def update_readme(posts):
    template_path = Path("README_template.md")
    readme_path = Path("README.md")
    try:
        template_content = template_path.read_text()

        # 포스트 데이터를 원하는 형식으로 변환합니다.
        formatted_posts = '\n'.join(format_post(post) for post in posts)

        # 출력 데이터를 템플릿에 적용하여 README.md 파일 생성
        with readme_path.open("w") as readme_file:
            readme_file.write(template_content.format(posts=formatted_posts))
        print("README.md 업데이트 성공!")
    except Exception as e:
        print(f"README.md 업데이트 도중 오류가 발생했습니다 확인하세요: {e}")

def main():
    output_file = "output.json"

    # JSON 파일에서 데이터 읽기
    with open(output_file) as json_file:
        data = json.load(json_file)

    # README.md 파일 업데이트
    update_readme(data)

if __name__ == "__main__":
    main()
