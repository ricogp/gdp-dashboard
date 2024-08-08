import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

df_rodadas = pd.read_csv('df_rodadas.csv')
df_cobertura = pd.read_csv('df_final_cobertura_Q2_24.csv')

data_range = st.sidebar.slider('Select Days Range', 0, 365, (0, 365))

df_cobertura = df_cobertura[df_cobertura['Time Since Announced'].between(data_range[0], data_range[-1])]
df_cobertura['Time Since Announced'] = df_cobertura['Time Since Announced'].astype(int)

unique_status = df_cobertura["Classification"].unique()

df_cobertura['Investor Names'] = df_cobertura['Investor Names'].str.split(', ')
df_cobertura_inv = df_cobertura.explode('Investor Names').reset_index(drop=True)
df_cobertura_inv.dropna(subset=['Investor Names'], inplace=True)

classification_filter = st.sidebar.selectbox('',unique_status)

col1, col2, col3 = st.columns(3) 

df_filtro = df_cobertura_inv [df_cobertura_inv ['Classification'] == classification_filter]

total_startups = df_cobertura['Organization Name'].nunique()
filter_startups = df_filtro['Organization Name'].nunique()

percentual = (filter_startups/ total_startups) * 100

col1.metric("Total Startups", total_startups)
col2.metric("Total Startups por Classificação", filter_startups)
col3.metric("Percentual", f"{percentual:.2f}%")

def create_stacked_bar_chart(data):
    fig = px.bar(data, x=data.index, y=data.columns,
                 labels={'value': 'Percentage', 'index': 'Funding Type'},
                 title='Percentual de Classificação por Tipo de Rodada')
    return fig

df_filtered_count = df_filtro.groupby(['Funding Type', 'Classification'])['Organization Name'].nunique().unstack().fillna(0)

total_startups_by_funding_filtered = df_cobertura.groupby('Funding Type')['Organization Name'].nunique()

df_filtered_percentage = df_filtered_count.div(total_startups_by_funding_filtered, axis=0) * 100
df_filtered_percentage['Restante'] = 100 - df_filtered_percentage.sum(axis=1)

fig = create_stacked_bar_chart(df_filtered_percentage)

st.plotly_chart(fig)

df_filtro1 = df_cobertura[df_cobertura['Classification'] == classification_filter]
unique_funding_type = df_filtro1['Funding Type'].sort_values().unique() 

with st.expander("Ver Startups Por Tipo de Rodada"):
    col4, col5 = st.columns(2) 

    investor_filter = col4.selectbox('',unique_funding_type)
    df_select = df_filtro1[df_filtro1['Funding Type'] == investor_filter]
    df_select = df_select[['Organization Name', 'Money Raised (in USD)', 'Funding Type', 'Total Funding Amount (in USD)', 'Organization Location', 'Announced Date']]

    total_startups_select = df_select['Organization Name'].nunique()
    col5.metric("Total Startups por Tipo Rodada", total_startups_select)

    st.dataframe(df_select, height=200, width=700)

    docs = "https://docs.google.com/document/d/1VwGlzViQ647hrtJ2khw2r1HpgnDOVn47O5UwoYgEhLU/edit"
    st.link_button("Docs - Análises", docs)


    unique_startups_select = df_select['Organization Name'].unique()
    startup_filter = st.selectbox('',unique_startups_select)

    df_filtered = df_cobertura[df_cobertura['Organization Name'] == startup_filter]
    link = df_filtered['Organization Name URL'].values[0] 
    description = df_filtered['Organization Description'].values[0] 
    industries = df_filtered['Organization Industries'].values[0]

    col6, col7 = st.columns(2)

    col6.link_button("Crunchbase", link)
    col7.caption(industries)

    st.caption(description)

    #prompt = st.chat_input("Say something")
    #if prompt:
        #st.write(f"User has sent the following prompt: {prompt}")
    
    # Create a form
    with st.form("my_form"):

        # Add input fields
        name = st.text_input("Name", value=startup_filter)
        n_founders = st.number_input("Número de Fundadores", min_value=1, max_value=5, value=2)

        for i in range(n_founders):
            st.write(f"Fundador {i + 1}")
            col20, col21, col22 = st.columns(3)
        
            with col20:
                founder_name = st.text_input(f"Nome do Fundador {i + 1}")
            with col21:
                cargo = st.text_input(f"Cargo {i + 1}")
            with col22:
                gender = st.selectbox(f"Gênero {i + 1}", ["Masculino", "Feminino"])
        
            col23, col24 = st.columns(2)
            with col23:
                education = st.selectbox(f"MBA ou Universidade Fora? {i + 1}", ["Sim", "Não"])
            with col24:
                prof = st.selectbox(f"Passou por startup de ponta? {i + 1}", ["Sim", "Não"])
            desc_founder = st.text_input(f"Histórico do Fundador {i + 1}")
        
        # Add a submit button
        submit_button = st.form_submit_button("Submit")

    # Handle form submission
    if submit_button:
        # Create a DataFrame or any other document type to store the input data
        data = {
            "Organization Name": [name],
            "Age": [age],
            "Gender": [gender],
            "Email": [email]
        }
        df = pd.DataFrame(data)
        
        # Display the collected data
        st.write("Collected Data:")
        st.write(df)
        
        # Save the data to a CSV file (or any other format you prefer)
        df.to_csv('form_data.csv', index=False)
        st.write("Data saved to form_data.csv")

        # Criar um formulário


#st.dataframe(df_filtered_percentage['Nao tivemos acesso'].dropna().to_frame().T)

df_investors_sum = df_filtro.groupby(['Investor Names']).size().reset_index(name='Count')

fig_treemap = px.treemap(df_investors_sum, path=['Investor Names'], values='Count', title='Quantidade de Rodadas por Fundo')

st.plotly_chart(fig_treemap, use_container_width=True)


unique_investor = df_filtro["Investor Names"].sort_values().unique()
investor_filter = st.selectbox('',unique_investor) 

df_select = df_filtro[df_filtro['Investor Names'] == investor_filter]
df_select = df_select[['Organization Name','Investor Names','Money Raised (in USD)', 'Funding Type', 'Total Funding Amount (in USD)', 'Organization Location', 'Announced Date']]

st.dataframe(df_select)