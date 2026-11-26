# PARA_BORGES — Dossiê de Continuidade Urgente (Grupo 6, prazo 26/11/2026 às 12h30)

> **ATENÇÃO (Arthur Borges e assistente de IA):**
> O prazo da atividade no Classroom foi ajustado para **hoje, 26/11/2026 às 12h30**.
> A **Parte Específica (Pump it Up — Gustavo)** está **100% executada, testada e no GitHub** (EDA completa, CSV tratado sem nulos, Classificador sem *data leakage*, 7 figuras finais limpas, Storytelling + Notas compiladas e Dashboard Streamlit rodando).
>
> **O que ficou sob responsabilidade do Arthur Borges agora:**
> 1. **Parte Comum** (que estava com o Sacramento e ficou incompleta — ver Seção 2 abaixo).
> 2. **Relatório técnico completo em PDF (`relatorio.pdf` na raiz do repo)** reunindo **Parte Comum + Parte Específica** (incluindo revisão final das **Notas Analíticas** da Parte Específica usando os dados/interpretações abaixo).
> 3. **Completar a seção do Arthur Borges (e coletar a do Sacramento) em `docs/DECLARACAO_IA.md` e gerar/assinar `docs/DECLARACAO_IA.pdf` por todos os integrantes ativos** *(obrigatório — ausência ou falta de assinatura zera a nota!)*.
> 4. **Preencher `docs/MATRIZ_CONTRIBUICAO.md`** (deixada pendente de propósito pelo Gustavo até o Arthur Borges concluir e commitar as entregas dele).
> 5. **Fazer pelo menos 1 commit com autoria do Arthur Borges** no repositório GitHub (regra obrigatória do enunciado; siga `_CONTEXTO_IA/04_CONVENCOES.md`: **sem** `Co-Authored-By`, 1 commit por etapa, sempre `git pull` antes de `git push`).
> 6. **Slides da apresentação** (para a defesa de **03/12/2026**).

---

## 1. O que JÁ ESTÁ PRONTO na Parte Específica (Gustavo — NÃO precisa refazer!)

| Artefato | Caminho no repo | Estado |
| --- | --- | --- |
| EDA completa (4 pilares + MAR + outliers + tratamento) | `src/parte_especifica/eda.ipynb` | 100% rodada (101 células, 0 erros) + todas as 8 seções autorais concluídas |
| Dataset limpo (0 nulos, `snake_case`, 59.333 × 31) | `data/parte_especifica/clean/pump_it_up_clean.csv` | Exportado e validado |
| Classificador extra (Árvore baseline + Random Forest, sem *data leakage*, auditoria `decision_path`) | `src/parte_especifica/classificador.ipynb` | 100% rodado (29 células, 0 erros) + Seção 6.1 autoral concluída |
| Métricas e importâncias em CSV | `out/parte_especifica/06_metricas_classificadores.csv`, `06_importancia_features.csv` | Exportados |
| **7 figuras finais limpas (para `relatorio.pdf` e slides)** | `out/parte_especifica/07_expl_01`..`04.png` e `08_explan_01`, `02a`, `02b.png` | Fundo branco, `dpi=150`, Okabe-Ito + cinza `#C6C6C6`, rodapé com fonte/período/n, sem sobreposição |
| Figuras de apoio da EDA e do Classificador | `out/parte_especifica/01_*.png` .. `06_*.png` | Todas geradas (ex.: `02_ausencia_por_regiao.png`, `06_matriz_confusao_modelos.png`) |
| Storytelling + Notas Analíticas compiladas | `docs/STORYTELLING_E_NOTAS.md` | Completo com base nos textos do Gustavo (revisar ao levar para `relatorio.pdf`) |
| Dashboard Streamlit completo | `.streamlit/config.toml`, `src/parte_especifica/data_loader.py`, `src/parte_especifica/dashboard.py` | Testado via `AppTest` (0 erros, 0 warnings); roda com `streamlit run src/parte_especifica/dashboard.py` |
| Glossário completo de colunas | `docs/GLOSSARIO.md` | Pronto |
| Declaração de Uso de IA (parte do Gustavo preenchida) | `docs/DECLARACAO_IA.md` e rascunho `docs/DECLARACAO_IA.pdf` | Falta preencher seções de Borges e Sacramento e coletar assinaturas |

