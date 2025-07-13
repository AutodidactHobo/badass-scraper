# orchestrator.py
# Entry point for recursive scraping, parsing, enrichment, prompting, and generation

import os
from scripts.scrape_sources import collect_article_links
from scripts.extract_content import extract_and_structure
from scripts.enrich_semantics import enrich_article
from scripts.build_prompt import format_prompt
from scripts.generate_article import generate_and_save_article
from utils.logging_utils import init_logger

logger = init_logger()

RAW_DIR = "data/raw"
STRUCTURED_DIR = "data/structured"
ENRICHED_DIR = "data/enriched"
PROMPTS_DIR = "data/prompts"
OUTPUT_DIR = "output/FOR AUDIT"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(STRUCTURED_DIR, exist_ok=True)
os.makedirs(ENRICHED_DIR, exist_ok=True)
os.makedirs(PROMPTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_pipeline():
    logger.info("PHASE 1 — Scraping article links")
    articles = collect_article_links()

    for article in articles:
        try:
            logger.info(f"PHASE 2 — Extracting: {article['title'][:80]}...")
            structured = extract_and_structure(article)
            if not structured or len(structured.get("paragraphs", [])) < 3:
                logger.warning("Insufficient content. Skipping.")
                continue

            logger.info("PHASE 3 — Enriching with semantics")
            enriched = enrich_article(structured)

            logger.info("PHASE 4 — Building prompt")
            prompt_text = format_prompt(enriched)

            logger.info("PHASE 5 — Generating and saving article")
            generate_and_save_article(prompt_text, enriched, OUTPUT_DIR)

        except Exception as e:
            logger.error(f"FAILED on article: {article.get('title')} — {e}")

if __name__ == "__main__":
    run_pipeline()
