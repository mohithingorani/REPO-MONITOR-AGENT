import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json",
}

REQUEST_TIMEOUT = 10
