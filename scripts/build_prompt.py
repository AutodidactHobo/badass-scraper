# build_prompt.py
# Phase 4: Create article writing prompt from enriched structure

def format_prompt(article):
    title = article.get("title", "Untitled")
    keywords = article.get("macro_keywords", [])
    quotes = [p for i, p in enumerate(article["paragraphs"]) if "quote" in article["source_tags"][i]]
    tone = "Skeptical, strategic, evidence-based. No filler."

    outline = f"""
TITLE: {title}

STRUCTURE:
1. Analytical Lede
2. Legal + Strategic Frame
3. Policy Implications
4. Risk and Foresight
5. Conclusion

TONE: {tone}
KEYWORDS: {', '.join(keywords[:5])}

SOURCE HOOKS:
"""
    outline += "\n".join([f"- {q}" for q in quotes[:3]])
    outline += "\n\n[BEGIN ARTICLE DRAFT HERE]"

    return outline
