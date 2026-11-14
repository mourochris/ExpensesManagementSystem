# Expense Management System (EMS)

Expense Management System is a Python command-line application designed to help users easily record, organize, and analyze their personal expenses.

It allows users to explore their spending history, review expenses by date or category, and automatically calculate totals, making personal expense tracking simpler and more convenient.

## Key Features

### Category Breakdown

Explore expenses within a specific category to understand where your money goes. Review spending across different years, inspect monthly totals, and see summaries of upcoming expenses associated with that category.

### Analyze Expenses

Search expenses by description to discover how much you've spent on particular purchases, services, or recurring costs over time.

EMS organizes matching recorded expenses by year and month, calculates their combined total, and provides a separate summary of upcoming matching expenses.

### Monthly Overview

Get a simplified financial overview of a selected month, including total spending and a breakdown of expenses by category.

This helps users understand spending patterns and identify areas that may need attention.

## Additional Features

- **Add Expenses:** Record expenses with an amount, description, date, and category.
- **Browse Expenses:** Explore expenses by year or by a specific month.
- **Delete Expenses:** Remove expenses by unique ID or search criteria, with confirmation before deletion.
- **Automatic Saving:** Save changes to a local JSON file automatically.
- **Upcoming Expenses:** Distinguish future expenses from recorded spending in supported reports.

## Requirements

- Python 3
- A terminal or command-line application

EMS uses only Python's standard library. No additional packages are required.

## Getting Started

### 1. Download the application

Visit the [GitHub repository](https://github.com/mourochris/ExpensesManagementSystem).

Select **Code → Download ZIP**, then extract the downloaded folder.

Alternatively, clone the repository using Git:

```bash
git clone https://github.com/mourochris/ExpensesManagementSystem.git
```

### 2. Open the project directory

If you cloned the repository, navigate into it:

```bash
cd ExpensesManagementSystem
```

If you downloaded the ZIP, navigate to its extracted folder instead.

### 3. Run EMS

Execute:

```bash
python3 expenses_manager.py
```

On systems where Python 3 is available through `python`, you can use that command instead.

### 4. Start managing expenses

Follow the interactive terminal menu to add, browse, analyze, and manage your expense records.

## Data Storage

EMS stores expense records locally in an `expenses.json` file.

- Changes are saved automatically after successful additions and deletions.
- Existing records are loaded when the application starts.
- If no expense file exists, EMS starts with an empty list.
- The expense file is created automatically when the first expense is saved.

Personal expense records are excluded from the GitHub repository.

**Important:** Keep a backup of `expenses.json` to protect your records against accidental deletion or hardware failure.

When moving to a new installation, copy your existing expense file into the directory from which EMS will run.

## Version

**Version:** 1.0.0

This release provides the core functionality for recording, organizing, and analyzing personal expenses.

Additional features and improvements may be introduced in future versions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.