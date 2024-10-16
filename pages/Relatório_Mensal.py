import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Topics section
st.subheader("Relatório Mensal - Deal Flow")

with st.expander("Critérios e Classificações"):
    st.subheader("Classification")
    st.write("1. Seleção Adversa:")
    st.write("   Não tivemos acesso")
    st.write("2. Tomada de Decisão/ Análise:")
    st.write("   Falso Negativo (aqui podemos incorporar o Processo Lento)")
    st.write("   Verdadeiro Negativo")
    st.write("   Indefinido (ainda não se provou ser um Falso Negativo ou Verdadeiro Negativo)")
    st.write("   Portfolio")
    st.write("   Dúvida (quando não ficou clara a classificação olhando o Domenique)")
    st.write("   Lost to another players (quando avaliamos uma startup, gostamos dela, mas ela captou com outro)")
    st.write("   Em análise (estamos analisando a startup e ela ainda não passou do nosso estágio, mas recebeu alguma rodada no Crunchbase)")

# Caminho do arquivo CSV
csv_file_path = 'df_final_cobertura_historico.csv'

# Função para carregar o DataFrame inicial e armazenar no session_state
def load_data():
    return pd.read_csv(csv_file_path)

# Inicializa o DataFrame no session_state se ainda não estiver definido
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Resetar o índice para evitar problemas nos editores
st.session_state.df.reset_index(drop=True, inplace=True)

# Filtros de Ano e Mês
unique_year = np.sort(st.session_state.df["Year"].unique())[::-1]
unique_month = np.sort(st.session_state.df["Month"].unique())

col1, col2 = st.columns(2)
year_filter = col1.selectbox('Selecione o Ano', unique_year)
month_filter = col2.selectbox('Selecione o Mês', unique_month)


# Filtragem do DataFrame com base nas seleções
df_filtro = st.session_state.df[(st.session_state.df['Year'] == year_filter) & (st.session_state.df['Month'] == month_filter)]
name_startups_filtrado = df_filtro['Organization Name'].unique()
df_filtro1 = df_filtro[['Organization Name', 'Classification', 'Funding Type', 'Money Raised (in USD)','stagename', 'Investor Names','Announced Date', 'Organization Name URL']]
df_filtro1 = df_filtro1[df_filtro1['Classification'] != 'Não se aplica']

col3, col4, col5 = st.columns(3)

# Filter the original DataFrame to include only rows with these organization names
df_filtrado = df_filtro1[df_filtro1['Organization Name'].isin(name_startups_filtrado)]
df_filtrado = df_filtrado[['Organization Name', 'Classification', 'stagename', 'Funding Type','Money Raised (in USD)', 'Announced Date']]

# 
n_total_startups = df_filtrado['Organization Name'].nunique()
col3.metric("Total Startups", n_total_startups)
nao_acesso = df_filtrado[df_filtrado['Classification'] == 'Nao tivemos acesso']
n_n_acesso_startups = nao_acesso['Organization Name'].nunique()
col4.metric("Total Startups Não Tivemos Acesso", n_n_acesso_startups)
percentual = (n_n_acesso_startups / n_total_startups) * 100 if n_total_startups > 0 else 0
col5.metric("Percentual", f"{percentual:.2f}%")

# Exibir editor interativo para editar classificações
edited_df = st.data_editor(df_filtrado, key="data_editor1")

#Dataframe que traz o histórico de captação das startups
df_name = st.session_state.df[st.session_state.df['Organization Name'].isin(name_startups_filtrado)]
df_name = df_name[df_name['Classification'] != 'Não se aplica']
df_name = df_name[['Organization Name', 'Classification', 'stagename', 'Funding Type','Money Raised (in USD)', 'Announced Date']]


with st.expander("Histórico de Rodada das Startups"):
    edited_df2 = st.data_editor(df_name, key="data_editor2")

col6, col7= st.columns(2)

# Botão para salvar alterações
if col6.button("Salvar Alterações"):
    st.write("Salvando alterações...")

    # Atualizar a coluna 'Classification' no DataFrame principal
    for index, row in edited_df.iterrows():
        org_name = row['Organization Name']
        classification = row['Classification']

        # Atualiza apenas a classificação correspondente à empresa
        st.session_state.df.loc[
            st.session_state.df['Organization Name'] == org_name, 
            'Classification'
        ] = classification

    # Salvar as alterações no CSV
    st.session_state.df.to_csv(csv_file_path, index=False)
    st.success("Alterações salvas no CSV!")

docs = 'https://docs.google.com/document/d/1H6_vHu8biml93LA4h3mniRoA_PgYHOEYTysyMbdmg9o/edit'
col7.link_button("Docs - Análises", docs)

df_investors_exploded = df_filtro1.copy()

df_investors_exploded['Investor Names'] = df_investors_exploded['Investor Names'].str.split(',')
df_investors_exploded = df_investors_exploded.explode('Investor Names')
df_investors_exploded['Investor Names'] = df_investors_exploded['Investor Names'].str.strip()

# Contagem de investidores e tipos de financiamento
n_investors = df_investors_exploded['Investor Names'].value_counts()
n_funding_type = df_filtro1['Funding Type'].value_counts()

# Gráfico de barras para investidores
fig_investors = px.bar(
    n_investors, 
    x=n_investors.index, 
    y=n_investors.values, 
    labels={'x': 'Investidor', 'y': 'Contagem'},
    title='Distribuição de Investidores'
)
fig_investors.update_layout(xaxis_tickangle=-45)

# Gráfico circular para tipos de financiamento
fig_funding_type = px.pie(
    values=n_funding_type.values, 
    names=n_funding_type.index, 
    title='Distribuição de Tipos de Financiamento',
    hole=0.4  # Gráfico do tipo "doughnut"
)

# Exibir gráficos
st.plotly_chart(fig_investors, use_container_width=True)
st.plotly_chart(fig_funding_type, use_container_width=True)
