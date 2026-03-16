# Agent Projects

Building toward an autonomous AI agent that reads theology and politics, forms its own ideologies, and posts them to Instagram.

This repo documents the build — each mini project teaches one core skill.

---

##  Project 1 — News Fetcher Agent
`NewsFetcherAgent/`

Pulls articles from theology and politics sources via RSS feeds and NewsAPI. Cleans the text and stores everything in a local SQLite database on a timed schedule.

```bash
cd NewsFetcherAgent
source venv/bin/activate
python main.py --once    # fetch articles
python main.py --view    # see what was stored
```

---

##  Project 2 — Tagger Agent
`TaggerAgent/`

Reads the stored articles and sends them to Claude to extract themes, ideological lean, theological tradition, and emotional tone. Writes the results back into the same database.

```bash
cd TaggerAgent
source venv/bin/activate
python main.py           # tag all articles
python main.py --view    # inspect results
```

> Run NewsFetcherAgent first to populate the database.

---

## Project 3 — Memory Agent
`MemoryAgent/`

Converts tagged articles into vector embeddings and stores them in a local Chroma database. Enables semantic search — find relevant articles by concept rather than keyword. Also maintains a separate collection for the agent's own generated thoughts, ready for the Synthesis Agent.

```bash
cd MemoryAgent
source venv/bin/activate
python main.py           # index all tagged articles into Chroma
python main.py --search  # interactive semantic search
python main.py --stats   # see how many vectors are stored
```

> Run TaggerAgent first to populate tagged articles.

---

## Coming Next

| # | Project | Skill |
|---|---------|-------|
| 4 | Synthesis Agent | Multi-step LLM chaining + persona engineering |
| 5 | Image Pipeline | Image generation + visual templating |
| 6 | Publisher | Streamlit dashboard + Instagram API |
