import re
from datetime import datetime

def parse_text(text):
    data = {'category': '', 'amount': 0, 'quantity': 0, 'person': '', 'place': ''}
    text = text.lower()

    # Kategoriya va miqdor
    if 'dori' in text:
        data['category'] = 'Dori'
        quantity_match = re.search(r'(\d+)\s*dor', text)
        if quantity_match:
            data['quantity'] = int(quantity_match.group(1))
    elif 'tuxum' in text:
        data['category'] = 'Tuxum'
        quantity_match = re.search(r'(\d+)\s*tuxum', text)
        if quantity_match:
            data['quantity'] = int(quantity_match.group(1))

    # Narx
    price_match = re.search(r'(\d+)\s*(bo‘lsaham|ming|so‘m)?', text)
    if price_match:
        amount = int(price_match.group(1))
        data['amount'] = amount * 1000 if 'bo‘lsaham' in text or 'ming' in text else amount

    # Joy va odam
    places = ['qoqon', 'marg‘ilon']
    for place in places:
        if place in text:
            data['place'] = place.capitalize()
    persons = ['orasta', 'gulbahor']
    for person in persons:
        if person in text:
            data['person'] = person.capitalize()

    return data if data['category'] else None
