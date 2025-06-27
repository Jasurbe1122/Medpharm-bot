from fpdf import FPDF

def generate_pdf_report(user_id, entries):
    filename = f"{user_id}_report.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Xarajat Hisoboti", ln=True, align="C")

    for entry in entries:
        line = f"{entry['time']} | {entry['category']} | {entry['amount']} so'm"
        if entry.get("person"):
            line += f" | {entry['person']}"
        if entry.get("location"):
            line += f" | {entry['location']}"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    return filename
