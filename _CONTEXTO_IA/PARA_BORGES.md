# PARA_BORGES: Integração Final Concluída (26/11/2026)

> **TUDO INTEGRADO (Parte Específica + Parte Comum Wine Quality):**
> O trabalho da Parte Comum que você subiu no commit `86287c9` (**Wine Quality combinado**, UCI 186, `6.497 × 13`) já foi revisado, reexecutado em ordem (`eda.ipynb` e `kmeans_metricas.ipynb` alinhados a `k = 3` vs. `k = 7`, `44,47%` vs. `45,67%`) e integrado em:
> - `relatorio.pdf` (10 páginas A4 completas, sem quadros pendentes)
> - `docs/APRESENTACAO_AVD_G6.pdf` (14 slides 16:9 completos, sem quadros pendentes)
> - `src/parte_especifica/dashboard.py` (Aba 4 atualizada para **Wine Quality** com transição animada `k = 3` -> `k = 7` em PCA 2D)
> - `docs/ROTEIRO_APRESENTACAO.md` (dividido nos 3, com você nos Slides 10 a 12)
> - `docs/GUIA_ARGUICAO_E_VARIAVEIS.md` (colinha das 31 variáveis Pump it Up + 13 variáveis Wine Quality + 20 perguntas)
> - `docs/MATRIZ_CONTRIBUICAO.md` (atualizada com a participação real de Gustavo, Arthur Borges e Sacramento)
> - `docs/DECLARACAO_IA.md` e `docs/DECLARACAO_IA.pdf` (seção do Arthur preenchida com `ChatGPT` conforme marcações nos notebooks)
>
> **ÚNICA PENDÊNCIA:** confirmar sua seção e adicionar as assinaturas finais de **Arthur Borges** e **João Vitor do Sacramento** em `docs/DECLARACAO_IA.pdf` e garantir que os 3 postem o link do repositório no Classroom!

---

## 1. O que JÁ ESTÁ 100% PRONTO e no GitHub (NÃO precisa refazer!)

| Entregável | Caminho no repo | Estado |
| --- | --- | --- |
| EDA completa Pump it Up (4 pilares + MAR + outliers + tratamento) | `src/parte_especifica/eda.ipynb` | 100% executada (101 células, 0 erros) + 8 seções autorais prontas |
| CSV tratado (59.333 × 31, 0 NaNs, 0 negativos) | `data/parte_especifica/clean/pump_it_up_clean.csv` | Validado |
| Classificador sem *data leakage* (Árvore 75,33% + RF 80,58% + auditoria `decision_path`) | `src/parte_especifica/classificador.ipynb` | 100% executado (29 células, 0 erros) + Seção 6.1 autoral |
| 7 figuras finais limpas (4 Exploratórias + 3 Explanatórias) | `out/parte_especifica/07_expl_01..04.png` e `08_explan_01`, `02a`, `02b.png` | Identidade visual Seção 2.1 + Okabe-Ito, auditadas visualmente |
| Storytelling + 7 Notas Analíticas | `docs/STORYTELLING_E_NOTAS.md` | Compiladas das interpretações autorais do Gustavo |
| **Dashboard Streamlit + Bônus UX/UI (+1,0 pt)** | `.streamlit/config.toml`, `src/parte_especifica/data_loader.py`, `src/parte_especifica/dashboard.py` | 5 abas, tema RecifeView, `st.pills`, `st.segmented_control`, `@st.fragment`, Comparador de 2 Regiões, Heatmap livre 2 variáveis, Auditoria `decision_path` e **Aba 4 animada do K-Means Obesity em PCA 2D** |
| **Relatório Técnico PDF (base completa)** | `relatorio.pdf` + `docs/gerar_relatorio.py` | 9 páginas A4 limpas (~2 MB), Parte Específica 100% pronta + bloco amarelo sinalizado na Página 9 para Parte Comum |
| **Apresentação 16:9 PDF** | `docs/APRESENTACAO_AVD_G6.pdf` + `docs/gerar_apresentacao.py` | 14 slides widescreen limpos (~1,8 MB), Parte Específica pronta + slots amarelos nos Slides 11, 12 e 13 para Parte Comum |
| **Roteiro de Apresentação dividido em 3** | `docs/ROTEIRO_APRESENTACAO.md` | Ordem: 1º Gustavo (Slides 1 a 9), 2º Arthur Borges (Slides 10 a 12), 3º Sacramento (Slides 13 e 14) |
| **Guia de Treino para Arguição e Variáveis** | `docs/GUIA_ARGUICAO_E_VARIAVEIS.md` | Protocolo 15s para 2 variáveis ao vivo, colinha das 31 colunas (Pump it Up) + 17 (Obesity), 14 pares prováveis e 20 perguntas difíceis |
| Glossário completo | `docs/GLOSSARIO.md` | Pronto |
| Declaração de Uso de IA (parte do Gustavo confirmada) | `docs/DECLARACAO_IA.md`, `docs/DECLARACAO_IA.pdf` | Falta preencher/assinar Arthur Borges e Sacramento |

