import streamlit as st
import pandas as pd
import plotly.express as px
# Assumindo que a função load_data está no seu arquivo utils.py
from utils import load_data

st.set_page_config(layout="wide")
st.title("📊 Análise Geral do Perfil dos Participantes")
st.markdown("Esta página apresenta a distribuição das principais variáveis da pesquisa.")

df_original = load_data()

<<<<<<< Updated upstream
# --- TRADUÇÃO E PREPARAÇÃO DOS DADOS ---
=======
>>>>>>> Stashed changes
df = df_original.copy()
df['family_history'] = df['family_history'].replace({'Yes': 'Sim', 'No': 'Não'})
df['treatment'] = df['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
df['benefits'] = df['benefits'].replace({'Yes': 'Sim', 'No': 'Não', "Don't know": 'Não sabe'})

# --- Filtros na Barra Lateral ---
st.sidebar.header("Filtros")
<<<<<<< Updated upstream
paises = st.sidebar.multiselect("País:", options=df["country"].unique(), default=df["country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["gender_group"].unique(), default=df["gender_group"].unique())

df_filtrado = df[(df["country"].isin(paises)) & (df["gender_group"].isin(generos))]
df_idade_limpa = df_filtrado[(df_filtrado['age'] >= 15) & (df_filtrado['age'] <= 80)].copy()

# --- LAYOUT PRINCIPAL ---
st.markdown(f"**Mostrando resultados para {df_filtrado.shape[0]} participantes.**")
=======
paises = st.sidebar.multiselect("País:", options=df["Country"].unique(), default=df["Country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["Gender_clean"].unique(), default=df["Gender_clean"].unique())

df_filtrado = df[(df["Country"].isin(paises)) & (df["Gender_clean"].isin(generos))]

total_participantes = df_filtrado.shape[0]
counts_genero = df_filtrado['Gender_clean'].value_counts()
homens = counts_genero.get('Homem', 0)
mulheres = counts_genero.get('Mulher', 0)
outros = counts_genero.get('Outro/Prefiro não dizer', 0)

texto_resultados = (
    f"**Mostrando resultados para {total_participantes} participantes:** "
    f"{mulheres} mulheres, {homens} homens e {outros} de outros gêneros."
)
st.markdown(texto_resultados)
# -----------------------------------------

>>>>>>> Stashed changes
st.markdown("---")

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Histórico Familiar
with col1:
    history_counts = df_filtrado['family_history'].value_counts().reset_index()
    history_counts.columns = ['Histórico Familiar', 'Quantidade']
<<<<<<< Updated upstream
    # CORREÇÃO: Formatação/indentação
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    # CORREÇÃO: Formatação/indentação
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    # CORREÇÃO: Formatação/indentação
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    df_idade_limpa['treatment'] = df_idade_limpa['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
    fig_box = px.box(df_idade_limpa, x='treatment', y='age', color='treatment',
        title='Distribuição da Idade por Tratamento',
        labels={"treatment": "Buscou Tratamento?", "age": "Idade"},
        color_discrete_sequence=px.colors.qualitative.Set2)


    st.plotly_chart(fig_box, use_container_width=True)





st.markdown("---")


st.markdown("Observação: Os dados de idade foram filtrados entre 15 e 80 anos.")
=======
    df_idade_limpa = df_filtrado[(df_filtrado['Age'] >= 15) & (df_filtrado['Age'] <= 80)].copy()
    fig_idade = px.histogram(
        df_idade_limpa,
        x='Age', 
        title='<b>Distribuição de Idade dos Participantes</b>',
        labels={'Age': 'Idade', 'count': 'Quantidade de Pessoas'},
        nbins=20
    )
    st.plotly_chart(fig_idade, use_container_width=True)
>>>>>>> Stashed changes
