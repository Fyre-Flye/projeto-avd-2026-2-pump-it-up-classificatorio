# 03 — Parte Específica: Pump it Up (responsável: Gustavo)

## Dataset
- **Fonte:** [DrivenData — Pump it Up: Data Mining the Water Table](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/). Dados da Taarifa e do Ministério da Água da Tanzânia.
- **Arquivo:** `data/parte_especifica/raw/pump_it_up_train.csv`, com 59.400 linhas × 41 colunas (40 atributos + `status_group`).
- **Tarefa:** classificação multiclasse de `status_group`:
  - `functional`: funciona e não precisa de reparo (54,3%)
  - `non functional`: não funciona (38,4%)
  - `functional needs repair`: funciona, mas precisa de reparo (7,3%, classe minoritária)
- Registros de 2002 a 2013. Há 33 qualitativas e 7 quantitativas, segundo a planilha da prof.
- **Status: dataset APROVADO pela professora.**

## Comentários da professora (planilha da turma, aba Datasets). Todos precisam ser tratados na EDA.
1. **Faltantes explícitos:** `scheme_name` 48,5%, `scheme_management` 6,5%, `installer` 6,2%, `funder` 6,1%, `public_meeting` 5,6%, `permit` 5,1%, `subvillage` 0,6%.
2. **Zeros que escondem faltantes:** `population` 36,0%, `construction_year` 34,9%, `gps_height` 34,4%, `longitude = 0` 3,1% (1.812 linhas, com `latitude ≈ 0` nas mesmas). `installer`/`funder` com `'0'` ou `'-'` (~780).
3. **Mecanismo de ausência:** os zeros de `gps_height`, `construction_year` e `population` ocorrem **nas mesmas linhas** (correlação de 0,91 a 0,93 entre os indicadores) e se concentram em **algumas regiões** (Shinyanga, Mbeya, Kagera, Mwanza). A ausência depende da região, o que a prof considera ótimo para discutir o mecanismo.
4. **Descartes a avaliar:** `num_private` (98,7% zeros), `recorded_by` (valor único).
5. **Colunas redundantes:** `extraction_type`/`_group`/`_class`, `quantity`/`quantity_group`, `payment`/`payment_type` (e também `source`/`_type`/`_class`, `waterpoint_type`/`_group`, `water_quality`/`quality_group`, `management`/`management_group`).
6. **Alta cardinalidade:** `wpt_name` (~37 mil), `subvillage` (~19 mil), `installer` (~2,1 mil), `funder` (~1,9 mil).
7. **Outliers (IQR):** `amount_tsh` 18,8% (70% zeros, máximo de 350 mil), `population` 7,4% (máximo de 30.500).
8. **Correlações numéricas modestas:** após tratar os zeros, só `gps_height × longitude` (−0,63) e `amount_tsh × longitude` (−0,42) passam de 0,4 (Spearman).
9. **Incluir no repo as instruções de download** (o DrivenData exige cadastro), já feito em `data/parte_especifica/README.md`.

## Pergunta de pesquisa e público-alvo (decisão do Gustavo, em construção)
- Pergunta final (definida na seção 0.1): *"Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de reparo ou não funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas com necessidade de manutenção ou inoperantes?"*
- **Decidido: EDA + classificador simples** (Aulas 25 e 26): **`RandomForestClassifier`** (com `DecisionTreeClassifier` como baseline), usando **`Target Encoding`** para as variáveis nominais de alta cardinalidade (sempre dentro de `Pipeline`, ajustado apenas no conjunto de treino para evitar *data leakage*), divisão estratificada, matriz de confusão e métricas. Ordem: primeiro a EDA e o tratamento dos dados (decisões do Gustavo), depois o classificador em `src/parte_especifica/classificador.ipynb`, usando `data/parte_especifica/clean/`.
- **Público-alvo:** gestor público do Ministério de Águas da Tanzânia, interessado em priorizar manutenção e identificar bombas quebradas ou que precisam de reparo.

