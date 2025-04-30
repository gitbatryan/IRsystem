import os
import requests
from bs4 import BeautifulSoup

# 저장할 폴더
save_folder = "saved_texts"
os.makedirs(save_folder, exist_ok=True)

# 실패한 URL을 저장할 파일
failed_urls_file = "failed_urls.txt"

# 메인 heritage 리스트 페이지
main_url = "https://whc.unesco.org/en/list/"

# 메인 페이지 요청
response = requests.get(main_url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 모든 heritage 링크 수집
heritage_links = []
for a_tag in soup.find_all("a", href=True):
    href = a_tag['href']
    if href.startswith("/en/list/") and href.count('/') == 3:
        full_url = "https://whc.unesco.org" + href
        heritage_links.append(full_url)

# 중복 제거 + 정렬
heritage_links = sorted(set(heritage_links))

# 이미 저장된 파일 리스트
existing_files = set(os.listdir(save_folder))

print(f"전체 heritage 수: {len(heritage_links)}")
print(f"이미 저장된 파일 수: {len(existing_files)}")

# heritage 하나하나 방문
for url in heritage_links:
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        page_soup = BeautifulSoup(res.text, "html.parser")

        # 제목
        title_tag = page_soup.find("h1")
        if not title_tag:
            print(f"Cannot find title for {url}")
            with open(failed_urls_file, "a", encoding="utf-8") as f:
                f.write(f"{url}\n")
            continue
        title = title_tag.text.strip()

        # 파일명 만들기
        safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip() + ".txt"

        # 이미 저장된 파일이면 스킵
        if safe_title in existing_files:
            print(f"⏩ 이미 저장된 파일: {safe_title}, 스킵")
            continue

        # 나라 정보
        country = "Unknown"
        country_tag = page_soup.select_one("a.d-block strong")
        if country_tag:
            country = country_tag.text.strip()

        # Outstanding Universal Value 찾기
        ouv_heading = page_soup.find(lambda tag: tag.name in ["h2", "h3"] and "Outstanding Universal Value" in tag.text)
        if not ouv_heading:
            print(f"No Outstanding Universal Value section found for {url}")
            with open(failed_urls_file, "a", encoding="utf-8") as f:
                f.write(f"{url}\n")
            continue

        # 본문 수집
        content = []
        for sibling in ouv_heading.find_next_siblings():
            if sibling.name in ["h2", "h3"]:
                break
            if sibling.name in ["p", "div"]:
                text = sibling.get_text(separator="\n", strip=True)
                if text:
                    content.append(text)
        full_text = "\n\n".join(content)

        # 저장
        file_path = os.path.join(save_folder, safe_title)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"country : {country}\n\n")
            f.write(full_text)

        print(f"✅ Saved: {file_path}")

    except Exception as e:
        print(f"❌ Error at {url}: {e}")
        with open(failed_urls_file, "a", encoding="utf-8") as f:
            f.write(f"{url}\n")

print("\n✅ 크롤링 완료.")
