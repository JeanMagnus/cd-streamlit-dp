import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("📈 Comparações por Grupos")
df = load_data()

aba = st.selectbox("Escolha uma análise:", [
    "Tratamento x Histórico Familiar",
    "Ambiente de Trabalho x Tratamento",
    "Faixa Etária x Tratamento",
    "Gênero x Tratamento"
])

if aba == "Tratamento x Histórico Familiar":
    cross_tab = pd.crosstab(df['family_history'], df['treatment']).reset_index().melt(id_vars='family_history')
    fig = px.bar(cross_tab, x='family_history', y='value', color='treatment', title="Tratamento x Histórico Familiar", labels={'value': 'Quantidade'})
    st.plotly_chart(fig)

elif aba == "Ambiente de Trabalho x Tratamento":
    remote_treat = pd.crosstab(df['remote_work'], df['treatment']).reset_index().melt(id_vars='remote_work')
    fig = px.bar(remote_treat, x='remote_work', y='value', color='treatment', title="Trabalho Remoto x Tratamento", labels={'value': 'Quantidade'})
    st.plotly_chart(fig)

elif aba == "Faixa Etária x Tratamento":
    df = df[(df['Age'] >= 15) & (df['Age'] <= 80)].copy()
    bins = [15, 24, 34, 44, 54, 64, 80]
    labels = ['15-24', '25-34', '35-44', '45-54', '55-64', '65-80']
    df['faixa_etaria'] = pd.cut(df['Age'], bins=bins, labels=labels)
    faixa_treat = pd.crosstab(df['faixa_etaria'], df['treatment']).reset_index().melt(id_vars='faixa_etaria')
    fig = px.bar(faixa_treat, x='faixa_etaria', y='value', color='treatment', title="Faixa Etária x Tratamento", labels={'value': 'Quantidade'})
    st.plotly_chart(fig)

elif aba == "Gênero x Tratamento":
    genero_treat = pd.crosstab(df['Gender_clean'], df['treatment']).reset_index().melt(id_vars='Gender_clean')
    fig = px.bar(genero_treat, x='Gender_clean', y='value', color='treatment', title="Gênero x Tratamento", labels={'value': 'Quantidade'})
    st.plotly_chart(fig)