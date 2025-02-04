import requests
from bs4 import BeautifulSoup
import json
import os
import random
from pathlib import Path

def is_absolute(url):
    return bool(requests.utils.urlparse(url).netloc)

def get_random_blog_posts(url, css_selector):
    output_data = []

    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.select(css_selector)
        all_links = []

        for article in articles:
            links = article.find_all("a")
            all_links.extend(links)

        selected_links = random.sample(all_links, min(3, len(all_links)))

        for link in selected_links:
            # Get the title
            title_element = link.select_one("div.notion-collection-card-body > div:nth-child(1) > span > span > span > span")
            title = title_element.text.strip() if title_element else ""

            # Get the summary
            summary_element = link.select_one("div.notion-collection-card-body > div:nth-child(2)")
            summary = summary_element.text.strip() if summary_element else ""

            # Get the date
            date_element = link.select_one("div.notion-collection-card-body > div:nth-child(3)")
            
            if date_element and '202' in date_element.text:
                index_202 = date_element.text.index('202')
                date_text= date_element.text[:index_202]
            
                href=link["href"]
                
                if not is_absolute(href):
                    href=url.rstrip("/") + href.lstrip(".")
                
                post_data={
                    "title":title,
                    "summary":summary,
                    "date":date_text,
                    "url":href,
                }
                
                output_data.append(post_data)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error while scraping {url}: {e}")

    return output_data

def save_output_to_json(posts_data, output_file):
    """포스트 데이터를 JSON 파일로 저장합니다."""
    output_path = Path(output_file)
    try:
        with output_path.open("w", encoding='utf-8') as json_file:
            json.dump(posts_data, json_file, ensure_ascii=False, indent=2)
        print(f"{output_path}에 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"{output_path}에 저장하는 동안 오류가 발생했습니다: {e}")
    return str(output_path)

def get_user_posts(user_id):
    """특정 Qiita 유저의 포스트 목록을 가져옵니다."""
    base_url = f"https://qiita.com/api/v2/users/{user_id}/items"
    headers = {
        'Accept': 'application/json',
    }

    qiita_token = os.environ.get('QIITA_TOKEN')
    if qiita_token:
        headers['Authorization'] = f'Bearer {qiita_token}'
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        posts = response.json()
        
        # 포스트 정보 정리
        posts_data = []
        for post in posts:
            post_info = {
                'title': post['title'],
                'url': post['url'],
                'created_at': post['created_at'],
                'likes_count': post['likes_count'],
                'tags': [tag['name'] for tag in post['tags']]
            }
            posts_data.append(post_info)
            
        return posts_data
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return []

def main():
    user_id = "gammjya"
    output_file = "output.json"
    
    # Qiita 포스트 가져오기
    posts = get_user_posts(user_id)
    
    if posts:
        # 최신 3개의 포스트만 선택
        recent_posts = posts[:3]
        
        # JSON 파일로 저장
        save_output_to_json(recent_posts, output_file)
        
        print(f"\n{user_id}의 최신 포스트 목록:")
        for i, post in enumerate(recent_posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   URL: {post['url']}")
            print(f"   작성일: {post['created_at']}")
            print(f"   좋아요: {post['likes_count']}")
            print(f"   태그: {', '.join(post['tags'])}")

if __name__ == "__main__":
    main()
