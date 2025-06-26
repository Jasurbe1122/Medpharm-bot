
import re

def parse_text(text):
    text = text.lower().strip()

    match = re.search(r"(?P<name>\w+)[\s:,-]*(?P<amount>\d+\s*(ta|kg|quti|dona|litr)?)?[\s:,-]*(?P<price>\d{3,})", text)
    if not match:
        return None

    return {
        "name": match.group("name"),
        "amount": match.group("amount") or "1 dona",
        "price": match.group("price")
    }
