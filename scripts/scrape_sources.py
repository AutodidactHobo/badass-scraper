# scrape_sources.py
# Phase 1: Scrape index pages for article links and titles

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import logging

ACTIVE_SOURCES = [
https://chinai.substack.com/",
https://stratechery.com/",
https://neil.substack.com/",
https://eaobservatory.substack.com/",
https://every.to/",
https://read.substack.com/",
https://ai.readmultiplex.com/",
https://www.justsecurity.org/recent-articles/",
https://www.racket.news/s/america-this-week/"
https://eugeneyan.com/start-here/
https://tldr.tech/webdev/archives
https://tldr.tech/marketing/archives
https://tldr.tech/ai/archives
https://tldr.tech/data/archives
https://tldr.tech/crypto/archives
https://tldr.tech/devops/archives
https://www.reallygoodbusinessideas.com/sitemap/2025
https://jamesclear.com/3-2-1
https://www.thefp.com/archive
https://contrarian.substack.com/archive
https://www.lawdork.com/archive
https://joycevance.substack.com/archive
https://www.wakeuptopolitics.com/archive
https://courtaccountability.substack.com/archive
https://www.thealtmedia.com/archive
https://www.allysammarco.com/archive
https://www.marytrump.org/archive
https://taradublin.substack.com/archive
https://www.niemanlab.org/feed/
https://blogs.edf.org/climate411/feed/
https://www.yrp.ca/en/Modules/News/rss.aspx?newsId=24701210-512e-427c-82c4-5f5930c2181b
]

def collect_article_links():
    collected = []
    seen_titles = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for base_url in ACTIVE_SOURCES:
            try:
                page.goto(base_url, timeout=15000)
                soup = BeautifulSoup(page.content(), "html.parser")
                
                for a in soup.find_all("a", href=True):
                    href = a['href']
                    if "/p/" in href or "article" in href:
                        full_url = href if href.startswith("http") else base_url.rstrip("/") + href
                        title = a.text.strip()[:120]
                        if title and title not in seen_titles:
                            collected.append({"title": title, "url": full_url, "source": base_url})
                            seen_titles.add(title)
            except Exception as e:
                logging.warning(f"Failed to scrape {base_url}: {e}")
        browser.close()
    return collected