---

## 2. EXATAMENTE o que faltou da Parte Comum (Sacramento) e precisa entrar no `relatorio.pdf` e nos slides

Estado encontrado em `notebooks/parte_comum/` (dataset escolhido pelo Sacramento: **Obesity, UCI 544**, `data/parte_comum/obesity/ObesityDataSet_raw_and_data_sinthetic.csv`, `2.111 × 17`, `NObeyesdad` com 7 classes, 0 nulos, 24 duplicadas, ~77% SMOTE):

- `notebooks/parte_comum/eda.ipynb`: apenas 6 de 22 células executadas (só checagem estrutural e 5 gráficos básicos em `out/parte_comum/`: `01_histogramas_1.png`, `01_histogramas_2.png`, `02_distribuicao_classes.png`, `03_categoricas_1.png`, `03_categoricas_2.png`).
- `notebooks/parte_comum/kmeans_metricas.ipynb`: **0 de 18 células executadas** (ainda esqueleto!).

### Itens exatos que precisam ser completados e inseridos no Relatório e na Apresentação:

1. **Seção 6.2 do Relatório (`notebooks/parte_comum/eda.ipynb`):**
   - **Pilar distribucional e relacional:** matriz de correlação das 8 numéricas (`Age`, `Height`, `Weight`, `FCVC`, `NCP`, `CH2O`, `FAF`, `TUE`) + boxplots / tabelas de contingência cruzando atributos com `NObeyesdad` (ex.: `Weight`, `Height`, `FAF`, `Gender`, `family_history_with_overweight`).
   - **Pilar de outliers e tratamento:** detecção via IQR/boxplots + decisão justificada sobre manter/tratar outliers e o que fazer com as **24 linhas duplicadas** e as **8 variáveis categóricas**.
   - Preencher todas as interpretações autorais pendentes no notebook e salvar figuras em `out/parte_comum/`.
2. **Seção 6.3 do Relatório e Slide 11 (`notebooks/parte_comum/kmeans_metricas.ipynb`):**
   - Padronização com `StandardScaler` nas variáveis numéricas (já justificada na Seção 6.1 do `relatorio.pdf` — confirmar se usaram só as 8 numéricas ou se codificaram categóricas).
   - **Passada 1 (`k` livre de 2 a 10):** gráfico do **Método do Cotovelo** (curva de inércia) + justificativa autoral do `k` escolhido + visualização dos grupos (ex.: PCA 2D ou `Weight × Height`).
   - **Passada 2 (`k` fixo = 7):** rodar K-Means com `k = 7` (= nº real de classes de `NObeyesdad`) + visualização dos 7 grupos.
   - Salvar os PNGs finais em `out/parte_comum/` (ex.: `04_cotovelo.png`, `05_clusters_passadas.png`).
3. **Seção 6.4 do Relatório e Slide 12 (`kmeans_metricas.ipynb`):**
   - Mapeamento de cada cluster para a classe majoritária de `NObeyesdad` (tabela de mapeamento nas duas passadas).
   - **Matriz de confusão** da Passada 1 (pode ser retangular) e da Passada 2 (quadrada 7×7), salvas em `out/parte_comum/` (ex.: `06_matrizes_confusao_kmeans.png`).
   - **Acurácia de coincidência, precisão e recall por classe** nas duas passadas (usando `zero_division=0` para classes sem cluster mapeado).
   - *(Dica: a Aba 4 do Dashboard Streamlit em `src/parte_especifica/data_loader.py` -> `executar_kmeans_parte_comum()` já roda uma referência em tempo real nas 8 numéricas padronizadas; se o seu notebook usar o mesmo `random_state=42`, `k_livre` e colunas, os números ficarão 100% idênticos entre notebook, relatório, slides e dashboard!)*
