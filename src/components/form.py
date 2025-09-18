import streamlit as st
from datetime import datetime
import uuid

def create_transaction_form():
    # Reset valor_novo se necessário
    if st.session_state.get("reset_valor_novo", False):
        st.session_state.valor_novo = 0.0
        st.session_state.reset_valor_novo = False

    if "valor_novo" not in st.session_state:
        st.session_state.valor_novo = 0.0

    with st.form("transaction_form"):
        tipo = st.radio("Tipo", ["Entrada", "Saída"], index=0)
        data = st.date_input("Data", value=datetime.today())
        valor = st.number_input(
            "Valor",
            min_value=0.0,
            format="%.2f",
            key="valor_novo_cadastro"  # <-- chave única para cadastro
        )
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
            if transaction["tipo"] == "Saída":
                transaction["valor"] = -abs(transaction["valor"])
            st.session_state.reset_valor_novo = True  # Sinaliza para resetar na próxima execução
            return transaction
    return None