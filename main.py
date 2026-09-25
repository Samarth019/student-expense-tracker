# main.py
# This is the main file - it just shows the menu and calls the right
# function from expense_manager.py depending on what the user picks.
# Run it with: python main.py

import storage
import expense_manager as em

MENU = """
==========================================
        STUDENT EXPENSE TRACKER
==========================================
1. Add an expense
2. View all expenses
3. View expenses by category
4. View this month's summary
5. Set / check monthly budget
6. Delete an expense
7. Exit
------------------------------------------
"""


def print_expense(e):
    # just a helper so I don't have to write this print line everywhere
    print(f"  [{e['id']:>3}] {e['date']}  {e['category']:<18} Rs.{e['amount']:>8.2f}  {e['note']}")


def add_expense_flow(expenses):
    print("\n-- Add New Expense --")
    for i, cat in enumerate(em.CATEGORIES, start=1):
        print(f"  {i}. {cat}")

    try:
        amount = float(input("Amount spent: Rs."))
    except ValueError:
        print("That doesn't look like a valid number, cancelling.")
        return

    choice = input(f"Category (1-{len(em.CATEGORIES)}): ").strip()
    try:
        category = em.CATEGORIES[int(choice) - 1]
    except (ValueError, IndexError):
        # if they type something invalid, just put it under "Other"
        # instead of crashing
        category = "Other"
        print("Invalid choice, defaulting to 'Other'.")

    note = input("Note (what was it for?): ").strip()
    date_str = input("Date (YYYY-MM-DD, leave blank for today): ").strip()

    if date_str:
        new_expense = em.add_expense(expenses, amount, category, note, date_str)
    else:
        new_expense = em.add_expense(expenses, amount, category, note)

    print("\nAdded:")
    print_expense(new_expense)


def view_all(expenses):
    print("\n-- All Expenses --")
    if not expenses:
        print("  No expenses recorded yet.")
        return

    # showing oldest first, feels more natural to read
    for e in sorted(expenses, key=lambda x: x["date"]):
        print_expense(e)

    print(f"\n  Total: Rs.{em.total_spent(expenses):.2f}")


def view_by_category(expenses):
    print("\nAvailable categories:", ", ".join(em.CATEGORIES))
    cat = input("Enter category to filter by: ").strip()
    filtered = em.filter_by_category(expenses, cat)

    if not filtered:
        print(f"  No expenses found under '{cat}'.")
        return

    print(f"\n-- Expenses in '{cat}' --")
    for e in filtered:
        print_expense(e)
    print(f"\n  Subtotal: Rs.{em.total_spent(filtered):.2f}")


def monthly_summary(expenses):
    from datetime import datetime
    now = datetime.now()
    this_month = em.filter_by_month(expenses, now.year, now.month)

    print(f"\n-- Summary for {now.strftime('%B %Y')} --")
    if not this_month:
        print("  Nothing recorded this month yet.")
        return

    # sort by amount, highest spending category first
    breakdown = em.spending_by_category(this_month)
    for cat, amt in sorted(breakdown.items(), key=lambda x: -x[1]):
        print(f"  {cat:<18} Rs.{amt:>8.2f}")

    print(f"\n  Total spent this month: Rs.{em.total_spent(this_month):.2f}")


def budget_flow(expenses):
    budget_data = storage.load_budget()
    current = budget_data.get("monthly_budget")

    if current:
        print(f"\nCurrent monthly budget: Rs.{current:.2f}")
    else:
        print("\nNo budget set yet.")

    change = input("Set a new budget? (y/n): ").strip().lower()
    if change == "y":
        try:
            new_budget = float(input("Enter monthly budget: Rs."))
            storage.save_budget({"monthly_budget": new_budget})
            current = new_budget
            print("Budget updated.")
        except ValueError:
            print("Invalid amount, budget left unchanged.")

    if current:
        spent, budget, remaining, is_over = em.check_budget(expenses, current)
        print(f"\nSpent so far this month: Rs.{spent:.2f} / Rs.{budget:.2f}")
        if is_over:
            print(f"  You are OVER budget by Rs.{abs(remaining):.2f}!")
        else:
            print(f"  Rs.{remaining:.2f} remaining this month.")


def delete_flow(expenses):
    # show the list first so the user can see which id to pick
    view_all(expenses)
    if not expenses:
        return
    try:
        exp_id = int(input("\nEnter ID of expense to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    removed = em.delete_expense(expenses, exp_id)
    if removed:
        print(f"Deleted: {removed['note']} (Rs.{removed['amount']:.2f})")
    else:
        print("No expense found with that ID.")


def main():
    expenses = storage.load_expenses()
    print("Welcome back! You have", len(expenses), "expense(s) logged so far.")

    # keep showing the menu until the user chooses to exit
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense_flow(expenses)
        elif choice == "2":
            view_all(expenses)
        elif choice == "3":
            view_by_category(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            budget_flow(expenses)
        elif choice == "6":
            delete_flow(expenses)
        elif choice == "7":
            print("Goodbye! Keep an eye on that spending.")
            break
        else:
            print("Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()