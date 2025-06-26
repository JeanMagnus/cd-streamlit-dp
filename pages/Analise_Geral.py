import streamlit as st
import plotly.express as px
from utils import load_data

# Configuração da página
st.set_page_config(page_title="Análise Geral", layout="wide")

# Título
st.markdown("## 🧠 Análise Geral da Saúde Mental na Área de Tecnologia")
st.markdown("---")

# Carregando dados
df = load_data()

# Métricas rápidas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Participantes", len(df))
col2.metric("Com Tratamento", df['treatment'].value_counts().get('Yes', 0))
col3.metric("Com Histórico Familiar", df['family_history'].value_counts().get('Yes', 0))

# Visualização dos dados
st.markdown("### 🔎 Pré-visualização dos Dados")
st.dataframe(df.head(), use_container_width=True)

# Estatísticas descritivas
st.markdown("### 📊 Estatísticas Descritivas")
st.write(df.describe())

# Gráfico de distribuição de histórico familiar
st.markdown("### 🧬 Distribuição de Histórico Familiar")
history_counts = df['family_history'].value_counts().reset_index()
history_counts.columns = ['Histórico Familiar', 'Quantidade']

fig_pie = px.pie(
    history_counts,
    values='Quantidade',
    names='Histórico Familiar',
    title='Histórico Familiar de Problemas Mentais',
    color_discrete_sequence=px.colors.sequential.RdBu
)

st.plotly_chart(fig_pie, use_container_width=True)
