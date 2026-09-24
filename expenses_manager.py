import string
import random
from datetime import datetime
import json


def take_only_float(input_string):
    while True:
        try:
            valid_input = float(input(input_string))
            if valid_input <= 0:
                raise ValueError
            return valid_input
        except ValueError:
            print("Please enter a valid input.")


def get_date():
    while True:
        try:
            date = input(
                "Please enter the date of the expense (dd-mm-YYYY): ")
            datetime.strptime(date, "%d-%m-%Y")
            return date
        except ValueError:
            print("Please provide a valid date.")


def get_month_year():
    while True:
        try:
            input_year = input("Year(YYYY): ")
            input_month = input("Month(mm): ")
            input_year = datetime.strptime(input_year, "%Y")
            input_month = datetime.strptime(input_month, "%m")
            return input_year.year, input_month.month
        except ValueError:
            print("Please provide valid dates.")


def valid_menu_choices(input_string):
    while True:
        try:
            valid_input = int(input(input_string))
            if 0 < valid_input <= 9:
                return valid_input
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid number between your choices.")


def check_if_data_exists(expenses_manager):
    if not expenses_manager:
        print("There are no stored expenses at the moment.")
        return True


def expense_display(expense):
    print(f"""ID: {expense["id"]}
Amount: {expense["amount"]:.2f}€
Description: {expense["description"]}
Date: {expense["date"]}
Category: {expense["category"]}
              """)


def generate_id(expenses_manager):
    characters = string.ascii_uppercase + string.digits
    while True:
        new_id = ''.join(random.choice(characters) for i in range(8))
        for expense in expenses_manager:
            if new_id == expense["id"]:
                break
        else:
            break
    return new_id


def save_expenses(expenses_manager):
    with open("expenses.json", "w") as file:
        json.dump(expenses_manager, file)


def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            expenses_manager = json.load(file)
        return expenses_manager
    except FileNotFoundError:
        return []


def add_expenses(expenses_manager, ):
    amount = take_only_float("Please enter the expense amount: ")
    description = input(
        "Please enter the description of the expense: ").title().strip()
    date = get_date()
    category = input(
        "Please enter the category of the expense: ").title().strip()
    new_id = generate_id(expenses_manager)
    new_expense = {"id": new_id, "amount": amount,
                   "description": description, "date": date, "category": category}
    expenses_manager.append(new_expense)


def show_all_expenses(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    for expense in expenses_manager:
        expense_display(expense)


def show_expenses_by_category(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    matches_found = 0
    certain_category = input(
        "Please enter the certain category you want to inspect: ").title().strip()
    for expense in expenses_manager:
        if certain_category == expense["category"]:
            expense_display(expense)
            matches_found += 1
    if not matches_found:
        print(
            f"There is no {certain_category} category in the list at the moment")


def monthly_overview(expenses_manager):
    total_monthly_amount = 0
    total_categories_amount = {}
    input_year, input_month = get_month_year()
    for expense in expenses_manager:
        converted_date = datetime.strptime(expense["date"], "%d-%m-%Y")
        if converted_date.month == input_month and converted_date.year == input_year:
            total_monthly_amount += expense["amount"]
            if expense["category"] not in total_categories_amount:
                total_categories_amount[expense["category"]
                                        ] = 0
            total_categories_amount[expense["category"]] += expense["amount"]
    print(f"""
===== MONTHLY OVERVIEW OF {input_year}-{input_month}=====
          """)
    for category in total_categories_amount:
        print(f"""{category}: {total_categories_amount[category]:.2f}€""")

    print(f"""Total monthly amount: {total_monthly_amount:.2f}€.
          """)


def display_menu():
    print(
        """  ===== EXPENSE MANAGEMENT SYSTEM =====

        1. Add Expense
        2. Show all Expenses
        3. Show Expenses by Category
        4. Monthly Overview
        5. Category Breakdown
        6. Expense History
        7. Delete Expense
        8. Save
        9. Exit""")


def main():
    expenses_manager = load_expenses()
    display_menu()

    while True:

        input_choice = valid_menu_choices("Choose your option (1-9): ")

        if input_choice == 1:
            add_expenses(expenses_manager)
            save_expenses(expenses_manager)
        elif input_choice == 2:
            show_all_expenses(expenses_manager)
        elif input_choice == 3:
            show_expenses_by_category(expenses_manager)
        elif input_choice == 4:
            monthly_overview(expenses_manager)
        elif input_choice == 8:
            save_expenses(expenses_manager)
        elif input_choice == 9:
            print("Thank you for using the Expense Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()
