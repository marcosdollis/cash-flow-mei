import streamlit as st
from datetime import datetime
import uuid

def transaction_form(save_transaction):
    st.header("Registro de Transações")
    
    transaction_type = st.selectbox("Tipo de Transação", ["entrada", "saída"], index=0)
    transaction_date = st.date_input("Data", datetime.today())
    value = st.number_input("Valor", min_value=0.0, format="%.2f")
    description = st.text_input("Descrição")
    
    if st.button("Salvar"):
        transaction = {
            "type": transaction_type,
            "date": transaction_date,
            "value": value,
            "description": description
        }
        save_transaction(transaction)

def create_transaction_form():
    with st.form("transaction_form"):
        tipo = st.radio("Tipo", ["Entrada", "Saída"], index=0)
        data = st.date_input("Data", value=datetime.today())
        valor = st.number_input("Valor", min_value=None, format="%.2f")
        descricao = st.text_input("Descrição")
        submitted = st.form_submit_button("Salvar")
        if submitted:
            transaction = {
                "id": str(uuid.uuid4()),
                "tipo": tipo,
                "data": data.strftime("%Y-%m-%d"),
                "valor": valor,
                "descricao": descricao
            }
            # Ajuste o valor para transações de saída
            if transaction["tipo"] == "Saída":
                transaction["valor"] = -abs(transaction["valor"])
            return transaction
    return None