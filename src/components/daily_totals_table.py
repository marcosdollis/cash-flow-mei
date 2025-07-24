from datetime import datetime
import pandas as pd
import streamlit as st

def daily_totals_table(transactions):
    if transactions.empty:
        st.write("No transactions recorded.")
        return

    transactions['date'] = pd.to_datetime(transactions['date'])
    daily_totals = transactions.groupby(transactions['date'].dt.date).sum().reset_index()
    daily_totals.columns = ['Date', 'Total']

    st.subheader("Daily Total of Transactions")
    st.dataframe(daily_totals)

def display_daily_totals_table(df):
    # Agrupa por data e soma os valores
    daily_totals = df.groupby('data')['valor'].sum().reset_index()
    st.subheader("Somatório por dia de lançamento")
    st.dataframe(daily_totals)