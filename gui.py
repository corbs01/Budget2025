# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from income import convert_to_monthly as convert_income
from expenses import convert_to_monthly as convert_expense
from storage import save_budget_data, load_budget_data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        ttk.Button(self.root, text="Show Expense Pie Chart", command=self.show_expense_pie_chart).pack(pady=5)
        ttk.Button(self.root, text="Edit Expenses", command=self.build_expense_editor).pack(pady=5)
        ttk.Button(self.root, text="Return to Main Menu", command=self.build_main_menu).pack(pady=5)

    def save_budget(self):
        save_budget_data(self.incomes, self.expenses)
        messagebox.showinfo("Saved", "Your budget has been saved.")

    def show_expense_pie_chart(self):
        summary = {}
        for e in self.expenses:
            group = e["category_group"]
            summary.setdefault(group, 0)
            summary[group] += e["monthly_equivalent"]

        if not summary:
            messagebox.showinfo("No Data", "No expenses to display in chart.")
            return

        # Create chart
        labels = list(summary.keys())
        values = list(summary.values())

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures pie is round
        fig.tight_layout()

        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Breakdown Chart")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def build_expense_editor(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="✏️ Edit Expenses", font=("Helvetica", 16)).pack(pady=10)

        self.expense_listbox = tk.Listbox(self.root, width=60)
        self.expense_listbox.pack(pady=10)

        for idx, exp in enumerate(self.expenses):
            text = f"{idx+1}. {exp['item']} - ${exp['amount']} ({exp['frequency']}) in {exp['category_group']}"
            self.expense_listbox.insert(tk.END, text)

        ttk.Button(self.root, text="Edit Selected", command=self.edit_selected_expense).pack(pady=5)
        ttk.Button(self.root, text="Back to Summary", command=self.show_summary).pack(pady=5)

    def edit_selected_expense(self):
        try:
            idx = self.expense_listbox.curselection()[0]
            self.current_edit_index = idx
            exp = self.expenses[idx]
        except IndexError:
            messagebox.showerror("Error", "Please select an expense to edit.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Edit Expense", font=("Helvetica", 14)).pack(pady=10)

        self.edit_name = tk.Entry(self.root)
        self.edit_name.insert(0, exp['item'])
        self.edit_name.pack(pady=5)

        self.edit_amount = tk.Entry(self.root)
        self.edit_amount.insert(0, str(exp['amount']))
        self.edit_amount.pack(pady=5)

        self.edit_freq = ttk.Combobox(self.root, values=["weekly", "fortnightly", "monthly", "quarterly", "annual"])
        self.edit_freq.set(exp['frequency'])
        self.edit_freq.pack(pady=5)

        self.edit_group = ttk.Combobox(self.root, values=list(CATEGORIES.keys()))
        self.edit_group.set(exp['category_group'])
        self.edit_group.pack(pady=5)

        ttk.Button(self.root, text="Save Changes", command=self.save_edited_expense).pack(pady=10)
        ttk.Button(self.root, text="Cancel", command=self.build_expense_editor).pack(pady=5)

    def save_edited_expense(self):
        try:
            name = self.edit_name.get()
            amount = float(self.edit_amount.get())
            freq = self.edit_freq.get()
            group = self.edit_group.get()
            monthly = convert_expense(amount, freq)

            self.expenses[self.current_edit_index] = {
                "item": name,
                "amount": amount,
                "frequency": freq,
                "monthly_equivalent": monthly,
                "category_group": group
            }

            messagebox.showinfo("Saved", f"Updated {name}.")
            self.build_expense_editor()

        except ValueError:
            messagebox.showerror("Error", "Invalid values entered.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
