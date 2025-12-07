import database
import analysis

def get_user_input():
    """Helper function to get clean data from the user."""
    from datetime import date
    date_entry = input(f"Enter Date (YYYY-MM-DD) [Default: {date.today()}]: ")
    if not date_entry:
        date_entry = str(date.today())
    
    print("\n--- Categories ---")
    categories = {
        '1': 'Food', 
        '2': 'Travel', 
        '3': 'Bills', 
        '4': 'Shopping', 
        '5': 'Other'
    }
    for key, val in categories.items():
        print(f"{key}. {val}")
    
    cat_choice = input("Select Category (1-5): ")
    category = categories.get(cat_choice, "Other")

    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("Invalid amount. Setting to 0.")
        amount = 0.0

    description = input("Enter Description (Optional): ")

    return date_entry, category, amount, description

def view_expenses():
    expenses = database.get_all_expenses()
    if not expenses:
        print("\nNo expenses found yet.")
        return

    print("\n" + "="*50)
    print(f"{'ID':<5} {'Date':<12} {'Category':<10} {'Amount':<10} {'Description'}")
    print("-" * 50)
    
    for row in expenses:
        print(f"{row['id']:<5} {row['date']:<12} {row['category']:<10} {row['amount']:<10.2f} {row['description']}")
    print("="*50 + "\n")

def delete_expense_ui():
    """UI flow for deleting an expense."""
    view_expenses() 
    try:
        ex_id = int(input("Enter the ID of the expense to DELETE: "))
        confirm = input(f"Are you sure you want to delete ID {ex_id}? (y/n): ")
        if confirm.lower() == 'y':
            database.delete_expense(ex_id)
        else:
            print("Operation cancelled.")
    except ValueError:
        print("Invalid ID. Please enter a number.")

def update_expense_ui():
    """UI flow for updating an expense."""
    view_expenses()
    try:
        ex_id = int(input("Enter the ID of the expense to UPDATE: "))
        print(f"\n--- Enter New Details for ID {ex_id} ---")
        data = get_user_input() 
        database.update_expense(ex_id, data[0], data[1], data[2], data[3])
    except ValueError:
        print("Invalid ID. Please enter a number.")

def main():
    database.initialize_db()

    while True:
        print("\nEXPENSE TRACKER MENU")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. 📊 Data Analysis")
        print("6. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            data = get_user_input()
            database.add_expense(data[0], data[1], data[2], data[3])
        
        elif choice == '2':
            view_expenses()

        elif choice == '3':
            delete_expense_ui()

        elif choice == '4':
            update_expense_ui()
        
        elif choice == '5':
            analysis.generate_analysis()
        
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()