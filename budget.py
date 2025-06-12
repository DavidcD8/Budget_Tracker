import json  # Allows us to save/load data in JSON format (like a dictionary)
import os    # Helps check if the file exists
import matplotlib.pyplot as plt  # For plotting charts
from datetime import datetime

# This is the name of the file where we’ll store the data
DATA_FILE = "budget_data.json"


def show_expense_chart(data):
    # Filter only expenses (amounts < 0)
    expenses = [t for t in data["transactions"] if t["amount"] < 0]
    if not expenses:
        print("No expenses to show.")
        return

    # Group expenses by category
    categories = {}
    for t in expenses:
        cat = t.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + abs(t["amount"])

    # Prepare data for pie chart
    labels = categories.keys()
    values = categories.values()

    # Create pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.axis("equal")  # Make the pie chart a circle
    plt.tight_layout()
    plt.show()



# Load previous data from file if it exists
def load_data():
    if os.path.exists(DATA_FILE):  # Check if data file already exists
        with open(DATA_FILE, "r") as file:
            return json.load(file)  # Load and return the data from the file
    # If file doesn’t exist, start with default values
    return {"transactions": [], "balance": 0.0}



# Save the data back to the file (after each transaction)
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)  # Pretty-print the data to file


# Add a transaction (income or expense)
def add_transaction(data, amount, description, category,txn_type):
     # Ensure amount is positive or negative based on the type
    if txn_type.lower() == "income":
        amount = abs(amount)
    else:
        amount = -abs(amount)

    date_str = datetime.now().strftime("%Y-%m-%d")
    # Store this transaction in our list
    data["transactions"].append({
        "amount": amount,
        "description": description,
        "category": category,
        "date": date_str,
    })
    # Update the balance
    data["balance"] += amount
    # Save the updated data to file
    save_data(data)
    # Print a confirmation
    print(f"Transaction added. New balance: €{data['balance']:.2f}")




# This function lets the user delete a transaction from the list
def delete_transaction(data):
    if not data["transactions"]:    # If there are no transactions, show a message and return early
        print("No transactions to delete.")
        return
    
    print("\n--- Delete a Transaction ---")
    
    for i, t in enumerate(data["transactions"], start=1):  # i = 1, 2, 3...
        print(f"{i}. €{t['amount']:.2f} | {t['description']} | {t['category']}")

     # Ask the user to choose which number to delete
    try:
        choice = int(input("Enter the number of the transaction to delete: "))

        # Convert to 0-based index and check bounds
        if 1 <= choice <= len(data["transactions"]):
            removed = data["transactions"].pop(choice - 1)  # Delete from the list   

        # Adjust the balance based on what was removed
            data["balance"] -= removed["amount"]
            print(f"Deleted: €{removed['amount']:.2f} | {removed['description']}")

            save_data(data)  # Save changes to file

        else:
            print("Invalid number. Please try again.")

    except ValueError:
        print("Please enter a valid number.")




# Show all transactions and the current balance
def show_summary(data):
    print("\n--- Transaction History ---")
    print("Date       | Amount    | Description     | Category")
    for t in data["transactions"]:
        sign = "+" if t["amount"] > 0 else "-"
        print(f"{t['date']} | {sign}€{abs(t['amount']):7.2f} | {t['description']:<15} | {t.get('category', 'N/A'):<10}")

    print(f"\nCurrent balance: €{data['balance']:.2f}\n")




# The main program loop (user interface)
def main():
    # Load any saved data
    data = load_data()

    # Infinite loop until the user exits
    while True:
        # Display the main menu
        print("\n1. Add Income")
        print("2. Add Expense")
        print("3. Delete Transaction")
        print("4. Show Summary")
        print("5. Show Expense Chart")
        print("6. Exit")

        # Get user input
        choice = input("Choose an option: ")

        # Based on input, do something
        if choice == "1":
            amount = float(input("Enter income amount: "))
            desc = input("Description: ")
            cat = input("Category (e.g., salary, freelance): ")
            add_transaction(data, amount, desc, cat, "income")
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            desc = input("Description: ")
            cat = input("Category: eg: food, salary, bills: ")
            add_transaction(data, amount, desc, cat, "expense")
        elif choice == "3":
            delete_transaction(data)
        elif choice == "4":
            show_summary(data)
        elif choice == "5":
            show_expense_chart(data)

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")





# This tells Python to run main() only if the script is run directly
if __name__ == "__main__":
    main()
