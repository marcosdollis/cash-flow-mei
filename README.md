# MEI Cash Flow App

This project is a Streamlit application designed to help Microempreendedores Individuais (MEIs) manage their cash flow effectively. It allows users to record transactions, view registered entries, and analyze daily totals.

## Features

- Input form for transactions with fields for:
  - Transaction type (defaulting to "entrada")
  - Today's date
  - Value
  - Description
- Table displaying registered transactions with options to edit values
- Daily totals table to summarize transactions

## Project Structure

```
mei-cashflow-app
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── components
│   │   ├── form.py             # Input form for transactions
│   │   ├── transactions_table.py # Table for registered transactions
│   │   └── daily_totals_table.py # Table for daily totals
│   └── utils
│       └── data_manager.py      # Utility functions for data management
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mei-cashflow-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- Use the input form to add new transactions.
- View and edit existing transactions in the registered entries table.
- Check the daily totals table for a summary of your transactions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.