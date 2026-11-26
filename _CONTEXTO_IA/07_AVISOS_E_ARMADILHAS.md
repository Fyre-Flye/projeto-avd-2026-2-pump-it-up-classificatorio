# 07 — Avisos e armadilhas (leia antes de mexer)

Coisas que não estão claras nos outros arquivos e que já causaram, ou podem causar, erro, retrabalho ou nota zero.

## 1. Prazos
- **Entrega: quinta, 26/11/2026 às 12h30**, pelo Classroom (todos os integrantes ativos postam o link do repositório). **Apresentação e defesa: quinta, 03/12/2026.**
- A semana tem outras provas dos integrantes (AA em 30/11 e 02/12, Segurança da Informação em 01/12). Deixe o trabalho em estado commitável a qualquer momento.
- **Status real em 26/11/2026 (11h50):** Parte Específica (EDA, CSV limpo, classificador sem *data leakage*, 7 figuras finais, storytelling/notas, dashboard Streamlit com Bônus UX/UI e Aba 4 K-Means animada), base do `relatorio.pdf`, apresentação 16:9 (`docs/APRESENTACAO_AVD_G6.pdf`), roteiro em 3 (`docs/ROTEIRO_APRESENTACAO.md`) e guia de arguição (`docs/GUIA_ARGUICAO_E_VARIAVEIS.md`) estão **prontos e no GitHub**. Ainda **pendentes** (com Arthur Borges e assinaturas do grupo): conclusão da Parte Comum (`notebooks/parte_comum/eda.ipynb` e `kmeans_metricas.ipynb`), inserção das Seções `6.2` a `6.5` em `docs/gerar_relatorio.py` e Slides 11 a 13 em `docs/gerar_apresentacao.py`, assinaturas de Arthur Borges e Sacramento em `docs/DECLARACAO_IA.pdf` e preenchimento de `docs/MATRIZ_CONTRIBUICAO.md` (ver `PARA_BORGES.md`).

## 2. Uso de IA: o que zera a nota
- Todo uso de IA precisa estar **declarado**, e **toda ferramenta** entra: Claude Code, Gemini/Antigravity e qualquer outra. A marcação no código é `# [IA] <ferramenta> – <finalidade>`, com o nome verdadeiro da ferramenta. Quando duas ferramentas mexem na mesma célula, as duas entram.
- `docs/DECLARACAO_IA.md` precisa citar as ferramentas usadas, na seção de cada integrante. Se você usou uma ferramenta que ainda não consta lá, **avise o Gustavo**.
- Trechos marcados `[AUTORAL]` (no `dashboard.py` e nos notebooks) e células `Interpretação autoral` são **do aluno**. Não preencha, nem "como sugestão".
- Nunca registre prompts nem trechos de conversa com o Gustavo em arquivo do repositório. A declaração descreve os usos por **tipo**, de forma geral.

## 3. Armadilhas do dado e do modelo (Pump it Up)
- **`status_group` é o alvo (rótulo real), não uma coluna de entrada.** No classificador ele só pode ser `y`. Usá-lo como entrada é vazamento de dados e infla o resultado.
- **Divisão treino/teste estratificada** (a classe `functional needs repair` é rara, cerca de 7%), com **ajuste do encoder e do scaler só no treino**, e `random_state=42`. Reporte **recall e precisão por classe**, não só a acurácia.
- **Colunas que podem "entregar" a resposta:** antes de usar uma coluna no modelo, pergunte se ela seria conhecida *antes* de saber se a bomba funciona. Essa avaliação é do Gustavo.
- **Zeros que escondem faltantes** (`population`, `construction_year`, `gps_height`, `longitude`/`latitude`) e os faltantes explícitos: o tratamento é decisão do Gustavo (seção 6 do `eda.ipynb`) e precisa de justificativa por mecanismo de ausência. **Não remova linhas nem imputar por conta própria.**
- **Colunas redundantes** (famílias `*_type`/`*_group`/`*_class`, `quantity*`, `payment*`): usar duas versões da mesma informação no modelo é redundância. Qual versão manter é decisão do Gustavo.
- **`region_code` e `district_code` não casam um a um** com `region` e `lga`; não os trate como chave.
- **Nomes de colunas tratadas sem acento e sem espaço** (exigência do Streamlit).
- O dashboard lê **só** de `data/parte_especifica/clean/` (nunca de `raw/`).

## 4. Notebooks
- Devem rodar **no Jupyter local e no Google Colab**. Mantenha a célula que clona o repositório no Colab e use `ROOT`, `DATA_DIR` e `OUT_DIR`; nunca caminhos absolutos da máquina.
- Antes de commitar um notebook: *Restart & Run All*, sem erro, execuções em ordem. Saídas e figuras novas entram **no mesmo commit** da mudança que as gerou.
- Quando uma figura é dividida ou renomeada, **remova a antiga** (`git rm`) para não ficar PNG órfão em `out/`.
- Ninguém edita o notebook de outro integrante sem alinhamento: Arthur Borges e Sacramento cuidam de `notebooks/parte_comum/` e Gustavo, de `src/parte_especifica/`.
- Uma EDA = **código + `> **Como ler:**`**. Nunca escreva no notebook o que um gráfico "mostra".

## 5. O que não vai para o Git
`.venv/`, `*_leitura.html`, planilha da turma (`Requisitos/*.xlsx`), pastas `DatasetParte*/`, chaves e tokens. O repositório é **público**.

## 6. Quando houver dúvida
Pergunte ao Gustavo antes de: apagar arquivo, reescrever histórico, mudar a estrutura de pastas exigida pelo enunciado, mudar a identidade visual definida em `06_GUIDELINES_PDF_E_APRESENTACAO.md` (seção 2.1), decidir tratamento de dado, escolher gráfico explanatório ou fechar a pergunta de pesquisa. Prefira não fazer a fazer errado, porque a avaliação é individual e o uso indevido de IA zera o projeto.