### Lista exata das figuras da Parte Específica recomendadas para o `relatorio.pdf`
- **Qualidade / Ausência MAR (opcional para a seção de EDA):**
  - `out/parte_especifica/02_ausencia_por_coluna.png`
  - `out/parte_especifica/02_ausencia_por_regiao.png`
  - `out/parte_especifica/02_coocorrencia_ausencia.png`
- **4 Visualizações Exploratórias oficiais (Seção 4 do enunciado):**
  1. `out/parte_especifica/07_expl_01_distribuicao_status.png` — Distribuição de `status_group`
  2. `out/parte_especifica/07_expl_02_status_por_categoria.png` — Situação por 4 variáveis categóricas principais
  3. `out/parte_especifica/07_expl_03_contraste_regional_mapa.png` — Ranking regional (21 regiões) + Mapa geográfico
  4. `out/parte_especifica/07_expl_04_heatmap_quantity_extraction.png` — Heatmap `quantity × extraction_type_class`
- **3 Visualizações Explanatórias oficiais (mínimo exigido é 2; manter as 3 cobre Big Idea + Classificador):**
  1. `out/parte_especifica/08_explan_01_tecnologia_com_agua.png` — Tecnologia com água suficiente (`quantity = enough`)
  2. `out/parte_especifica/08_explan_02a_idade_vs_falha.png` — Envelhecimento da rede (`idade_no_registro` sem imputados MAR)
  3. `out/parte_especifica/08_explan_02b_classificador_metricas.png` — Desempenho do Random Forest + Top 10 atributos (responde à 2ª parte da pergunta)
- **Apoio da seção de Classificador (se quiser incluir no relatório):**
  - `out/parte_especifica/06_matriz_confusao_modelos.png` (Árvore vs. Random Forest lado a lado)
  - `out/parte_especifica/06_comparativo_metricas_modelos.png`

---

## 2. Estado REAL da Parte Comum (o que estava com o Sacramento)

Ao verificar o repositório em **26/11/2026 às 10h43**:
- `notebooks/parte_comum/eda.ipynb`: 22 células no total, **apenas 6 células de código executadas** (gerou apenas `01_histogramas_1.png`, `01_histogramas_2.png`, `02_distribuicao_classes.png`, `03_categoricas_1.png`, `03_categoricas_2.png` em `out/parte_comum/`).
- `notebooks/parte_comum/kmeans_metricas.ipynb`: 18 células no total, **0 células executadas** (esqueleto ainda vazio!).
- **Datasets disponíveis em `data/parte_comum/`:** `obesity/ObesityDataSet_raw_and_data_sinthetic.csv` e `wine_quality/` (`winequality-*.csv`). Confira qual dataset o Sacramento começou em `notebooks/parte_comum/eda.ipynb` (pelas imagens `03_categoricas`, é **Obesity**!) ou substitua/integre com o trabalho paralelo do Arthur Borges mantendo a estrutura obrigatória:
  - `notebooks/parte_comum/eda.ipynb`
  - `notebooks/parte_comum/kmeans_metricas.ipynb`
  - `out/parte_comum/`
- **Checklist obrigatório da Parte Comum (vale 4,0 pts na rubrica):**
  1. EDA nos 4 pilares (estrutural, distribucional, relacional, outliers).
  2. Padronização (`StandardScaler` ou `MinMaxScaler`) + explicar no relatório por que K-Means exige padronização.
  3. K-Means em **duas passadas**: Passada 1 (`k` livre de 2 a 10 + Método do Cotovelo) e Passada 2 (`k` fixo = nº real de classes), visualizando os grupos nas duas passadas.
  4. Mapeamento cada cluster → classe real majoritária; **Matriz de confusão** (pode ser retangular na Passada 1, quadrada na Passada 2); **acurácia, precisão e recall por classe**.
  5. **Discussão crítica no relatório:** comparar Passada 1 vs. Passada 2 (qual gerou grupos mais coerentes?) e discutir se a granularidade das classes originais faz sentido nos dados (lembrando que K-Means não vê rótulos durante o treino!).

---

