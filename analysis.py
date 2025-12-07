import pandas as pd
import matplotlib.pyplot as plt
import database

def generate_analysis():
    """Loads data from DB and generates a statistical report and graph."""
    conn = database.get_connection()
    
    # 1. Load Data into Pandas DataFrame
    # This replaces writing "SELECT * ..." loops manually
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        print("\n⚠ No data available to analyze yet. Add some expenses first!")
        return

    # Ensure the date column is treated as actual Dates, not text
    df['date'] = pd.to_datetime(df['date'])

    print("\n" + "="*40)
    print("📊 EXPENSE ANALYSIS REPORT")
    print("="*40)

    # 2. Basic Statistics
    total_spent = df['amount'].sum()
    average_spent = df['amount'].mean()
    # We count rows to see total transactions
    total_transactions = len(df)

    print(f"💰 Total Amount Spent:   ${total_spent:,.2f}")
    print(f"🧾 Total Transactions:   {total_transactions}")
    print(f"📉 Average per Spend:    ${average_spent:,.2f}")
    print("-" * 40)

    # 3. Spending by Category (The "Group By" magic)
    print("\n📂 SPENDING BY CATEGORY:")
    # Group data by 'category', sum the 'amount', and sort descending
    category_stats = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    # Print the table
    print(category_stats.to_string())
    print("-" * 40)

    # 4. Visualization (Pie Chart)
    user_choice = input("\nDo you want to see a graph? (y/n): ")
    if user_choice.lower() == 'y':
        print("🎨 Opening Pie Chart...")
        
        plt.figure(figsize=(8, 6))
        # Create a pie chart using the category stats we calculated above
        plt.pie(category_stats, labels=category_stats.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Total Expenses: ${total_spent:,.2f}')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        plt.show()