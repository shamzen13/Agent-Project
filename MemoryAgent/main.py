"""
main.py
Entry point for the Memory Agent.

Usage:
    python main.py              → indexes all tagged articles into Chroma
    python main.py --search     → interactive semantic search mode
    python main.py --stats      → shows collection counts
"""

import sys
import logging
from src.indexer import run_indexing_cycle
from src.searcher import search_memory, format_search_results
from src.vector_store import get_collection_counts

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/memory.log"),
    ]
)

logger = logging.getLogger(__name__)


def interactive_search():
    """
    Runs an interactive search loop in the terminal.
    Type a concept and see the most semantically relevant articles returned.
    Type 'quit' to exit.
    """
    print("\n" + "="*60)
    print("  MEMORY AGENT — SEMANTIC SEARCH")
    print("  Type a concept to search. Type 'quit' to exit.")
    print("="*60 + "\n")

    while True:
        query = input("  Search: ").strip()

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            print("  Exiting search.")
            break

        #category filter optional
        category = None
        if query.startswith("theology:"):
            category = "theology"
            query = query.replace("theology:", "").strip()
        elif query.startswith("politics:"):
            category = "politics"
            query = query.replace("politics:", "").strip()

        results = search_memory(query, n_articles=5, n_thoughts=3, category_filter=category)
        print(format_search_results(results))


def show_stats():
    counts = get_collection_counts()
    print(f"\n{'='*40}")
    print(f"  MEMORY STATS")
    print(f"{'='*40}")
    print(f"  Articles in Chroma:  {counts['articles']}")
    print(f"  Thoughts in Chroma:  {counts['thoughts']}")
    print(f"{'='*40}\n")


def main():
    args = sys.argv[1:]

    if "--search" in args:
        interactive_search()

    elif "--stats" in args:
        show_stats()

    else:
        logger.info("startning Memory Agent — indexing articles...")
        run_indexing_cycle()
        logger.info("Done. Run with --search to query memory.")
        logger.info("Run with --stats to see collection counts.")


if __name__ == "__main__":
    main()