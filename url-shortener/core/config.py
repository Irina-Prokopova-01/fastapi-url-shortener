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

# API_TOKENS: frozenset[str] = frozenset(
#     {
#         "jhfdgkhkthuehfkjdbfjv",
#         "rrSpMES6ozOvoxQKTTGc8g",
#     }
# )

# Only for demo!
# no real ustrs in code!!
USERS_DB: dict[str, str] = {
    "sam": "passw",
    "bob": "pass",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_DB_TOKENS = 1

REDIS_TOKENS_SET_NAME = "tokens"
