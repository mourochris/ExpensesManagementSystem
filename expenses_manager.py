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


def get_month_year(choice):
    while True:
        try:
            if choice == "month_year":
                input_year_month = input("Year-month(YYYY-mm): ")
                input_year_month = datetime.strptime(input_year_month, "%Y-%m")
                return input_year_month
            else:
                input_year = input("Year(YYYY): ")
                input_year = datetime.strptime(
                    f"{input_year}-12-31", "%Y-%m-%d")
                return input_year
        except ValueError:
            print("Please provide valid dates.")


def valid_menu_choices(input_string):
    while True:
        try:
            valid_input = int(input(input_string))
            if 0 < valid_input <= 8:
                return valid_input
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid number between your choices.")


def check_if_data_exists(expenses_manager):
    if not expenses_manager:
        print("There are no stored expenses at the moment.")
        return True


def yes_no_answer(expresion):
    valid_choices = ["y", "n"]
    while True:
        choice = input(expresion).lower().strip()
        if choice not in valid_choices:
            print("Please enter a valid choice.")
        else:
            return choice


def category_input(expenses_manager):
    no_matches = 0
    prefered_category = input(
        "Please enter the prefered category: ").title().strip()
    for expense in expenses_manager:
        if prefered_category == expense["category"]:
            return prefered_category
        else:
            no_matches += 1
    if no_matches == len(expenses_manager):
        creation_choice = yes_no_answer(
            f"There are no matching category results with '{prefered_category}'. Do you want to create a new expense with this category? (y/n): ")
        if creation_choice == "y":
            return creation_choice
        else:
            print("You are now going back to main menu.")
            return "n"


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


def monthly_overview(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    total_monthly_amount = 0
    total_categories_amount = {}
    input_year_month = get_month_year("month_year")
    for expense in expenses_manager:
        converted_date = datetime.strptime(expense["date"], "%d-%m-%Y")
        if converted_date.month == input_year_month.month and converted_date.year == input_year_month.year:
            total_monthly_amount += expense["amount"]
            if expense["category"] not in total_categories_amount:
                total_categories_amount[expense["category"]
                                        ] = 0
            total_categories_amount[expense["category"]] += expense["amount"]
    print(f"""
===== MONTHLY OVERVIEW OF {input_year_month.year}-{input_year_month.month}=====
          """)
    for category in total_categories_amount:
        print(f"""{category}: {total_categories_amount[category]:.2f}€""")

    print(f"""Total monthly amount: {total_monthly_amount:.2f}€.
          """)


def category_breakdown(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    continue_choice = ""
    current_date = datetime.now()
    prefered_category = category_input(expenses_manager)
    if prefered_category == "y":
        return True
    elif prefered_category == "n":
        return

    while True:
        if continue_choice == "y":
            current_date = year_of_choice
        yearly_total_amount = 0
        categorized_expenses = []
        for expense in expenses_manager:
            expense_date = datetime.strptime(expense["date"], "%d-%m-%Y")
            if expense["category"] == prefered_category and current_date.year == expense_date.year and current_date >= expense_date:
                yearly_total_amount += expense["amount"]
                categorized_expenses.append(expense)
        if categorized_expenses:
            for month in range(1, 13):
                converted_month = datetime.strptime(str(month), "%m").month
                monthly_expenses = []
                monthly_total_amount = 0
                for expense in categorized_expenses:
                    expense_date = datetime.strptime(
                        expense["date"], "%d-%m-%Y")
                    if converted_month == expense_date.month:
                        monthly_total_amount += expense["amount"]
                        monthly_expenses.append(expense)
                if monthly_total_amount:
                    print(f"""
===== EXPENSES OF {converted_month}-{expense_date.year} =====
                      """)
                    for expense in monthly_expenses:
                        expense_display(expense)
                    print(f"Total Monthly amount: {monthly_total_amount:.2f}€")
            print(f"""
=======================================================
    Total Yearly amount: {yearly_total_amount:.2f}€""")
        else:
            print(
                f"There are no expenses in the category '{prefered_category}' for the year {current_date.year}.")
        continue_choice = yes_no_answer(
            "Do you want to inspect the category for another year?(y/n): ")
        if continue_choice == "n":
            break
        year_of_choice = get_month_year("year")


def display_menu():
    print(
        """  ===== EXPENSE MANAGEMENT SYSTEM =====

        1. Add Expense
        2. Show all Expenses
        3. Monthly Overview
        4. Category Breakdown
        5. Expense History
        6. Delete Expense
        7. Save
        8. Exit""")


def main():
    expenses_manager = load_expenses()
    display_menu()

    while True:

        input_choice = valid_menu_choices("Choose your option (1-8): ")

        if input_choice == 1:
            add_expenses(expenses_manager)
            save_expenses(expenses_manager)
        elif input_choice == 2:
            show_all_expenses(expenses_manager)
        elif input_choice == 3:
            monthly_overview(expenses_manager)
        elif input_choice == 4:
            creation_choice = category_breakdown(expenses_manager)
            if creation_choice:
                add_expenses(expenses_manager)
                save_expenses(expenses_manager)
        elif input_choice == 7:
            save_expenses(expenses_manager)
        elif input_choice == 8:
            print("Thank you for using the Expense Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()
