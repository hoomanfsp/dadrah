import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    START_PAGE = int(os.getenv("START_PAGE", 1))
    END_PAGE = int(os.getenv("END_PAGE", 2))
    BASE_URL = os.getenv("BASE_URL", "https://www.dadrah.ir/consulting-catalog.php?page=")
    LINK_OUTPUT_FILE = os.getenv("LINK_OUTPUT_FILE", "data/linkes_first.txt")
    JSON_OUTPUT_FILE = os.getenv("JSON_OUTPUT_FILE", "data/output.json")
    HEADERS = {
        "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0")
    }
