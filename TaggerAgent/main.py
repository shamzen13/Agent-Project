"""
main.py
Entry point for the Tagger Agent.

Usage:
    python main.py          → tags all untagged articles
    python main.py --view   → prints recently tagged articles
    python main.py --stats  → shows tagging stats
"""

import sys
import logging
from src.database import add_tags_columns, get_recent_tagged, get_tagged_count, get_untagged_count
from src.processor import run_tagging_cycle

#logigng setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/tagger.log"),
    ]
)

logger = logging.getLogger(__name__)


def view_tagged():
    """pretty prints recently tagged articles."""
    articles = get_recent_tagged(limit=10)

    print(f"\n{'='*60}")
    print(f"  RECENTLY TAGGED ARTICLES")
    print(f"{'='*60}\n")

    if not articles:
        print("  No tagged articles yet. Run python main.py first.")
        return

    for a in articles:
        print(f"  [{a['category'].upper()}] {a['title'][:65]}")
        print(f"  Summary:    {a['summary'][:120]}")
        print(f"  Themes:     {a['themes']}")
        print(f"  Lean:       {a['ideological_lean']}")
        print(f"  Tradition:  {a['theological_tradition']}")
        print(f"  Tone:       {a['emotional_tone']}")
        print()


def show_stats():
    """Prints tagging progress stats."""
    tagged = get_tagged_count()
    untagged = get_untagged_count()
    total = tagged + untagged

    print(f"\n{'='*40}")
    print(f"  TAGGING STATS")
    print(f"{'='*40}")
    print(f"  Tagged:    {tagged} / {total}")
    print(f"  Remaining: {untagged}")
    print(f"{'='*40}\n")


def main():
    args = sys.argv[1:]

    
    add_tags_columns()

    if "--view" in args:
        view_tagged()

    elif "--stats" in args:
        show_stats()

    else:
        logger.info("Starting Tagger Agent...")
        run_tagging_cycle()
        logger.info("Run with --view to inspect results.")


if __name__ == "__main__":
    main()