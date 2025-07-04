import json
import os
import requests
from bs4 import BeautifulSoup
from app.config import Config
import logging

class QAScraper:
    def __init__(self):
        self.headers = Config.HEADERS

    def fetch_html(self, url):
        try:
            res = requests.get(url, headers=self.headers)
            if res.status_code == 200:
                return res.text
            else:
                logging.warning(f"[!] Failed to fetch: {url} (status {res.status_code})")
                return None
        except Exception as e:
            logging.error(f"[!] Request error on {url}: {e}")
            return None

    def parse_page(self, url):
        html = self.fetch_html(url)
        if not html:
            return None

        try:
            soup = BeautifulSoup(html, "lxml")
            q_card = soup.find("div", class_="card p-3 bg-question shadow-sm rounded")
            q_body = q_card.find("div", class_="card-body").get_text(separator="\n", strip=True)

            answers = []
            answer_cards = soup.find_all("div", class_="card-body")
            for card in answer_cards:
                section = card.find("div", class_="media")
                if section:
                    paragraphs = section.find_all("p")
                    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
                    if text:
                        answers.append(text)

            return {
                "url": url,
                "question_body": q_body,
                "answers": answers
            }

        except Exception as e:
            logging.error(f"[!] Parsing failed on {url}: {e}")
            return None

    def parse_all(self, input_file=Config.LINK_OUTPUT_FILE, output_file=Config.JSON_OUTPUT_FILE):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(input_file, encoding="utf-8") as f:
            links = [l.strip() for l in f if l.strip()]

        results = []
        for i, url in enumerate(links, 1):
            logging.info(f"[{i}/{len(links)}] Parsing: {url}")
            data = self.parse_page(url)
            if data:
                results.append(data)

            if i % 200 == 0:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                logging.info(f"[✓] Auto-saved at {i} entries")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        logging.info(f"\n[✓] Done! Parsed {len(results)} Q&A items.")
