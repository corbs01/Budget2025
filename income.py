
def convert_to_monthly(amount, frequency):
    if frequency == 'weekly':
        return round((amount * 52) / 12, 2)
    elif frequency == 'fortnightly':
        return round((amount * 26) / 12, 2)
    elif frequency == 'monthly':
        return amount
    else:
        print("Invalid frequency. Defaulting to monthly.")
        return amount

def collect_income():
    income_sources = []
    
    print("\n--- Income Entry ---")
    while True:
        name = input("Enter income source name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break

        try:
            amount = float(input("Enter amount (net): $"))
            frequency = input("Enter frequency (weekly/fortnightly/monthly): ").lower()
            monthly = convert_to_monthly(amount, frequency)

            income_sources.append({
                "name": name,
                "amount": amount,
                "frequency": frequency,
                "monthly_equivalent": monthly
            })

            print(f"✅ Added: {name} – ${amount} ({frequency}) → ${monthly} monthly\n")

        except ValueError:
            print("❌ Invalid input. Please try again.\n")

    return income_sources

def calculate_total_monthly_income(income_sources):
    return round(sum([src["monthly_equivalent"] for src in income_sources]), 2)
