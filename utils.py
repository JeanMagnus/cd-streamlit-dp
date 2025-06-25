import pandas as pd
import streamlit as st

def classify_gender_custom(g):
    g = str(g).strip().lower()
    male_terms = ['cis male', 'm', 'male', 'man']
    female_terms = ['cis female', 'f', 'female', 'woman']
    trans_terms = ['trans', 'transgender']
    nonbinary_terms = ['non-binary', 'nonbinary', 'nb']

    if g in male_terms:
        return 'Homem'
    elif g in female_terms:
        return 'Mulher'
    elif g in trans_terms:
        return 'Trans'
    elif g in nonbinary_terms:
        return 'Não-binárie'
    else:
        return 'Outro'

@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv')
    df['Gender_clean'] = df['Gender'].apply(classify_gender_custom)
    return df
