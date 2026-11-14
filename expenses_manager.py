import string
import random
from datetime import datetime
import json
import re
import math


def deletion_menu_choice():
    valid_menu_choices = "1", "2", "3", "4", "q"
    while True:
        deletion_choice = input("""  
        ===== SELECT YOUR DELETION METHOD ====
1. By Unique ID
2. By entire Month or Year
3. By entire Categoty
4. By Description
q. To go back to main menu.

Select the number of method you prefer: """).strip()
        if deletion_choice in valid_menu_choices:
            return deletion_choice
        else:
            print("""
Please select a valid method.""")


def take_only_float(input_string):
    while True:
        try:
            valid_input = float(input(input_string))
            if valid_input <= 0 or not math.isfinite(valid_input):
                raise ValueError
            return valid_input
        except ValueError:
            print("Please enter a valid input.")


def filter_expenses_by_category(expenses_manager, prefered_category):
    recorded_expenses = []
    future_expenses = []
    now = datetime.now()
    for expense in expenses_manager:
        if expense["category"] == prefered_category:
            date = datetime.strptime(expense["date"], "%d-%m-%Y")
            if date <= now:
                recorded_expenses.append(expense)
            else:
                future_expenses.append(expense)
    return recorded_expenses, future_expenses


def filter_expenses_by_date(expenses_manager, input_year, choice_for_month, input_month):
    date_filtered_expenses = []
    for expense in expenses_manager:
        expense_date = datetime.strptime(expense["date"], "%d-%m-%Y")
        matches_year = False
        matches_month = False
        if input_year.year == expense_date.year:
            matches_year = True
        if choice_for_month == "y" and input_month.month == expense_date.month:
            matches_month = True
        if matches_year and (choice_for_month == "n" or matches_month):
            date_filtered_expenses.append(expense)
    return date_filtered_expenses


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
            elif choice == "year":
                input_year = input("Year(YYYY): ")
                input_year = datetime.strptime(
                    f"{input_year}-12-31", "%Y-%m-%d")
                return input_year
            elif choice == "month":
                input_month = input("Month(mm): ")
                input_month = datetime.strptime(input_month, "%m")
                return input_month
        except ValueError:
            print("Please provide valid dates.")


def valid_menu_choices(input_string):
    while True:
        try:
            valid_input = int(input(input_string))
            if 0 < valid_input <= 7:
                return valid_input
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid number between your choices.")


def valid_period_choice(input_string):
    valid_choices = ["P", "F", "B"]
    while True:
        choice = input(input_string).upper().strip()
        if choice in valid_choices:
            return choice
        else:
            print("Please enter a valid choice.")


def check_if_data_exists(expenses_manager):
    if not expenses_manager:
        print("There are no stored expenses at the moment.")
        return True


def valid_display_mode(display_mode):
    valid_choices = ["category_deletion", "date_deletion", "analyze"]
    try:
        if display_mode in valid_choices:
            return True
        else:
            raise ValueError(
                "Unsupported display mode. Please contact the developer to issue a fix.")
    except ValueError as display_error:
        print(display_error)
        return False


def yes_no_answer(expresion):
    valid_choices = ["y", "n"]
    while True:
        choice = input(expresion).lower().strip()
        if choice not in valid_choices:
            print("Please enter a valid choice.")
        else:
            return choice


def category_input(expenses_manager):
    prefered_category = input(
        "Please enter the prefered category: ").title().strip()
    for expense in expenses_manager:
        if prefered_category == expense["category"]:
            break
    else:
        return None
    return prefered_category


def find_expense_by_id(expenses_manager, id_selection):
    for expense in expenses_manager:
        if expense["id"] == id_selection:
            return expense
    return None


def expense_display(expense):
    print(f"""ID: {expense["id"]}
Amount: {expense["amount"]:.2f}€
Description: {expense["description"]}
Date: {expense["date"]}
Category: {expense["category"]}
              """)


def future_expense_display(future_expenses):
    print(f"""
Upcoming expenses found: {len(future_expenses)}
Upcoming expenses total amount: {sum(expense["amount"] for expense in future_expenses):.2f}€
              """)


