import streamlit as st
from pages import Analise_Geral, Comparacoes, Correlacoes

st.set_page_config(page_title="Projeto Saúde Mental", layout="wide")
st.title("🧠 Saúde Mental no Setor de Tecnologia")



st.markdown("""
Neste projeto, será utilizado o dataset **"Mental Health in Tech Survey"**, disponível no Kaggle, que reúne respostas de profissionais da área de tecnologia sobre saúde mental no ambiente de trabalho. A pesquisa foi organizada pela **OSMI (Open Sourcing Mental Illness)**, organização que promove conscientização sobre saúde mental, especialmente em ambientes técnicos.

A análise desse tipo de dado é extremamente relevante, pois a saúde mental vem se tornando um tema central nas discussões sobre qualidade de vida no trabalho. Identificar padrões, barreiras ao tratamento e relações com condições laborais pode ajudar empresas e profissionais a tomarem decisões mais conscientes e humanizadas.

Explore as páginas ao lado para navegar entre:
- 📊 Estatísticas e visualizações gerais
- 📈 Comparações por gênero, país, idade e trabalho remoto
- 🔁 Correlações entre fatores de apoio e tratamento


""")
#st.image("https://miro.medium.com/v2/resize:fit:1200/1*iEzMdG7CQyLP6JAL51_X1g.png", use_column_width=True)
