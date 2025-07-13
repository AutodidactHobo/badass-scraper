# Badass Scraper
Turn high-signal feeds into strategic summaries - fast, local, and LLM-enhanced.

## What it does
- Scrapes curated feeds like Substack, EA Observatory, Strat, etc.
- Extracts content and enriches it with semantic tags
- Builds a strategic writing prompt (skeptical tone, structured)
- Generates a draft article via local LLM (Mistral)

## Why it matters
- No API keys or vendor lock-in
- Real writing quality - not chatbot fluff
- Extensible, clean Python - great for learning or production
- Curated to extract signal from noise

## How to run

```bash
git clone badass-scraper
cd badass-scraper
pip install -r requirements.txt
playwright install
python badass_scraper.py
