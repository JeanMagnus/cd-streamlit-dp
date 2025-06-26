import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página (Melhor prática) ---
st.set_page_config(page_title="Dashboard de Saúde Mental na Tech",
                   page_icon="🧠",
                   layout="wide")

# --- Carregamento e Limpeza dos Dados (Usando Cache para performance) ---
# Mantenha sua função load_data() como está, só vamos adicionar o cache.
# Se sua função já está em utils.py, perfeito.
@st.cache_data
def load_data():
    # Vou replicar a lógica de limpeza aqui para o exemplo ser completo
    df = pd.read_csv('https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv')
    
    # Padronização de Gênero (Mantendo o que você já fez)
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
    df = df[df['family_history'].isin(['Yes', 'No'])]
    df = df[df['treatment'].isin(['Yes', 'No'])]
    
    # Renomeando colunas para os gráficos
    df.rename(columns={'family_history': 'Histórico Familiar', 'treatment': 'Procurou Tratamento'}, inplace=True)
    return df

df = load_data()

# --- TÍTULO ---
st.title("🧠 Análise de Saúde Mental no Setor de Tecnologia")
st.markdown("##")

# --- KPIs PRINCIPAIS ---
total_participantes = len(df)
procurou_tratamento_df = df[df['Procurou Tratamento'] == 'Yes']
pct_tratamento = (len(procurou_tratamento_df) / total_participantes) * 100

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de Participantes:")
    st.subheader(f"{total_participantes}")
with middle_column:
    st.subheader("Buscaram Tratamento:")
    st.subheader(f"{pct_tratamento:.1f}%")
with right_column:
    st.subheader("Com Histórico Familiar:")
    pct_hist_familiar = (df[df['Histórico Familiar'] == 'Yes'].shape[0] / total_participantes) * 100
    st.subheader(f"{pct_hist_familiar:.1f}%")

st.markdown("---")


# --- GRÁFICOS PRINCIPAIS (A história central) ---
left_column, right_column = st.columns(2)

with left_column:
    # Gráfico 1: Histórico Familiar vs. Tratamento (Seu insight mais forte!)
    st.subheader("O impacto do Histórico Familiar na busca por tratamento")
    df_hist = df.groupby(['Histórico Familiar', 'Procurou Tratamento']).size().reset_index(name='count')
    fig_hist = px.bar(df_hist, 
                      x="Histórico Familiar", 
                      y="count", 
                      color="Procurou Tratamento",
                      title="Busca por Tratamento vs. Histórico Familiar",
                      barmode='group',
                      text_auto=True,
                      labels={'count': 'Nº de Pessoas', 'Procurou Tratamento': 'Tratamento?'},
                      color_discrete_map={'Yes': '#1f77b4', 'No': '#ff7f0e'})
    fig_hist.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_hist)


with right_column:
    # Gráfico 2: Proporção de Tratamento por Gênero
    st.subheader("Como o Gênero influencia a busca por ajuda")
    df_gender_prop = df.groupby('Gender_clean')['Procurou Tratamento'].value_counts(normalize=True).mul(100).rename('percentual').reset_index()
    fig_gender = px.bar(df_gender_prop, 
                        x="Gender_clean", 
                        y="percentual", 
                        color="Procurou Tratamento", 
                        title="Proporção de Tratamento por Gênero",
                        text_auto='.1f',
                        labels={'percentual': '% de Pessoas', 'Gender_clean': 'Gênero', 'Procurou Tratamento': 'Tratamento?'},
                        color_discrete_map={'Yes': '#1f77b4', 'No': '#ff7f0e'})
    fig_gender.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_gender)