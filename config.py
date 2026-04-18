import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY_HERE")
ADMIN_ID = 507453159
DATABASE_PATH = "faceup.db"

SERVICES = {
    "first": {"name": "Перший візит", "duration": 90, "price": 1000},
    "repeat": {"name": "Повторний візит", "duration": 60, "price": 1000},
}
