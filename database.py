import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"

def get_connection():
    """Connects to the database and ensures rows act like dictionaries."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows accessing data by column name
    return conn

def initialize_db():
    """Creates the table if it doesn't exist."""
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, category, amount, description):
    """Inserts a new expense into the database."""
    conn = get_connection()
    try:
        conn.execute('''
            INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (date, category, amount, description))
        conn.commit()
        print("✅ Expense added successfully!")
    except Exception as e:
        print(f"❌ Error adding expense: {e}")
    finally:
        conn.close()

def get_all_expenses():
    """Fetches all expenses, sorted by newest first."""
    conn = get_connection()
    rows = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    """Deletes an expense by its ID."""
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        # cursor.rowcount tells us how many rows were affected
        if cursor.rowcount > 0:
            print("✅ Expense deleted successfully!")
        else:
            print("❌ Error: ID not found.")
    except Exception as e:
        print(f"❌ Error deleting expense: {e}")
    finally:
        conn.close()

def update_expense(expense_id, date, category, amount, description):
    """Updates an existing expense by its ID."""
    conn = get_connection()
    try:
        cursor = conn.execute('''
            UPDATE expenses 
            SET date = ?, category = ?, amount = ?, description = ?
            WHERE id = ?
        ''', (date, category, amount, description, expense_id))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Expense updated successfully!")
        else:
            print("❌ Error: ID not found.")
    except Exception as e:
        print(f"❌ Error updating expense: {e}")
    finally:
        conn.close()