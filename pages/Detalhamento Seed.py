import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import altair as alt
import plotly.express as px

st.markdown("## Detalhamento Investidores Seed - Seleção Adversa Relevante (Series A)")

df_planilha_relevantes = pd.read_csv('PlanilhaManual_SeriesA.csv')
df_merged = pd.read_csv('merged_data.csv')

df = df_merged.merge(df_planilha_relevantes[['Organization Name', 'Analise descarte']], 
                           on='Organization Name', 
                           how='left')

df = df.dropna(subset=['Analise descarte'])

df_nao_acesso = df[df['Analise descarte']=='Não tivemos acesso']
df_acesso = df[df['Analise descarte']!='Não tivemos acesso']


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
df_investors = df_investors[['Organization Name', 'Money Raised (in USD)','Funding Type', 'Announced Date']].drop_duplicates()
col2.dataframe(df_investors)


n_nao_acesso = df_nao_acesso['Organization Name'].nunique()
acesso = df_acesso['Organization Name'].nunique()

