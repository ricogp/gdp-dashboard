import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import seaborn as sns

st.markdown("## Detalhamento Sourcing Startups Series A")

df_planilha_relevantes = pd.read_csv('PlanilhaManual_SeriesA.csv')
df_merged = pd.read_csv('merged_data.csv')

df = df_merged.merge(df_planilha_relevantes[['Organization Name', 'Analise descarte']], 
                           on='Organization Name', 
                           how='left')

df = df.dropna(subset=['Analise descarte'])

df_acesso = df[~df['Analise descarte'].isin(['Não tivemos acesso', 'Não se aplica'])]

df_grouped = df_acesso.groupby('Organization Name')[['sourcename', 'detailed_source', 'Analise descarte', 'Total Funding Amount (in USD)']].first().reset_index()

value = df_grouped['sourcename'].value_counts()

st.markdown("#### Quadro com todas startups")
st.dataframe(df_grouped)

st.markdown("#### Quadro com quantidade por Sourcing")
st.table(value)

unique_source = df_grouped['sourcename'].unique()
source_filter = st.selectbox('Selecione a Sourcing - Detalhamento',unique_source)

df_detail_source = df_grouped[df_grouped['sourcename'] == source_filter]

df_detail_source = df_detail_source[['Organization Name', 'detailed_source', 'Analise descarte']]
df_detail_source = df_detail_source.sort_values('detailed_source')

st.dataframe(df_detail_source)

