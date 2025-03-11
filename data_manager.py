import pandas as pd
from datetime import date
import os

class DataManager:
    def __init__(self):
        self.file_path = "data/transactions.csv"
        self._ensure_data_file()
        
    def _ensure_data_file(self):
        """Ensure the data directory and file exist."""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['date', 'budget', 'expense'])
            df.to_csv(self.file_path, index=False)
    
    def add_transaction(self, date: date, budget: float, expense: float):
        """Add a new transaction to the CSV file."""
        df = self.get_transactions()
        
        # Update existing entry for the date or add new one
        new_row = pd.DataFrame({
            'date': [date],
            'budget': [budget],
            'expense': [expense]
        })
        
        # Remove existing entry for the same date if it exists
        df = df[df['date'] != date]
        
        # Append new row
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Save to CSV
        df.to_csv(self.file_path, index=False)
    
    def get_transactions(self) -> pd.DataFrame:
        """Get all transactions as a DataFrame."""
        try:
            df = pd.read_csv(self.file_path)
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=['date', 'budget', 'expense'])
