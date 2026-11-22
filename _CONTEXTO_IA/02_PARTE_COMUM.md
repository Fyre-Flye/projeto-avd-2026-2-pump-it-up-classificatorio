# 02 — Parte Comum: Wine Quality **ou** Obesity (responsável: Sacramento)

## Primeira decisão: qual dataset (é do Sacramento)
O enunciado deixa o grupo escolher **um** dos dois datasets. Os dois estão no repositório. A IA não deve escolher pelo aluno, mas pode explicar as consequências de cada opção.

| | Wine Quality (UCI 186) | Obesity (UCI 544) |
| --- | --- | --- |
| Pasta | `data/parte_comum/wine_quality/` | `data/parte_comum/obesity/` |
| Arquivo(s) | `winequality-red.csv` (1.599 × 12), `winequality-white.csv` (4.898 × 12) e `winequality-combined.csv` (os dois juntos, 6.497 × 13, com a coluna `wine_type`), separador **`;`** | `ObesityDataSet_raw_and_data_sinthetic.csv` (2.111 × 17), separador `,` |
| Classe | `quality` (nota inteira) | `NObeyesdad` (7 níveis de peso/obesidade) |
| Nº de classes (= k da Passada 2) | tinto 6 (notas 3–8); branco 7 (notas 3–9); juntos 7 | 7 |
| Variáveis de entrada | 11 físico-químicas, todas numéricas | 8 numéricas (`Age`, `Height`, `Weight`, `FCVC`, `NCP`, `CH2O`, `FAF`, `TUE`) e 8 qualitativas (`Gender`, `family_history_with_overweight`, `FAVC`, `CAEC`, `SMOKE`, `SCC`, `CALC`, `MTRANS`) |
| Fatos verificados no arquivo | sem nulos | sem nulos; 24 linhas duplicadas; 77% dos dados são sintéticos (SMOTE), segundo a UCI; `FCVC`, `NCP`, `CH2O`, `FAF` e `TUE` têm valores fracionários |
| Decisões extras | tinto, só branco ou os dois juntos (`winequality-combined.csv`)? No combinado, `wine_type` é qualitativa: decidir se entra no K-Means | o que fazer com as 8 qualitativas no K-Means (o enunciado fala em padronizar as **numéricas**; encoding foi visto na Aula 26) |

Detalhes de cada dataset estão nos READMEs das pastas em `data/parte_comum/`.

## Arquivos de trabalho
| Onde | O quê |
| --- | --- |
| `notebooks/parte_comum/eda.ipynb` | EDA (4 pilares). O esqueleto já carrega os dois datasets |
| `notebooks/parte_comum/kmeans_metricas.ipynb` | padronização, K-Means (2 passadas), matriz e métricas |
| `out/parte_comum/` | onde salvar figuras (`.png`) e tabelas (`.csv`) |

Rode os notebooks com o diretório de trabalho na **raiz do repo** (o esqueleto já trata isso).

## Passo a passo (o que a rubrica cobra)
### 1. EDA (1,5 pt)
- **Estrutural:** `shape`, `dtypes`, `info()`, nulos, duplicados, tipo de cada variável (quantitativa contínua/discreta, qualitativa nominal/ordinal).
- **Distribucional:** histograma/KDE/boxplot de cada variável; distribuição da classe (`countplot`).
- **Relacional:** matriz de correlação (Pearson e/ou Spearman) com heatmap; relação de cada variável com a classe (boxplot por classe, tabela de contingência para as qualitativas).
- **Outliers:** identificar (IQR/boxplot ou z-score), discutir, tratar **ou** justificar não tratar. Lembrete: outliers afetam a padronização e o K-Means.

### 2. Padronização
- `StandardScaler` (ou `MinMaxScaler`) nas variáveis numéricas de entrada. A coluna de classe **não** entra no K-Means.
- Explicar no relatório por que o K-Means precisa disso (ele usa distância euclidiana, então variáveis em escala maior dominam).

### 3. K-Means, duas passadas (1,5 pt junto com as métricas)
- **Passada 1 (k livre):** `KMeans(n_clusters=k, random_state=42, n_init=10)` para k = 2..10, guardar a `inertia_`, plotar o **cotovelo** e escolher k.
- **Passada 2 (k fixo):** k = número real de classes do dataset escolhido.
- **Visualizar os grupos** de cada passada (ex.: dispersão de 2 variáveis coloridas pelo cluster, ou PCA em 2D, que foi visto na Aula 25).

### 4. Mapeamento, matriz e métricas
- Para cada cluster, achar a classe real **mais frequente** dentro dele (`pd.crosstab(cluster, classe)` → `idxmax`).
- Matriz de confusão **rótulo mapeado × rótulo real**. Na Passada 1 pode ficar retangular; na Passada 2, quadrada.
- **Acurácia, precisão e recall por classe** calculados **a partir da matriz** (pode conferir com `sklearn.metrics`). Atenção: se nenhum cluster for mapeado para uma classe, a precisão dela fica 0/0. Trate com `zero_division=0` e comente no relatório.

### 5. Discussão crítica (1,0 pt, autoral)
- Passada 1 × Passada 2: qual gerou grupos mais coerentes?
- Granularidade das classes: o enunciado dá como exemplo "Obesidade Grau I" × "Sobrepeso" e as notas 5 e 6 do vinho. As classes vizinhas são distinguíveis pelos dados?
- **A IA não escreve isso.** Ela pode revisar o texto do aluno.

## Bônus que conecta com o dashboard (opcional, combinar com o Gustavo)
O enunciado dá bônus por uma **página da Parte Comum no dashboard** e por **animação entre as passadas do K-Means**. Se o Sacramento salvar os resultados (labels de cada passada, inércias, matrizes) em `out/parte_comum/*.csv`, o dashboard consegue ler esses arquivos.
