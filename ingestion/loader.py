import os
import pdfplumber
import pytesseract
from PIL import Image
import docx

from ingestion.normalizer import normalize_ocr_layout


def load_files(folder):
    documents = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        content = ""

 
        # PDF
      
        if file.lower().endswith(".pdf"):
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    content += page.extract_text() or ""

       
        # DOCX
    
        elif file.lower().endswith(".docx"):
            doc = docx.Document(path)
            for p in doc.paragraphs:
                content += p.text + "\n"

      
        # IMAGE (LAYOUT-AWARE OCR)

        elif file.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(path)

            ocr_data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT
            )

            content = normalize_ocr_layout(ocr_data)

     
        # TEXT / MARKDOWN
  
        elif file.lower().endswith((".txt", ".md")):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

        if content.strip():
            documents.append({
                "source": file,
                "content": content
            })

    return documents
