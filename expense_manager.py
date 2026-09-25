# expense_manager.py
# This file has all the main functions for handling expenses -
# adding, deleting, filtering and totaling them up.
# main.py just calls these functions, it doesn't do the actual work itself.

from datetime import datetime
import storage

# list of categories shown in the menu when adding an expense
CATEGORIES = [
    "Food",
    "Transport",
    "Books & Supplies",
    "Rent",
    "Entertainment",
    "Subscriptions",
    "Other",
]


def next_id(expenses):
    # every expense needs a unique id, so just take the highest one used
    # so far and add 1. if list is empty, start from 1.
    if not expenses:
        return 1
    return max(e["id"] for e in expenses) + 1


def add_expense(expenses, amount, category, note, date_str=None):
    # if no date given, just use today's date
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "id": next_id(expenses),
        "amount": round(float(amount), 2),
        "category": category,
        "note": note,
        "date": date_str,
    }

    expenses.append(expense)
    storage.save_expenses(expenses)  # save to file right away so nothing is lost
    return expense


def delete_expense(expenses, expense_id):
    # go through the list and remove the expense with matching id
    for i, e in enumerate(expenses):
        if e["id"] == expense_id:
            removed = expenses.pop(i)
            storage.save_expenses(expenses)
            return removed
    return None  # id not found


def filter_by_category(expenses, category):
    # simple filter, case-insensitive so "food" and "Food" both work
    return [e for e in expenses if e["category"].lower() == category.lower()]


def filter_by_month(expenses, year, month):
    # only keep expenses that fall in the given month/year
    result = []
    for e in expenses:
        e_date = datetime.strptime(e["date"], "%Y-%m-%d")
        if e_date.year == year and e_date.month == month:
            result.append(e)
    return result


def total_spent(expenses):
    # just adds up the amount field for every expense
    return round(sum(e["amount"] for e in expenses), 2)


def spending_by_category(expenses):
    # groups expenses by category and adds up totals for each one
    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = totals.get(cat, 0) + e["amount"]

    return {cat: round(amt, 2) for cat, amt in totals.items()}


def check_budget(expenses, monthly_budget):
    # compares how much was spent this month vs the budget the user set
    now = datetime.now()
    this_month = filter_by_month(expenses, now.year, now.month)
    spent = total_spent(this_month)
    remaining = round(monthly_budget - spent, 2)
    is_over = spent > monthly_budget
    return spent, monthly_budget, remaining, is_over