## Estado atual (atualizado em 26/11/2026)
- **Feito — EDA e Tratamento completos (`✅` em todas as 8 seções autorais do `eda.ipynb`):**
  - Notebook `src/parte_especifica/eda.ipynb` tem 101 células (45 de código), roda inteiro sem erro, com coluna `glossario` nas tabelas, hierarquia H1–H4, descrições curtas, títulos (`<caption>`) em todas as tabelas, layouts `3×2`/`3×1` legíveis, Plotly corrigido (`plotly_mimetype`), paletas semânticas (`YlOrRd`/`Blues`/`RdBu_r`), cruzamentos multivariados das top 3 qualitativas e todas as interpretações autorais (`0.1`, `1.6`, `2.6`, `3.7`, `4.9`, `5.5`, `6.1` e `7.1`) concluídas e humanizadas.
  - **Dataset tratado exportado (Etapa 1 concluída):** `data/parte_especifica/clean/pump_it_up_clean.csv` (**59.333 linhas × 31 colunas**, 13,78 MB, **0 `NaN`**, **0 idades negativas**, **0 altitudes negativas**, nomes 100% em `snake_case` sem acento).
  - **Colunas do CSV limpo (31):** `id`, `date_recorded`, `ano_registro`, `amount_tsh`, `gps_height`, `longitude`, `latitude`, `population`, `construction_year`, `idade_no_registro`, `ausente_population`, `ausente_construction_year`, `ausente_gps_height`, `ausente_coords`, 12 qualitativas baixa cardinalidade (`quantity`, `extraction_type_class`, `waterpoint_type_group`, `payment_type`, `quality_group`, `source_class`, `management_group`, `scheme_management`, `basin`, `region`, `public_meeting`, `permit`), 4 qualitativas alta cardinalidade (`lga`, `ward`, `funder`, `installer`) e alvo (`status_group`).
  - **Classificador construído, executado e interpretado (Etapa 2 100% concluída):** `src/parte_especifica/classificador.ipynb` (29 células, roda inteiro sem erro, lendo só de `data/parte_especifica/clean/pump_it_up_clean.csv`). Reverte os imputados via flags `ausente_*` antes do `train_test_split` estratificado (80/20, `random_state=42`) e aplica `ImputadorCascata` + `ColumnTransformer` (`OneHotEncoder` nas 12 baixa cardinalidade + `TargetEncoder` nas 4 alta cardinalidade) dentro do `Pipeline` (zero *data leakage*, Aula 26). Resultados objetivos no teste: `DecisionTreeClassifier` (baseline) = 75,33% acurácia / 62,82% Macro F1; `RandomForestClassifier` (200 árvores) = 80,58% acurácia / 67,64% Macro F1. Inclui a **Seção 5.5** (demonstração prática em 3 bombas reais do teste com probabilidades + **Tabela 5.5 de auditoria passo a passo `decision_path` da Árvore de Decisão**) e a **Seção 6.1 (`✅ [AUTORAL]`)** concluída. Figuras e tabelas salvas em `out/parte_especifica/06_*.png` e `06_*.csv`.
  - **Visualizações finais, Storytelling e Dashboard Streamlit construídos (Etapas 3 e 4 prontas para revisão final do Gustavo):**
    - `.streamlit/config.toml` (identidade visual limpa: fundo branco, texto escuro, `#0072B2`, sans-serif).
    - `src/parte_especifica/data_loader.py` (`@st.cache_data` para `pump_it_up_clean.csv` e CSVs do classificador; `@st.cache_resource` reproduzindo os dois pipelines sem *data leakage* + auditoria `decision_path`; utilitários pt-BR e gerador de resumo Markdown).
    - `src/parte_especifica/dashboard.py` (filtros dinâmicos interligados na sidebar + 5 KPIs dinâmicos + 4 abas: **Storytelling e Insights** com Big Idea e Explanatórias 1, 2A e 2B; **Exploração Interativa** com as 4 exploratórias + seletor de variável + mapa Carto Positron/offline + heatmap 2 variáveis livres + diagnóstico MAR; **Classificador e Auditoria** com matrizes de confusão, sorteio de 3 bombas reais com Cartões/Tabela + mapa + probabilidades + trilha `decision_path` da Árvore + simulador `st.form`; **Glossário e Exportação** pesquisável com download CSV e Markdown).
    - `src/parte_especifica/gerar_figuras_finais.py` exporta as 7 figuras limpas (fundo branco, `dpi=150`, Okabe-Ito + cinza `#C6C6C6`, rodapé com fonte/período/n) em `out/parte_especifica/`: `07_expl_01`..`04` e `08_explan_01`, `08_explan_02a`, `08_explan_02b`.
    - `docs/STORYTELLING_E_NOTAS.md` registra o storytelling compilado (Seção 3) e os moldes das 7 notas analíticas (com `[AUTORAL]` para revisão/preenchimento final pelo Gustavo).
