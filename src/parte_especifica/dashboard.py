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

# [IA] Gemini – marcação das seções de intervenção autoral exigidas pelo enunciado (sem escolher gráficos nem gerar análises)
# =============================================================================
# [AUTORAL] 1. Carga de dados tratados (data/parte_especifica/clean/) com @st.cache_data
#   - Definir colunas finais após as decisões da Seção 6 do eda.ipynb (sem acentos nos nomes).
#
# [AUTORAL] 2. Público-alvo e Storytelling
#   - Definir linguagem, hierarquia visual, identidade visual (.streamlit/config.toml) e filtros.
#
# [AUTORAL] 3. Visualizações Exploratórias (mínimo 4) + Notas Analíticas Autorais
#   - Escolher tipos de gráficos coerentes com os dados (título, legenda e eixos obrigatórios).
#   - Escrever nota analítica autoral para cada gráfico (o que mostra, insight, por que o gráfico).
#
# [AUTORAL] 4. Visualizações Explanatórias (mínimo 2, >=1 respondendo à pergunta) + Notas Analíticas
#   - Escolher tipos de gráficos e atributos pré-atentivos (cor, tamanho, posição) que destacam a mensagem.
#   - Escrever nota analítica autoral para cada gráfico.
#
# [AUTORAL] 5. (Opcional — Bônus Visual/UX até +1,0)
#   - Filtros dinâmicos interligados, seleção de variáveis/eixos, página da Parte Comum / animação K-Means.
# =============================================================================
