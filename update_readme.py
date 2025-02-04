import json
from pathlib import Path
from datetime import datetime

def format_post(post):
    """Qiita 포스트를 마크다운 형식으로 포맷팅합니다."""
    title = post["title"]
    url = post["url"]
    # ISO 형식의 날짜를 더 읽기 쉬운 형식으로 변환
    date = datetime.fromisoformat(post["created_at"].replace("Z", "+00:00")).strftime("%Y-%m-%d")
    return f"- [{title}]({url}) - {date}  "

def update_readme(posts):
    """README.md 파일을 업데이트합니다."""
    template_path = Path("README_template.md")
    readme_path = Path("README.md")
    try:
        template_content = template_path.read_text(encoding='utf-8')
        formatted_posts = '\n'.join(format_post(post) for post in posts)
        with readme_path.open("w", encoding='utf-8') as readme_file:
            readme_file.write(template_content.format(posts=formatted_posts))
        print("README.md 업데이트 성공!")
    except Exception as e:
        print(f"README.md 업데이트 도중 오류가 발생했습니다: {e}")

def main():
    output_file = "output.json"

    try:
        with open(output_file, encoding='utf-8') as json_file:
            posts = json.load(json_file)
        update_readme(posts)
    except Exception as e:
        print(f"JSON 파일 처리 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
