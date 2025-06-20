# main.py

from income import collect_income, calculate_total_monthly_income
from typing import List, Dict, Any

def run_budget_tool() -> None:
    """
    Runs the interactive budget tool, collecting income sources from the user,
    calculating the total monthly income, and displaying a summary.
    Handles errors gracefully and formats output for clarity.
    """
    print("✨ Welcome to your Interactive Budget Tool ✨")
    input("Press Enter to begin...")

    try:
        incomes: List[Dict[str, Any]] = collect_income()
        total_income: float = calculate_total_monthly_income(incomes)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        return

    print("\n🔎 Summary of Monthly Income:")
    for src in incomes:
        try:
            print(f"- {src['name']}: ${src['monthly_equivalent']:.2f}")
        except (KeyError, TypeError, ValueError):
            print(f"- [Invalid income entry]: {src}")

    print(f"\n💰 Total Monthly Income: ${total_income:.2f}\n")

if __name__ == "__main__":
    run_budget_tool()
