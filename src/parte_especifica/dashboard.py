"""Dashboard Streamlit — Parte Específica (Pump it Up).

Execução, a partir da raiz do repositório:
    streamlit run src/parte_especifica/dashboard.py
"""

# [IA] Claude Code – esqueleto inicial do app (placeholder até a EDA ficar pronta)
import streamlit as st

st.set_page_config(
    page_title="Pump it Up — Grupo 6",
    page_icon="💧",
    layout="wide",
)

st.title("Pump it Up: bombas d'água na Tanzânia")
st.caption("Projeto Final AVD 2026.2 — Grupo 6")

st.info(
    "Dashboard em construção. As visualizações entram depois da EDA "
    "(`src/parte_especifica/eda.ipynb`), lendo os dados tratados em "
    "`data/parte_especifica/clean/`."
)