4. **Seção 6.5 do Relatório e Slide 13 (Discussão Crítica — vale 1,0 pt na rubrica!):**
   - Comparar **Passada 1 (`k` livre) vs. Passada 2 (`k = 7`)**: qual formou grupos mais coerentes nos dados?
   - Discutir criticamente a **granularidade das 7 classes originais** (`Insufficient_Weight`, `Normal_Weight`, `Overweight_Level_I`, `Overweight_Level_II`, `Obesity_Type_I`, `Obesity_Type_II`, `Obesity_Type_III`): o K-Means separa bem os extremos, mas níveis intermediários de IMC sobrepõem-se no espaço numérico sem supervisão.

---

## 3. Como atualizar `relatorio.pdf` e `docs/APRESENTACAO_AVD_G6.pdf` em 2 minutos

Os dois PDFs já estão 100% diagramados na identidade visual oficial (`_CONTEXTO_IA/06_GUIDELINES_PDF_E_APRESENTACAO.md`, Seção 2.1):

1. **No Relatório (`docs/gerar_relatorio.py`):**
   - Localize o bloco `<div class="box-alerta">` na variável `p9` (Página 9).
   - Substitua o alerta pelas Seções **6.2 a 6.5** com os gráficos de `out/parte_comum/` (use `img_tag(OUT_COM / "seu_grafico.png", "width:85%;")`) e, se precisar, crie `p10 = wrap_page(...)` para a Discussão Crítica + Seção 7 e adicione `p10` no `return [p1, ..., p10]`.
   - Rode na raiz do repositório:
     ```powershell
     python docs\gerar_relatorio.py
     ```
   - Confira se não apareceu nenhum `[AVISO] Pagina X teve conteudo excedente` no terminal!
2. **Na Apresentação (`docs/gerar_apresentacao.py`):**
   - Substitua os quadros `<div class="box-alerta">` nos **Slides 11, 12 e 13** (`s11`, `s12`, `s13`) pelas figuras de `out/parte_comum/`, métricas exatas e 3 bullets autorais da Discussão Crítica.
   - Rode na raiz do repositório:
     ```powershell
     python docs\gerar_apresentacao.py
     ```
   - Confira se não apareceu nenhum `[AVISO] Slide X teve conteudo excedente`!
3. **Alinhamento final:** verifique se os números de `kmeans_metricas.ipynb`, `relatorio.pdf`, `docs/APRESENTACAO_AVD_G6.pdf` e `docs/ROTEIRO_APRESENTACAO.md` batem 100%, e se o `k_livre` padrão em `src/parte_especifica/dashboard.py` (Aba 4) reflete o `k` escolhido no notebook.

---

## 4. Checklist de Ação Imediata para Arthur Borges (até 12h30 de 26/11/2026)

- [ ] Concluir `notebooks/parte_comum/eda.ipynb` e `notebooks/parte_comum/kmeans_metricas.ipynb` e salvar PNGs/CSVs em `out/parte_comum/`.
- [ ] Inserir Seções 6.2 a 6.5 em `docs/gerar_relatorio.py` e rodar `python docs/gerar_relatorio.py` para atualizar `relatorio.pdf`.
- [ ] Inserir figuras e métricas nos Slides 11 a 13 em `docs/gerar_apresentacao.py` e rodar `python docs/gerar_apresentacao.py`.
- [ ] Preencher as seções de **Arthur Borges** e **Sacramento** em `docs/DECLARACAO_IA.md` e gerar `docs/DECLARACAO_IA.pdf` com **assinaturas de todos os 3 integrantes ativos**.
- [ ] Atualizar `docs/MATRIZ_CONTRIBUICAO.md` marcando todas as contribuições reais do grupo (Gustavo, Arthur Borges e Sacramento).
- [ ] Fazer commits separados por etapa com autoria do Arthur Borges (**sem** `Co-Authored-By`), rodar `git pull --no-rebase --no-edit origin master` e `git push origin master`.
- [ ] Postar o link do repositório no Classroom até **12h30** e estudar `docs/ROTEIRO_APRESENTACAO.md` + `docs/GUIA_ARGUICAO_E_VARIAVEIS.md` para a defesa de **03/12/2026**.
