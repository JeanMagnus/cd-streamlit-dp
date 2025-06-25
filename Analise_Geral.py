import streamlit as st
import plotly.express as px
from utils import load_data

st.title("📊 Análise Geral dos Dados")

df = load_data()

st.subheader("Pré-visualização dos Dados")
st.dataframe(df.head())

st.subheader("Estatísticas Descritivas")
st.write(df.describe())

st.subheader("Distribuição de Histórico Familiar")
history_counts = df['family_history'].value_counts().reset_index()
history_counts.columns = ['Histórico Familiar', 'Count']

fig_pie = px.pie(
    history_counts,
    values='Count',
    names='Histórico Familiar',
    title='Histórico Familiar de Problemas Mentais',
    color_discrete_sequence=['#66b3ff', '#ff9999']
)
st.plotly_chart(fig_pie)
