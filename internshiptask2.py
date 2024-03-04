import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

# Initialize SQLite database
conn = sqlite3.connect('budget_tracker.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY, type TEXT, category TEXT, amount REAL, date TEXT)''')
conn.commit()

# Function to record income or expense
def record_transaction(transaction_type, category, amount):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
              (transaction_type, category, amount, current_date))
    conn.commit()

# Function to calculate remaining budget
def calculate_budget():
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = c.fetchone()[0] or 0
    remaining_budget = income - expenses
    return remaining_budget

# Function to analyze expenses by category
def analyze_expenses():
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    expense_data = c.fetchall()
    return expense_data

# Function to handle button click event for recording transaction
def record_transaction_click():
    transaction_type = transaction_type_var.get()
    category = category_entry.get()
    amount = float(amount_entry.get())
    record_transaction(transaction_type, category, amount)
    update_budget_label()

# Function to update budget label
def update_budget_label():
    remaining_budget = calculate_budget()
    budget_label.config(text=f"Remaining Budget: {remaining_budget}")

# Function to handle button click event for analyzing expenses
def analyze_expenses_click():
    expense_data = analyze_expenses()
    expense_analysis_text.delete('1.0', tk.END)
    for category, amount in expense_data:
        expense_analysis_text.insert(tk.END, f"{category}: {amount}\n")

# Function to save transactions to a text file
def save_to_file():
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    with open("transaction_history.txt", "w") as file:
        file.write("Transaction History:\n")
        for transaction in transactions:
            file.write(f"{transaction[4]} - {transaction[1]} - {transaction[2]} - {transaction[3]}\n")
    file_name_label.config(text="File saved as: transaction_history.txt\nSearch the file on your device with the mentioned name")

# Function to reset data
def reset_data():
    c.execute("DELETE FROM transactions")
    conn.commit()
    update_budget_label()
    expense_analysis_text.delete('1.0', tk.END)
    file_name_label.config(text="")

# Main window
root = tk.Tk()
root.title("Personal Budget Tracker")

# Transaction type
transaction_type_var = tk.StringVar(root)
transaction_type_label = tk.Label(root, text="Transaction Type:")
transaction_type_label.grid(row=0, column=0, padx=5, pady=5)
transaction_type_combobox = ttk.Combobox(root, textvariable=transaction_type_var, values=["Income", "Expense"])
transaction_type_combobox.grid(row=0, column=1, padx=5, pady=5)

# Category
category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

# Amount
amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Record Transaction button
record_transaction_button = tk.Button(root, text="Record Transaction", command=record_transaction_click)
record_transaction_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Budget label
budget_label = tk.Label(root, text="")
budget_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Analyze Expenses button
analyze_expenses_button = tk.Button(root, text="Analyze Expenses", command=analyze_expenses_click)
analyze_expenses_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Expense Analysis
expense_analysis_label = tk.Label(root, text="Expense Analysis:")
expense_analysis_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
expense_analysis_text = tk.Text(root, height=5, width=30)
expense_analysis_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Save to File button
save_to_file_button = tk.Button(root, text="Save to File", command=save_to_file)
save_to_file_button.grid(row=8, column=0, padx=5, pady=5)
file_name_label = tk.Label(root, text="")
file_name_label.grid(row=8, column=1, padx=5, pady=5)

# Reset Data button
reset_data_button = tk.Button(root, text="Reset Data", command=reset_data)
reset_data_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Update budget label initially
update_budget_label()

root.mainloop()
