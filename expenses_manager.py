def only_numbers(input_string):
    while True:
        try:
            valid_input = int(input(input_string))
            if 0 < valid_input <= 9:
                return valid_input
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid number between your choices.")


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
    while True:

        display_menu()

        input_choice = only_numbers("Choose your option (1-9): ")

        if input_choice == 9:
            print("Thank you for using the Expense Management System. Goodbye!")
            break


if __name__ == "__main__":
    main()
