# 02 — Parte Comum: Wine Quality (responsável: Sacramento)

## Arquivos
| Onde | O quê |
| --- | --- |
| `data/parte_comum/winequality-red.csv` | 1.599 vinhos tintos × 12 colunas, separador **`;`** |
| `data/parte_comum/winequality-white.csv` | 4.898 vinhos brancos × 12 colunas, separador **`;`** |
| `data/parte_comum/winequality.names` | descrição oficial do dataset (UCI 186) |
| `notebooks/parte_comum/eda.ipynb` | EDA (4 pilares), com esqueleto pronto |
| `notebooks/parte_comum/kmeans_metricas.ipynb` | padronização, K-Means (2 passadas), matriz e métricas, com esqueleto pronto |
| `out/parte_comum/` | onde salvar figuras (`.png`) e tabelas (`.csv`) |

Leitura: `pd.read_csv("data/parte_comum/winequality-red.csv", sep=";")`. Rode o notebook com o diretório de trabalho na **raiz do repo** (o esqueleto já trata isso).

Variáveis: 11 físico-químicas contínuas (`fixed acidity`, `volatile acidity`, `citric acid`, `residual sugar`, `chlorides`, `free sulfur dioxide`, `total sulfur dioxide`, `density`, `pH`, `sulphates`, `alcohol`) e a classe `quality` (nota inteira). Fatos verificados nos arquivos: tinto tem notas de 3 a 8 (6 classes); branco tem notas de 3 a 9 (7 classes).

## Decisão que o Sacramento precisa tomar (e justificar no relatório)
Usar **só tinto**, **só branco** ou **os dois juntos**? Isso muda o número real de classes, que é o **k da Passada 2**. A IA não deve decidir isso pelo aluno. Ela pode explicar as consequências de cada opção.

## Passo a passo (o que a rubrica cobra)
### 1. EDA (1,5 pt)
- **Estrutural:** `shape`, `dtypes`, `info()`, nulos, duplicados, tipo de cada variável (quantitativa contínua/discreta, qualitativa ordinal).
- **Distribucional:** histograma/KDE/boxplot de cada variável; distribuição da classe (`countplot`).
- **Relacional:** matriz de correlação (Pearson e/ou Spearman) com heatmap; relação de cada variável com `quality` (boxplot por classe, por exemplo).
- **Outliers:** identificar (IQR/boxplot ou z-score), discutir, tratar **ou** justificar não tratar. Lembrete: outliers afetam a padronização e o K-Means.

### 2. Padronização
- `StandardScaler` (ou `MinMaxScaler`) **só nas variáveis numéricas de entrada**. A coluna `quality` não entra no K-Means.
- Explicar no relatório por que o K-Means precisa disso (ele usa distância euclidiana, então variáveis em escala maior dominam).

### 3. K-Means, duas passadas (1,5 pt junto com as métricas)
- **Passada 1 (k livre):** `KMeans(n_clusters=k, random_state=42, n_init=10)` para k = 2..10, guardar a `inertia_`, plotar o **cotovelo** e escolher k.
- **Passada 2 (k fixo):** k = número real de classes da escolha feita acima.
- **Visualizar os grupos** de cada passada (ex.: dispersão de 2 variáveis coloridas pelo cluster, ou PCA em 2D, que foi visto na Aula 25).

### 4. Mapeamento, matriz e métricas
- Para cada cluster, achar a classe real **mais frequente** dentro dele (`pd.crosstab(cluster, quality)` → `idxmax`).
- Matriz de confusão **rótulo mapeado × rótulo real**. Na Passada 1 pode ficar retangular; na Passada 2, quadrada.
- **Acurácia, precisão e recall por classe** calculados **a partir da matriz** (pode conferir com `sklearn.metrics`). Atenção: se nenhum cluster for mapeado para uma classe, a precisão dela fica 0/0. Trate com `zero_division=0` e comente no relatório.

### 5. Discussão crítica (1,0 pt, autoral)
- Passada 1 × Passada 2: qual gerou grupos mais coerentes?
- Granularidade: as notas vizinhas (ex.: 5 e 6) são distinguíveis pelos dados?
- **A IA não escreve isso.** Ela pode revisar o texto do aluno.

## Bônus que conecta com o dashboard (opcional, combinar com o Gustavo)
O enunciado dá bônus por uma **página da Parte Comum no dashboard** e por **animação entre as passadas do K-Means**. Se o Sacramento salvar os resultados (labels de cada passada, inércias, matrizes) em `out/parte_comum/*.csv`, o dashboard consegue ler esses arquivos.
