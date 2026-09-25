# Student Expense Tracker

A simple command-line application that helps students log their daily
expenses, see where their money is going, and stay within a monthly budget.

I built this as a course project - it's plain Python with no external
libraries, so it should run anywhere Python 3 is installed.

## Features

- Add an expense with amount, category, note, and date
- View all logged expenses
- Filter expenses by category (Food, Transport, Rent, etc.)
- Get a summary of spending for the current month, broken down by category
- Set a monthly budget and get warned when you go over it
- Delete an expense by its ID
- All data is saved locally in `data/expenses.json`, so it's still there
  the next time you run the program

## Project Structure

```
student_expense_tracker/
├── main.py               # CLI menu / entry point
├── expense_manager.py     # Core logic: add, delete, filter, summarize
├── storage.py              # Reads/writes the JSON data files
├── data/                       # Created automatically, stores your data
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7 or newer
- No external packages needed (everything used is part of the Python
  standard library)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/{your-username}/{repo-name}.git
   cd {repo-name}
   ```

2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   ```

3. Install dependencies (there aren't any, but this is here in case that
   changes):
   ```
   pip install -r requirements.txt
   ```

## Running the Project

From inside the project folder, run:

```
python main.py
```

You'll see a menu like this:

```
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
```

Just type the number of what you want to do and follow the prompts.

### Example: adding an expense

```
Choose an option (1-7): 1
Amount spent: Rs.150
Category (1-7): 1
Note (what was it for?): Bus fare to college
Date (YYYY-MM-DD, leave blank for today):
```

Your expense is saved immediately to `data/expenses.json`, so nothing is
lost if you close the program.

## Notes

- Amounts are shown in Rupees (Rs.) by default - you can change the
  currency label in `main.py` if you need a different one.
- The budget is tracked per calendar month (based on today's date), not
  per 30-day period.
- `data/expenses.json` and `data/budget.json` are created the first time
  you add an expense or set a budget, so the repo doesn't ship with any
  personal data in it.

## Possible Improvements

- Export expenses to a CSV or PDF report
- Multi-user support with login
- A simple GUI (currently CLI-only as required by the assignment)
