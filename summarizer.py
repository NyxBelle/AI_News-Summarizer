import os
from openai import OpenAI
from textwrap import shorten

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """You are a helpful summarization assistant.
Given an article title and content (or description),
produce a concise, clear summary as 4–8 short bullet points.
Keep them factual, neutral, each bullet short (6–18 words).
Also return a one-line headline-style summary.
"""

def summarize_article(title, content, max_tokens=300):
    """
    Summarize an article using OpenAI API.
    Returns a formatted summary string.
    If summarization fails, returns a friendly placeholder.
    """
    if not openai.api_key:
        return "Summary unavailable: missing OpenAI API key."

    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Title: {title}\n\nContent: {content}\n\nReturn: 1) A one-line headline summary, 2) 4-8 bullet points. Use plain text."}
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
        print("Error generating summary:", e)
        return "Summary unavailable at the moment."
