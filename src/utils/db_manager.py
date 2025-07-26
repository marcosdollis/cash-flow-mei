import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2

load_dotenv()  # Loads variables from .env

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def get_connection():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

def load_transactions():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()
    return df

def save_transaction(transaction):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (tipo, data, valor, descricao, empresa) VALUES (%s, %s, %s, %s, %s)",
        (transaction['tipo'], transaction['data'], transaction['valor'], transaction['descricao'], transaction['empresa'])
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_transaction(row_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = %s", (row_id,))
    conn.commit()
    cur.close()
    conn.close()

def load_empresas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM empresas", conn)
    conn.close()
    return df

def save_empresa(empresa):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO empresas (nome, chave, data_cadastro, trial_expira_em, email, senha) VALUES (%s, %s, %s, %s, %s, %s)",
        (empresa['nome'], empresa['chave'], empresa['data_cadastro'], empresa['trial_expira_em'], empresa['email'], empresa['senha'])
    )
    conn.commit()
    cur.close()
    conn.close()

def update_transaction(row_id, tipo, data, valor, descricao):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE transactions SET tipo=%s, data=%s, valor=%s, descricao=%s WHERE id=%s",
        (tipo, data, valor, descricao, int(row_id))  # Conversão aqui
    )
    conn.commit()
    cur.close()
    conn.close()

# Testando a conexão
try:
    conn = get_connection()
    print("Conexão OK!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")