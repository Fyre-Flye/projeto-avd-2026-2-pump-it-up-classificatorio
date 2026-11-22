# 05 — Conteúdo dado em aula (limite de escopo)

Tudo no projeto deve caber no que foi visto na disciplina. Resumo das agendas dos slides (pasta `AVD/Slides` do Gustavo):

| Aula | Tema | Pontos usados no projeto |
| --- | --- | --- |
| 01–03 | Introdução, Data-Driven, Infra de BI | contexto |
| 05 | Pipeline de dados; percepção humana | **atributos pré-atentivos**, **Gestalt**, mapeamento de cores e **acessibilidade** |
| 06 | Organização visual, princípios de design, tipos de gráfico | **hierarquia visual**, padrões de leitura, **princípios de Tufte**, taxonomia/escolha de gráficos, **storytelling com dados** |
| 09 | EDA parte 1 | princípios da EDA; **dados ausentes (MCAR, MAR, MNAR)**, imputação por média/mediana/moda ou considerando outras variáveis, "remover como última opção"; **outliers** (IQR/boxplot) |
| 10 | EDA parte 2 | estatística descritiva; qualitativas; **bivariada** (boxplot, violinplot, tabelas de contingência em heatmap); **multivariada** (matriz de correlação Pearson × Spearman, heatmap com dendrograma); histograma/KDE |
| 14 | Agrupamento e normalização | **discretização** (amplitude fixa/Sturges, quantis, semântica); **K-Means**; **MinMaxScaler × StandardScaler**, `inverse_transform` para visualizar na escala original; cuidado com data leakage; **método do cotovelo** e silhueta como apoio visual |
| 15 | Revisão AV1 | — |
| 21–23 | Streamlit 1, 2 e 3 | anatomia do app, widgets, containers, layout; gráficos interativos e **cache**; métricas/KPIs; identidade visual; deploy no Community Cloud |
| 25 | Introdução a Ciência de Dados e ML | tipos de aprendizagem; tarefas (classificação, regressão, clustering); algoritmos (regressão logística, árvore, **Random Forest**, MLP básico, **K-Means**, DBSCAN, **PCA**, t-SNE) |
| 26 | Feature engineering e métricas | criação/transformação de features; **encoding** (label, one-hot, dummy, target, frequency, hash; tabela "qual encoding usar"); divisão hold-out/K-Fold/estratificação; **data leakage**; **matriz de confusão, acurácia, precisão, recall, F1**, ROC/AUC |

## Observações de escopo
- O Qui-Quadrado aparece nos slides, mas `scipy` **não** está na lista de libs permitidas. Se usar, calcule com pandas/numpy.
- O repositório-modelo da prof para Streamlit (Aulas 21 a 23) usa `data/raw` × `data/clean`, `src/data_loader.py` com `@st.cache_data` e `.streamlit/config.toml` para o tema. Siga esse padrão no dashboard.
