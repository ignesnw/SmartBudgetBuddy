import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_manager import DataManager
from ai_advisor import AIAdvisor
from utils import calculate_savings, format_currency

# Initialize
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
if 'ai_advisor' not in st.session_state:
    st.session_state.ai_advisor = AIAdvisor()

# Page config
st.set_page_config(
    page_title="Personal Finance Advisor",
    page_icon="💰",
    layout="wide"
)

# Title and description
st.title("💰 Personal Finance Advisor")
st.markdown("""
Track your daily spending and get AI-powered suggestions for your savings!
Input your daily budget and actual expenses to see how much you can save.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Daily Budget & Expenses")

    # Date selector (default to today)
    selected_date = st.date_input(
        "Select Date",
        datetime.now().date()
    )

    # Budget and expense inputs
    daily_budget = st.number_input(
        "Daily Budget (Rp)",
        min_value=0,
        value=100000,
        step=50000,
        format="%d"
    )

    daily_expense = st.number_input(
        "Daily Expense (Rp)",
        min_value=0,
        value=0,
        step=50000,
        format="%d"
    )

    if st.button("Save Entry"):
        st.session_state.data_manager.add_transaction(
            selected_date,
            daily_budget,
            daily_expense
        )
        st.success("Entry saved successfully!")

# Main content area - Two columns layout
savings_col, suggestions_col = st.columns([1, 2])

# Left column - Savings Overview
with savings_col:
    st.header("💳 Savings Overview")

    df = st.session_state.data_manager.get_transactions()
    if not df.empty:
        # Calculate weekly savings
        weekly_data = df[df['date'] >= (datetime.now().date() - timedelta(days=7))]
        weekly_savings = calculate_savings(weekly_data)

        # Calculate monthly savings
        monthly_data = df[df['date'] >= (datetime.now().date() - timedelta(days=30))]
        monthly_savings = calculate_savings(monthly_data)

        # Display savings metrics
        st.subheader("Weekly Savings")
        st.metric("This Week", format_currency(weekly_savings))

        st.subheader("Monthly Savings")
        st.metric("This Month", format_currency(monthly_savings))

        # Recent transactions
        st.subheader("Recent Transactions")
        display_df = df.copy()
        display_df['budget'] = display_df['budget'].apply(format_currency)
        display_df['expense'] = display_df['expense'].apply(format_currency)

        st.dataframe(
            display_df.sort_values('date', ascending=False).head(5),
            use_container_width=True
        )
    else:
        st.info("Start by adding your daily budget and expenses!")

# Right column - AI Suggestions
with suggestions_col:
    st.header("💡 Investment Recommendations")

    if not df.empty:
        tab1, tab2 = st.tabs(["Weekly Investment Ideas", "Monthly Investment Ideas"])

        with tab1:
            if weekly_savings > 0:
                suggestions = st.session_state.ai_advisor.get_suggestions(weekly_savings)
                st.markdown(suggestions)
            else:
                st.info("Add this week's transactions to get personalized suggestions!")

        with tab2:
            if monthly_savings > 0:
                suggestions = st.session_state.ai_advisor.get_suggestions(monthly_savings)
                st.markdown(suggestions)
            else:
                st.info("Add this month's transactions to get personalized suggestions!")
    else:
        st.info("Add some transactions to get personalized investment suggestions!")