from fastapi import FastAPI
from pydantic import BaseModel
from API.chatbot_logic import chat_response
from API.textsummarization_logic import summarize_text
from API.upload_routes import upload_router

# Run: uvicorn Main:app --reload
app = FastAPI()

app.include_router(upload_router, prefix="/files", tags=["File Upload"])

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