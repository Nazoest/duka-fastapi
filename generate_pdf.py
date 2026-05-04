from fpdf import FPDF
from cloudinary_upload import upload_pdf
pdf = FPDF()

def generate_receipt(text,file_name):
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(200, 10, txt=text, align='C')
    pdf.output(f"receipts/{file_name}.pdf")
    upload_pdf(f"{file_name}")

