import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(layout="wide")
st.title("Análise Geral dos Dados")

df = load_data()

# Filtros
st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("País de residência:", options=df["Country"].unique(), default=df["Country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["Gender_clean"].unique(), default=df["Gender_clean"].unique())

df_filtrado = df[(df["Country"].isin(paises)) & (df["Gender_clean"].isin(generos))]
df_idade_limpa = df_filtrado[(df_filtrado['Age'] >= 15) & (df_filtrado['Age'] <= 80)].copy()

st.markdown("### Estatísticas Descritivas da Idade")
st.dataframe(df_idade_limpa['Age'].describe().to_frame(), use_container_width=True)

col1, col2 = st.columns(2)

# Gráfico de histórico familiar
with col1:
    history_counts = df_filtrado['family_history'].replace({'Yes': 'Sim', 'No': 'Não'}).value_counts().reset_index()
    history_counts.columns = ['Histórico Familiar', 'Quantidade']
    fig_familia = px.pie(
        history_counts, 
        values='Quantidade', 
        names='Histórico Familiar',
        title='Histórico Familiar de Problemas Mentais',
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    fig_familia.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=1))
    col1.plotly_chart(fig_familia, use_container_width=True)

# Gráfico de tratamento
with col2:
    treat_counts = df_filtrado['treatment'].replace({'Yes': 'Sim', 'No': 'Não'}).value_counts().reset_index()
    treat_counts.columns = ['Tratamento', 'Quantidade']
    fig_tratamento = px.bar(
        treat_counts, 
        x='Tratamento', 
        y='Quantidade', 
        color='Tratamento',
        title='Busca por Tratamento',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_tratamento.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    col2.plotly_chart(fig_tratamento, use_container_width=True)

col3, col4 = st.columns(2)

# Gráfico de benefícios
with col3:
    benefits_counts = df_filtrado['benefits'].replace({'Yes': 'Sim', 'No': 'Não', "Don't know": 'Não sabe'}).value_counts().reset_index()
    benefits_counts.columns = ['Benefícios', 'Quantidade']
    fig_benefits = px.pie(
        benefits_counts, 
        values='Quantidade', 
        names='Benefícios',
        title='Benefícios Relacionados à Saúde Mental',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    # --- AJUSTE DA LEGENDA ---
    fig_benefits.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    col3.plotly_chart(fig_benefits, use_container_width=True)

# Gráfico de boxplot (idade x tratamento)
with col4:
    df_idade_limpa['treatment'] = df_idade_limpa['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
    fig_box = px.box(df_idade_limpa, x='treatment', y='Age', color='treatment',
        title='Distribuição da Idade por Tratamento',
        labels={
            "treatment": "Buscou Tratamento?",
            "Age": "Idade"
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_box.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.6, xanchor="right", x=0.95))
    col4.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("Observação: Os dados de idade foram filtrados entre 15 e 80 anos.")