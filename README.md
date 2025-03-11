# Personal Finance Tracker

A Streamlit-based personal finance app that helps track your daily budget and expenses, providing AI-powered suggestions for your savings.

## Features

- Daily budget and expense tracking
- Weekly and monthly savings calculations
- AI-powered suggestions for savings allocation (investments, travel, education)
- Personal financial goals tracking

## Setup

1. Clone the repository
2. Install dependencies using Python package manager
3. Set up environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key (optional, fallback suggestions available)

## Usage

1. Run the Streamlit app:
```bash
streamlit run main.py
```

2. Access the app in your browser at http://localhost:5000

## Project Structure

```
├── .streamlit/          # Streamlit configuration
├── data/               # Data storage
│   └── transactions.csv
├── main.py            # Main application
├── ai_advisor.py      # AI suggestion generation
├── data_manager.py    # Data handling
└── utils.py           # Utility functions
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
