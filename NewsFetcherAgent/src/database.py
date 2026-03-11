import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

import os

def get_connection():
    """ returns a connection to the sqlite db"""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "poltheo-news-fetcher.db")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # dictiory-like row structure

    return conn



def init_db():
    """creates articles table if one doesnt exist or so """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    content TEXT,
    published_at TEXT,
    fetched_at TEXT NOT NULL,
    category TEXT 
    )
    """
    )

    conn.commit()
    conn.close()
    logger.info("Database init")


def article_exists(url : str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def insert_article(source: str, title: str, url: str, content: str, published_at : str, category : str):
    """inserts a new article into the database. Skips if url already exists"""
    if article_exists(url):
        logger.debug(f"Duplicate skipped {title[:60]}")
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    INSERT INTO articles(source, title, url, content, published_at, fetched_at, category)
    VALUES (?,?,?,?,?,?,?)
    """,
    (source,
     title,
     url,
     content,
     published_at,
     datetime.utcnow().isoformat(),
     category)
    )
    
    conn.commit()
    conn.close()
    logger.info(f"Saved: [{category.upper()}] {title[:70]}")
    
    return True

def get_recent_articles(limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source, title, url, category, fetched_at
        FROM articles
        ORDER BY fetched_at DESC
        LIMIT ?
    """ ,(limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows



def get_article_count():
    """Returns total number of articles stored."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles")
    count = cursor.fetchone()[0]
    conn.close()
    return count


    
    
    
    