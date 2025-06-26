import matplotlib.pyplot as plt

def create_pie_chart(expenses):
    categories = {}
    for _, category, amount, _, _ in expenses:
        categories[category] = categories.get(category, 0) + amount
    plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    plt.savefig("pie_chart.png")
    plt.close()
    return "pie_chart.png"

def create_bar_chart(expenses):
    categories = {}
    for _, category, amount, _, _ in expenses:
        categories[category] = categories.get(category, 0) + amount
    plt.bar(categories.keys(), categories.values())
    plt.savefig("bar_chart.png")
    plt.close()
    return "bar_chart.png"