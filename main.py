import logging
from app.link_extractor import LinkExtractor
from app.qa_scraper import QAScraper
from app.config import Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    le = LinkExtractor()
    scraper = QAScraper()

    links = le.extract_links(Config.START_PAGE, Config.END_PAGE)
    le.save_links(links)

    scraper.parse_all()
