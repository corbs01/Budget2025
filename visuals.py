# visuals.py

import matplotlib.pyplot as plt

def plot_expense_breakdown(expense_summary):
    labels = list(expense_summary.keys())
    values = list(expense_summary.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Monthly Expenses by Category")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
