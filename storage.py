# storage.py
# This file takes care of saving and loading data to/from a local JSON
# file. Keeping this separate from the main logic so if I ever want to
# switch to a real database later, I only need to change this one file.

import json
import os

DATA_FILE = os.path.join("data", "expenses.json")
BUDGET_FILE = os.path.join("data", "budget.json")


def load_expenses():
    # if the file doesn't exist yet (first time running the app),
    # just return an empty list instead of crashing
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        # in case the file got corrupted somehow, don't crash the whole app
        print("Warning: could not read expenses.json properly, starting fresh.")
        return []


def save_expenses(expenses):
    # make sure the data folder exists before trying to write into it
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def load_budget():
    # budget is kept in its own small file, separate from the expenses list
    if not os.path.exists(BUDGET_FILE):
        return {}
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_budget(budget_data):
    os.makedirs(os.path.dirname(BUDGET_FILE), exist_ok=True)
    with open(BUDGET_FILE, "w") as f:
        json.dump(budget_data, f, indent=2)