"""
config.py
Loads environment variables from .env file.
All API keys and settings live here.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads from .env file in root directory

# ── API Keys ──────────────────────────────────
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "7b88fd53e1134ebbba0a53649553e740")   # get free key at newsapi.org

# ── Scheduler Settings ────────────────────────
FETCH_INTERVAL_HOURS = int(os.getenv("FETCH_INTERVAL_HOURS", "4"))

# ── Database ──────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "news_fetcher.db")
