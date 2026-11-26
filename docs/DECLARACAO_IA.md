# Declaração de Uso de IA — Projeto Final AVD 2026.2, Grupo 6

**Integrantes ativos:** Gustavo Henrique Cruz de Oliveira; Arthur de Assis Borges; João Vitor do Sacramento Bezerra da Cunha  
**Período do trabalho:** 22/11/2026 a 26/11/2026  

## Regras seguidas (enunciado)
- **Permitido, com registro:** dúvidas conceituais; entender erros e depurar código do grupo; apoio com pandas, scikit-learn e Streamlit; revisão de ortografia e clareza.
- **Proibido:** gerar análises, discussões, conclusões ou notas analíticas sem autoria do grupo; pedir que a IA interprete gráficos ou escolha sozinha o tipo de gráfico/história sem decisão do aluno; entregar código que ninguém do grupo saiba explicar.
- Todos os trechos de código feitos com apoio de IA estão marcados com `# [IA] <ferramenta> – <finalidade>`.

---

## 1. Gustavo Henrique Cruz de Oliveira (Parte Específica: Pump it Up, Dashboard e Diagramação)

### Ferramentas utilizadas
Claude Code (Anthropic) e Gemini via Antigravity (Google).

### Tipos de pedido feitos
- **Organização do projeto:** criação da estrutura de pastas exigida pelo enunciado, `README.md`, `requirements.txt`, `.gitignore`, esqueletos dos notebooks e do dashboard, e da pasta `_CONTEXTO_IA/` com as regras do projeto.
- **Consulta ao material de aula e dúvidas conceituais:** leitura dos slides oficiais (`AVD/Slides/`, Aulas 01, 05, 06, 09, 10, 14, 15, 21 a 23, 25 e 26) e do enunciado para tirar dúvidas conceituais (alta cardinalidade, mecanismos MCAR/MAR/MNAR, One-Hot vs. Target Encoding, árvores/Random Forest, importância por impureza vs. correlação isolada, robustez a outliers, data leakage e formato da Big Idea) mantendo o projeto estritamente no escopo da disciplina.
- **Geração e melhoria de código para a EDA da Parte Específica** (`src/parte_especifica/eda.ipynb`): código para os 4 pilares, inclusão da coluna `glossario` nas tabelas, hierarquia de seções, títulos (`<caption>`), ajustes de layout (`3x2`/`3x1`), correção do renderizador Plotly, paletas semânticas acessíveis (`YlOrRd`, `Blues`, `RdBu_r`), cruzamentos multivariados escolhidos pelo aluno e código da Seção 6 (implementando as decisões de tratamento do aluno e exportação para `data/parte_especifica/clean/pump_it_up_clean.csv`).
- **Revisão de ortografia, clareza e conferência factual de números** nos textos autorais escritos pelo aluno na EDA (`0.1`, `1.6`, `2.6`, `3.7`, `4.9`, `5.5`, `6.1` e `7.1`), no Classificador (`6.1`) e na Big Idea.
- **Geração de código para o classificador** (`src/parte_especifica/classificador.ipynb`): pipeline sem *data leakage* (reversão controlada das flags `ausente_*` antes do split estratificado 80/20, `ImputadorCascata`, `OneHotEncoder` + `TargetEncoder`, `DecisionTreeClassifier` baseline e `RandomForestClassifier`), matrizes de confusão, métricas por classe, importância agregada das variáveis e demonstração auditável passo a passo (`decision_path`) em 3 bombas reais do teste.
- **Geração de código para figuras finais e dashboard Streamlit com Bônus UX/UI** (`.streamlit/config.toml`, `src/parte_especifica/data_loader.py`, `src/parte_especifica/gerar_figuras_finais.py` e `src/parte_especifica/dashboard.py`): aplicação das boas práticas de UI/UX em Streamlit (`SKILL_DESIGN/` + identidade visual RecifeView Seção 2.1 + paleta Okabe-Ito), cache separado (`@st.cache_data` e `@st.cache_resource`), controles nativos modernos (`st.pills`, `st.segmented_control`, `@st.fragment`), Comparador lado a lado de duas regiões, Heatmap livre de duas variáveis, aba interativa do classificador com sorteio e auditoria `decision_path`, Aba 4 animada do K-Means Wine Quality (PCA 2D), 7 figuras estáticas limpas e exportação CSV/Markdown.
- **Padronização visual dos gráficos da Parte Comum e diagramação em PDF** (`notebooks/parte_comum/`, `docs/gerar_relatorio.py` -> `relatorio.pdf`, `docs/gerar_apresentacao.py` -> `docs/APRESENTACAO_AVD_G6.pdf`, `docs/ROTEIRO_APRESENTACAO.md/.pdf`, `docs/GUIA_ARGUICAO_E_VARIAVEIS.md/.pdf` e `docs/GLOSSARIO.md`): ajuste de títulos, eixos em pt-BR, legendas e paleta dos gráficos de *Wine Quality* (preservando integralmente todos os cálculos e conclusões do Arthur Borges), compilação editorial dos textos autorais em PDFs padronizados (A4 e 16:9), organização do roteiro dividido entre os 3 integrantes e guia de estudo de variáveis e perguntas técnicas para a arguição de 03/12/2026.

