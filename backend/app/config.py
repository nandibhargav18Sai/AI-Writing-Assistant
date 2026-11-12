import os

from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


ENV_FILE = BASE_DIR / ".env"


load_dotenv(
    ENV_FILE
)


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

NOTION_TOKEN = os.getenv(
    "NOTION_TOKEN"
)

NOTION_PAGE_ID = os.getenv(
    "NOTION_PAGE_ID"
)

API_KEY = os.getenv(
    "API_KEY"
)


if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is missing in .env file"
    )