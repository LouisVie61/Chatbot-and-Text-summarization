from fastapi import FastAPI
from pydantic import BaseModel
from business_logic.chatbot_logic import chat_response
from business_logic.textsummarization_logic import summarize_text

# Run: uvicorn main:app --reload
app = FastAPI()

class Chat_Request(BaseModel):
    user_input: str

class Summarization_Request(BaseModel):
    text: str

@app.post("/chatbot/")
async def chatbot(request: Chat_Request):
    response = chat_response(request.user_input)
    return {"response": response}

@app.post("/summarize/")
async def summarize(request: Summarization_Request):
    summary = summarize_text(request.text)
    return {"summary": summary}