import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from scipy import stats

st.set_page_config(layout="wide") # Opcional: deixa o layout mais largo
st.title("📈 Comparações por Grupos")

df = load_data()

# Dicionário para traduzir todas as respostas possíveis para português
mapa_traducao_geral = {
    'Yes': 'Sim',
    'No': 'Não',
    'Maybe': 'Talvez',
    "Don't know": 'Não Sei',
    'Some of them': 'Algum deles'
}

# Dicionário central de cores para todo o aplicativo
mapa_cores_geral = {
    'Sim': 'lightgreen',
    'Não': 'lightcoral',
    'Talvez': 'skyblue',
    'Não Sei': 'khaki',
    'Algum deles': 'khaki'
}


df['treatment_pt'] = df['treatment'].map(mapa_traducao_geral)
df['family_history_pt'] = df['family_history'].map(mapa_traducao_geral)
df['remote_work_pt'] = df['remote_work'].map(mapa_traducao_geral)
df['seek_help_pt'] = df['seek_help'].map(mapa_traducao_geral)
df['supervisor_pt'] = df['supervisor'].map(mapa_traducao_geral)


aba = st.selectbox("Escolha uma análise:", [
    "Tratamento x Histórico Familiar",
    "Ambiente de Trabalho x Tratamento",
    "Faixa Etária x Tratamento",
    "Gênero x Tratamento",
    "Proporção de Tratamento por Gênero",
    "Percepções sobre Apoio no Trabalho",
    "Medo de Consequências por Gênero"  
])

# --- Gráficos de Quantidade ---

if aba == "Tratamento x Histórico Familiar":
    # Usar as colunas traduzidas '_pt'
    cross_tab = pd.crosstab(df['family_history_pt'], df['treatment_pt']).reset_index().melt(id_vars='family_history_pt')
    fig = px.bar(
        cross_tab, 
        x='family_history_pt', 
        y='value', 
        color='treatment_pt',
        title="Tratamento x Histórico Familiar", 
        labels={'family_history_pt': 'Histórico Familiar', 'value': 'Quantidade', 'treatment_pt': 'Fez Tratamento?'},
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores
    )
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Ambiente de Trabalho x Tratamento":
    cross_tab = pd.crosstab(df['remote_work_pt'], df['treatment_pt']).reset_index().melt(id_vars='remote_work_pt')
    fig = px.bar(
        cross_tab, 
        x='remote_work_pt', 
        y='value', 
        color='treatment_pt', 
        title="Trabalho Remoto x Tratamento", 
        labels={'remote_work_pt': 'Trabalha Remoto?', 'value': 'Quantidade', 'treatment_pt': 'Fez Tratamento?'},
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores
    )
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Faixa Etária x Tratamento":
    df_idade = df[(df['age'] >= 15) & (df['age'] <= 80)].copy()
    bins = [15, 24, 34, 44, 54, 64, 80]
    labels = ['15-24', '25-34', '35-44', '45-54', '55-64', '65-80']
    df_idade['faixa_etaria'] = pd.cut(df_idade['age'], bins=bins, labels=labels)
    
    cross_tab = pd.crosstab(df_idade['faixa_etaria'], df_idade['treatment_pt']).reset_index().melt(id_vars='faixa_etaria')
    fig = px.bar(
        cross_tab, 
        x='faixa_etaria', 
        y='value', 
        color='treatment_pt', 
        title="Faixa Etária x Tratamento", 
        labels={'faixa_etaria': 'Faixa Etária', 'value': 'Quantidade', 'treatment_pt': 'Fez Tratamento?'},
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores
    )
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Gênero x Tratamento":
    cross_tab = pd.crosstab(df['gender_group'], df['treatment_pt']).reset_index().melt(id_vars='gender_group')
    fig = px.bar(
        cross_tab, 
        x='gender_group', 
        y='value', 
        color='treatment_pt', 
        title="Gênero x Tratamento", 
        labels={'gender_group': 'Gênero', 'value': 'Quantidade', 'treatment_pt': 'Fez Tratamento?'},
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Gráficos de Proporção ---

elif aba == "Proporção de Tratamento por Gênero":
    prop_treat = (
        df.groupby('gender_group')['treatment_pt'] # Usar a coluna traduzida
        .value_counts(normalize=True)
        .rename('proporcao')
        .reset_index()
    )

    fig = px.bar(
        prop_treat,
        x='gender_group',
        y='proporcao',
        color='treatment_pt', # Usar a coluna traduzida
        title='Percentual de Tratamento por Gênero',
        labels={'gender_group': 'Gênero', 'proporcao': 'Percentual (%)', 'treatment_pt': 'Fez Tratamento?'},
        text=prop_treat['proporcao'].apply(lambda x: f'{x*100:.1f}%'),
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores
    )

    fig.update_layout(barmode='stack', yaxis_tickformat='.0%', height=500)
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Percepções sobre Apoio no Trabalho":
    st.markdown("### Proporção de pessoas que podem buscar ajuda")
    grupo_ajuda = df.groupby(['gender_group', 'seek_help_pt']).size().reset_index(name='count')
    grupo_ajuda['proporcao'] = grupo_ajuda.groupby('gender_group')['count'].transform(lambda x: x / x.sum())

    fig1 = px.bar(
        grupo_ajuda, x='gender_group', y='proporcao', color='seek_help_pt',
        barmode='group', title='Proporção de pessoas que podem buscar ajuda, por grupo de gênero',
        labels={'proporcao': 'Proporção', 'gender_group': 'Gênero', 'seek_help_pt': 'Busca Ajuda?'},
        color_discrete_map=mapa_cores_geral
    )
    fig1.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    
    st.markdown("### Disposição para Falar com Supervisor sobre Saúde Mental")
    grupo_supervisor = df.groupby(['gender_group', 'supervisor_pt']).size().reset_index(name='count')
    grupo_supervisor['proporcao'] = grupo_supervisor.groupby('gender_group')['count'].transform(lambda x: x / x.sum())
    
    fig2 = px.bar(
        grupo_supervisor, x='gender_group', y='proporcao', color='supervisor_pt',
        barmode='group', title='Disposição para Falar com Supervisor, por Gênero',
        labels={'proporcao': 'Proporção de Respostas', 'gender_group': 'Gênero', 'supervisor_pt': 'Disposição'},
        color_discrete_map=mapa_cores_geral
    )
    fig2.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig2, use_container_width=True)

