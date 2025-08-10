import os
from gtts import gTTS
from pathlib import Path
import hashlib

AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech(text, prefix="summary"):
    # generate deterministic filename from text hash
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    filename = f"{prefix}-{h}.mp3"
    dest = AUDIO_DIR / filename
    if dest.exists():
        return str(dest)
    tts = gTTS(text=text, lang="en")
    tts.save(str(dest))
    return str(dest)
