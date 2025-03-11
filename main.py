import streamlit as st
import pandas as pd
import plotly.express as px
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

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Display transactions and savings
    st.subheader("Your Financial Overview")

    df = st.session_state.data_manager.get_transactions()
    if not df.empty:
        # Calculate savings
        total_savings = calculate_savings(df)

        # Display metrics
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.metric("Total Savings", format_currency(total_savings))
        with metrics_col2:
            weekly_savings = calculate_savings(
                df[df['date'] >= (datetime.now().date() - timedelta(days=7))]
            )
            st.metric("Weekly Savings", format_currency(weekly_savings))
        with metrics_col3:
            monthly_savings = calculate_savings(
                df[df['date'] >= (datetime.now().date() - timedelta(days=30))]
            )
            st.metric("Monthly Savings", format_currency(monthly_savings))

        # Plotting
        fig = px.line(
            df,
            x='date',
            y=['budget', 'expense'],
            title='Budget vs Expenses Over Time (in Rupiah)'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display transactions table
        st.subheader("Recent Transactions")

        # Format currency columns
        display_df = df.copy()
        display_df['budget'] = display_df['budget'].apply(format_currency)
        display_df['expense'] = display_df['expense'].apply(format_currency)

        st.dataframe(
            display_df.sort_values('date', ascending=False),
            use_container_width=True
        )
    else:
        st.info("No transactions recorded yet. Start by adding your daily budget and expenses!")

with col2:
    # AI Suggestions based on weekly/monthly savings
    st.subheader("💡 AI Savings Suggestions")

    if not df.empty:
        # Use weekly or monthly savings for suggestions
        weekly_tab, monthly_tab = st.tabs(["Weekly Savings", "Monthly Savings"])

        with weekly_tab:
            if weekly_savings > 0:
                suggestions = st.session_state.ai_advisor.get_suggestions(weekly_savings)
                st.markdown(suggestions)
            else:
                st.info("Add some transactions to get weekly savings suggestions!")

        with monthly_tab:
            if monthly_savings > 0:
                suggestions = st.session_state.ai_advisor.get_suggestions(monthly_savings)
                st.markdown(suggestions)
            else:
                st.info("Add some transactions to get monthly savings suggestions!")
    else:
        st.info("Add some transactions to get personalized savings suggestions!")