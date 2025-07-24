import streamlit as st

def display_transactions_table(transactions, start_edit_callback, delete_transaction_callback):
    st.subheader("Transações cadastradas")
    if transactions.empty:
        st.info("Nenhuma transação cadastrada.")
        return

    # Ajuste das larguras das colunas: últimas colunas maiores para os botões
    for idx, row in transactions.iterrows():
        cols = st.columns([1, 2, 2, 2, 3, 2, 2])
        cols[0].write(str(row['id'])[:8])
        cols[1].write(row['tipo'])
        cols[2].write(row['data'])
        cols[3].write(f"R$ {row['valor']:.2f}")
        cols[4].write(row['descricao'])
        if cols[5].button("Editar", key=f"edit_{row['id']}"):
            start_edit_callback(row['id'])
            st.rerun()
        if cols[6].button("Excluir", key=f"delete_{row['id']}"):
            delete_transaction_callback(row['id'])