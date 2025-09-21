import os
import logging
from PyPDF2 import PdfReader
from docx import Document
import structlog
from structlog import configure, processors, stdlib, threadlocal, dev

# Existing logging setup remains the same
logger = structlog.get_logger()

def format_markdown_response(text):
    return f"**Response:** {text}"

def handle_fallback(error):
    return "I'm sorry, but the service is temporarily unavailable. Please try again later or contact support."

# New: Extract text from files
def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            text = "".join([page.extract_text() for page in reader.pages])
        elif ext == '.docx':
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        logger.info("Text extracted", file=file_path, length=len(text))
        return text
    except Exception as e:
        logger.error("File extraction failed", file=file_path, error=str(e))
        return ""

def load_documents_from_directory(directory):
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.pdf', '.txt', '.docx')):
                path = os.path.join(root, file)
                text = extract_text_from_file(path)
                if text:
                    documents.append({"file": file, "text": text})
    return documents