## 3. TODAS as Interpretações Autorais do Gustavo (copiadas fielmente para o Relatório)

> **IMPORTANTE:** Todo o texto abaixo foi escrito/validado pelo Gustavo. Use-o como base fiel para redigir a Parte Específica do `relatorio.pdf` e revisar as notas analíticas, **sem inventar números novos** e seguindo `_CONTEXTO_IA/06_GUIDELINES_PDF_E_APRESENTACAO.md` (fundo branco, pt-BR, sem emojis, sem travessão `—` em texto novo, paleta Okabe-Ito).

### 3.1 Pergunta de pesquisa e público-alvo (`eda.ipynb`, 0.1)
- **Público-alvo:** Gestores do Ministério de Águas da Tanzânia.
- **Pergunta final:** *"Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de reparo ou não funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas com necessidade de manutenção ou inoperantes?"*

### 3.2 Análise Estrutural (`eda.ipynb`, 1.6)
- Base bruta: **59.400 linhas × 41 colunas** (variável-alvo `status_group`). Sem `id`s repetidos, mas existem **36 linhas duplicadas ignorando `id`** (removidas na Seção 6).
- Colunas irrelevantes/redundantes: `recorded_by` é constante (`GeoData Consultants Ltd`); `region_code` é inconsistente com `region` (7 regiões têm mais de um código e alguns códigos pertencem a mais de uma região → manter `region`); 7 famílias de colunas redundantes (decisão: manter apenas as versões generalizadas: `extraction_type_class`, `quantity`, `payment_type`, `quality_group`, `source_class`, `waterpoint_type_group`, `management_group` + `scheme_management`).
- Alta cardinalidade: falta de padronização de digitação (`strip().lower()` reduziu `installer` de 2.145 para 1.935 e `scheme_name` de 2.695 para 2.576). Para as 4 de alta cardinalidade mantidas (`lga`, `ward`, `funder`, `installer`), decisão: **Target Encoding** com `RandomForestClassifier` ajustado somente no treino (Aula 26). Descartadas `wpt_name` (~37 mil) e `subvillage` (~19 mil).

### 3.3 Qualidade dos Dados e Mecanismo de Ausência (`eda.ipynb`, 2.6)
- A ausência **não é aleatória** (descarta MCAR): os zeros suspeitos de `population` (36,0%), `construction_year` (34,9%) e `gps_height` (34,4%) têm coocorrência de **0,91 a 0,93** entre si e concentram-se entre **88,6% e 100%** em 6 regiões (Dodoma, Kagera, Mbeya, Tabora, Shinyanga e Mwanza), enquanto as outras 15 regiões ficam abaixo de 7,3%. Como a ausência depende da variável observável `region`, caracteriza-se **MAR (Missing At Random)** (Aula 09).
- Não apagar as linhas (perderia ~1/3 dos dados e quase 100% de 6 regiões inteiras).
- Tratamento adotado: converter zeros suspeitos (`population`, `construction_year`, `gps_height`, `longitude`/`latitude`) em `NaN`, salvar 4 flags binárias `ausente_*` (permitindo reversão anti-*data leakage* no classificador) e aplicar **imputação agrupada em cascata pela mediana (`lga -> region -> basin`)** — necessária porque 4 regiões (Dodoma, Kagera, Mbeya e Tabora) têm 0 valores válidos nessas colunas, enquanto todas as 9 bacias (`basin`) têm ao menos 988 valores válidos.
- Categóricas com `NaN`, `'0'` ou `'-'` (`scheme_management`, `installer`, `funder`, `public_meeting`, `permit`) preenchidas com `"desconhecido"`. Descartadas `num_private` (98,7% zeros, sem descrição oficial) e `scheme_name` (48,5% ausente, sobreposta a `scheme_management`). Mantida `amount_tsh` com `0` (70,0% zeros), pois separa `status_group` (`45,4%` vs. `22,2%` de `non functional` entre `== 0` e `> 0`).

