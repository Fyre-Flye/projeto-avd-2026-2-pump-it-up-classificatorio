# Declaração de Uso de IA — Projeto Final AVD 2026.2, Grupo 6

> **Rascunho em construção.** Cada integrante atualiza a sua seção ao longo do projeto. No final, a versão completa é exportada para `docs/DECLARACAO_IA.pdf` e **assinada por todos os integrantes**, como o enunciado exige.

**Integrantes:** Gustavo Henrique Cruz de Oliveira; João Vitor do Sacramento Bezerra da Cunha
**Período do trabalho:** 22/11/2026 a 26/11/2026

## Regras seguidas (enunciado)
- **Permitido, com registro:** dúvidas conceituais; entender erros e depurar código do grupo; apoio com pandas, scikit-learn e Streamlit; revisão de ortografia e clareza.
- **Proibido:** gerar análises, discussões, conclusões ou notas analíticas; pedir que a IA interprete gráficos, escolha o tipo de gráfico ou monte a história da análise explanatória.
- Trechos de código feitos com apoio de IA estão marcados com `# [IA] <ferramenta> – <finalidade>`.

---

## Gustavo Henrique Cruz de Oliveira (Parte Específica e organização do repositório)

### Ferramenta
Claude Code (Anthropic) e Gemini via Antigravity (Google).

### Tipos de pedido feitos
- **Organização do projeto:** criação da estrutura de pastas exigida pelo enunciado, README, `requirements.txt`, `.gitignore`, esqueletos dos notebooks e do dashboard, e da pasta `_CONTEXTO_IA/` com as regras do projeto.
- **Consulta ao material de aula e dúvidas conceituais:** leitura dos slides oficiais (`AVD/Slides/`, especialmente Aulas 05, 06, 09, 10, 14, 25 e 26) e do enunciado para tirar dúvidas conceituais (alta cardinalidade, mecanismos MCAR/MAR/MNAR, One-Hot vs. Target Encoding, árvores/Random Forest, robustez a outliers, data leakage) e manter o projeto no escopo da disciplina.
- **Geração e melhoria de código para a EDA da Parte Específica** (`src/parte_especifica/eda.ipynb`): código que calcula e plota os 4 pilares, inclusão de coluna `glossario` nas tabelas, hierarquia H1–H4 e títulos (`<caption>`), ajustes de layout (`3×2`/`3×1`), correção do renderizador Plotly, paletas semânticas acessíveis (`YlOrRd`, `Blues`, `RdBu_r`), cruzamentos multivariados escolhidos pelo aluno e código da Seção 6 (implementando as decisões de tratamento do aluno e exportação para `data/parte_especifica/clean/pump_it_up_clean.csv`). Todas as células de código estão marcadas com `# [IA]`.
- **Revisão de ortografia, clareza e conferência factual de números** nos textos autorais escritos pelo aluno nas seções da EDA (sem gerar análises ou conclusões próprias da IA).
- **Geração de código para o classificador** (`src/parte_especifica/classificador.ipynb`): pipeline sem *data leakage* (reversão controlada das flags `ausente_*` antes do split estratificado, `ImputadorCascata`, `OneHotEncoder` + `TargetEncoder`, `DecisionTreeClassifier` e `RandomForestClassifier`), matrizes de confusão, métricas por classe e importância agregada das variáveis. Célula de interpretação (`6.1`) mantida em branco para preenchimento autoral.
- **Glossário** (`docs/GLOSSARIO.md`): tradução e definição dos termos técnicos do dataset e da EDA, a partir da página do DrivenData, dos slides das aulas e de pesquisa na web. Os termos sem fonte foram marcados como "a confirmar". Não há interpretação de dados nesse arquivo.
- *(a preencher ao longo do projeto: apoio com Streamlit, revisão final do relatório etc.)*

### O que foi aceito, modificado ou rejeitado e por quê
- *(a preencher)*

---

## João Vitor do Sacramento Bezerra da Cunha (Parte Comum)

### Ferramenta
*(a preencher)*

### Tipos de pedido feitos
*(a preencher)*

### O que foi aceito, modificado ou rejeitado e por quê
*(a preencher)*

---

## Assinaturas

| Integrante | Assinatura | Data |
| --- | --- | --- |
| Gustavo Henrique Cruz de Oliveira | | |
| João Vitor do Sacramento Bezerra da Cunha | | |
