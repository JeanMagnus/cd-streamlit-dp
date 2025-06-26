# pages/01_📊_Analise_Geral.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise Geral", layout="wide")

# Função para carregar os dados
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("📊 Análise Geral da Pesquisa sobre Saúde Mental")

st.markdown("""
A pesquisa tem como foco avaliar a saúde mental de profissionais da área de tecnologia, coletando informações sobre diagnóstico, tratamento, ambiente de trabalho e histórico familiar. A seguir, apresentamos uma visão geral dos dados.
""")

# KPIs principais
col1, col2, col3 = st.columns(3)
col1.metric("Total de Participantes", f"{len(df):,}")
col2.metric("Variáveis Coletadas", len(df.columns))
col3.metric("Ano da Pesquisa", "2014")

st.markdown("---")

# Pré-visualização dos Dados
st.subheader("🔍 Prévia dos Dados")
st.dataframe(df.head(), use_container_width=True)

# Estatísticas
st.subheader("📌 Estatísticas Descritivas")
st.dataframe(df.describe(include='all'), use_container_width=True)

st.markdown("---")

# Gráfico de Pizza: Histórico Familiar
st.subheader("🧬 Histórico Familiar de Transtornos Mentais")

history = df['family_history'].value_counts().reset_index()
history.columns = ['Histórico Familiar', 'Contagem']

fig_pie = px.pie(
    history,
    values='Contagem',
    names='Histórico Familiar',
    title='Distribuição de Histórico Familiar',
    color_discrete_sequence=px.colors.sequential.Blues
)
st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico de Barras: Distribuição de Tratamento
st.subheader("🏥 Participantes em Tratamento")

treat = df['treatment'].value_counts().reset_index()
treat.columns = ['Tratamento', 'Contagem']

fig_bar = px.bar(
    treat,
    x='Tratamento',
    y='Contagem',
    color='Tratamento',
    title='Distribuição dos Participantes em Tratamento',
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("----")

st.caption("Fonte dos dados: [Kaggle Mental Health in Tech Survey](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey)")
