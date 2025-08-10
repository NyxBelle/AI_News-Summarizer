import os
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_article(content):
    """
    Summarize an article into clear bullet points using Groq's LLaMA 3 model.
    """

    try:
        logger.info("Generating summary with Groq LLaMA3...")
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes news into 3-5 short bullet points."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following article into bullet points:\n\n{content}"
                }
            ],
            max_tokens=300,
            temperature=0.5,
            timeout=30
        )
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        logger.error(f"Groq summarization failed: {e}")
        return f"Error generating summary: {e}"
