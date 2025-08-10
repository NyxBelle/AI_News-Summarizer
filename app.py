import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from models import init_db, SessionLocal, Summary
from scheduler import start_scheduler, fetch_and_store_top_headlines
from news_fetcher import search_news
from tts import text_to_speech
from sqlalchemy import desc
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="templates")

# initialize DB
init_db()

# start scheduler (only if you want in-process scheduler)
if os.getenv("START_SCHEDULER", "1") == "1":
    scheduler = start_scheduler(app)

@app.route("/")
def index():
    session = SessionLocal()
    try:
        items = session.query(Summary).order_by(desc(Summary.created_at)).limit(25).all()
        return render_template("index.html", items=items)
    finally:
        session.close()

@app.route("/history")
def history():
    session = SessionLocal()
    try:
        items = session.query(Summary).order_by(desc(Summary.created_at)).all()
        return render_template("history.html", items=items)
    finally:
        session.close()

@app.route("/search")
def search():
    q = request.args.get("q")
    if not q:
        return redirect(url_for("index"))
    # search NewsAPI and summarize & return results (not stored)
    articles = search_news(q)
    # naive summarization using summarizer (sync)
    from summarizer import summarize_article
    results = []
    for a in articles:
        summary = summarize_article(a["title"], a["content"])
        # generate audio but do not save DB entry (optional)
        audio_path = text_to_speech(summary)
        results.append({
            "title": a["title"],
            "url": a["url"],
            "source": a["source"],
            "published_at": a["published_at"],
            "summary_text": summary,
            "audio": audio_path
        })
    return render_template("index.html", items=results, search_query=q)

@app.route("/api/refresh", methods=["POST", "GET"])
def api_refresh():
    # trigger fetch+store (useful for Cronjob calling this endpoint)
    try:
        fetch_and_store_top_headlines()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/static/audio/<path:filename>")
def audio(filename):
    return send_from_directory(Path("static/audio"), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
