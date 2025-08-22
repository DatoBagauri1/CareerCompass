import os
import logging
from typing import Optional

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using PyPDF2."""
    if PyPDF2 is None:
        logging.error("PyPDF2 not available. Install with: pip install PyPDF2")
        return ""
    
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file using python-docx."""
    if Document is None:
        logging.error("python-docx not available. Install with: pip install python-docx")
        return ""
    
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_text_from_file(file_path: str) -> str:
    """Extract text from file based on extension."""
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return ""
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        logging.error(f"Unsupported file type: {file_ext}")
        return ""
