# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from income import convert_to_monthly as convert_income
from expenses import convert_to_monthly as convert_expense
from storage import save_budget_data, load_budget_data

CATEGORIES = {
    "Essentials": [
        "Rent/Mortgage", "Groceries", "Electricity", "Water", "Internet", 
        "Transport", "Phone", "Health", "Insurance", "Debt Payments", "Education", "Pets"
    ],
    "Discretionary": [
        "Eating Out", "Entertainment", "Shopping", "Personal Care", 
        "Fitness", "Social/Events", "Travel/Saving For"
    ],
    "Irregular": [
        "Holidays", "Home Maintenance", "Car WOF/Servicing", 
        "Annual Bills", "Term Fees/School"
    ],
    "One-Off": [
        "Unexpected Costs", "Emergency Fund Top-Ups", "Tech/Appliance Replacements"
    ]
}


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Budget Tool")
        self.root.geometry("500x600")

        self.incomes = []
        self.expenses = []

        self.build_main_menu()

    def build_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="✨ Welcome to the Budget Tool ✨", font=("Helvetica", 18)).pack(pady=20)
        ttk.Button(self.root, text="Start New Budget", command=self.start_budget).pack(pady=10)
        ttk.Button(self.root, text="Load Previous Budget", command=self.load_budget).pack(pady=10)

    def start_budget(self):
        self.incomes = []
        self.expenses = []
        self.build_income_entry()

    def load_budget(self):
        data = load_budget_data()
        self.incomes = data["incomes"]
        self.expenses = data["expenses"]
        self.show_summary()

    def build_income_entry(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Income", font=("Helvetica", 14)).pack(pady=10)

        self.income_name = tk.Entry(self.root)
        self.income_name.pack(pady=5)
        self.income_name.insert(0, "Source name")

        self.income_amount = tk.Entry(self.root)
        self.income_amount.pack(pady=5)
        self.income_amount.insert(0, "Amount")

        self.income_freq = ttk.Combobox(self.root, values=["weekly", "fortnightly", "monthly"])
        self.income_freq.set("monthly")
        self.income_freq.pack(pady=5)

        ttk.Button(self.root, text="Add Income", command=self.add_income).pack(pady=10)
        ttk.Button(self.root, text="Next: Expenses", command=self.build_expense_entry).pack(pady=10)

    def add_income(self):
        try:
            name = self.income_name.get()
            amount = float(self.income_amount.get())
            freq = self.income_freq.get()
            monthly = convert_income(amount, freq)

            self.incomes.append({
                "name": name,
                "amount": amount,
                "frequency": freq,
                "monthly_equivalent": monthly
            })

            messagebox.showinfo("Income Added", f"{name} – ${monthly}/month")

            self.income_name.delete(0, tk.END)
            self.income_amount.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid income details.")

    def build_expense_entry(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Expense", font=("Helvetica", 14)).pack(pady=10)

        self.expense_name = tk.Entry(self.root)
        self.expense_name.pack(pady=5)
        self.expense_name.insert(0, "Expense name")

        self.expense_amount = tk.Entry(self.root)
        self.expense_amount.pack(pady=5)
        self.expense_amount.insert(0, "Amount")

        self.expense_freq = ttk.Combobox(self.root, values=["weekly", "fortnightly", "monthly", "quarterly", "annual"])
        self.expense_freq.set("monthly")
        self.expense_freq.pack(pady=5)

        self.expense_group = ttk.Combobox(self.root, values=list(CATEGORIES.keys()))
        self.expense_group.set("Essentials")
        self.expense_group.pack(pady=5)

        ttk.Button(self.root, text="Add Expense", command=self.add_expense).pack(pady=10)
        ttk.Button(self.root, text="Finish & Show Summary", command=self.show_summary).pack(pady=10)

    def add_expense(self):
        try:
            name = self.expense_name.get()
            amount = float(self.expense_amount.get())
            freq = self.expense_freq.get()
            monthly = convert_expense(amount, freq)

            self.expenses.append({
                "item": name,
                "amount": amount,
                "frequency": freq,
                "monthly_equivalent": monthly,
                "category_group": self.expense_group.get()

            })

            messagebox.showinfo("Expense Added", f"{name} – ${monthly}/month")

            self.expense_name.delete(0, tk.END)
            self.expense_amount.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid expense details.")

    def show_summary(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        total_income = sum(i["monthly_equivalent"] for i in self.incomes)
        total_expense = sum(e["monthly_equivalent"] for e in self.expenses)
        balance = total_income - total_expense

        status = "🟢 Surplus" if balance > 0 else "🟡 Break-even" if balance == 0 else "🔴 Deficit"

        tk.Label(self.root, text="📊 Budget Summary", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Total Income: ${total_income:.2f}").pack()
        tk.Label(self.root, text=f"Total Expenses: ${total_expense:.2f}").pack()
        tk.Label(self.root, text=f"Balance: ${balance:.2f}").pack()
        tk.Label(self.root, text=f"Status: {status}", font=("Helvetica", 12)).pack(pady=10)

        ttk.Button(self.root, text="Save Budget", command=self.save_budget).pack(pady=5)
        ttk.Button(self.root, text="Return to Main Menu", command=self.build_main_menu).pack(pady=5)

    def save_budget(self):
        save_budget_data(self.incomes, self.expenses)
        messagebox.showinfo("Saved", "Your budget has been saved.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
