import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    url = "https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("Visão Geral da Pesquisa")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Participantes", len(df))
col2.metric("Colunas", len(df.columns))
col3.metric("Ano da Pesquisa", "2014")

# Prévia da Tabela
st.subheader("Visualização Inicial dos Dados")
st.dataframe(df.head(), use_container_width=True)

# Contagem por histórico familiar
st.subheader("Distribuição - Histórico Familiar")
hist_counts = df['family_history'].value_counts().reset_index()
hist_counts.columns = ['Histórico Familiar', 'Quantidade']
fig_pie = px.pie(hist_counts, names='Histórico Familiar', values='Quantidade', title="Histórico Familiar de Problemas Mentais")
st.plotly_chart(fig_pie, use_container_width=True)
