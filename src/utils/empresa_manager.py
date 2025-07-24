import pandas as pd
import os
from datetime import datetime, timedelta
import uuid

CSV_PATH = "empresas.csv"

def load_empresas():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, dtype=str)
    else:
        return pd.DataFrame(columns=["id", "nome", "email", "senha", "chave", "data_cadastro", "trial_expira_em"])

def save_empresa(nome, email, senha):
    df = load_empresas()
    data_cadastro = datetime.today().date()
    trial_expira_em = data_cadastro + timedelta(days=15)
    chave = str(uuid.uuid4())[:8]  # Chave gerada automaticamente
    nova_empresa = {
        "id": len(df) + 1,
        "nome": nome,
        "email": email,
        "senha": senha,
        "chave": chave,
        "data_cadastro": data_cadastro.strftime("%Y-%m-%d"),
        "trial_expira_em": trial_expira_em.strftime("%Y-%m-%d")
    }
    df = pd.concat([df, pd.DataFrame([nova_empresa])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    return chave

def autentica_empresa(email, senha):
    df = load_empresas()
    email = str(email).strip()
    senha = str(senha).strip()
    empresa = df[(df['email'] == email) & (df['senha'] == senha)]
    if not empresa.empty:
        return empresa.iloc[0].to_dict()
    return None