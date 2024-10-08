import streamlit as st
import pandas as pd
import numpy as np

# Carregar o DataFrame do arquivo CSV
csv_file_path = 'df_final_cobertura_historico.csv'  # Caminho do seu arquivo CSV

# Inicializa o session_state com o DataFrame do CSV se não estiver definido
if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv(csv_file_path)

# Resetar o índice para garantir que o data_editor funcione corretamente
st.session_state.df.reset_index(drop=True, inplace=True)

# Obter anos e meses únicos para o filtro
unique_year = np.sort(st.session_state.df["Year"].unique())[::-1] # Certifique-se de usar st.session_state.df
unique_month = np.sort(st.session_state.df["Month"].unique())

col1,col2 = st.columns(2)

# Widgets para selecionar ano e mês no sidebar
year_filter = col1.selectbox('Selecione o Ano', unique_year)
month_filter = col2.selectbox('Selecione o Mês', unique_month)

# Filtragem do DataFrame com base nas seleções
df_filtro = st.session_state.df[(st.session_state.df['Year'] == year_filter) & (st.session_state.df['Month'] == month_filter)]
name_startups_filtrado = df_filtro['Organization Name'].unique()
df_filtro1 = df_filtro[['Organization Name', 'Classification', 'Funding Type', 'Money Raised (in USD)','stagename', 'Investor Names','Announced Date', 'Organization Name URL']]
df_filtro1 = df_filtro1[df_filtro1['Classification'] != 'Não se aplica']

col3, col4, col5 = st.columns(3)

n_total_startups = df_filtro1['Organization Name'].nunique()
col3.metric("Total Startups", n_total_startups)
nao_acesso = df_filtro1[df_filtro1['Classification'] == 'Nao tivemos acesso']
n_n_acesso_startups = nao_acesso['Organization Name'].nunique()
col4.metric("Total Startups Não Tivemos Acesso", n_n_acesso_startups)
percentual = (n_n_acesso_startups / n_total_startups) * 100 if n_total_startups > 0 else 0
col5.metric("Percentual", f"{percentual:.2f}%")

# Filter the original DataFrame to include only rows with these organization names
df_filtrado = st.session_state.df[st.session_state.df['Organization Name'].isin(name_startups_filtrado)]
df_filtrado = df_filtrado[['Organization Name', 'Classification', 'stagename', 'Funding Type','Money Raised (in USD)', 'Announced Date']]

# Criar o dataframe interativo com os dados filtrados
edited_df = st.data_editor(df_filtro1, key="data_editor")

with st.expander("Histórico de Rodada das Startups"):
    edited_df2 = st.data_editor(df_filtrado, key="data_editor2")

col6, col7= st.columns(2)

# Adiciona um botão para salvar as alterações
if col6.button("Salvar Alterações"):
    # Atualiza o dataframe no session_state
    st.session_state.df.update(edited_df2)

    # Salva o DataFrame editado de volta ao CSV
    st.session_state.df.to_csv(csv_file_path, index=False)  # Salva sem o índice
    st.success("Alterações salvas no CSV!")

# Mostra o dataframe atualizado
#st.write("DataFrame Atualizado:")
#st.write(st.session_state.df[st.session_state.df['Organization Name'].isin(name_startups_filtrado)][['Organization Name', 'Classification']])

col8, col9= st.columns(2)

df_filtro2 = df_filtro[df_filtro['Classification'] != 'Não se aplica']
df_investors_exploded = df_filtro2.copy()

df_investors_exploded['Investor Names'] = df_investors_exploded['Investor Names'].str.split(',')
df_investors_exploded = df_investors_exploded.explode('Investor Names')
df_investors_exploded['Investor Names'] = df_investors_exploded['Investor Names'].str.strip()

n_investors = df_investors_exploded['Investor Names'].value_counts()

n_funding_type = df_filtro2['Funding Type'].value_counts()

col8.dataframe(n_investors, height=200, width=1200)
col9.dataframe(n_funding_type, height=200, width=1200)

# Supondo que st.session_state.df seja o DataFrame que você deseja salvar
csv_path = '/workspaces/gdp-dashboard/df_final_cobertura_historico_updated.csv'

# Função para salvar o CSV
def save_csv():
    st.session_state.df.to_csv(csv_path, index=False)
    st.success(f"Arquivo salvo em: {csv_path}")

# Criando o botão para salvar o CSV
if col7.button('Salvar CSV'):
    save_csv()

docs = 'https://docs.google.com/document/d/1H6_vHu8biml93LA4h3mniRoA_PgYHOEYTysyMbdmg9o/edit'
st.link_button("Docs - Análises", docs)