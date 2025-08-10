import os, requests
from datetime import datetime, timezone

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWSAPI_TOP_HEADLINES = "https://newsapi.org/v2/top-headlines"
NEWSAPI_EVERYTHING = "https://newsapi.org/v2/everything"

def fetch_top_headlines(country="us", page_size=20):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not set")
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": page_size
    }
    resp = requests.get(NEWSAPI_TOP_HEADLINES, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return _normalize_articles(data.get("articles", []))

def search_news(query, page_size=15):
    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not set")
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "language": "en"
    }
    resp = requests.get(NEWSAPI_EVERYTHING, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return _normalize_articles(data.get("articles", []))

def _normalize_articles(articles):
    out = []
    for a in articles:
        out.append({
            "title": a.get("title"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "published_at": _parse_date(a.get("publishedAt")),
            "content": a.get("content") or a.get("description") or ""
        })
    return out

def _parse_date(datestr):
    if not datestr:
        return None
    try:
        return datetime.fromisoformat(datestr.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None
