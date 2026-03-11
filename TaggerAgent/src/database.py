
"""
The Tagger Agent doesn't have its own database. It borrows the FetcherAgent's database.
It reaches across into FetcherAgent's SQLite file, reads articles that haven't been tagged yet, sends them to Claude, then writes the results back into the same file.
So the database.py here has two jobs — reading untagged articles and writing tags back.
"""

import sqlite3
import logging
import os


logger = logging.getLogger(__name__)

#path to fetchers database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEO_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(THEO_DIR, "NewsFetcherAgent" ,"poltheo-news-fetcher.db")

def get_connection():
    """returns a connection to thte sqlite db"""

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_tags_columns():

    """
    adds tagging columns to the articles table if they dont exist yet
    can run multiple times
    """

    conn = get_connection()
    cursor = conn.cursor()

    #each col is added seperately so if one alr exists it doesnt crash

    columns_to_add = [
        ("summary" , "TEXT"),
        ("themes" , "TEXT"),
        ("idealogical_lean" , "TEXT"),
        ("emotional_tone" , "TEXT"),
        ("tagged", "INTEGER DEFAULT 0"),
        #0 if untagged and 1 if tagged   
    ]

    for col_name, col_type, in columns_to_add:
        
        try:
            cursor.execute(f"ALTER TABLE articles ADD COLUMN {col_name} {col_type}")
            logger.info(f"added column : {col_name}")
        except sqlite3.OperationalError:
            # col alr exists, skip
            pass

    conn.commit()
    conn.close()
    logger.info(" tage cols ready")


def get_untagged_articles(limit: int = 10):
    """
    returns articles that havent been tagged yet, priotises articles that have content to analyze
    """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, source, title, content, category
    FROM articles
    WHERE (tagged = 0 OR tagged IS NULL)
    AND content IS NOT NULL
    AND content != '' 
    ORDER BY fetched_at DESC
    LIMIT ?
""", (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def save_tags(article_id: int, summary: str, themes: list,
              ideological_lean: str, theological_tradition: str,
              emotional_tone: str):
    """ writes the structured tags back to the articles row """

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE articles
        SET summary = ?,
            themes = ?,
            ideological_lean = ?,
            theological_tradition = ?,
            emotional_tone = ?,
            tagged = 1
        WHERE id = ?               
    """,(
        summary,
        ", ".join(themes),
        ideological_lean,
        theological_tradition,
        emotional_tone,
        article_id  

    #The ", ".join(themes) converts a Python list like ["power", "faith", "justice"] into a single string "power, faith, justice" 
    #because SQLite can't store a Python list directly.

    ))
    conn.commit()
    conn.close()


def get_tagged_count():
    """returns how many articles have been tagged"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE tagged = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_untagged_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE tagged = 0 OR tagged IS NULL")
    count = cursor.fetchone()[0]
    conn.close()
    return count 


def get_recent_tagged(limit : int = 10 ):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, source, title, category, summary, themes, ideological_lean, theological_tradition, emotional_tone
        FROM articles
        WHERE tagged = 1
        ORDER BY id DESC
        LIMIT ?
""", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows 





    