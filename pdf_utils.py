from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf_report(expenses, chat_id, total):
    pdf_file = f"report_{chat_id}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.drawString(100, 800, f"Guruh Hisoboti ({chat_id})")
    y = 750
    for name, category, amount, place, date in expenses:
        c.drawString(100, y, f"{name}: {category} - {amount} so‘m, {place}, {date}")
        y -= 20
    c.drawString(100, y, f"Umumiy: {total} so‘m")
    c.save()
    return pdf_file
