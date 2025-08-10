import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "facebook/bart-large-cnn"

def summarize_article(content):
    """
    Summarize an article using Hugging Face's BART model via the Inference API.
    Returns a short bullet-point style summary.
    """
    if not HF_API_KEY:
        return "Error: Hugging Face API key not set."

    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": content,
        "parameters": {"max_length": 200, "min_length": 50, "do_sample": False}
    }

    try:
        logger.info("Sending request to Hugging Face for summarization...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            summary = data[0]["summary_text"].strip()
            # Convert to bullet points
            bullet_points = "• " + summary.replace(". ", ".\n• ")
            return bullet_points
        else:
            logger.error(f"Unexpected Hugging Face response: {data}")
            return f"Error: Unexpected response from Hugging Face API: {data}"

    except requests.exceptions.RequestException as e:
        logger.error(f"Hugging Face API request failed: {e}")
        return f"Error generating summary: {e}"
