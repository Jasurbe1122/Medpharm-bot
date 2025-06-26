from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from charts import create_pie_chart, create_bar_chart

def generate_pdf_report(expenses, chat_id):
    pdf_file = f"report_{chat_id}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.drawString(100, 800, f"Guruh Hisoboti ({chat_id})")
    y = 750
    total = 0
    for name, category, amount, place, date in expenses:
        c.drawString(100, y, f"{name}: {category} - {amount} so‘m, {place}, {date}")
        y -= 20
        total += amount
    c.drawString(100, y, f"Umumiy: {total} so‘m")
    y -= 40

    pie_chart = create_pie_chart(expenses)
    c.drawImage(pie_chart, 100, y - 200, width=300, height=200)
    y -= 220

    bar_chart = create_bar_chart(expenses)
    c.drawImage(bar_chart, 100, y - 200, width=300, height=200)
    c.save()
    return pdf_file