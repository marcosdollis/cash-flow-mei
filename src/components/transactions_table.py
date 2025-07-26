import streamlit as st
import pandas as pd
import datetime

# Inicializa o estado da sessão para o valor da transação
if 'valor_novo' not in st.session_state:
    st.session_state.valor_novo = 0.0  # valor inicial

def display_transactions_table(transactions, start_edit_callback, delete_transaction_callback):
    st.subheader("Transações cadastradas")
    if transactions.empty:
        st.info("Nenhuma transação cadastrada.")
        return

    # Filtro de intervalo de datas
    datas_unicas = pd.to_datetime(transactions['data']).dt.date
    min_date = datas_unicas.min()
    max_date = datas_unicas.max()

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Garante que yesterday está dentro do range de datas disponíveis
    start_default = yesterday if yesterday >= min_date else min_date
    end_default = today if today <= max_date else max_date

    start_date, end_date = st.date_input(
        "Filtrar transações por intervalo de datas",
        value=(start_default, end_default),
        min_value=min_date,
        max_value=max_date
    )

    # Filtra o DataFrame pelo intervalo selecionado
    mask = (pd.to_datetime(transactions['data']).dt.date >= start_date) & \
           (pd.to_datetime(transactions['data']).dt.date <= end_date)
    df_filtrado = transactions[mask]

    if df_filtrado.empty:
        st.info("Nenhuma transação para o período selecionado.")
        return

    for _, row in df_filtrado.iterrows():
        with st.container():
            cols = st.columns([2, 1])
            with cols[0]:
                st.markdown(f"**Tipo:** {row['tipo']}")
                st.markdown(f"**Data:** {row['data']}")
                st.markdown(f"**Valor:** R$ {row['valor']:.2f}")
                st.markdown(f"**Descrição:** {row['descricao']}")
            with cols[1]:
                st.write("")
                if st.button("Editar", key=f"edit_{row['id']}"):
                    start_edit_callback(row['id'])
                if st.button("Excluir", key=f"del_{row['id']}"):
                    delete_transaction_callback(row['id'])
        st.markdown("---")

with st.form("form_nova_transacao"):
    # ... outros campos ...
    valor = st.number_input("Valor", min_value=0.0, value=st.session_state.valor_novo, format="%.2f", key="valor_novo")
    # ... outros campos ...
    submitted = st.form_submit_button("Salvar")

    if submitted:
        # ... salva a transação ...
        st.session_state.valor_novo = 0.0  # limpa o campo após salvar
        st.success("Transação salva com sucesso!")
        st.rerun()