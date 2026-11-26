# Projeto Final AVD 2026.2 — Grupo 6 (Pump it Up, classificação)

Projeto da Avaliação II de **Análise e Visualização de Dados (AVD)** — CESAR School, 2026.2.
Título do enunciado: *Projeto Final: Agrupamento, EDA e Dashboard Interativo*.

| Parte | Dataset | Conteúdo | Responsável |
| --- | --- | --- | --- |
| **Comum** | [Wine Quality combinado (UCI 186)](https://archive.ics.uci.edu/dataset/186) | EDA (4 pilares), padronização, K-Means em duas passadas (`k = 3` e `k = 7`), matriz de confusão, métricas e discussão crítica | Arthur Borges e João Vitor do Sacramento |
| **Específica** | [Pump it Up: Data Mining the Water Table (DrivenData)](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/) | Pergunta de pesquisa, EDA, classificador sem *data leakage*, storytelling, 7 visualizações, dashboard Streamlit com Bônus UX/UI, relatório, apresentação e guia de defesa | Gustavo Henrique Cruz de Oliveira |

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

# PARTE ESPECÍFICA (notebooks, figuras, dashboard e PDFs)
jupyter notebook src/parte_especifica/eda.ipynb
jupyter notebook src/parte_especifica/classificador.ipynb
streamlit run src/parte_especifica/dashboard.py
python docs/gerar_relatorio.py
python docs/gerar_apresentacao.py
```

**No Google Colab** (sem instalar nada): abra [`eda.ipynb` no Colab](https://colab.research.google.com/github/Fyre-Flye/projeto-avd-2026-2-pump-it-up-classificatorio/blob/master/src/parte_especifica/eda.ipynb) e rode a primeira célula de código, que clona o repositório. O Colab sempre abre a versão mais recente da `master`.

Execute os comandos **a partir da raiz do repositório**. As figuras geradas vão para `out/parte_comum/` e `out/parte_especifica/`.

## Dados

- `data/parte_comum/`: os dois datasets permitidos pelo enunciado, e o grupo usa um. São eles `wine_quality/` (`winequality-red.csv`, `winequality-white.csv` e `winequality-combined.csv` com os dois juntos, separador `;`) e `obesity/` (`ObesityDataSet_raw_and_data_sinthetic.csv`). Comparação em [data/parte_comum/README.md](data/parte_comum/README.md).
- `data/parte_especifica/raw/pump_it_up_train.csv`: dataset bruto (59.400 linhas × 41 colunas, valores e rótulos unificados). Como baixar do DrivenData (exige cadastro): [data/parte_especifica/README.md](data/parte_especifica/README.md).
- `data/parte_especifica/clean/`: dataset tratado, exportado ao final da EDA. O dashboard lê **só** desta pasta.

## Estrutura

```
├─ README.md
├─ requirements.txt
├─ docs/                      # Declaração de Uso de IA, matriz de contribuição, glossário
├─ data/
│  ├─ parte_comum/            # Wine Quality e Obesity (o grupo usa um)
│  └─ parte_especifica/       # Pump it Up (raw/ e clean/)
├─ out/
│  ├─ parte_comum/            # figuras e tabelas da Parte Comum
│  └─ parte_especifica/       # figuras e tabelas da Parte Específica
├─ notebooks/parte_comum/     # eda.ipynb, kmeans_metricas.ipynb
├─ src/
│  ├─ parte_comum/            # (optamos por notebooks; ver README da pasta)
│  └─ parte_especifica/       # eda.ipynb, dashboard.py
├─ _CONTEXTO_IA/              # contexto do projeto para assistentes de IA (ver Uso de IA)
├─ Requisitos/                # enunciado (PDF com e sem marcação de quem faz cada parte) e print do checkpoint
└─ relatorio.pdf              # relatório técnico (entregue ao final)
```

## Uso de IA

O uso de IA generativa segue as regras do enunciado e está registrado em `docs/DECLARACAO_IA.pdf`. Trechos de código feitos com apoio de IA estão marcados com `# [IA] <ferramenta> – <finalidade>`. Análises, interpretações, discussões e notas analíticas são autorais do grupo.

A pasta `_CONTEXTO_IA/` reúne as regras do projeto num formato que um assistente de IA consegue ler. Para IAs que não leem o repositório (ChatGPT ou Gemini no navegador), o aluno cola o conteúdo de `_CONTEXTO_IA/COLAR_NA_IA.md` no começo da conversa. Ela existe para que o apoio de IA, quando usado, fique dentro do que o enunciado permite.

## Status

- [x] Estrutura inicial do repositório
- [x] Parte Comum: EDA completa do *Wine Quality* combinado (`6.497 × 13`, `notebooks/parte_comum/eda.ipynb`)
- [x] Parte Comum: padronização (`StandardScaler`), K-Means em duas passadas (`k = 3` e `k = 7`), matrizes, métricas e discussão crítica (`notebooks/parte_comum/kmeans_metricas.ipynb`)
- [x] Parte Específica: código e interpretações da EDA (4 pilares), tratamento dos dados (`59.333 × 31`) e pergunta de pesquisa
- [x] Parte Específica: classificador (Árvore de Decisão baseline 75,33% + Random Forest 80,58%, sem *data leakage*, auditoria `decision_path`)
- [x] Parte Específica: storytelling + 7 visualizações finais (4 exploratórias + 3 explanatórias) e notas analíticas (`docs/STORYTELLING_E_NOTAS.md`)
- [x] Parte Específica: dashboard Streamlit com identidade visual RecifeView + Bônus Visual/UX (`src/parte_especifica/dashboard.py`, 5 abas incluindo K-Means Wine Quality animado)
- [x] Relatório técnico completo (`relatorio.pdf`), Apresentação 16:9 (`docs/APRESENTACAO_AVD_G6.pdf`), Roteiro em 3 (`docs/ROTEIRO_APRESENTACAO.md`), Guia de Arguição (`docs/GUIA_ARGUICAO_E_VARIAVEIS.md`) e Matriz de Contribuição (`docs/MATRIZ_CONTRIBUICAO.md`)
- [ ] Coleta final das assinaturas de Arthur Borges e Sacramento em `docs/DECLARACAO_IA.pdf`
