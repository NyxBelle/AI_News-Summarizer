import os
from openai import OpenAI
from textwrap import shorten

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

SYSTEM_PROMPT = """You are a helpful summarization assistant. 
Given an article title and content (or description), produce:
1) A concise one-line headline summary.
2) 4–8 short bullet points (6–18 words each), factual and neutral.
Return plain text, with the headline first, then bullet points.
"""

def summarize_article(title, content, max_tokens=300):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set")

    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Title: {title}\n\nContent: {content}"}
    ]

    try:
        # Call OpenAI Chat Completions API
        resp = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.2,
            max_tokens=max_tokens
        )

        text = resp.choices[0].message.content.strip()

        # Parse: headline = first line, rest = bullet points
        parts = [line.strip() for line in text.splitlines() if line.strip()]
        headline = parts[0] if parts else shorten(title, width=80)
        bullets = [p for p in parts[1:] if p.startswith("-") or p.startswith("•") or p.startswith("*")]

        # Fallback: split by periods if no bullet markers
        if not bullets and len(parts) > 1:
            rest = " ".join(parts[1:])
            cand = [x.strip() for x in rest.split(".") if x.strip()]
            bullets = ["- " + c for c in cand[:6]]

        return headline + "\n" + "\n".join(bullets)

    except Exception as e:
        return f"Error generating summary: {str(e)}"
