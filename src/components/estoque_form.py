import streamlit as st
import pandas as pd
from utils.db_manager import save_estoque_item, load_estoque_items

def create_estoque_form():
    if "estoque" not in st.session_state:
        st.session_state.estoque = pd.DataFrame(columns=["nome", "quantidade", "preco_custo", "preco_loja", "markup", "margem_lucro"])

    st.subheader("Novo item de estoque")
    nome = st.text_input("Nome do item")
    quantidade = st.number_input("Quantidade", min_value=0, step=1)
    preco_custo = st.number_input("Preço de custo", min_value=0.0, format="%.2f")
    preco_loja = st.number_input("Preço loja", min_value=0.0, format="%.2f")

    # Cálculo do markup e margem de lucro em tempo real
    markup = ((preco_loja - preco_custo) / preco_custo * 100) if preco_custo > 0 else 0
    margem_lucro = ((preco_loja - preco_custo) / preco_loja * 100) if preco_loja > 0 else 0

    st.info(f"Markup: {markup:.2f}%")
    st.info(f"Margem de Lucro: {margem_lucro:.2f}%")

    if st.button("Salvar") and nome:
        novo_item = {
            "nome": nome,
            "quantidade": quantidade,
            "preco_custo": preco_custo,
            "preco_loja": preco_loja,
            "markup": markup,
            "margem_lucro": margem_lucro,
            "empresa": st.session_state.chave_empresa  # <-- GARANTA QUE ESTE CAMPO EXISTE!
        }
        save_estoque_item(novo_item)
        st.success("Item cadastrado com sucesso!")

    # Exibe os itens cadastrados do banco
    itens = load_estoque_items(st.session_state.chave_empresa)
    if not itens.empty:
        st.subheader("Itens cadastrados")
        st.dataframe(itens)