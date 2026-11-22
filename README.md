# Projeto Final AVD 2026.2 — Grupo 6 (Pump it Up, classificação)

Projeto da Avaliação II de **Análise e Visualização de Dados (AVD)** — CESAR School, 2026.2.
Título do enunciado: *Projeto Final: Agrupamento, EDA e Dashboard Interativo*.

| Parte | Dataset | Conteúdo | Responsável |
| --- | --- | --- | --- |
| **Comum** | [Wine Quality (UCI 186)](https://archive.ics.uci.edu/dataset/186) | EDA (4 pilares), padronização, K-Means em duas passadas, matriz de confusão e métricas, discussão crítica | João Vitor do Sacramento |
| **Específica** | [Pump it Up: Data Mining the Water Table (DrivenData)](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/) | Pergunta de pesquisa, EDA, storytelling, 6 visualizações, dashboard Streamlit, notas analíticas | Gustavo Henrique Cruz de Oliveira |

A matriz de contribuição está em [docs/MATRIZ_CONTRIBUICAO.md](docs/MATRIZ_CONTRIBUICAO.md).

## Calendário

| Etapa | Data |
| --- | --- |
| Checkpoint do dataset da Parte Específica | 27/10/2026 (aprovado) |
| Acompanhamentos em sala | 17/11, 19/11 e 24/11 |
| Entrega do material (todos os integrantes postam o link no Classroom) | 26/11/2026 |
| Apresentação | 03/12/2026 |

## Instalação

Requer **Python 3.11+**.

```bash
# 1. Criar o ambiente virtual
py -m venv .venv            # Windows
python3 -m venv .venv       # macOS / Linux

# 2. Ativar
.venv\Scripts\Activate.ps1  # Windows (PowerShell)
source .venv/bin/activate   # macOS / Linux

# 3. Instalar as dependências
python -m pip install -r requirements.txt
```

Bibliotecas usadas (apenas as permitidas pelo enunciado): pandas, numpy, matplotlib, seaborn, plotly, scikit-learn e streamlit. `jupyter`/`ipykernel` servem só para abrir os notebooks.

## Como executar

```bash
# PARTE COMUM (notebooks Jupyter)
jupyter notebook notebooks/parte_comum/eda.ipynb
jupyter notebook notebooks/parte_comum/kmeans_metricas.ipynb

# PARTE ESPECÍFICA
jupyter notebook src/parte_especifica/eda.ipynb
streamlit run src/parte_especifica/dashboard.py
```

Execute os comandos **a partir da raiz do repositório**. As figuras geradas vão para `out/parte_comum/` e `out/parte_especifica/`.

## Dados

- `data/parte_comum/`: `winequality-red.csv` e `winequality-white.csv` (separador `;`) e `winequality.names`. Detalhes em [data/parte_comum/README.md](data/parte_comum/README.md).
- `data/parte_especifica/raw/pump_it_up_train.csv`: dataset bruto (59.400 linhas × 41 colunas, valores e rótulos unificados). Como baixar do DrivenData (exige cadastro): [data/parte_especifica/README.md](data/parte_especifica/README.md).
- `data/parte_especifica/clean/`: dataset tratado, exportado ao final da EDA. O dashboard lê **só** desta pasta.

## Estrutura

```
├─ README.md
├─ requirements.txt
├─ docs/                      # Declaração de Uso de IA, matriz de contribuição
├─ data/
│  ├─ parte_comum/            # Wine Quality
│  └─ parte_especifica/       # Pump it Up (raw/ e clean/)
├─ out/
│  ├─ parte_comum/            # figuras e tabelas da Parte Comum
│  └─ parte_especifica/       # figuras e tabelas da Parte Específica
├─ notebooks/parte_comum/     # eda.ipynb, kmeans_metricas.ipynb
├─ src/
│  ├─ parte_comum/            # (optamos por notebooks; ver README da pasta)
│  └─ parte_especifica/       # eda.ipynb, dashboard.py
├─ _CONTEXTO_IA/              # contexto do projeto para assistentes de IA (ver Uso de IA)
└─ relatorio.pdf              # relatório técnico (entregue ao final)
```

## Uso de IA

O uso de IA generativa segue as regras do enunciado e está registrado em `docs/DECLARACAO_IA.pdf`. Trechos de código feitos com apoio de IA estão marcados com `# [IA] <ferramenta> – <finalidade>`. Análises, interpretações, discussões e notas analíticas são autorais do grupo.

A pasta `_CONTEXTO_IA/` reúne as regras do projeto num formato que um assistente de IA consegue ler. Ela existe para que o apoio de IA, quando usado, fique dentro do que o enunciado permite.

## Status

- [x] Estrutura inicial do repositório
- [ ] Parte Comum: EDA Wine Quality
- [ ] Parte Comum: padronização + K-Means (duas passadas) + métricas
- [ ] Parte Comum: discussão crítica
- [x] Parte Específica: código da EDA (4 pilares)
- [ ] Parte Específica: interpretações da EDA, tratamento dos dados e pergunta de pesquisa final
- [ ] Parte Específica: storytelling + 6 visualizações + notas analíticas
- [ ] Parte Específica: dashboard Streamlit
- [ ] Relatório PDF, Declaração de IA assinada, matriz de contribuição final
