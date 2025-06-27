import re

def parse_text(text):
    words = text.lower().split()
    amount = 0
    category = "nomaʼlum"
    person = None
    location = None

    for word in words:
        if word.isdigit():
            amount = int(word)
        elif word not in ["so‘m", "sum", "ming", "kg"]:
            if not category or category == "nomaʼlum":
                category = word
            elif not person:
                person = word
            elif not location:
                location = word

    return {"category": category, "amount": amount, "person": person, "location": location}