def yearly_display_preview(yearly_expenses, yearly_expense_date, display_mode, show_yearly_total):
    print(f"""
===== {yearly_expense_date} =====
                      """)
    total_yearly_amount = 0
    for month in range(12, 0, -1):
        total_monthly_amount = 0
        monthly_expenses = []
        coverted_month = datetime.strptime(str(month), "%m")
        for yearly_expense in yearly_expenses:
            yearly_expense_date = datetime.strptime(
                yearly_expense["date"], "%d-%m-%Y")
            if coverted_month.month == yearly_expense_date.month:
                total_monthly_amount += yearly_expense["amount"]
                monthly_expenses.append(yearly_expense)
        total_yearly_amount += total_monthly_amount
        if monthly_expenses:
            print(f"""
> {coverted_month.strftime("%B")}
                      """)
            for monthly_expense in monthly_expenses:
                if display_mode == "analyze":
                    print(
                        f"""{monthly_expense["date"]} | {monthly_expense["description"]} | {monthly_expense["amount"]:.2f}€
""")
                elif display_mode == "date_deletion":
                    print(
                        f"""{monthly_expense["description"]} | {monthly_expense["amount"]:.2f}€
""")
                elif display_mode == "category_deletion":
                    print(
                        f"""{monthly_expense["category"]} | {monthly_expense["amount"]:.2f}€
""")

            if total_monthly_amount:
                print(f"Total Monthly amount: {total_monthly_amount:.2f}€")
    if total_yearly_amount and show_yearly_total:
        print(f"""
===============================
Total Yearly amount: {total_yearly_amount:.2f}€
                      """)


def display_expenses_summary(matching_expenses, display_mode, show_yearly_total=True):
    valid_pass = valid_display_mode(display_mode)
    if not valid_pass:
        print("This feature is temporarily unavailable. You can use the rest of the features normally.")
        return False
    if not matching_expenses:
        print("No expenses found to display.")
        return
    sort_expenses(matching_expenses)
    yearly_expenses = []
    grand_total_amount = sum(expense["amount"]
                             for expense in matching_expenses)
    for expense in matching_expenses:
        expense_date = datetime.strptime(
            expense["date"], "%d-%m-%Y")
        if yearly_expenses and expense_date.year == yearly_expense_date.year:
            yearly_expenses.append(expense)
        elif yearly_expenses and expense_date.year != yearly_expense_date.year:
            yearly_display_preview(
                yearly_expenses, yearly_expense_date.year, display_mode, show_yearly_total)
            yearly_expenses.clear()
            yearly_expenses.append(expense)
        else:
            yearly_expenses.append(expense)
        yearly_expense_date = datetime.strptime(
            yearly_expenses[0]["date"], "%d-%m-%Y")
    else:
        yearly_display_preview(
            yearly_expenses, yearly_expense_date.year, display_mode, show_yearly_total)
    print(f"""
======================================================
Occurrences: {len(matching_expenses)}
Grand Total amount: {grand_total_amount:.2f}€
              """)
    return True


def period_selection_statement(matching_expenses, future_expenses, filter_type):
    if matching_expenses and future_expenses:
        period_choice = valid_period_choice(
            f"There are both past and upcoming expenses in this {filter_type}. In which expenses are you interested? ((past)P/(future)F/ or (both)B): ")
        if period_choice == "F":
            return future_expenses
        elif period_choice == "B":
            return matching_expenses + future_expenses
    elif not matching_expenses and future_expenses:
        return future_expenses
    elif not matching_expenses and not future_expenses:
        return False
    return matching_expenses


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


def sort_expenses(expenses_manager):
    expenses_manager.sort(key=lambda expense: datetime.strptime(
        expense["date"], "%d-%m-%Y"), reverse=True)


def search_expenses(expenses_manager):
    filtered_expenses = []
    future_expenses = []
    while True:
        prefered_description = re.findall(
            "[a-z]+", input("Search description: ").lower())
        if prefered_description:
            for expense in expenses_manager:
                expense_description = re.findall(
                    "[a-z]+", expense["description"].lower())
                for description_part in prefered_description:
                    if description_part not in expense_description:
                        break
                else:
                    current_date = datetime.now()
                    expense_date = datetime.strptime(
                        expense["date"], "%d-%m-%Y")
                    if expense_date <= current_date:
                        filtered_expenses.append(expense)
                    else:
                        future_expenses.append(expense)
            return filtered_expenses, future_expenses

        else:
            print("This is not a valid search description.")


