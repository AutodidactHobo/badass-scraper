# enrich_semantics.py
# Phase 3: Add keyword vectors, paragraph roles, quote detection

from sentence_transformers import SentenceTransformer, util
from keybert import KeyBERT
import re
import numpy as np

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=embed_model)

CUE_TAGS = {
    "lede": ["in recent weeks", "this article explores", "in the wake of"],
    "argument": ["we argue", "this demonstrates", "suggests that"],
    "case_law": ["v. ", "supreme court", "precedent"],
    "policy": ["should be", "must consider", "recommend"],
    "cta": ["in conclusion", "moving forward", "ultimately"]
}
QUOTE_REGEX = r'(["\'])(?:(?=(\\?))\2.)*?\1'
URL_REGEX = r'https?://\S+'

def enrich_article(article):
    if not article.get("paragraphs"):
        return article

    text = " ".join(article["paragraphs"])
    embeddings = embed_model.encode(article["paragraphs"], convert_to_tensor=True)
    topic_vec = embed_model.encode(text, convert_to_tensor=True)
    sims = util.cos_sim(topic_vec, embeddings)[0].cpu().numpy()

    roles = []
    anchors = []
    for i, p in enumerate(article["paragraphs"]):
        roles.append(next((k for k, cues in CUE_TAGS.items() if any(c in p.lower() for c in cues)), "body"))
        tags = []
        if re.search(QUOTE_REGEX, p): tags.append("quote")
        if re.search(URL_REGEX, p): tags.append("link")
        if any(w in p.lower() for w in ["according to", "reported"]): tags.append("external_claim")
        anchors.append(tags)

    keywords = [kw[0] for kw in kw_model.extract_keywords(text, top_n=7)]

    article.update({
        "macro_keywords": keywords,
        "paragraph_roles": roles,
        "source_tags": anchors,
        "relevance_scores": sims.tolist(),
        "topic_score": float(np.mean(sims))
    })
    return article