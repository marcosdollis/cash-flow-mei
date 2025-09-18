import streamlit as st
import pandas as pd
import calendar
from components.form import create_transaction_form
from components.transactions_table import display_transactions_table
from components.daily_totals_table import display_daily_totals_table
from components.estoque_form import create_estoque_form
from utils.data_manager import load_transactions, save_transactions
from utils.empresa_manager import save_empresa, autentica_empresa
import os
import datetime

# Simulação de usuários e empresas
USERS = {
    "empresa1": {"senha": "123", "chave": "EMP001"},
    "empresa2": {"senha": "abc", "chave": "EMP002"},
    "empresa3": {"senha": "senha", "chave": "EMP003"}
}

DATABASE_URL = os.getenv("DATABASE_URL")
USE_DATABASE = True  # Altere para True para usar o banco PostgreSQL

if USE_DATABASE:
    from utils.db_manager import load_transactions, save_transaction
else:
    from utils.data_manager import load_transactions, save_transactions

def login_screen():
    st.title("Login")
    with st.form("form_login"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            empresa = autentica_empresa(email, senha)
            if empresa:
                st.session_state.logged_in = True
                st.session_state.empresa = empresa['nome']
                st.session_state.chave_empresa = empresa['chave']
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
    if st.button("Cadastrar nova empresa"):
        st.session_state.show_cadastro_empresa = True
        st.rerun()

def fluxo_caixa():
    st.title(f"Controle de Fluxo de Caixa - {st.session_state.empresa}")

    if 'transactions' not in st.session_state or not isinstance(st.session_state.transactions, pd.DataFrame):
        st.session_state.transactions = load_transactions()
    df = st.session_state.transactions

    chave_empresa = st.session_state.chave_empresa
    df = st.session_state.transactions

    # Filtra apenas os registros da empresa logada
    df_empresa = df[df['empresa'] == chave_empresa]

    # Formulário de edição no topo
    if 'edit_id' in st.session_state and st.session_state.edit_id is not None:
        idx = df_empresa.index[df_empresa['id'] == st.session_state.edit_id]
        if not idx.empty:
            row = df_empresa.loc[idx[0]]
            with st.form("edit_form"):
                tipo = st.radio("Tipo", ["Entrada", "Saída"], index=0 if row['tipo'] == "Entrada" else 1)
                data = st.date_input("Data", value=pd.to_datetime(row['data']))
                valor = st.number_input(
                    "Valor",
                    min_value=None,
                    value=float(row['valor']),
                    format="%.2f",
                    key="valor_novo_edicao"  # <-- chave única para edição
                )
                descricao = st.text_input("Descrição", value=row['descricao'])
                submitted = st.form_submit_button("Salvar edição")
                if submitted:
                    # Ajusta o sinal do valor conforme o tipo
                    if tipo == "Saída":
                        valor = -abs(valor)
                    else:
                        valor = abs(valor)
                    if USE_DATABASE:
                        from utils.db_manager import update_transaction
                        update_transaction(
                            row['id'],
                            tipo,
                            data.strftime("%Y-%m-%d"),
                            valor,
                            descricao
                        )
                        st.session_state.transactions = load_transactions()
                        st.session_state.edit_id = None
                        st.success("Transação editada!")
                        st.rerun()
                    else:
                        df.at[idx[0], 'tipo'] = tipo
                        df.at[idx[0], 'data'] = data.strftime("%Y-%m-%d")
                        df.at[idx[0], 'valor'] = valor
                        df.at[idx[0], 'descricao'] = descricao
                        save_transactions(df)
                        st.session_state.transactions = load_transactions()
                        st.session_state.edit_id = None
                        st.success("Transação editada!")
                        st.rerun()
            st.button("Cancelar edição", on_click=lambda: st.session_state.update({'edit_id': None}))
        else:
            st.session_state.edit_id = None

    # Formulário de cadastro
    # Só mostra o formulário de cadastro se NÃO estiver editando
    if 'edit_id' not in st.session_state or st.session_state.edit_id is None:
        transaction = create_transaction_form()
        if transaction and isinstance(transaction, dict):
            # Adiciona a chave única da empresa logada
            transaction["empresa"] = st.session_state.chave_empresa
            # Se for saída, salva o valor como negativo
            if transaction["tipo"] == "Saída":
                transaction["valor"] = -abs(transaction["valor"])
            if USE_DATABASE:
                save_transaction(transaction)
                st.session_state.transactions = load_transactions()
            else:
                df = st.session_state.transactions
                df = pd.concat([df, pd.DataFrame([transaction])], ignore_index=True)
                save_transactions(df)
                st.session_state.transactions = load_transactions()
            # NÃO modifique st.session_state.valor_novo aqui!
            st.success("Transação salva com sucesso!")
            st.rerun()

    # Tabela com botões de edição
    def start_edit_callback(row_id):
        st.session_state.edit_id = row_id
        st.rerun()

    def delete_transaction_callback(row_id):
        if USE_DATABASE:
            from utils.db_manager import delete_transaction
            delete_transaction(row_id)
            st.session_state.transactions = load_transactions()
            st.success("Transação excluída!")
            st.rerun()
        else:
            df = st.session_state.transactions
            df = df[df['id'] != row_id].reset_index(drop=True)
            save_transactions(df)
            st.session_state.transactions = load_transactions()
            st.success("Transação excluída!")
            st.rerun()

    if not df_empresa.empty:
        display_transactions_table(df_empresa, start_edit_callback, delete_transaction_callback)
        display_daily_totals_table(df_empresa)
    else:
        st.info("Nenhuma transação cadastrada para esta empresa.")

    if st.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.empresa = None
        st.rerun()

def main_app():
    if 'transactions' not in st.session_state:
        st.session_state.transactions = load_transactions()
    df = st.session_state.transactions
    chave_empresa = st.session_state.chave_empresa  # Adicione esta linha
    df_empresa = df[df['empresa'] == chave_empresa]

    # Inicializa o DataFrame de transações se não existir
    if 'transactions' not in st.session_state or not isinstance(st.session_state.transactions, pd.DataFrame):
        st.session_state.transactions = load_transactions()

    st.sidebar.title("Menu")
    menu = ["Lançamentos", "Somatório por Dia", "Estoque"]
    page = st.sidebar.selectbox("Menu", menu)

    if page == "Lançamentos":
        st.title(f"Controle de Fluxo de Caixa - {st.session_state.empresa}")

        # Formulário de edição no topo
        if 'edit_id' in st.session_state and st.session_state.edit_id is not None:
            idx = df_empresa.index[df_empresa['id'] == st.session_state.edit_id]
            if not idx.empty:
                row = df_empresa.loc[idx[0]]
                with st.form("edit_form"):
                    tipo = st.radio("Tipo", ["Entrada", "Saída"], index=0 if row['tipo'] == "Entrada" else 1)
                    data = st.date_input("Data", value=pd.to_datetime(row['data']))
                    valor = st.number_input(
                        "Valor",
                        min_value=None,
                        value=float(row['valor']),
                        format="%.2f",
                        key="valor_novo_edicao"  # <-- chave única para edição
                    )
                    descricao = st.text_input("Descrição", value=row['descricao'])
                    submitted = st.form_submit_button("Salvar edição")
                    if submitted:
                        # Ajusta o sinal do valor conforme o tipo
                        if tipo == "Saída":
                            valor = -abs(valor)
                        else:
                            valor = abs(valor)
                        if USE_DATABASE:
                            from utils.db_manager import update_transaction
                            update_transaction(
                                row['id'],
                                tipo,
                                data.strftime("%Y-%m-%d"),
                                valor,
                                descricao
                            )
                            st.session_state.transactions = load_transactions()
                            st.session_state.edit_id = None
                            st.success("Transação editada!")
                            st.rerun()
                        else:
                            df.at[idx[0], 'tipo'] = tipo
                            df.at[idx[0], 'data'] = data.strftime("%Y-%m-%d")
                            df.at[idx[0], 'valor'] = valor
                            df.at[idx[0], 'descricao'] = descricao
                            save_transactions(df)
                            st.session_state.transactions = load_transactions()
                            st.session_state.edit_id = None
                            st.success("Transação editada!")
                            st.rerun()
                st.button("Cancelar edição", on_click=lambda: st.session_state.update({'edit_id': None}))
            else:
                st.session_state.edit_id = None

        # Formulário de cadastro
        # Só mostra o formulário de cadastro se NÃO estiver editando
        if 'edit_id' not in st.session_state or st.session_state.edit_id is None:
            transaction = create_transaction_form()
            if transaction and isinstance(transaction, dict):
                # Adiciona a chave única da empresa logada
                transaction["empresa"] = chave_empresa
                # Se for saída, salva o valor como negativo
                if transaction["tipo"] == "Saída":
                    transaction["valor"] = -abs(transaction["valor"])
                if USE_DATABASE:
                    save_transaction(transaction)
                    st.session_state.transactions = load_transactions()
                else:
                    df = st.session_state.transactions
                    df = pd.concat([df, pd.DataFrame([transaction])], ignore_index=True)
                    save_transactions(df)
                    st.session_state.transactions = load_transactions()
                # NÃO modifique st.session_state.valor_novo aqui!
                st.success("Transação salva com sucesso!")
                st.rerun()

        # Tabela com botões de edição
        def start_edit_callback(row_id):
            st.session_state.edit_id = row_id
            st.rerun()

        def delete_transaction_callback(row_id):
            if USE_DATABASE:
                from utils.db_manager import delete_transaction
                delete_transaction(row_id)
                st.session_state.transactions = load_transactions()
                st.success("Transação excluída!")
                st.rerun()
            else:
                df = st.session_state.transactions
                df = df[df['id'] != row_id].reset_index(drop=True)
                save_transactions(df)
                st.session_state.transactions = load_transactions()
                st.success("Transação excluída!")
                st.rerun()

        if not df_empresa.empty:
            display_transactions_table(df_empresa, start_edit_callback, delete_transaction_callback)
        else:
            st.info("Nenhuma transação cadastrada para esta empresa.")

    elif page == "Somatório por Dia":
        st.title(f"Somatório por Dia - {st.session_state.empresa}")

        # Filtro de datas: pega todo o intervalo disponível
        datas_validas = pd.to_datetime(df_empresa['data'], errors='coerce').dropna()
        if not datas_validas.empty:
            min_date = datas_validas.min().date()
            max_date = datas_validas.max().date()
        else:
            today = datetime.date.today()
            min_date = today
            max_date = today

        start_date, end_date = st.date_input(
            "Filtrar por intervalo de datas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Agora, use start_date e end_date normalmente
        # Filtra o DataFrame pelo range de datas
        df_filtrado = df_empresa[
            (pd.to_datetime(df_empresa['data']) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(df_empresa['data']) <= pd.to_datetime(end_date))
        ]

        if not df_filtrado.empty:
            # Somatório por dia
            df_soma_dia = df_filtrado.groupby('data')['valor'].sum().reset_index()
            st.subheader("Somatório por Dia")
            st.dataframe(df_soma_dia)
            st.line_chart(df_soma_dia.set_index('data')['valor'])

            # Somatório mensal por tipo (Entradas/Saídas)
            df_filtrado['mes'] = pd.to_datetime(df_filtrado['data']).dt.to_period('M').astype(str)
            df_soma_mes_tipo = df_filtrado.groupby(['mes', 'tipo'])['valor'].sum().unstack(fill_value=0)
            df_soma_mes_tipo = df_soma_mes_tipo.reindex(columns=['Entrada', 'Saída'], fill_value=0)

            st.subheader("Entradas e Saídas Mensais")
            st.bar_chart(df_soma_mes_tipo[['Entrada', 'Saída']])

            # Calcula saldo mensal
            df_soma_mes_tipo['Saldo'] = df_soma_mes_tipo.get('Entrada', 0) + df_soma_mes_tipo.get('Saída', 0)
            df_soma_mes_tipo['Margem Líquida (%)'] = df_soma_mes_tipo.apply(
                lambda row: (row['Saldo'] / row['Entrada'] * 100) if row['Entrada'] != 0 else 0, axis=1
            )

            st.subheader("Saldo Mensal")
            st.line_chart(df_soma_mes_tipo['Saldo'])

            st.subheader("Margem Líquida Mensal (%)")
            st.line_chart(df_soma_mes_tipo['Margem Líquida (%)'])

            st.dataframe(df_soma_mes_tipo[['Entrada', 'Saída', 'Saldo', 'Margem Líquida (%)']])

            # Média diária apenas dos valores de entrada
            df_entradas = df_filtrado[df_filtrado['tipo'] == 'Entrada']
            df_soma_dia_entradas = df_entradas.groupby('data')['valor'].sum().reset_index()
            media_diaria_entradas = df_soma_dia_entradas['valor'].mean()
            st.subheader("Média Diária das Entradas")
            st.metric(label="Média Diária de Entradas", value=f"R$ {media_diaria_entradas:.2f}")

            # Descobre o mês e ano do filtro final
            if not df_soma_dia_entradas.empty:
                ultimo_dia = pd.to_datetime(df_soma_dia_entradas['data']).max()
                mes = ultimo_dia.month
                ano = ultimo_dia.year
                dias_projetados = calendar.monthrange(ano, mes)[1]
                faturamento_projetado = media_diaria_entradas * dias_projetados
                st.subheader(f"Projeção de Faturamento para {dias_projetados} dias ({mes:02d}/{ano})")
                st.metric(label="Faturamento Projetado", value=f"R$ {faturamento_projetado:.2f}")
        else:
            st.info("Nenhum lançamento no intervalo selecionado.")

        # Agrupa por dia e tipo
        df_soma_dia_tipo = df_filtrado.groupby(['data', 'tipo'])['valor'].sum().unstack(fill_value=0)
        df_soma_dia_tipo = df_soma_dia_tipo.reindex(columns=['Entrada', 'Saída'], fill_value=0)

        st.subheader("Entradas e Saídas Dia a Dia")
        st.line_chart(df_soma_dia_tipo[['Entrada', 'Saída']])

        # --- Projeção Mensal ---
        df_filtrado['mes'] = pd.to_datetime(df_filtrado['data']).dt.to_period('M').astype(str)

        # Soma dos valores reais faturados por mês (apenas entradas)
        faturado_mes = df_filtrado[df_filtrado['tipo'] == 'Entrada'].groupby('mes')['valor'].sum().reset_index(name='Faturado')

        # Média diária por mês (apenas entradas)
        df_dia_mes_entradas = df_filtrado[df_filtrado['tipo'] == 'Entrada'].groupby(['mes', 'data'])['valor'].sum().reset_index()
        media_diaria_mes_entradas = df_dia_mes_entradas.groupby('mes')['valor'].mean().reset_index(name='Média Diária Entradas')

        # Junta as tabelas
        tabela_proj = pd.merge(media_diaria_mes_entradas, faturado_mes, on='mes', how='left')

        # Dias no mês e projeção
        tabela_proj['Dias no Mês'] = tabela_proj['mes'].apply(lambda x: calendar.monthrange(int(x[:4]), int(x[5:]))[1])
        tabela_proj['Projeção Mensal'] = tabela_proj['Média Diária Entradas'] * tabela_proj['Dias no Mês']

        st.subheader("Projeção de Faturamento Mensal (Entradas)")
        st.dataframe(tabela_proj[['mes', 'Média Diária Entradas', 'Dias no Mês', 'Projeção Mensal', 'Faturado']])

        # Termômetro de lucro
        saldo = df_empresa['valor'].sum()
        entradas = df_empresa[df_empresa['tipo'] == 'Entrada']['valor'].sum()
        despesas = df_empresa[df_empresa['tipo'] == 'Saída']['valor'].sum()
        dias_entrada = (df_empresa[df_empresa['tipo'] == 'Entrada']['data'].nunique())
        dias_mes = (df_empresa['data'].nunique())

        if saldo > 0:
            st.success("Saúde financeira: Saudável 🟢")
        else:
            st.error("Saúde financeira: Alerta 🔴")

        # Constância de entradas
        percentual_entrada = (dias_entrada / dias_mes) * 100
        if percentual_entrada >= 80:
            st.success(f"Constância de entradas: {percentual_entrada:.1f}% (Constante)")
        elif percentual_entrada >= 50:
            st.warning(f"Constância de entradas: {percentual_entrada:.1f}% (Regular)")
        else:
            st.error(f"Constância de entradas: {percentual_entrada:.1f}% (Baixa)")

        # Equilíbrio receitas/despesas
        receitas = df_empresa[df_empresa['tipo'] == 'Entrada']['valor'].sum()
        despesas = df_empresa[df_empresa['tipo'] == 'Saída']['valor'].sum()
        if receitas >= abs(despesas):
            st.success("Equilíbrio: Receitas cobrem despesas 🟢")
        else:
            st.error("Equilíbrio: Despesas maiores que receitas 🔴")


    elif page == "Estoque":
        st.title("Cadastro de Itens do Estoque")
        create_estoque_form()
        
    

    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.empresa = None
        st.rerun()

def page_somatorio_por_dia(df_empresa):
    st.title(f"Saúde Financeira - {st.session_state.empresa}")

    # --- Indicadores de saúde financeira ---
    # Calcule os valores necessários
    saldo = df_empresa['valor'].sum()
    receitas = df_empresa[df_empresa['tipo'] == 'Entrada']['valor'].sum()
    despesas = abs(df_empresa[df_empresa['tipo'] == 'Saída']['valor'].sum())
    dias_mes = pd.to_datetime(df_empresa['data']).dt.day.nunique()
    dias_entrada = pd.to_datetime(df_empresa[df_empresa['tipo'] == 'Entrada']['data']).dt.day.nunique()

    # Termômetro de lucro
    if saldo > 0:
        st.success("Saúde financeira: Saudável 🟢")
    else:
        st.error("Saúde financeira: Alerta 🔴")

    # Constância de entradas
    if dias_mes > 0:
        percentual_entrada = (dias_entrada / dias_mes) * 100
    else:
        percentual_entrada = 0
    if percentual_entrada >= 80:
        st.success(f"Constância de entradas: {percentual_entrada:.1f}% (Constante)")
    elif percentual_entrada >= 50:
        st.warning(f"Constância de entradas: {percentual_entrada:.1f}% (Regular)")
    else:
        st.error(f"Constância de entradas: {percentual_entrada:.1f}% (Baixa)")

    # Equilíbrio receitas/despesas
    if receitas >= despesas:
        st.success("Equilíbrio: Receitas cobrem despesas 🟢")
    else:
        st.error("Equilíbrio: Despesas maiores que receitas 🔴")

    # --- Resto da página ---
    # ... gráficos, filtros, tabelas ...

def cadastro_empresa():
    st.title("Cadastro de Empresa")
    with st.form("form_cadastro_empresa"):
        nome = st.text_input("Nome da empresa")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Cadastrar empresa")
        if submitted:
            if nome.strip() and email.strip() and senha.strip():
                chave = save_empresa(nome.strip(), email.strip(), senha.strip())
                st.success(f"Empresa cadastrada com sucesso! Trial de 15 dias iniciado.\nChave gerada: {chave}")
            else:
                st.error("Preencha todos os campos.")

def main():
    if st.session_state.get("show_cadastro_empresa", False):
        cadastro_empresa()
        # Botão para voltar ao login
        if st.button("Voltar para Login"):
            st.session_state.show_cadastro_empresa = False
            st.rerun()
    elif 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_screen()
    else:
        main_app()

if __name__ == "__main__":
    main()
