
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import csv

def generate_pdf(user_id):
    folder = "data"
    filename = next((f for f in os.listdir(folder) if f.startswith(str(user_id))), None)
    if not filename:
        return None

    filepath = os.path.join(folder, filename)
    pdf_path = f"{folder}/{filename.replace('.csv', '.pdf')}"

    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, f"📄 Hisobot: {filename}")
    y = 750

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            line = " | ".join(row)
            c.drawString(50, y, line)
            y -= 20
            if y < 50:
                c.showPage()
                y = 800

    c.save()
    return pdf_path
