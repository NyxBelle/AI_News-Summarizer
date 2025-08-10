# AI_News-Summarizer
# AI News Summarizer

Deploys a Flask app that:
- fetches news from NewsAPI
- summarizes with OpenAI GPT
- generates MP3 summaries (gTTS)
- stores summaries in SQLite (SQLAlchemy)
- hourly updates via APScheduler (or via Render Cron calling /api/refresh)

## Setup (local)
1. Copy `.env.example` -> `.env` and fill keys.
2. python -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. python app.py

## Deploy (Render)
1. Push repo to GitHub.
2. In Render: New -> Web Service -> connect repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Set environment variables (NEWS_API_KEY, OPENAI_API_KEY, OPENAI_MODEL, DATABASE_URL)
6. (Optional) Set `START_SCHEDULER=0` and create a Render Cron Job to `POST` your `/api/refresh` endpoint hourly.
