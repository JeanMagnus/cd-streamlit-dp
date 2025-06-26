import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(layout="wide")
st.title("📊 Análise Geral dos Dados")

# Carregar dados
df = load_data()

# ==========================
# Filtro lateral
# ==========================
st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("País de residência:", options=df["Country"].unique(), default=df["Country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["Gender_clean"].unique(), default=df["Gender_clean"].unique())

# Aplicar filtros
df = df[df["Country"].isin(paises)]
df = df[df["Gender_clean"].isin(generos)]

# ==========================
# Estatísticas descritivas
# ==========================
st.markdown("### 📌 Estatísticas Descritivas da Idade (dados filtrados)")
df_idade_limpa = df[(df['Age'] >= 15) & (df['Age'] <= 80)]  # Limpa valores absurdos
st.dataframe(df_idade_limpa['Age'].describe().to_frame(), use_container_width=True)

# ==========================
# Visualização em colunas
# ==========================
col1, col2 = st.columns(2)

# Histórico familiar - Pizza
history_counts = df['family_history'].value_counts().reset_index()
history_counts.columns = ['Histórico Familiar', 'Quantidade']
fig_familia = px.pie(
    history_counts,
    values='Quantidade',
    names='Histórico Familiar',
    title='🧬 Histórico Familiar de Problemas Mentais',
    color_discrete_sequence=px.colors.sequential.RdBu
)
col1.plotly_chart(fig_familia, use_container_width=True)

# Tratamento - Barras
treat_counts = df['treatment'].value_counts().reset_index()
treat_counts.columns = ['Tratamento', 'Quantidade']
fig_tratamento = px.bar(
    treat_counts,
    x='Tratamento',
    y='Quantidade',
    color='Tratamento',
    title='💊 Busca por Tratamento',
    color_discrete_sequence=px.colors.qualitative.Vivid
)
col2.plotly_chart(fig_tratamento, use_container_width=True)

# ==========================
# Segunda linha de gráficos
# ==========================
col3, col4 = st.columns(2)

# Benefícios oferecidos pela empresa - Pizza
benefits_counts = df['benefits'].value_counts().reset_index()
benefits_counts.columns = ['Benefícios', 'Quantidade']
fig_benefits = px.pie(
    benefits_counts,
    values='Quantidade',
    names='Benefícios',
    title='🏥 Benefícios Relacionados à Saúde Mental',
    color_discrete_sequence=px.colors.sequential.Agsunset
)
col3.plotly_chart(fig_benefits, use_container_width=True)

# Boxplot idade x tratamento
fig_box = px.box(
    df_idade_limpa,
    x='treatment',
    y='Age',
    color='treatment',
    title='📊 Distribuição da Idade por Tratamento',
    color_discrete_sequence=px.colors.qualitative.Set2
)
col4.plotly_chart(fig_box, use_container_width=True)

# ==========================
# Observações finais
# ==========================
st.markdown("---")
st.markdown("🔎 **Observação:** Os dados foram filtrados para manter apenas idades entre 15 e 80 anos, removendo outliers extremos.")
