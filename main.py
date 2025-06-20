from income import collect_income, calculate_total_monthly_income
from expenses import collect_expenses, calculate_total_expenses, summarize_expenses_by_category
from typing import List, Dict, Any

def run_budget_tool() -> None:
    print("✨ Welcome to your Interactive Budget Tool ✨")
    input("Press Enter to begin...")

    try:
        incomes: List[Dict[str, Any]] = collect_income()
        total_income: float = calculate_total_monthly_income(incomes)

        expenses: List[Dict[str, Any]] = collect_expenses()
        total_expenses: float = calculate_total_expenses(expenses)
        expense_summary: Dict[str, float] = summarize_expenses_by_category(expenses)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        return

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

if __name__ == "__main__":
    run_budget_tool()
