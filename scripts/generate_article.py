# generate_article.py
# Phase 5: Call local Mistral via LM Studio to generate and save article

import requests
import os
import re

def safe_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)[:80] + ".txt"

def generate_and_save_article(prompt, article, output_dir):
    model_name = "mistral-7b-instruct-v0.1"  # Use exact model name shown from /v1/models

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a strategic policy analyst writing skeptical legal-tech commentary."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        r = requests.post("http://localhost:1234/v1/chat/completions", json=payload)
        content = r.json()['choices'][0]['message']['content']
    except Exception as e:
        content = f"[GENERATION ERROR] {e}"

    filename = safe_filename(article.get("title", "untitled"))
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(content)
