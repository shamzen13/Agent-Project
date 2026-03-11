# Agent Projects

Building toward an autonomous AI agent that reads theology and politics, forms its own ideologies, and posts them to Instagram (this feature might not apply since its not cost effective but the code should work once paid for)

This repo documents the build — each mini project teaches one core skill.

---

## Mini Project 1 — News Fetcher Agent
`NewsFetcherAgent/`

Pulls articles from theology and politics sources via RSS feeds and NewsAPI. Cleans the text and stores everything in a local SQLite database on a timed schedule.

```bash
cd NewsFetcherAgent
source venv/bin/activate
python main.py --once    # fetch articles
python main.py --view    # see what was stored
```

---

## Mini Project 2 — Tagger Agent
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

## Coming Next

| # | Project | Skill |
|---|---------|-------|
| 3 | Memory Agent | Vector databases + semantic search |
| 4 | Synthesis Agent | Multi-step LLM chaining + persona |
| 5 | Image Pipeline | Image generation + visual templating |
| 6 | Publisher | Streamlit dashboard + Instagram API |