### 3.4 Análise Distribucional (`eda.ipynb`, 3.7)
- Variável-alvo desbalanceada (base limpa `n = 59.333`): `functional` **54,3%** (32.226), `non functional` **38,4%** (22.794), `functional needs repair` **7,3%** (4.313, classe minoritária) → exige precisão, recall e F1 por classe além da acurácia.
- Quantitativas (Aula 10): `amount_tsh` (assimetria 57,81) e `population` (10,99) fortemente assimétricas à direita → usar mediana e escala logarítmica nas visualizações. `construction_year` (−0,73) moderada à esquerda; `gps_height` (−0,20), `longitude` (−0,13) e `latitude` (−0,25) com assimetria baixa.
- Recorte temporal (`date_recorded`): 99,95% em 2011, 2012 e 2013; os 31 registros residuais de 2002/2004 (0,05%) concentravam **todas as 9 idades negativas** (`construction_year > date_recorded`) e foram removidos.
- Qualitativas: maior instalador é `DWE` (31,2% dos válidos), maior financiador é `Government Of Tanzania`, e `never pay` soma 42,7% de `payment_type` (forte esforço público). Alta concentração em poucas categorias: `management_group` (`user-group`, 88,4%), `quality_group` (`good`, 85,6%), `source_class` (`groundwater`, 77,1%), `quantity` (`enough`, 55,9%; `insufficient`, 25,5%), `extraction_type_class` (`gravity`, 45,1%; `handpump`, 27,7%).

### 3.5 Análise Relacional (`eda.ipynb`, 4.9)
- **Disponibilidade de água (`quantity`):** `dry` (96,9% `non functional`) e `unknown` (71,2%) dominam a inoperância; `insufficient` (38,1%) fica perto da média geral (38,4%), acima de `seasonal` (32,3%) e `enough` (27,5%).
- **Tecnologia de extração (`extraction_type_class`):** mesmo com `quantity == enough` (`n = 33.150`), `motorpump` (45,9% inoperantes, `n = 1.539`), `wind-powered` (44,1%, amostra pequena `n = 59`) e `submersible` (33,0%, `n = 3.874`) falham muito mais que sistemas simples como `gravity` (18,4%, `n = 15.311`), `handpump` (23,5%, `n = 9.488`) e `rope pump` (23,8%, `n = 281`). Categoria `other` chega a 76,7% inoperantes mesmo com água suficiente.
- **Qualidade da água (`quality_group`):** associação menor no geral, mas `salty` (48,2% inoperantes) e `unknown` (84,1%) sobem bastante frente a `good` (35,7%).
- **Quantitativas:** correlações de Spearman modestas; só `gps_height × longitude` (−0,63) passa de 0,4 em módulo. `population` não separa funcionais de inoperantes (mediana 150 em ambas; 200 em `needs repair`). **`idade_no_registro`** separa bem: mediana **9 anos** (`functional`), **14 anos** (`functional needs repair`) e **18 anos** (`non functional` — o dobro das funcionais), com taxa de falha subindo de 23,9% (0 a 5 anos) para 60,8% (> 30 anos) nos 38.674 registros sem imputação.
- **Contraste regional:** Iringa (78,2% funcionais; 19,5% inoperantes) e Arusha (68,5% funcionais; 26,3% inoperantes) têm os melhores cenários; Lindi (64,2% inoperantes), Mtwara (62,4%) e Tabora (54,4%) têm os piores.

### 3.6 Outliers e Tratamento Final (`eda.ipynb`, 5.5 e 6.1)
- 9 linhas com idade negativa removidas junto aos 31 registros de 2002/2004.
- 1.496 (1.495 após deduplicação) registros com `gps_height < 0` (mediana −18 m, mín −90 m) concentram-se nas 5 regiões litorâneas (Pwani, Mtwara, Lindi, Dar es Salaam e Tanga) → erro vertical do GPS no nível do mar → corrigidos para `0` **após** imputação dos zeros originais (sem perder as linhas).
- Outliers positivos de `amount_tsh` (18,8% pelo IQR, máx 350.000) e `population` (7,4% pelo IQR, máx 30.500) **mantidos**: são plausíveis no domínio e modelos baseados em árvores (`RandomForest`/`DecisionTree`) são robustos a outliers numéricos; nas visualizações compensa-se com mediana e escala log.
- Dataset final: `data/parte_especifica/clean/pump_it_up_clean.csv` (**59.333 × 31**, **0 NaNs**, **0 idades negativas**, **0 altitudes negativas**, 100% ASCII `snake_case`).

