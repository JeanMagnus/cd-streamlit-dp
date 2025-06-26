import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard de Saúde Mental na Tech",
                   page_icon="🧠",
                   layout="wide")

# --- Carregamento e Limpeza dos Dados (Função única com cache) ---
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv')
    
    # Limpeza de Gênero
    male_terms = ['Cis Male', 'Cis Man', 'M', 'Mail', 'Make', 'Mal', 'Male', 'Male (CIS)', 'Malr', 'Man', 'cis male', 'm', 'maile', 'male', 'msle']
    female_terms = ['Cis Female', 'F', 'Femake', 'Female', 'Female (cis)', 'Woman', 'cis-female/femme', 'f', 'femail', 'female', 'woman']
    trans_terms = ['Female (trans)', 'Trans woman', 'Trans-female']
    nonbinary_terms = ['Agender', 'All', 'Androgyne', 'Enby', 'Genderqueer', 'Guy (-ish) ^_^', 'Nah', 'Neuter', 'fluid', 'male leaning androgynous', 'non-binary', 'ostensibly male, unsure what that really means', 'p', 'queer', 'queer/she/they', 'something kinda male?', 'Male-ish', 'A little about you']

    def classify_gender_custom(g):
        g = str(g).strip()
        if g in male_terms: return 'Homem'
        elif g in female_terms: return 'Mulher'
        elif g in trans_terms: return 'Trans'
        elif g in nonbinary_terms: return 'Não-binário'
        else: return 'Outro'
    
    df['Gender_clean'] = df['Gender'].apply(classify_gender_custom)

    # Limpeza de outras colunas e remoção de dados inválidos
    df_clean = df[df['family_history'].isin(['Yes', 'No'])]
    df_clean = df_clean[df_clean['treatment'].isin(['Yes', 'No'])]
    df_clean = df_clean[df_clean['remote_work'].isin(['Yes', 'No'])]
    df_clean = df_clean[(df_clean['Age'] >= 18) & (df_clean['Age'] <= 75)]

    # Criar faixas etárias
    bins = [18, 24, 34, 44, 54, 65, 75]
    labels = ['18-24', '25-34', '35-44', '45-54', '55-65', '65+']
    df_clean['faixa_etaria'] = pd.cut(df_clean['Age'], bins=bins, labels=labels, right=False)

    return df_clean

df = load_data()

# --- TÍTULO ---
st.title("🧠 Dashboard: Saúde Mental no Setor de Tecnologia")
st.markdown("##")

# --- CRIAÇÃO DAS ABAS ---
tab1, tab2, tab3 = st.tabs(["📊 Análise Geral", "⚖️ Comparações", "🔗 Correlação"])


# ======== ABA 1: ANÁLISE GERAL ========
with tab1:
    st.header("Visão Geral do Perfil e Comportamento")

    # KPIs
    total_participantes = len(df)
    pct_tratamento = (df[df['treatment'] == 'Yes'].shape[0] / total_participantes) * 100

    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric(label="Total de Participantes Analisados", value=f"{total_participantes}")
    with kpi2:
        st.metric(label="% que Buscaram Tratamento", value=f"{pct_tratamento:.1f}%")

    st.markdown("---")

    # Gráficos Principais
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("O Fator Determinante: Histórico Familiar")
        fig_hist = px.histogram(df, x='family_history', color='treatment', barmode='group', text_auto=True,
                                title='Busca por Tratamento vs. Histórico Familiar',
                                labels={'family_history': 'Histórico Familiar', 'count': 'Nº de Pessoas', 'treatment': 'Buscou Tratamento?'})
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.subheader("Diferenças na Busca por Ajuda entre Gêneros")
        # Usando o histograma com proporção para um gráfico 100% empilhado
        fig_gender = px.histogram(df, x='Gender_clean', color='treatment', barnorm='percent', text_auto='.1f',
                                  title='Proporção de Tratamento por Gênero',
                                  labels={'Gender_clean': 'Gênero', 'treatment': 'Buscou Tratamento?'})
        st.plotly_chart(fig_gender, use_container_width=True)

# ======== ABA 2: COMPARAÇÕES ========
with tab2:
    st.header("Comparações por Ambiente e Demografia")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Trabalho Remoto vs. Presencial")
        fig_remote = px.histogram(df, x='remote_work', color='treatment', barnorm='percent', text_auto='.1f',
                                  title='Proporção de Tratamento por Modelo de Trabalho',
                                  labels={'remote_work': 'Trabalho Remoto?', 'treatment': 'Buscou Tratamento?'},
                                  color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_remote, use_container_width=True)
    
    with col2:
        st.subheader("Busca por Tratamento por Faixa Etária")
        fig_age = px.histogram(df, x='faixa_etaria', color='treatment', barmode='group', text_auto=True,
                               title='Contagem de Tratamento por Faixa Etária',
                               labels={'faixa_etaria': 'Faixa Etária', 'count': 'Nº de Pessoas', 'treatment': 'Buscou Tratamento?'},
                               category_orders={"faixa_etaria": ['18-24', '25-34', '35-44', '45-54', '55-65', '65+']},
                               color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_age, use_container_width=True)

# ======== ABA 3: CORRELAÇÃO ========
with tab3:
    st.header("Análise de Correlação e Influência de Fatores")
    
    st.markdown("""
    A matriz de correlação mostra a força da relação entre diferentes fatores e a **busca por tratamento**. 
    Valores próximos de 1 (azul forte) ou -1 (vermelho forte) indicam uma correlação forte. Valores próximos de 0 indicam pouca ou nenhuma correlação.
    """)

    # Preparando dados para correlação (seu código da EDA)
    cols_corr = ['treatment', 'benefits', 'care_options', 'seek_help', 'anonymity', 'family_history', 'remote_work']
    df_corr = df[cols_corr].copy()
    
    for col in cols_corr:
        df_corr[col] = df_corr[col].map({'Yes': 1, 'No': 0})

    df_corr.dropna(inplace=True)
    corr_matrix = df_corr.corr()
    
    # Renomeando para português para o gráfico
    labels_pt = {
        'treatment': 'Tratamento', 'benefits': 'Benefícios', 'care_options': 'Opções de Cuidado',
        'seek_help': 'Busca por Ajuda', 'anonymity': 'Anonimato', 'family_history': 'Hist. Familiar', 'remote_work': 'Trab. Remoto'
    }
    corr_matrix.rename(columns=labels_pt, index=labels_pt, inplace=True)

    # Criando o heatmap
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    plt.title('Matriz de Correlação: Fatores vs. Busca por Tratamento')
    
    st.pyplot(fig)
    
    st.markdown("""
    **Conclusão da Correlação:**
    - **Histórico Familiar (0.37):** Possui a correlação positiva mais significativa com a busca por tratamento.
    - **Opções de Cuidado (0.26):** Também mostra uma correlação relevante.
    - **Outros Fatores:** Os demais fatores como benefícios, anonimato e trabalho remoto apresentam correlação muito baixa, indicando menor influência direta na decisão de buscar tratamento neste conjunto de dados.
    """)