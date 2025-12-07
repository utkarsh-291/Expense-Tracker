import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import database
import ai_helper

st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

def main():
    st.title("Personal Finance Analytics Dashboard")
    
    database.initialize_db()

    menu = ["Add Expense", "AI Assistant", "View Data", "Analytics", "Manage"]    
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Expense":
        st.subheader("Add a New Transaction")
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date")
            category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
        
        with col2:
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            description = st.text_input("Description (Optional)")

        if st.button("Add Expense"):
            database.add_expense(date, category, amount, description)
            st.success(f"Added {category} expense of ${amount}!")

    elif choice == "AI Assistant":
        st.subheader("AI Smart Add")
        st.write("Type naturally, e.g., *'I spent 500 rupees on pizza yesterday'*")
        
        user_text = st.text_input("Tell the AI about your expense:")
        
        if st.button("Parse with AI"):
            if user_text:
                with st.spinner("AI is thinking..."):
                    data, error = ai_helper.parse_expense_with_ai(user_text)
                
                if error:
                    st.error(error)
                else:
                    st.success("AI extracted the details!")
                    st.json(data) 
                    st.session_state['ai_data'] = data
            else:
                st.warning("Please enter some text.")

        if 'ai_data' in st.session_state:
            data = st.session_state['ai_data']
            if st.button("Confirm & Save to DB"):
                database.add_expense(data['date'], data['category'], data['amount'], data['description'])
                st.success("Saved successfully!")
                del st.session_state['ai_data']

    elif choice == "View Data":
        st.subheader("Transaction History")
        rows = database.get_all_expenses()
        
        if rows:
            df = pd.DataFrame([dict(row) for row in rows])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses found. Add some first!")

    elif choice == "Analytics":
        st.subheader("Spending Analysis")
        conn = database.get_connection()
        df = pd.read_sql_query("SELECT * FROM expenses", conn)
        conn.close()

        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            
            # KPI Metrics
            total_spent = df['amount'].sum()
            avg_spent = df['amount'].mean()
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Spent", f"${total_spent:,.2f}")
            kpi2.metric("Average Transaction", f"${avg_spent:,.2f}")
            kpi3.metric("Total Transactions", len(df))
            
            st.divider()

            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Spending by Category")
                cat_sum = df.groupby('category')['amount'].sum()
                fig, ax = plt.subplots()
                ax.pie(cat_sum, labels=cat_sum.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal') 
                st.pyplot(fig)
            
            with col2:
                st.markdown("### Daily Spending Trend")
                daily_sum = df.groupby('date')['amount'].sum()
                st.line_chart(daily_sum)

        else:
            st.warning("Not enough data to generate analysis.")

    elif choice == "Manage":
        st.subheader("Manage Expenses")
        rows = database.get_all_expenses()
        if rows:
            df = pd.DataFrame([dict(row) for row in rows])
            st.dataframe(df)
            
            delete_id = st.number_input("Enter ID to Delete", min_value=1, step=1)
            if st.button("Delete Expense"):
                database.delete_expense(delete_id)
                st.warning(f"Expense ID {delete_id} deleted (if it existed). Refresh to see changes.")
        else:
            st.info("Nothing to delete.")

if __name__ == '__main__':
    main()