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

    datas_validas = pd.to_datetime(transactions['data'], errors='coerce').dropna()
    if not datas_validas.empty:
        min_date = datas_validas.min().date()
        max_date = datas_validas.max().date()
        # Últimos 7 dias ou todo o range disponível
        if (max_date - min_date).days >= 6:
            default_start = max_date - datetime.timedelta(days=6)
        else:
            default_start = min_date
        default_end = max_date
    else:
        today = datetime.date.today()
        min_date = today
        max_date = today
        default_start = today
        default_end = today

    def sanitize_range(start, end, min_date, max_date):
        if start < min_date:
            start = min_date
        if end > max_date:
            end = max_date
        if start > end:
            start = min_date
            end = max_date
        return start, end

    try:
        start_date, end_date = st.date_input(
            "Filtrar transações por intervalo de datas",
            value=(default_start, default_end),
            min_value=min_date,
            max_value=max_date
        )
        start_date, end_date = sanitize_range(start_date, end_date, min_date, max_date)
    except Exception:
        start_date, end_date = default_start, default_end

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