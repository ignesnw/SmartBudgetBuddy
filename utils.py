import pandas as pd

def calculate_savings(df: pd.DataFrame) -> float:
    """Calculate total savings from a DataFrame of transactions."""
    total_budget = df['budget'].sum()
    total_expense = df['expense'].sum()
    return total_budget - total_expense

def format_currency(amount: float) -> str:
    """Format amount as Indonesian Rupiah."""
    return f"Rp {amount:,.0f}"