import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Uma boa prática para dar um visual mais profissional desde o início
st.set_page_config(page_title="Análise Geral | Saúde Mental na Tech",
                   page_icon="🧠",
                   layout="wide")

# --- Carregamento e Limpeza dos Dados ---
# Usar @st.cache_data faz com que os dados sejam carregados apenas uma vez, melhorando a performance.
# Se você já tem essa função em utils.py, pode mantê-la lá.
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv')
    
    # Padronização e Limpeza (Replicando a lógica da sua EDA)
    df_clean = df[df['family_history'].isin(['Yes', 'No'])]
    df_clean = df_clean[df_clean['treatment'].isin(['Yes', 'No'])]
    
    # Renomeando colunas para os gráficos ficarem mais claros
    df_clean.rename(columns={
        'family_history': 'Histórico Familiar',
        'treatment': 'Procurou Tratamento'
    }, inplace=True)
    return df_clean

# --- Início do Dashboard ---
st.title("📊 Análise Geral dos Dados")
df = load_data()

# --- KPIs (Indicadores Chave) ---
# Em vez de mostrar a tabela, mostramos os números mais importantes no topo.
st.markdown("### Visão Geral")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total de Participantes", df.shape[0])
with col2:
    pct_tratamento = (df[df['Procurou Tratamento'] == 'Yes'].shape[0] / df.shape[0]) * 100
    st.metric("% que Procuraram Tratamento", f"{pct_tratamento:.1f}%")

st.markdown("---")

# --- Visualizações de Insights ---
# Substituímos o gráfico de pizza por um que conta uma história mais completa.
st.subheader("O Fator mais Relevante: Histórico Familiar")

# Usamos colunas para organizar melhor os gráficos
left_column, right_column = st.columns(2)

with left_column:
    # Este gráfico é uma melhoria direta do seu gráfico de pizza.
    # Ele mostra não só a distribuição, mas a relação com a busca por tratamento.
    fig_hist = px.histogram(
        df,
        x='Histórico Familiar',
        color='Procurou Tratamento',
        barmode='group',
        text_auto=True,
        title='<b>Busca por Tratamento vs. Histórico Familiar</b>',
        labels={'count': 'Nº de Pessoas'},
        color_discrete_map={'Yes': '#1f77b4', 'No': '#ff7f0e'}
    )
    fig_hist.update_layout(
        yaxis_title="Número de Pessoas",
        legend_title_text='Buscou Tratamento?'
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with right_column:
    # Adicionamos um texto para explicar o insight do gráfico.
    st.markdown("<br><br>", unsafe_allow_html=True) # Espaçamento
    st.markdown(
        """
        #### Análise do Gráfico:
        O insight mais forte da análise é evidente aqui:
        
        - **Com Histórico Familiar:** A maioria (365) buscou tratamento.
        - **Sem Histórico Familiar:** A situação se inverte, e a maioria (495) **não** buscou tratamento.
        
        Isso sugere que a vivência ou conhecimento prévio sobre saúde mental na família é um fator determinante na decisão de procurar ajuda.
        """
    )