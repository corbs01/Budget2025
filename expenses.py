# expenses.py

def convert_to_monthly(amount, frequency):
    if frequency == 'weekly':
        return round((amount * 52) / 12, 2)
    elif frequency == 'fortnightly':
        return round((amount * 26) / 12, 2)
    elif frequency == 'monthly':
        return amount
    elif frequency == 'quarterly':
        return round(amount / 3, 2)
    elif frequency == 'annual':
        return round(amount / 12, 2)
    else:
        print("Invalid frequency. Defaulting to monthly.")
        return amount

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

def collect_expenses():
    all_expenses = []

    print("\n--- Expense Entry ---")
    for category_group, items in CATEGORIES.items():
        print(f"\n📂 {category_group}:")

        for item in items:
            while True:
                response = input(f"Do you want to add '{item}'? (yes/no): ").lower()
                if response in ('yes', 'no'):
                    break
                print("❌ Please enter 'yes' or 'no'.")
            if response == 'yes':
                try:
                    amount = float(input(f"Enter amount for {item}: $"))
                    frequency = input("Enter frequency (weekly/fortnightly/monthly/quarterly/annual): ").lower()
                    monthly_equivalent = convert_to_monthly(amount, frequency)

                    all_expenses.append({
                        "category_group": category_group,
                        "item": item,
                        "amount": amount,
                        "frequency": frequency,
                        "monthly_equivalent": monthly_equivalent
                    })

                    print(f"✅ Added: {item} – ${amount} ({frequency}) → ${monthly_equivalent} monthly")

                except ValueError:
                    print("❌ Invalid input. Skipping...\n")

    return all_expenses

def calculate_total_expenses(expenses):
    return round(sum([e["monthly_equivalent"] for e in expenses]), 2)

def summarize_expenses_by_category(expenses):
    summary = {}
    for e in expenses:
        group = e["category_group"]
        summary.setdefault(group, 0)
        summary[group] += e["monthly_equivalent"]
    return summary
