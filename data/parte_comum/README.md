# Dados — Parte Comum (Wine Quality)

- **Fonte:** UCI Machine Learning Repository, [Wine Quality (id 186)](https://archive.ics.uci.edu/dataset/186).
- **Citação pedida pelos autores (`winequality.names`):** P. Cortez, A. Cerdeira, F. Almeida, T. Matos e J. Reis. *Modeling wine preferences by data mining from physicochemical properties*. Decision Support Systems, Elsevier, 47(4):547-553, 2009.
- **Arquivos:**
  - `winequality-red.csv`: 1.599 vinhos tintos × 12 colunas
  - `winequality-white.csv`: 4.898 vinhos brancos × 12 colunas
  - `winequality.names`: descrição original das variáveis
- **Separador:** `;` → `pd.read_csv(caminho, sep=";")`
- **Colunas:** 11 variáveis físico-químicas de entrada + `quality` (nota de 0 a 10; nos arquivos aparecem de 3 a 8 no tinto e de 3 a 9 no branco).

Download manual, se precisar: na página da UCI, clique em *Download* e extraia `winequality-red.csv` e `winequality-white.csv` nesta pasta.
