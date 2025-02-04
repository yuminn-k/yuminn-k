import json
from pathlib import Path
from datetime import datetime

def format_post(post):
    """Qiita 포스트를 마크다운 형식으로 포맷팅합니다."""
    title = post.get("title", "제목 없음")
    url = post.get("url", "#")
    created_at = post.get("created_at", "")
    
    try:
        # ISO 형식의 날짜를 더 읽기 쉬운 형식으로 변환
        if created_at:
            date = datetime.fromisoformat(created_at.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        else:
            date = "날짜 없음"
    except (ValueError, AttributeError):
        date = "날짜 형식 오류"
        
    return f"- [{title}]({url}) - {date}  "

def update_readme(posts):
    """README.md 파일을 업데이트합니다."""
    template_path = Path("README_template.md")
    readme_path = Path("README.md")
    try:
        template_content = template_path.read_text(encoding='utf-8')
        
        # 포스트가 없는 경우 기본 메시지 표시
        if not posts:
            formatted_posts = "아직 작성된 포스트가 없습니다."
        else:
            # 포스트 목록을 마크다운 형식으로 변환
            formatted_posts = []
            for post in posts:
                title = post.get('title', '제목 없음')
                url = post.get('url', '#')
                created_at = post.get('created_at', '')
                
                try:
                    if created_at:
                        date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    else:
                        date = "날짜 없음"
                except (ValueError, AttributeError):
                    date = "날짜 형식 오류"
                
                formatted_post = f"- [{title}]({url}) - {date}"
                formatted_posts.append(formatted_post)
            
            formatted_posts = '\n'.join(formatted_posts)
        
        # 템플릿의 {posts} 부분을 포맷팅된 포스트로 교체
        updated_content = template_content.replace("{posts}", formatted_posts)
        
        # 새로운 README.md 파일 작성
        with readme_path.open("w", encoding='utf-8') as readme_file:
            readme_file.write(updated_content)
            
        print("README.md 업데이트 성공!")
    except Exception as e:
        print(f"README.md 업데이트 도중 오류가 발생했습니다: {e}")
        raise

def main():
    output_file = "output.json"

    try:
        with open(output_file, encoding='utf-8') as json_file:
            posts = json.load(json_file)
        update_readme(posts)
    except Exception as e:
        print(f"JSON 파일 처리 중 오류가 발생했습니다: {e}")
        raise

if __name__ == "__main__":
    main()
