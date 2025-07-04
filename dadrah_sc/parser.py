import json
import os
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[!] Failed to fetch: {url} (status {response.status_code})")
            return None
    except Exception as e:
        print(f"[!] Request error on {url}: {e}")
        return None

def parse_page(url):
    html = fetch_html(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    try:
        q_card = soup.find("div", class_="card p-3 bg-question shadow-sm rounded")
        q_body = q_card.find("div", class_="card-body").get_text(separator="\n", strip=True)

        answer_cards = soup.find_all("div", class_="card-body")
        #print(answer_cards)
        answers = []

        for card in answer_cards:
            section = card.find("div", class_="media")
            if section:
                paragraphs = section.find_all("p")
                text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                if text:
                    answers.append(text)

        return {
            "question_body": q_body,
            "answers": answers
        }

    except Exception as e:
        print(f"[!] Parsing failed on: {url} - {e}")
        return None


def parse_all_links(input_file="data/linkes_first.txt", output_file="data/output.json"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, encoding="utf-8") as f:
        links = [l.strip() for l in f if l.strip()]

    results = []
    for i, url in enumerate(links, 1):
        print(f"[{i}/{len(links)}] Parsing: {url}")
        data = parse_page(url)
        if data:
            results.append(data)

        # Save every 200 entries
        if i % 50 == 0 :
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f" Auto-saved at {i} entries")

    # Final save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n Done! Parsed {len(results)} Q&A items and saved to {output_file}")

if __name__ == "__main__":
    parse_all_links()
