
import csv
import os
from datetime import datetime

def save_to_csv(user_id, username, data):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{user_id}_{username}.csv"
    is_new = not os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["date", "name", "amount", "price"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), data["name"], data["amount"], data["price"]])
