from PyPDF2 import PdfReader
from docx import Document

def extract_text(file_content: bytes, file_extension: str) -> str:
    if file_extension == "pdf":
        reader = PdfReader(file_content)
        text = "".join(page.extract_text() for page in reader.pages)
    elif file_extension == "docx":
        doc = Document(file_content)
        text = "\n".join(para.text for para in doc.paragraphs)
    else:
        raise ValueError("Unsupported file format")
    return text