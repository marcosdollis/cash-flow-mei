import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

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

def load_empresas():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM empresas", conn)
    conn.close()
    return df

def save_empresa(nome, email, senha):
    data_cadastro = datetime.today().date()
    trial_expira_em = data_cadastro + timedelta(days=15)
    chave = str(uuid.uuid4())[:8]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO empresas (nome, email, senha, chave, data_cadastro, trial_expira_em) VALUES (%s, %s, %s, %s, %s, %s)",
        (nome, email, senha, chave, data_cadastro, trial_expira_em)
    )
    conn.commit()
    cur.close()
    conn.close()
    return chave

def autentica_empresa(email, senha):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM empresas WHERE email = %s AND senha = %s",
        (str(email).strip(), str(senha).strip())
    )
    empresa = cur.fetchone()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    if empresa:
        return dict(zip(columns, empresa))
    return None