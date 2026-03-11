"""
config.py
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "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")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set. Add it to your .env file.")