import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")  # Defina isso nos secrets do Streamlit Cloud ou .env local

def get_engine():
    return create_engine(DATABASE_URL)

def load_transactions():
    engine = get_engine()
    try:
        return pd.read_sql("SELECT * FROM transacoes", engine)
    except Exception:
        # Se a tabela não existir, retorna DataFrame vazio
        return pd.DataFrame(columns=["id", "tipo", "data", "valor", "descricao", "empresa"])

def save_transaction(transaction):
    engine = get_engine()
    df = pd.DataFrame([transaction])
    df.to_sql("transacoes", engine, if_exists="append", index=False)