def add_expenses(expenses_manager, ):
    amount = take_only_float("Please enter the expense amount: ")
    description = input(
        "Please enter the description of the expense: ").strip()
    date = get_date()
    category = input(
        "Please enter the category of the expense: ").title().strip()
    new_id = generate_id(expenses_manager)
    new_expense = {"id": new_id, "amount": amount,
                   "description": description, "date": date, "category": category}
    expenses_manager.append(new_expense)


def browse_expenses(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    input_year = get_month_year("year")
    choice_for_month = yes_no_answer(
        f"Do you want a specific month in the year {input_year.year}?(y/n): ")
    total_amount = 0
    if choice_for_month == "y":
        input_month = get_month_year("month")
        print(f"""
===== Expenses of {input_month.strftime("%B")} {input_year.year} =====
                   """)
    else:
        print(f"""
===== Expenses of {input_year.year} =====
                   """)
    date_filtered_expenses = filter_expenses_by_date(
        expenses_manager, input_year, choice_for_month, input_month if choice_for_month == "y" else None)
    for expense in date_filtered_expenses:
        expense_display(expense)
        total_amount += expense["amount"]
    if choice_for_month == "y":
        if total_amount:
            print(f"Total monthly amount: {total_amount:.2f}€")
        else:
            print(
                f"The month {input_month.strftime("%B")} has no recorded expenses.")
    else:
        if total_amount:
            print(f"Total yearly amount: {total_amount:.2f}€")
        else:
            print(f"The year {input_year.year} has no recorded expenses.")


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
    if prefered_category is None:
        creation_choice = yes_no_answer(
            "There are no matching category results. Do you want to create a new expense with this category? (y/n): ")
        if creation_choice == "y":
            return creation_choice
        else:
            print("You are now going back to main menu.")
            return creation_choice
    while True:
        if continue_choice == "y":
            current_date = year_of_choice
        yearly_total_amount = 0
        categorized_expenses, future_expenses = filter_expenses_by_category(
            expenses_manager, prefered_category)
        yearly_categorized_expenses = []
        for expense in categorized_expenses:
            expense_date = datetime.strptime(expense["date"], "%d-%m-%Y")
            if current_date.year == expense_date.year:
                yearly_total_amount += expense["amount"]
                yearly_categorized_expenses.append(expense)
        if yearly_categorized_expenses:
            for month in range(1, 13):
                converted_month = datetime.strptime(str(month), "%m")
                monthly_expenses = []
                monthly_total_amount = 0
                for expense in yearly_categorized_expenses:
                    expense_date = datetime.strptime(
                        expense["date"], "%d-%m-%Y")
                    if converted_month.month == expense_date.month:
                        monthly_total_amount += expense["amount"]
                        monthly_expenses.append(expense)
                if monthly_total_amount:
                    print(f"""
===== EXPENSES OF {converted_month.strftime('%B')}-{expense_date.year} =====
                      """)
                    for expense in monthly_expenses:
                        expense_display(expense)
                    print(f"Total Monthly amount: {monthly_total_amount:.2f}€")
            print(f"""
=======================================================
    Total Yearly amount: {yearly_total_amount:.2f}€""")
        else:
            print(
                f"There are no expenses in the category '{prefered_category}' for the year {current_date.year} until now.")
        if current_date.year == datetime.now().year:
            if future_expenses:
                print(f"""
You have {len(future_expenses)} upcoming expenses in the category '{prefered_category}' worth a total amount of {sum(expense["amount"] for expense in future_expenses):.2f}€.""")
        continue_choice = yes_no_answer(
            "Do you want to inspect the category for another year?(y/n): ")
        if continue_choice == "n":
            break
        year_of_choice = get_month_year("year")


def analyze_expenses(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return
    filtered_expenses, future_expenses = search_expenses(expenses_manager)
    if filtered_expenses:
        executed = display_expenses_summary(filtered_expenses, "analyze")
        if not executed:
            return
        if future_expenses:
            future_expense_display(future_expenses)
    elif not filtered_expenses and future_expenses:
        print("Recorded expenses not found.")
        future_expense_display(future_expenses)
    else:
        print("No matching expenses were found.")


def delete_expense(expenses_manager):
    data_absence = check_if_data_exists(expenses_manager)
    if data_absence:
        return False
    deletion_choice = deletion_menu_choice()
    if deletion_choice == "1":
        id_selection = input("Unique ID: ").strip()
        matching_expense = find_expense_by_id(expenses_manager, id_selection)
        if matching_expense:
            print("""
Your matching expense:
                  """)
            expense_display(matching_expense)
            matching_expenses = [matching_expense]
        else:
            print("No expense found with the provided ID.")
            return False
    elif deletion_choice == "2":
        input_year = get_month_year("year")
        yearly_matches = filter_expenses_by_date(
            expenses_manager, input_year, "n", None)
        if not yearly_matches:
            print(
                f"There are no matching expenses for the year {input_year.year}")
            return False
        choice_for_month = yes_no_answer(
            f"Do you want a specific month in the year {input_year.year}?(y/n): ")
        if choice_for_month == "y":
            input_month = get_month_year("month")
        matching_expenses = filter_expenses_by_date(
            expenses_manager, input_year, choice_for_month, input_month if choice_for_month == "y" else None)
        current_date = datetime.now()
        if input_year.year == current_date.year:
            recorded_expenses = [expense for expense in matching_expenses if datetime.strptime(
                expense["date"], "%d-%m-%Y") <= current_date]
            future_expenses = [expense for expense in matching_expenses if datetime.strptime(
                expense["date"], "%d-%m-%Y") > current_date]
            matching_expenses = period_selection_statement(
                recorded_expenses, future_expenses, "date range")
        if not matching_expenses:
            if choice_for_month == "y":
                print(
                    f"There are no expenses recorded in {datetime.strftime(input_month, '%B')} {input_year.year}.")
            else:
                print(f"There are no expenses recorded in {input_year.year}.")
            return False
        executed = display_expenses_summary(
            matching_expenses, "date_deletion", show_yearly_total=(choice_for_month == "n"))
        if not executed:
            return False
    elif deletion_choice == "3":
        deletion_catecory = category_input(expenses_manager)
        matching_expenses, future_expenses = filter_expenses_by_category(
            expenses_manager, deletion_catecory)
        matching_expenses = period_selection_statement(
            matching_expenses, future_expenses, "category")
        if not matching_expenses:
            print(f"No eligible expenses found for this category.")
            return False
        executed = display_expenses_summary(
            matching_expenses, "category_deletion")
        if not executed:
            return False
    elif deletion_choice == "4":
        matching_expenses, future_expenses = search_expenses(expenses_manager)
        matching_expenses = period_selection_statement(
            matching_expenses, future_expenses, "description")
        if not matching_expenses:
            print(f"No eligible expenses found for this description.")
            return False
        executed = display_expenses_summary(matching_expenses, "date_deletion")
        if not executed:
            return False
    else:
        return False
    if matching_expenses:
        delete_confirm = yes_no_answer(
            "Are you sure you want to proceed with this deletion?(y/n) ")
        if delete_confirm == "y":
            for expense in matching_expenses:
                expenses_manager.remove(expense)
            print("Expense deleted successfully.")
            return True
    print("Deletion canceled. You will now be redirected to the main menu.")
    return False


def display_menu():
    print(
        """  ===== EXPENSE MANAGEMENT SYSTEM =====

        1. Add Expense
        2. Browse Expenses
        3. Monthly Overview
        4. Category Breakdown
        5. Analyze Expenses
        6. Delete Expense
        7. Exit""")


def main():
    expenses_manager = load_expenses()
    display_menu()
    while True:

        input_choice = valid_menu_choices("Choose your option (1-7): ")

        if input_choice == 1:
            add_expenses(expenses_manager)
            sort_expenses(expenses_manager)
            save_expenses(expenses_manager)
        elif input_choice == 2:
            browse_expenses(expenses_manager)
        elif input_choice == 3:
            monthly_overview(expenses_manager)
        elif input_choice == 4:
            creation_choice = category_breakdown(expenses_manager)
            if creation_choice == "y":
                add_expenses(expenses_manager)
                sort_expenses(expenses_manager)
                save_expenses(expenses_manager)
        elif input_choice == 5:
            analyze_expenses(expenses_manager)
        elif input_choice == 6:
            changes_made = delete_expense(expenses_manager)
            if changes_made:
                save_expenses(expenses_manager)
        elif input_choice == 7:
            print("Thank you for using the Expense Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()
