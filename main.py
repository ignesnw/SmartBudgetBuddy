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
if 'personal_goal' not in st.session_state:
    st.session_state.personal_goal = "My financial goals and dreams..."

# Page config
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide"
)

# Personal Goals Input
st.text_area(
    "What are your financial goals?",
    value=st.session_state.personal_goal,
    key="personal_goal_input",
    height=100
)

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

# Get transaction data
df = st.session_state.data_manager.get_transactions()

# Calculate savings if data exists
if not df.empty:
    weekly_data = df[df['date'] >= (datetime.now().date() - timedelta(days=7))]
    weekly_savings = calculate_savings(weekly_data)

    monthly_data = df[df['date'] >= (datetime.now().date() - timedelta(days=30))]
    monthly_savings = calculate_savings(monthly_data)

    # Display savings metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("This Week's Savings", format_currency(weekly_savings))
    with col2:
        st.metric("This Month's Savings", format_currency(monthly_savings))

    # Recent transactions in a smaller table
    with st.expander("Recent Transactions"):
        display_df = df.copy()
        display_df['budget'] = display_df['budget'].apply(format_currency)
        display_df['expense'] = display_df['expense'].apply(format_currency)
        st.dataframe(
            display_df.sort_values('date', ascending=False).head(5),
            use_container_width=True
        )

    # Recommendations section
    st.markdown("---")

    # Weekly recommendations
    st.header(f"With your weekly savings of {format_currency(weekly_savings)}, you can...")
    if weekly_savings > 0:
        suggestions = st.session_state.ai_advisor.get_suggestions(weekly_savings)
        st.markdown(suggestions)
    else:
        st.info("Keep tracking your expenses to see what you could do with your savings!")

    # Monthly recommendations
    st.header(f"With your monthly savings of {format_currency(monthly_savings)}, you can...")
    if monthly_savings > 0:
        suggestions = st.session_state.ai_advisor.get_suggestions(monthly_savings)
        st.markdown(suggestions)
    else:
        st.info("Keep tracking your expenses to see what you could do with your savings!")

else:
    st.info("Start by adding your daily budget and expenses!")