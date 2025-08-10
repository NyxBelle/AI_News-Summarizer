import os
from openai import OpenAI
import logging

# Logging for Render debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_article(content):
    """
    Summarize an article into clear, concise bullet points using GPT models.
    Falls back to GPT-3.5-turbo if GPT-4o-mini is unavailable.
    """

    models_to_try = [
        os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "gpt-3.5-turbo"
    ]

    for model in models_to_try:
        try:
            logger.info(f"Trying model: {model}")
            response = client.chat.completions.create(
                model=model,
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
                timeout=30  # prevents 504 Gateway Timeout on Render
            )
            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            logger.error(f"Model {model} failed: {e}")
            continue  # Try the next model

    return "Error: All models failed to generate a summary."
