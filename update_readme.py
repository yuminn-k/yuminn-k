import json
from pathlib import Path

# README.md 파일을 업데이트하는 함수
def update_readme(posts):
    template_path = Path("README_template.md")
    readme_path = Path("README.md")
    try:
        template_content = template_path.read_text()

        # 출력 데이터를 템플릿에 적용하여 README.md 파일 생성
        with readme_path.open("w") as readme_file:
            readme_file.write(template_content.format(posts=json.dumps(posts, indent=4)))
        print("README.md 업데이트 성공!")
    except Exception as e:
        print(f"README.md 업데이트 도중 오류가 발생했습니다: {e}")

def main():
    output_file = "output.json"

    # JSON 파일에서 데이터 읽기
    with open(output_file) as json_file:
        data = json.load(json_file)

    # README.md 파일 업데이트
    update_readme(data)

if __name__ == "__main__":
    main()
