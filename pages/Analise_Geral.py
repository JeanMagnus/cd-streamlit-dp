import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(layout="wide")
st.title("📊 Visão Geral da Pesquisa sobre Saúde Mental")

# Carregar dados
df = load_data()

# Filtro lateral
generos = df['Gender_clean'].dropna().unique().tolist()
genero_selecionado = st.sidebar.selectbox("Selecione o Gênero", ['Todos'] + generos)

# Filtro por gênero
if genero_selecionado != 'Todos':
    df = df[df['Gender_clean'] == genero_selecionado]

# Layout com colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico 1 - Histórico Familiar
hist_fam = df['family_history'].value_counts().reset_index()
hist_fam.columns = ['Histórico Familiar', 'Total']
fig1 = px.pie(hist_fam, values='Total', names='Histórico Familiar',
              title='Histórico Familiar de Problemas Mentais',
              color_discrete_sequence=px.colors.qualitative.Set3)
col1.plotly_chart(fig1, use_container_width=True)

# Gráfico 2 - Tratamento
trat = df['treatment'].value_counts().reset_index()
trat.columns = ['Tratamento', 'Total']
fig2 = px.bar(trat, x='Tratamento', y='Total', color='Tratamento',
              title='Pessoas que já buscaram tratamento')
col2.plotly_chart(fig2, use_container_width=True)

# Gráfico 3 - Trabalho Remoto
remote = df['remote_work'].value_counts().reset_index()
remote.columns = ['Trabalho Remoto', 'Total']
fig3 = px.bar(remote, x='Trabalho Remoto', y='Total', color='Trabalho Remoto',
              title='Trabalho Remoto')
col3.plotly_chart(fig3, use_container_width=True)

# Gráfico 4 - Benefícios
benefits = df['benefits'].value_counts().reset_index()
benefits.columns = ['Benefício de Saúde Mental', 'Total']
fig4 = px.pie(benefits, values='Total', names='Benefício de Saúde Mental',
              title='Empresa oferece benefícios para saúde mental?',
              color_discrete_sequence=px.colors.qualitative.Set2)
col4.plotly_chart(fig4, use_container_width=True)

# Gráfico 5 - Idade por Tratamento
df_idade = df[(df['Age'] >= 15) & (df['Age'] <= 80)].copy()
fig5 = px.box(df_idade, x='treatment', y='Age', color='treatment',
              title='Distribuição de Idade por Tratamento')
col5.plotly_chart(fig5, use_container_width=True)
