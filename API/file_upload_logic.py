import os
import shutil
import docx2txt
from pathlib import Path
from pypdf import PdfReader

# Define upload folder
UPLOAD_FOLDER = Path(__file__).parent.parent / "Uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}

def is_allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file) -> str:
    """Save the uploaded file to the upload folder."""
    file_path = UPLOAD_FOLDER / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(file_path)

def extract_text(file_path: str, content_type: str) -> str:
    """Extract text from PDF, DOCX, or TXT files."""
    text = ""
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == "pdf":
        with open(file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

    elif file_extension in ["doc", "docx"]:
        text = docx2txt.process(file_path)

    elif file_extension == "txt":
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    return text.strip() if text else "No text could be extracted."

