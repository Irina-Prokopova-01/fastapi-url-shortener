import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URL_STORAGE_FILEPATH = BASE_DIR / "short-url.json"

# C:\Users\User\PycharmProjects\fastapi-url-shortener\url-shortener\core\config.py
LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real token here! Only fake values

API_TOKENS: frozenset[str] = frozenset(
    {
        "Ykn4HsTExNoSwPAmwEt-3Q",
        "rrSpMES6ozOvoxQKTTGc8g",
    }
)
