from sqlalchemy.orm import Session
from transformers import pipeline
from Config.database import get_db, file_record

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_text_2(db: Session):
    newest_file = db.query(file_record).order_by(file_record.id.desc()).first()

    if not newest_file:
        return "No file found"

    text = newest_file.extracted_text
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

    return summary[0]['summary_text']