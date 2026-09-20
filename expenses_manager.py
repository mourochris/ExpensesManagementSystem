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
            date = input("Please enter the date of the expense (dd-mm-YYYY): ")
            datetime.strptime(date, "%d-%m-%Y")
            return date
        except ValueError:
            print("Please provide a valid date.")


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


def absense_of_category(expenses_manager, certain_category):
    for expense in expenses_manager:
        if certain_category in expense["category"]:
            return False
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


def add_expenses(expenses_manager):
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
    data_absense = check_if_data_exists(expenses_manager)
    if data_absense:
        return
    for expense in expenses_manager:
        expense_display(expense)


def show_expenses_by_category(expenses_manager):
    data_absense = check_if_data_exists(expenses_manager)
    if data_absense:
        return
    print_count = 0
    certain_category = input(
        "Please enter the certain category you want to inspect: ").title().strip()
    for expense in expenses_manager:
        if certain_category == expense["category"]:
            expense_display(expense)
            print_count += 1
    if not print_count:
        print(
            f"There is no {certain_category} categorie in the list at the moment")


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
        elif input_choice == 8:
            save_expenses(expenses_manager)
        elif input_choice == 9:
            print("Thank you for using the Expense Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()
