from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path

async def encrypt_pdf(filename, password):
    """Шифрование PDF файла паролем"""
    pdf_file = Path('./input/' + filename)
    new_file = f'./output/{pdf_file.stem}.pdf'

    pdfwriter = PdfWriter()
    pdf = PdfReader(pdf_file)

    for page in range(len(pdf.pages)):
        pdfwriter.add_page(pdf.pages[page])

    pdfwriter.encrypt(password)

    with open (new_file, 'wb') as file:
        pdfwriter.write(file)
