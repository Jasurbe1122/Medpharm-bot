
import re

def parse_text(text):
    name = "noma'lum"
    amount = 0
    unit = "dona"

    matches = re.findall(r"(\d+)", text)
    if matches:
        amount = int(matches[0])
    words = re.findall(r"[a-zA-Zа-яА-ЯёЁқҚўЎғҒҳҲʼ’‘]+", text)
    if words:
        name = words[0]
    if any(u in text.lower() for u in ['kg', 'litr', 'dona']):
        unit = 'kg' if 'kg' in text.lower() else ('litr' if 'litr' in text.lower() else 'dona')

    return {"name": name, "amount": amount, "unit": unit}
