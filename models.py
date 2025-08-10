from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///news.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512))
    url = Column(String(2048), nullable=False)
    source = Column(String(256))
    published_at = Column(DateTime)
    summary_text = Column(Text)
    audio_filename = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('url', name='uq_url'),  # prevent duplicates by URL
    )

def init_db():
    Base.metadata.create_all(bind=engine)
