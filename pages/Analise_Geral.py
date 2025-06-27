import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(layout="wide")
st.title("Análise Geral")
st.markdown("Esta página apresenta a distribuição das principais variáveis da pesquisa.")

df_original = load_data()

df = df_original.copy()
df['family_history'] = df['family_history'].replace({'Yes': 'Sim', 'No': 'Não'})
df['treatment'] = df['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
df['benefits'] = df['benefits'].replace({'Yes': 'Sim', 'No': 'Não', "Don't know": 'Não sabe'})

# Filtros na Barra Lateral
st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("País:", options=df["Country"].unique(), default=df["Country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["Gender_clean"].unique(), default=df["Gender_clean"].unique())

df_filtrado = df[(df["Country"].isin(paises)) & (df["Gender_clean"].isin(generos))]

# LAYOUT PRINCIPAL

# NOVA SEÇÃO DE KPIs DINÂMICOS
st.markdown("### Resultados para a Seleção Atual")

# Calcula as contagens com base nos dados filtrados
total_participantes = df_filtrado.shape[0]
counts_genero = df_filtrado['Gender_clean'].value_counts()
homens = counts_genero.get('Homem', 0)
mulheres = counts_genero.get('Mulher', 0)
outros = counts_genero.get('Outro/Prefiro não dizer', 0)

# Cria as colunas para os KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Participantes", total_participantes)
kpi2.metric("Mulheres", mulheres)
kpi3.metric("Homens", homens)
kpi4.metric("Outros Gêneros", outros)

st.markdown("---")

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Histórico Familiar
with col1:
    history_counts = df_filtrado['family_history'].value_counts().reset_index()
    history_counts.columns = ['Histórico Familiar', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_familia = px.pie(
        history_counts,
        values='Quantidade',
        names='Histórico Familiar',
        title='<b>Distribuição: Histórico Familiar de Problemas Mentais</b>'
    )
    fig_familia.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_familia, use_container_width=True)

# Gráfico 2: Distribuição da Busca por Tratamento
with col2:
    treat_counts = df_filtrado['treatment'].value_counts().reset_index()
    treat_counts.columns = ['Tratamento', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_tratamento = px.pie(
        treat_counts,
        values='Quantidade',
        names='Tratamento',
        title='<b>Distribuição: Busca por Tratamento</b>',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_tratamento.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_tratamento, use_container_width=True)

col3, col4 = st.columns(2)

# Gráfico 3: Distribuição de Benefícios
with col3:
    benefits_counts = df_filtrado['benefits'].value_counts().reset_index()
    benefits_counts.columns = ['Benefícios', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_benefits = px.pie(
        benefits_counts,
        values='Quantidade',
        names='Benefícios',
        title='<b>Distribuição: Benefícios de Saúde Mental Oferecidos</b>',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig_benefits.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_benefits, use_container_width=True)

# Gráfico 4: Distribuição de Idade
with col4:
    df_idade_limpa = df_filtrado[(df_filtrado['Age'] >= 15) & (df_filtrado['Age'] <= 80)].copy()
    fig_idade = px.histogram(
        df_idade_limpa,
        x='Age',
        title='<b>Distribuição de Idade dos Participantes</b>',
        labels={'Age': 'Idade', 'count': 'Quantidade de Pessoas'},
        nbins=20
    )
    st.plotly_chart(fig_idade, use_container_width=True)