- **Próximas etapas (roteiro):**
  - **Revisão do Gustavo (26/11):** revisar/preencher as notas analíticas autorais em `docs/STORYTELLING_E_NOTAS.md` (e decidir se mantém as 3 explanatórias E1 + E2A + E2B ou escolhe 2) e atualizar os expanders de nota em `dashboard.py`.
  - **Etapas 5 e 6:** preparo da arguição, relatório PDF (`relatorio.pdf`), `docs/DECLARACAO_IA.pdf` assinada e `docs/MATRIZ_CONTRIBUICAO.md`.
- **Arquivos adicionais:** `src/parte_especifica/classificador.ipynb`, `src/parte_especifica/data_loader.py`, `src/parte_especifica/gerar_figuras_finais.py`, `.streamlit/config.toml`, `docs/STORYTELLING_E_NOTAS.md`, `data/parte_especifica/clean/pump_it_up_clean.csv`, `out/parte_especifica/06_metricas_classificadores.csv`, `06_importancia_features.csv`, gráficos `06_*.png`, `07_expl_*.png` e `08_explan_*.png`.

### Como o notebook foi montado para ser fácil de ler
- Índice clicável no topo e legenda do notebook.
- Seção 1.4 "Esquema de relacionamento das colunas": 3 figuras (`01_esquema_*.png`) com os grupos de colunas, as famílias redundantes e a hierarquia de localização. Os números são calculados do dataset. Só descreve a estrutura, sem interpretar.
- Um `> **Como ler:**` antes de cada gráfico ou tabela. Ele só ensina a ler o resultado e **não interpreta**. Ao criar gráficos ou tabelas novos, siga o mesmo padrão e **não escreva** o que o resultado mostra.
- Figuras grandes divididas em figuras de até 6 painéis, salvas como `NN_nome_1.png`, `NN_nome_2.png` etc. Tabelas com cor e formatação (`DataFrame.style`).
- `TEMA_ESCURO` na célula de configuração (deixar `False` ao gerar as figuras do relatório). Um gráfico interativo em Plotly, com menu, na seção 4 (precisa de internet e não aparece no GitHub).
- **Google Colab:** a célula logo depois de "Configuração" clona o repositório e entra na pasta certa (só age se estiver no Colab). Link direto: https://colab.research.google.com/github/Fyre-Flye/projeto-avd-2026-2-pump-it-up-classificatorio/blob/master/src/parte_especifica/eda.ipynb. Sem isso o notebook falha na carga dos dados, porque o Colab só baixa o `.ipynb` e não a pasta `data/`. Se os dados não forem achados, o notebook mostra uma mensagem explicando.
- Página só de resultados, sem código: `jupyter nbconvert --to html --no-input src/parte_especifica/eda.ipynb --output-dir out/parte_especifica --output eda_leitura`. O HTML fica fora do Git.

### Glossário
`docs/GLOSSARIO.md` traduz e define as colunas, as categorias e os termos de estatística da EDA, sempre com a **fonte** de cada definição. A página do DrivenData não explica as categorias, então alguns itens estão marcados como "a confirmar" (unidades de `amount_tsh` e `gps_height`, `num_private`, siglas como `SWC`, entre outros). **Não invente o significado dessas pendências.**

## Arquivos
| Onde | O quê |
| --- | --- |
| `src/parte_especifica/eda.ipynb` | EDA do Pump it Up |
| `docs/GLOSSARIO.md` | glossário de colunas, categorias e termos, com fontes |
| `src/parte_especifica/dashboard.py` | app Streamlit (`streamlit run src/parte_especifica/dashboard.py`) |
| `data/parte_especifica/clean/` | CSV tratado exportado pela EDA; o dashboard lê só daqui |
| `out/parte_especifica/` | figuras e tabelas |
