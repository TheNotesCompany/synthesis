import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    all_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text and text.strip():
                all_text.append(text)
                continue

            # OCR fallback for image pages
            images = convert_from_path(
                pdf_path,
                first_page=page.page_number,
                last_page=page.page_number
            )
            ocr_text = pytesseract.image_to_string(images[0])
            all_text.append(ocr_text)

    return "\n".join(all_text)