elif aba == "Medo de Consequências por Gênero":
    st.markdown("### Análise: Medo de Consequências no Trabalho por Gênero")
    st.write(
        "Investigamos se o gênero influencia a percepção de que falar sobre saúde mental "
        "pode trazer consequências negativas no ambiente de trabalho."
    )

    # Traduzir a coluna específica para esta análise
    df['mental_health_consequence_pt'] = df['mental_health_consequence'].map(mapa_traducao_geral)

    # Análise Estatística (Teste Qui-quadrado) em um expander
    with st.expander("Ver análise estatística (Teste Qui-quadrado)"):
        contingency_mhc = pd.crosstab(df['gender_group'], df['mental_health_consequence_pt'])
        st.write("**Tabela de Contingência (Contagem)**")
        st.dataframe(contingency_mhc)

        try:
            chi2, p, dof, ex = stats.chi2_contingency(contingency_mhc)
            st.write("**Resultado do Teste Qui-quadrado:**")
            st.markdown(f"""
            * **Estatística Qui-quadrado (χ²):** `{chi2:.3f}`
            * **p-valor:** `{p:.4f}`
            """)

            if p < 0.05:
                st.success(
                    "**Conclusão:** Com um p-valor menor que 0.05, existe uma associação "
                    "estatisticamente significativa entre o gênero e o medo de consequências."
                )
            else:
                st.warning(
                    "**Conclusão:** Com um p-valor maior que 0.05, não há evidências de uma "
                    "associação estatisticamente significativa entre as variáveis."
                )
        except ValueError as e:
            st.error(f"Não foi possível realizar o teste Qui-quadrado. Erro: {e}")

    # Preparação dos dados para o gráfico de proporção
    prop_df = (
        df.groupby('gender_group')['mental_health_consequence_pt']
        .value_counts(normalize=True)
        .rename('proporcao')
        .reset_index()
    )

    # Criação do Gráfico de Proporção
    st.markdown("---")
    st.subheader("Gráfico de Proporção")

    fig = px.bar(
        prop_df,
        x='gender_group',
        y='proporcao',
        color='mental_health_consequence_pt',
        barmode='group',
        title='Proporção do Medo de Consequências no Trabalho por Gênero',
        labels={
            "gender_group": "Gênero",
            "proporcao": "Proporção das Respostas",
            "mental_health_consequence_pt": "Haverá consequências?"
        },
        text_auto='.2%',
        color_discrete_map=mapa_cores_geral # Aplicar mapa de cores global
    )
    fig.update_yaxes(tickformat=".0%") # Formatar eixo Y como porcentagem
    st.plotly_chart(fig, use_container_width=True)