# 04 — Convenções do repositório

## Estrutura (obrigatória pelo enunciado, não renomeie)
```
README.md, requirements.txt, relatorio.pdf
docs/DECLARACAO_IA.pdf            # assinada por todos (rascunho em docs/DECLARACAO_IA.md)
docs/GLOSSARIO.md, MATRIZ_CONTRIBUICAO.md
data/parte_comum/wine_quality|obesity/  # os dois datasets da Parte Comum (o grupo usa um)
data/parte_especifica/raw|clean/  # Pump it Up
out/parte_comum/  out/parte_especifica/
notebooks/parte_comum/eda.ipynb, kmeans_metricas.ipynb
src/parte_comum/                  # vazio de propósito (o grupo usa notebooks)
src/parte_especifica/eda.ipynb, dashboard.py
```
`Requisitos/` tem o enunciado (PDFs com e sem marcação) e o print do checkpoint. O resto dessa pasta (ex.: a planilha da turma, com dados pessoais de outros alunos) fica **fora do Git**.

Pastas locais **fora do Git** (estão no `.gitignore`): `DatasetParteComum/`, `DatasetParteEspecifica/`. Não as adicione.

## Caminhos
- Notebooks e scripts rodam **a partir da raiz do repo**. Os esqueletos têm uma célula que sobe até a raiz e define `ROOT`, `DATA_DIR` e `OUT_DIR`.
- Figuras: `out/<parte>/NN_nome_curto.png` (ex.: `out/parte_comum/03_cotovelo.png`), com `dpi=150` e `bbox_inches="tight"`.

## Código
- Nomes de variáveis e colunas tratadas **sem acento e sem espaço** (exigência do Streamlit), em `snake_case`.
- Gráficos sempre com título, rótulos de eixo e legenda quando houver mais de uma série.
- `random_state=42` em tudo que for aleatório (KMeans, train_test_split), para reprodutibilidade.
- Marcar trechos feitos com IA: `# [IA] <ferramenta> – <finalidade>`.
- Células de interpretação ficam com `> **[Interpretação autoral — preencher]**` até o aluno escrever.
- Antes de cada gráfico ou tabela vai um `> **Como ler:**` curto, que explica só como se lê o resultado, **sem interpretá-lo**.
- Figuras com muitos painéis são divididas em figuras de até 6 painéis (`NN_nome_1.png`, `NN_nome_2.png`).
- Notebooks devem rodar também no Google Colab: tenha uma célula inicial que clone o repositório (só no Colab) e não dependa de caminhos da sua máquina.
- Arquivos gerados que não vão para o Git: `*_leitura.html` (página de leitura do notebook).
- **Remoção de arquivos (regra do Gustavo):** nunca usar deleção permanente nem recursiva (`rm -rf`, `Remove-Item -Recurse` etc.). Sempre mover arquivos obsoletos/temporários para a **Lixeira do Windows** (`SendToRecycleBin`) e incluir um **audit rápido de deleção** no final da resposta listando o que foi enviado para a lixeira.
- **Estilo ao revisar textos autorais do Gustavo:** preservar o tom natural e direto do aluno (parágrafos corridos e simples). Evitar vícios de escrita de IA: nada de travessões (`—`) em excesso, nada de negritar todo número/termo técnico, nada de listas `- **Tópico:** ...` nem conectores artificiais (*"Em primeiro lugar"*, *"Em contrapartida"*, *"De forma semelhante"*, *"Por fim"*).

## Git
- Branch principal: `master`. Antes de começar: `git pull`. Cada um mexe nos arquivos da sua parte, para evitar conflito em notebook.
- **Um commit por feature/etapa, nunca tudo de uma vez.** A professora não gosta de commits que juntam tudo. Ex.: um commit para a EDA estrutural, outro para a distribucional, outro para a padronização, e assim por diante.
- Mensagens no padrão `PREFIXO: descrição curta em português`, com prefixos `ADD:` (novo), `UPD:` (atualização), `FIX:` (correção). Ex.: `ADD: EDA estrutural Wine Quality`.
- **Sem trailers de co-autoria de IA** nos commits.
- **Autoria:** os commits são só do Gustavo (nome e e-mail já configurados no git desta máquina). Não use `--author`, não altere o `git config`, não escreva `Co-Authored-By` nem cite a ferramenta de IA na mensagem. Se o git não tiver identidade configurada, avise em vez de configurar uma.
- **Um commit por vez:** agrupe por feature e faça `git add` só dos arquivos daquela feature (nunca `git add .` no fim do dia), com mensagem própria. Nunca junte etapas diferentes num commit só.
- **Push:** só com a autorização do Gustavo, sempre depois de `git pull`, e sem acumular: envie logo depois de commitar cada etapa aprovada, em vez de subir tudo de uma vez. Nunca use `push --force` sem ele pedir.
- **Divisão de ferramentas (desde 25/11/2026):** o Antigravity (Gemini) e o Claude Code apoiam apenas código (notebooks, dashboard e figuras) e scripts de diagramação de PDFs, sempre compilando decisões e textos autorais escritos pelos alunos (nunca gerando análises ou interpretações). Não edite um arquivo que a outra ferramenta pode estar editando (principalmente notebooks): rode `git status` antes de começar e avise o Gustavo se houver alteração que não é sua.
- O repositório é **público**: nada de dado pessoal de colegas, e-mail de terceiros, token, chave ou conversa privada, nem em código, nem em documento, nem em mensagem de commit.
- Antes de commitar notebook, rode tudo de cima a baixo (Kernel → Restart & Run All) para as saídas ficarem consistentes.
- Todos os integrantes precisam ter commits (exigência do enunciado).
- **Atualize `_CONTEXTO_IA/` a cada commit que muda algo relevante** (estado do trabalho, novos arquivos, novas convenções), para a IA do outro integrante sempre encontrar a situação real do projeto.
