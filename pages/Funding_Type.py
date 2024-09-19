import streamlit as st
import pandas as pd
import numpy as np

df_investors = pd.read_csv('df_investors.csv')

unique_status = sorted(df_investors["Funding Type"].unique())

st.markdown("### Análise de Investidores Por Funding Type")

filtro_ft = st.selectbox('**Escolha o Funding Type**', unique_status)
data_range = st.slider('**Year**', 2000,2024, (2000,2024,))

df_investors_filtrado = df_investors[df_investors['Funding Type']== filtro_ft]
df_investors_filtrado = df_investors_filtrado[df_investors_filtrado['Year'].between(data_range[0], data_range[-1])]
df_investors_filtrado['Year'] = df_investors_filtrado['Year'].astype(str)


investor_ft_counts = df_investors_filtrado['Investor Names'].value_counts()
investor_ft_percentages = (investor_ft_counts / investor_ft_counts.sum()) * 100
investor_ft_cumulative = investor_ft_percentages.cumsum()
investor_ft_percentages = investor_ft_percentages.round(2)
investor_ft_cumulative = investor_ft_cumulative.round(2)

investor_ft_df = pd.DataFrame({
    'Investment Count': investor_ft_counts,
    'Percentage of Total (%)': investor_ft_percentages,
    'Cumulative Percentage (%)': investor_ft_cumulative
})

lead_unique = df_investors_filtrado[['Organization Name', 'Lead Investors', 'Announced Date']].drop_duplicates()
investor_lead_ft_counts = lead_unique['Lead Investors'].value_counts()
investor_ft_percentages = (investor_lead_ft_counts / investor_lead_ft_counts.sum()) * 100
investor_ft_cumulative = investor_ft_percentages.cumsum()
investor_ft_percentages = investor_ft_percentages.round(2)
investor_ft_cumulative = investor_ft_cumulative.round(2)

investor_ft_df2 = pd.DataFrame({
    'Investment Count': investor_lead_ft_counts,
    'Percentage of Total (%)': investor_ft_percentages,
    'Cumulative Percentage (%)': investor_ft_cumulative
})

unique_ft_startups = df_investors_filtrado[['Organization Name', 'Year', 'Announced Date']].drop_duplicates()
startup_counts_by_year = unique_ft_startups.groupby('Year').size().reset_index(name='Counts')


col1, col2 = st.columns(2)

col1.markdown("###### Investimentos por Fundo")
col1.dataframe(investor_ft_df, height=350)
col2.markdown("###### Evolução das Rodadas por Ano")
col2.bar_chart(startup_counts_by_year.set_index('Year')['Counts'])

with st.expander("Investidores Líderes"):
    investor_ft_df2

with st.expander("Startups-Investidores Filtrados"):
    df_investors_filtrado2 = df_investors_filtrado[['Organization Name', 'Funding Type', 'Money Raised (in USD)', 'Investor Names', 'Announced Date']]
    df_investors_filtrado2