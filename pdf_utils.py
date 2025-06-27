
from fpdf import FPDF

def generate_pdf_report(user_id, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Xarajatlar Hisoboti", ln=True, align='C')
    for row in data:
        pdf.cell(200, 10, txt=f"{row[0]} - {row[1]} {row[2]}", ln=True)
    pdf.output(f"{user_id}_report.pdf")
