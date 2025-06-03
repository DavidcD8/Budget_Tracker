import json  # Allows us to save/load data in JSON format (like a dictionary)
import os    # Helps check if the file exists

# This is the name of the file where we’ll store the data
DATA_FILE = "budget_data.json"

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
def add_transaction(data, amount, description):
    # Store this transaction in our list
    data["transactions"].append({
        "amount": amount,
        "description": description
    })
    # Update the balance
    data["balance"] += amount
    # Save the updated data to file
    save_data(data)
    # Print a confirmation
    print(f"Transaction added. New balance: €{data['balance']:.2f}")

# Show all transactions and the current balance
def show_summary(data):
    print("\n--- Transaction History ---")
    for t in data["transactions"]:
        sign = "+" if t["amount"] > 0 else "-"
        print(f"{sign}€{abs(t['amount']):.2f} | {t['description']}")
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
        print("3. Show Summary")
        print("4. Exit")

        # Get user input
        choice = input("Choose an option: ")

        # Based on input, do something
        if choice == "1":
            amount = float(input("Enter income amount: "))
            desc = input("Description: ")
            add_transaction(data, amount, desc)
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            desc = input("Description: ")
            add_transaction(data, -amount, desc)  # Expenses are stored as negative numbers
        elif choice == "3":
            show_summary(data)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# This tells Python to run main() only if the script is run directly
if __name__ == "__main__":
    main()
