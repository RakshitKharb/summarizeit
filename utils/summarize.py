# utils/summarize.py

from transformers import pipeline

def initialize_summarizer():
    # Initialize the Hugging Face summarization pipeline with a smaller model
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return summarizer

def summarize_text(text, summarizer, max_length=150, min_length=40):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, truncation=True)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "An error occurred during summarization."