### 3.7 Classificador (`classificador.ipynb`, 6.1)
- Split estratificado 80/20 (`random_state=42`; treino `47.466`, teste `11.867`), revertendo imputados via `ausente_*` **antes** do split e ajustando `ImputadorCascata` + `OneHotEncoder` (12 baixa card.) + `TargetEncoder` (4 alta card.) dentro do `Pipeline` apenas no treino (zero *data leakage*).
- **Árvore de Decisão (baseline, `max_depth=15, min_samples_leaf=5`):** Acurácia teste **75,33%** (treino 79,85%), Macro F1 **62,82%** (`functional` F1 80,39%; `needs repair` Prec 47,35% / Rec 26,88% / F1 34,29%; `non functional` F1 73,77%).
- **Random Forest (`n_estimators=200, min_samples_leaf=2`):** Acurácia teste **80,58%** (treino 86,93%), Macro F1 **67,64%** (`functional` Prec 79,15% / Rec 91,02% / F1 84,67%; `needs repair` Prec 65,82% / Rec 27,00% / F1 38,29%; `non functional` Prec 84,42% / Rec 75,96% / F1 79,97%).
- **Top importâncias (RF):** `ward` (16,73%), `quantity` (11,75%), `funder` (10,11%), `installer` (9,64%), `lga` (8,31%), `waterpoint_type_group` (5,08%), `longitude` (4,64%), `latitude` (4,63%), `extraction_type_class` (4,58%), `gps_height` (2,90%).
- **Conclusão operacional (2ª metade da pergunta):** o Random Forest entrega melhor desempenho em escala para priorizar manutenção (embora ainda precise de atenção ao recall baixo de 27,0% na classe minoritária `functional needs repair`), enquanto a Árvore de Decisão oferece auditabilidade passo a passo (`decision_path`) para justificar decisões em campo — trade-off explorado ao vivo na Aba 3 do dashboard Streamlit.

### 3.8 Storytelling e Notas Analíticas (`docs/STORYTELLING_E_NOTAS.md`)
- Todos os 5 itens da Seção 3 do enunciado + as 7 notas analíticas (4 exploratórias + 3 explanatórias) já estão compilados em `docs/STORYTELLING_E_NOTAS.md` e espelhados nos expanders do `dashboard.py`.

---

## 4. Checklist de Ação Imediata para Arthur Borges (até 12h30 de 26/11/2026)

- [ ] **Parte Comum:** integrar/executar `notebooks/parte_comum/eda.ipynb` e `notebooks/parte_comum/kmeans_metricas.ipynb` (4 pilares + padronização + K-Means 2 passadas + matriz de confusão + acurácia/precisão/recall) e salvar figuras em `out/parte_comum/`.
- [ ] **Relatório PDF (`relatorio.pdf` na raiz):** gerar o PDF completo cobrindo Parte Específica (usando a Seção 3 acima + `docs/STORYTELLING_E_NOTAS.md` + PNGs de `out/parte_especifica/`) e Parte Comum (incluindo justificativa da padronização e discussão crítica Passada 1 × Passada 2 + granularidade das classes). Seguir `_CONTEXTO_IA/06_GUIDELINES_PDF_E_APRESENTACAO.md`.
- [ ] **Declaração de Uso de IA (`docs/DECLARACAO_IA.pdf`):** completar a seção do **Arthur Borges** (e do **Sacramento**) em `docs/DECLARACAO_IA.md`, coletar assinaturas dos 3 integrantes ativos e salvar o PDF final assinado em `docs/DECLARACAO_IA.pdf`.
- [ ] **Matriz de Contribuição (`docs/MATRIZ_CONTRIBUICAO.md`):** atualizar marcando a participação do Gustavo, do Sacramento e do Arthur Borges (deixada pendente de propósito até aqui).
- [ ] **Commits do Arthur Borges:** commitar por etapa (sem `Co-Authored-By`), dar `git pull` e `git push` para `origin/master`.
- [ ] **Classroom (até 12h30):** todos os integrantes ativos postam o link do repositório GitHub.
- [ ] **Apresentação (03/12):** montar os slides alinhados ao `relatorio.pdf` (mesmas figuras, números e cores).
