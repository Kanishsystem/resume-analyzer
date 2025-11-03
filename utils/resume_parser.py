# import PyPDF2
# import docx2txt
# import tempfile

# def extract_text(file):
#     text = ""
#     try:
#         if file.name.endswith(".pdf"):
#             pdf_reader = PyPDF2.PdfReader(file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text() or ""
#         elif file.name.endswith(".docx"):
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
#                 tmp.write(file.read())
#                 tmp.flush()
#                 text = docx2txt.process(tmp.name)
#         else:
#             text = ""
#     except Exception as e:
#         print("Error extracting:", e)
#         text = ""
#     return text.strip()
import PyPDF2
import docx2txt
import tempfile
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import os

# (Optional) Set the Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file):
    text = ""
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    # Fallback to OCR if page is image-based
                    images = convert_from_bytes(file.read())
                    for img in images:
                        text += pytesseract.image_to_string(img)
        elif file.name.endswith(".docx"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                tmp.flush()
                text = docx2txt.process(tmp.name)
        elif file.name.lower().endswith((".jpg", ".jpeg", ".png")):
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
        else:
            text = ""
    except Exception as e:
        print("Error extracting text:", e)
        text = ""
    return text.strip()
