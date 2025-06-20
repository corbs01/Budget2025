# storage.py

import json
from typing import List, Dict, Any

def save_budget_data(incomes: List[Dict[str, Any]], expenses: List[Dict[str, Any]]) -> None:
    data = {
        "incomes": incomes,
        "expenses": expenses
    }
    with open("budget_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("📁 Budget data saved to 'budget_data.json'.")

def load_budget_data() -> Dict[str, List[Dict[str, Any]]]:
    try:
        with open("budget_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("📁 No saved data found. Starting fresh.")
        return {"incomes": [], "expenses": []}
