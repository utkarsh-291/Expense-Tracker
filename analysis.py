import pandas as pd
import matplotlib.pyplot as plt
import database

def generate_analysis():
    """Loads data from DB and generates a statistical report and graph."""
    conn = database.get_connection()
    
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()

    if df.empty:
        print()
        print("No data available to analyze yet. Add some expenses first!")
        return

    df['date'] = pd.to_datetime(df['date'])

    print("\n" + "="*40)
    print(" EXPENSE ANALYSIS REPORT")
    print("="*40)

    total_spent = df['amount'].sum()
    average_spent = df['amount'].mean()
    total_transactions = len(df)

    print(f"Total Amount Spent:   ${total_spent:,.2f}")
    print(f"Total Transactions:   {total_transactions}")
    print(f"Average per Spend:    ${average_spent:,.2f}")
    print("-" * 40)

    print("\nSPENDING BY CATEGORY:")
    category_stats = df.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    print(category_stats.to_string())
    print("-" * 40)

    user_choice = input("\nDo you want to see a graph? (y/n): ")
    if user_choice.lower() == 'y':
        print(" Opening Pie Chart...")
        
        plt.figure(figsize=(8, 6))
        plt.pie(category_stats, labels=category_stats.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Total Expenses: ${total_spent:,.2f}')
        plt.axis('equal')
        
        plt.show()