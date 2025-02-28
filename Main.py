from fastapi import FastAPI, Depends
from pydantic import BaseModel
from API.chatbot_logic import chat_response, chat_response_ver2
from API.textsummarization_logic import summarize_text, summarize_text_2
from API.upload_routes import upload_router
from sqlalchemy.orm import Session
from Config.database import get_db

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

@app.post("/chatbot_2/")
async def chatbot_2(request: Chat_Request, db: Session = Depends(get_db)):
    response = chat_response_ver2(request.user_input, db)
    return {"response": response}

@app.post("/summarize/")
async def summarize(request: Summarization_Request):
    summary = summarize_text(request.text)
    return {"summary": summary}

@app.post("/summarize_text/")
async def summarize_text_2(db: Session = Depends(get_db)):
    summary = summarize_text_2(db)
    return {"summary": summary}
