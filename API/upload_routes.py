import os
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from API.file_upload_logic import save_file, extract_text, is_allowed_file
from Config.database import get_db, file_record

upload_router = APIRouter()

@upload_router.post("/upload", description="Upload a file and store extracted text in PostgreSQL")
async def upload_file_store_text(file: UploadFile, db: Session = Depends(get_db)):
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")

    file_path = save_file(file)
    extracted_text = extract_text(file_path, file.content_type)

    db_file = db.query(file_record).filter(file_record.file_name == file.filename).first()
    if db_file:
        return {"filename": file.filename, "status": "File already exists in database"}

    new_file = file_record(file_name=file.filename, extracted_text=extracted_text)
    db.add(new_file)
    db.commit()

    # Automatically delete the file after processing
    # os.remove(file_path)

    return {"filename": file.filename, "status": "File uploaded and text stored in PostgreSQL"}
