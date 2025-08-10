from apscheduler.schedulers.background import BackgroundScheduler
from news_fetcher import fetch_top_headlines
from summarizer import summarize_article
from tts import text_to_speech
from models import SessionLocal, Summary
from datetime import datetime
import traceback

def fetch_and_store_top_headlines():
    session = SessionLocal()
    try:
        articles = fetch_top_headlines()
        for a in articles:
            url = a["url"]
            # skip if exists
            exists = session.query(Summary).filter(Summary.url == url).first()
            if exists:
                continue
            # build content for summarizer - prefer content, fall back to title
            content = a.get("content") or a.get("title") or ""
            try:
                summary_text = summarize_article(a.get("title") or "No title", content)
            except Exception:
                summary_text = "Summary failed."
            audio_path = None
            try:
                audio_path = text_to_speech(summary_text)
            except Exception:
                audio_path = None
            s = Summary(
                title=a.get("title"),
                url=url,
                source=a.get("source"),
                published_at=a.get("published_at"),
                summary_text=summary_text,
                audio_filename=audio_path
            )
            session.add(s)
            session.commit()
    except Exception as e:
        print("Scheduler error:", e)
        traceback.print_exc()
    finally:
        session.close()

def start_scheduler(app=None):
    scheduler = BackgroundScheduler()
    # run at start and then every hour
    scheduler.add_job(fetch_and_store_top_headlines, 'interval', hours=1, next_run_time=datetime.utcnow())
    scheduler.start()
    return scheduler
