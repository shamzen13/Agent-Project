#reads tagged articles from the tagger agent database -READ ONLY



import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEO_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(THEO_DIR, "NewsFetcherAgent", "poltheo-news-fetcher.db")

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"db not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_tagged_articles(limit: int = 500) -> list:
    #articles ready to be embedded into vector store

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id,source,title,summary,themes,idealogical_lean,theological_tradition,emotional_tone,category
        FROM articles
        WHERE tagged = 1
        AND summary IS NOT NULL
        AND themes IS NOT NULL
        ORDER BY fetched_at DESC
        LIMIT ?    
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    logger.info(f"fetched {len(rows)} tagged artucles from sql db")
    return rows


def get_tagged_count() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE tagged = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count 