### O que foi aceito, modificado ou rejeitado e por quê
- **Aceito:** estrutura de pastas, código de tabelas/gráficos da EDA, pipeline anti-data-leakage do classificador, camada de cache e interface do dashboard Streamlit, padronização visual dos gráficos/PDFs e revisões de ortografia/conferência numérica.
- **Modificado pelo aluno:** remoção de colunas redundantes/irrelevantes (`num_private`, `scheme_name`, irmãos detalhados das 7 famílias), decisão de imputação em cascata (`lga -> region -> basin`) com flags `ausente_*`, ajuste visual de legendas sobrepostas nos gráficos do classificador e das anotações nas figuras explanatórias, definição do público-alvo e da Big Idea, ordem da apresentação e escolha de manter as 3 visualizações explanatórias junto às 4 exploratórias.
- **Rejeitado:** tentativas iniciais de delegar interpretação de gráficos ou uso de bibliotecas fora do escopo (como `scipy`/`ipywidgets`), mantendo as interpretações autorais do aluno e usando apenas as bibliotecas permitidas pelo enunciado.

---

## 2. Arthur de Assis Borges (Parte Comum: Wine Quality, EDA e K-Means)

### Ferramentas utilizadas
ChatGPT (OpenAI), conforme marcações `# [IA] ChatGPT – ...` em `notebooks/parte_comum/eda.ipynb` e `notebooks/parte_comum/kmeans_metricas.ipynb` (com posterior padronização visual dos gráficos via Gemini na integração final).

### Tipos de pedido feitos
- Apoio à implementação em Python (pandas, matplotlib, seaborn e scikit-learn) de cálculos, tabelas, gráficos da EDA (`notebooks/parte_comum/eda.ipynb`), `StandardScaler`, loop do Método do Cotovelo, K-Means em duas passadas (`k = 3` e `k = 7`), projeção PCA 2D, matrizes de confusão e métricas por classe (`notebooks/parte_comum/kmeans_metricas.ipynb`).

### O que foi aceito, modificado ou rejeitado e por quê
- **Aceito/Modificado pelo integrante:** estrutura de código das tabelas/gráficos e do K-Means, decisão pelo dataset combinado *Wine Quality* (6.497 × 13), manutenção das duplicatas/outliers, escolha de `k = 3` no Método do Cotovelo e discussão crítica comparativa.

---

## 3. João Vitor do Sacramento Bezerra da Cunha (Parte Comum: exploração inicial)

### Ferramentas utilizadas
*(a preencher pelo integrante antes da assinatura final)*

### Tipos de pedido feitos
*(a preencher pelo integrante antes da assinatura final)*

### O que foi aceito, modificado ou rejeitado e por quê
*(a preencher pelo integrante antes da assinatura final)*

---

## Assinaturas

| Integrante | Assinatura / Confirmação | Data |
| --- | --- | --- |
| Gustavo Henrique Cruz de Oliveira | Gustavo Henrique Cruz de Oliveira | 26/11/2026 |
| Arthur de Assis Borges | Arthur de Assis Borges | 26/11/2026 |
| João Vitor do Sacramento Bezerra da Cunha | *(pendente assinatura do integrante)* | 26/11/2026 |
