# extract_content.py
# Phase 2: Extract main content, paragraphs, headline from article URL

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from utils.file_ops import normalize_text

def extract_and_structure(article):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(article['url'], timeout=20000)
            soup = BeautifulSoup(page.content(), 'html.parser')
            paras = [normalize_text(p.get_text()) for p in soup.find_all('p') if len(p.get_text().strip()) > 50]
            article['paragraphs'] = list(dict.fromkeys(paras))[:30]  # Dedup and cap
        except Exception as e:
            article['paragraphs'] = []
            article['error'] = str(e)
        finally:
            browser.close()
    return article
