import requests
from bs4 import BeautifulSoup
import os
from app.config import Config
import logging

class LinkExtractor:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.HEADERS

    def extract_links(self, start, end):
        all_links = []

        for page_num in range(start, end + 1):
            url = f"{self.base_url}{page_num}"
            logging.info(f"Scraping page {page_num} -> {url}")
            try:
                res = requests.get(url, headers=self.headers)
                if res.status_code != 200:
                    logging.warning(f"[!] Failed to load page {page_num}")
                    continue

                soup = BeautifulSoup(res.text, "html.parser")
                questions = soup.find_all("div", id="consults-content")

                for q in questions:
                    link_tag = q.find("a", href=True)
                    if link_tag:
                        relative_link = link_tag["href"]
                        full_link = f"https://www.dadrah.ir/{relative_link}"
                        all_links.append(full_link)

            except Exception as e:
                logging.error(f"[!] Error fetching page {page_num}: {e}")

        return all_links

    def save_links(self, links, filename=Config.LINK_OUTPUT_FILE):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            for link in links:
                f.write(link + "\n")
        logging.info(f"[✓] Saved {len(links)} links to {filename}")
