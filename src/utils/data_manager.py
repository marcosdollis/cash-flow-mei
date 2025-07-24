import pandas as pd
import os

CSV_PATH = "transactions.csv"

def load_transactions():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        # Cria um DataFrame vazio com as colunas corretas
        return pd.DataFrame(columns=["id", "tipo", "data", "valor", "descricao"])

def save_transactions(df):
    df.to_csv(CSV_PATH, index=False)