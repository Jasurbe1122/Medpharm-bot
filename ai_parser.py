import re

def parse_text(text):
    data = {'category': '', 'amount': 0, 'quantity': 0, 'person': '', 'place': ''}
    text = text.lower()
    if 'dori' in text:
        data['category'] = 'Dori'
    elif 'tuxum' in text:
        data['category'] = 'Tuxum'

    price_match = re.search(r'(\d+)', text)
    if price_match:
        amount = int(price_match.group(1))
        data['amount'] = amount

    places = ['qoqon', 'marg‘ilon']
    for place in places:
        if place in text:
            data['place'] = place.capitalize()
    persons = ['orasta', 'gulbahor']
    for person in persons:
        if person in text:
            data['person'] = person.capitalize()

    return data if data['category'] else None