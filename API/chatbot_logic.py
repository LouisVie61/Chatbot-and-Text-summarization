import openai
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session
from Config.database import get_db, file_record
from transformers import pipeline

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = openai.OpenAI()

# chatbot_model = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1") (valueError: setup)

def chat_response(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}], # context information
    )
    return response.choices[0].message.content

def chat_response_ver2(user_input: str, db: Session):
    newest_upload_file = db.query(file_record).order_by(file_record.id.desc()).first()

    context_information = ""
    if newest_upload_file:
        context_information = newest_upload_file.extracted_text[:1500]

    # prompt = f"""
    # You are a great assistant can answer all questions related to provide file and input.
    # Add '.' after ending response.
    # File information:
    # {context_information}
    # User's question
    # {user_input}
    # Chatbot:
    # """
    # response = chatbot_model(prompt, max_length=200, num_return_sequences=1)

    context_information = ""
    if newest_upload_file:
        context_information = newest_upload_file.extracted_text[:1500]  # Limit text length for efficiency

    messages = [
        {"role": "system", "content": "You are a great assistant that answers questions based on the provided file and user input."},
        {"role": "user", "content": f"File Information: {context_information}"},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # return response[0]['generated_text'].replace(prompt, "").strip()
    return response.choices[0].message.content