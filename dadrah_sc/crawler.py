import requests
from bs4 import BeautifulSoup
import os

def extract_question_links(start_page, end_page):
    base_url = "https://www.dadrah.ir/consulting-catalog.php?page="
    all_links = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for page_num in range(start_page, end_page + 1):
        url = base_url + str(page_num)
        print(f"Scraping page {page_num} -> {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[!] Failed to load page {page_num}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        questions = soup.find_all("div", id="consults-content")

        for q in questions:
            link_tag = q.find("a", href=True)
            if link_tag:
                relative_link = link_tag["href"]
                full_link = f"https://www.dadrah.ir/{relative_link}"
                all_links.append(full_link)

    return all_links

def save_links_to_file(links, filename="data/linkes_first.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    print(f"[✓] Saved {len(links)} links to {filename}")

if __name__ == "__main__":
    try:
        start = int(input("Start page number: "))
        end = int(input("End page number: "))
        links = extract_question_links(start, end)
        save_links_to_file(links)
    except Exception as e:
        print(f"[!] Error: {e}")
