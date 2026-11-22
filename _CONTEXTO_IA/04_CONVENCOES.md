# 04 — Convenções do repositório

## Estrutura (obrigatória pelo enunciado, não renomeie)
```
README.md, requirements.txt, relatorio.pdf
docs/DECLARACAO_IA.pdf            # assinada por todos (rascunho em docs/DECLARACAO_IA.md)
data/parte_comum/                 # Wine Quality
data/parte_especifica/raw|clean/  # Pump it Up
out/parte_comum/  out/parte_especifica/
notebooks/parte_comum/eda.ipynb, kmeans_metricas.ipynb
src/parte_comum/                  # vazio de propósito (o grupo usa notebooks)
src/parte_especifica/eda.ipynb, dashboard.py
```
Pastas locais **fora do Git** (estão no `.gitignore`): `Requisitos/`, `DatasetParteComum/`, `DatasetParteEspecifica/`. Não as adicione.

## Caminhos
- Notebooks e scripts rodam **a partir da raiz do repo**. Os esqueletos têm uma célula que sobe até a raiz e define `ROOT`, `DATA_DIR` e `OUT_DIR`.
- Figuras: `out/<parte>/NN_nome_curto.png` (ex.: `out/parte_comum/03_cotovelo.png`), com `dpi=150` e `bbox_inches="tight"`.

## Código
- Nomes de variáveis e colunas tratadas **sem acento e sem espaço** (exigência do Streamlit), em `snake_case`.
- Gráficos sempre com título, rótulos de eixo e legenda quando houver mais de uma série.
- `random_state=42` em tudo que for aleatório (KMeans, train_test_split), para reprodutibilidade.
- Marcar trechos feitos com IA: `# [IA] <ferramenta> – <finalidade>`.
- Células de interpretação ficam com `> **[Interpretação autoral — preencher]**` até o aluno escrever.

## Git
- Branch principal: `master`. Antes de começar: `git pull`. Cada um mexe nos arquivos da sua parte, para evitar conflito em notebook.
- Mensagens no padrão `PREFIXO: descrição curta em português`, com prefixos `ADD:` (novo), `UPD:` (atualização), `FIX:` (correção). Ex.: `ADD: EDA estrutural Wine Quality`.
- **Sem trailers de co-autoria de IA** nos commits.
- Antes de commitar notebook, rode tudo de cima a baixo (Kernel → Restart & Run All) para as saídas ficarem consistentes.
- Todos os integrantes precisam ter commits (exigência do enunciado).
