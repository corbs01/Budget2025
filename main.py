# main.py

from income import collect_income, calculate_total_monthly_income

def run_budget_tool():
    print("✨ Welcome to your Interactive Budget Tool ✨")
    input("Press Enter to begin...")

    incomes = collect_income()
    total_income = calculate_total_monthly_income(incomes)

    print("\n🔎 Summary of Monthly Income:")
    for src in incomes:
        print(f"- {src['name']}: ${src['monthly_equivalent']}")

    print(f"\n💰 Total Monthly Income: ${total_income}\n")

if __name__ == "__main__":
    run_budget_tool()
