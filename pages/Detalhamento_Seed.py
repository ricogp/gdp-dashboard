import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import altair as alt
import plotly.express as px
import seaborn as sns

st.markdown("## Detalhamento Investidores Seed - Seleção Adversa Relevante (Series A)")

df_planilha_relevantes = pd.read_csv('PlanilhaManual_SeriesA.csv')
df_merged = pd.read_csv('merged_data.csv')

df = df_merged.merge(df_planilha_relevantes[['Organization Name', 'Analise descarte']], 
                           on='Organization Name', 
                           how='left')

df = df.dropna(subset=['Analise descarte'])

df['Analise Descarte Ajuste'] = df['Analise descarte'].apply(
    lambda x: x if x in ['Não tivemos acesso', 'Não se aplica'] else 'Tivemos acesso')

unique_analysis = df['Analise Descarte Ajuste'].unique()

filter_acesso = st.sidebar.selectbox('Selecione se quer as que não tivemos ou tivemos acesso', unique_analysis)
df_nao_acesso = df[df['Analise Descarte Ajuste']==filter_acesso]

df_rodadas_exploded = df_nao_acesso.copy()

df_rodadas_exploded['Investor Names'] = df_rodadas_exploded['Investor Names'].str.split(',')
df_rodadas_exploded = df_rodadas_exploded.explode('Investor Names')
df_rodadas_exploded['Investor Names'] = df_rodadas_exploded['Investor Names'].str.strip()
df_rodadas_exploded = df_rodadas_exploded.dropna(subset=['Investor Names'])

col1, col2 = st.columns(2)

unique_funding = df_rodadas_exploded['Funding Type'].unique()
funding_filter = col1.selectbox('Selecione a Sourcing - Detalhamento',unique_funding)

df_investor = df_rodadas_exploded[df_rodadas_exploded['Funding Type'] == funding_filter]
n_investors = df_investor['Investor Names'].value_counts()
col1.dataframe(n_investors, height=400, width=1200)

unique_investor = sorted(df_investor['Investor Names'].unique())
investor_filter = col2.selectbox('Selecione o Investidor - Detalhamento',unique_investor)

df_investors = df_investor[df_investor['Investor Names'] == investor_filter]
df_investors1 = df_investors[['Organization Name', 'Money Raised (in USD)','Funding Type', 'Announced Date']].drop_duplicates()
col2.dataframe(df_investors1)


n_nao_acesso = df_nao_acesso['Organization Name'].nunique()

#########
# Código utilizado para fazer as análises considerando os filtros acima - Fuding Type e Investor Name
#########
col3, col4 = st.columns(2)

startups_name = df_investors['Organization Name'].unique()
df_filtered = df_investor[df_investor['Organization Name'].isin(startups_name)]

coinvestors = df_filtered[df_filtered['Investor Names']!=investor_filter]
n_coinvestment = coinvestors['Investor Names'].value_counts()

col3.markdown("### Quem coinvestiu?")
col3.dataframe(n_coinvestment)

col4.markdown("### Quem fez o funding?")

funding_filter2 = col4.selectbox('Selecione a Sourcing',unique_funding)

df_filtered2 = df_rodadas_exploded[df_rodadas_exploded['Organization Name'].isin(startups_name)]
df_filtered2 = df_filtered2[df_filtered2['Funding Type']==funding_filter2]

df_filtered2 = df_filtered2['Investor Names'].value_counts()

col4.dataframe(df_filtered2, height=320, width=1200)

