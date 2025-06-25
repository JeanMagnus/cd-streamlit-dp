import streamlit as st


st.sidebar.success("Página Inicial", icon="🏠")
st.set_page_config(page_title="Projeto Saúde Mental", layout="wide")
st.title("🧠 Saúde Mental no Setor de Tecnologia")

st.markdown("""
Este projeto usa dados da **OSMI (Open Sourcing Mental Illness)** para analisar padrões relacionados à saúde mental entre profissionais de tecnologia.

Explore as páginas ao lado para navegar entre:
- 📊 Estatísticas e visualizações gerais
- 📈 Comparações por gênero, país, idade e trabalho remoto
- 🔁 Correlações entre fatores de apoio e tratamento

Os dados foram obtidos diretamente do repositório [OSMI](https://osmihelp.org/research).
""")

# st.image("https://miro.medium.com/v2/resize:fit:1200/1*iEzMdG7CQyLP6JAL51_X1g.png", use_column_width=True)
