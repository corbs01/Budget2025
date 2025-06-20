from income import collect_income, calculate_total_monthly_income
from expenses import collect_expenses, calculate_total_expenses, summarize_expenses_by_category
from storage import save_budget_data, load_budget_data
from typing import List, Dict, Any

    
def run_budget_tool() -> None:
    print("✨ Welcome to your Interactive Budget Tool ✨")

    use_saved = input("Would you like to load your previous budget? (yes/no): ").lower()
    if use_saved == "yes":
        data = load_budget_data()
        incomes = data["incomes"]
        expenses = data["expenses"]
    else:
        input("Press Enter to begin entering new data...")
        incomes = collect_income()
        expenses = collect_expenses()

    total_income = calculate_total_monthly_income(incomes)
    total_expenses = calculate_total_expenses(expenses)
    expense_summary = summarize_expenses_by_category(expenses)

    print("\n🔎 Income Summary:")
    for src in incomes:
        print(f"- {src['name']}: ${src['monthly_equivalent']:.2f}")
    print(f"💰 Total Monthly Income: ${total_income:.2f}")

    print("\n🔎 Expense Summary by Category:")
    for category, total in expense_summary.items():
        print(f"- {category}: ${total:.2f}")
    print(f"💸 Total Monthly Expenses: ${total_expenses:.2f}")

    balance = total_income - total_expenses
    status = (
        "🟢 Surplus – You're living within your means!"
        if balance > 0 else
        "🟡 Break-even – You're on the edge!" if balance == 0 else
        "🔴 Deficit – You're overspending!"
    )

    print(f"\n📊 Monthly Balance: ${balance:.2f}")
    print(f"📣 Status: {status}\n")

    save = input("Would you like to save this budget data? (yes/no): ").lower()
    if save == "yes":
        save_budget_data(incomes, expenses)



if __name__ == "__main__":
    run_budget_tool()
