# SKILL_DESIGN: skills de design para o dashboard (Bônus Visual e UX, até +1,0)

Pasta versionada no repositório. Reúne duas skills públicas, baixadas em 26/11/2026, para a IA consultar ao mexer na aparência do dashboard. As skills não foram alteradas e vêm com as licenças originais (Apache-2.0 exige manter a licença junto).

| Pasta | Origem | Licença | Para que serve |
| --- | --- | --- | --- |
| `streamlit_oficial/` | https://github.com/streamlit/agent-skills (`developing-with-streamlit`) | Apache-2.0 | Skill oficial do Streamlit. O `SKILL.md` manda rodar `scripts/discover.py`, que acha a documentação de referência (temas, layout, session_state, cache, fragments, componentes) que vem dentro do Streamlit instalado. Exige Streamlit 1.57 ou mais novo: o `.venv` do projeto tem 1.67. |
| `frontend_design_anthropic/` | https://github.com/anthropics/skills (`skills/frontend-design`) | ver `LICENSE.txt` | Princípios gerais de design de interface (tipografia, estrutura visual, movimento). Foi pensada para páginas web em HTML/CSS: no Streamlit, aproveite só os princípios. |

## Como usar
- Para Streamlit, comece pela `streamlit_oficial/SKILL.md`. O comando é `python SKILL_DESIGN/streamlit_oficial/scripts/discover.py --project-dir <raiz do projeto>` (use o Python do `.venv`). O script só localiza a documentação do Streamlit instalado.
- A `frontend_design_anthropic` é opcional e **perde para o projeto** quando houver conflito: ela pede "ponto de vista distinto" e risco estético, e o projeto já tem identidade definida em `_CONTEXTO_IA/06_GUIDELINES_PDF_E_APRESENTACAO.md` (seção 2.1).

## Limites que valem mesmo com a skill
- Só bibliotecas permitidas (pandas, numpy, matplotlib, seaborn, plotly, scikit-learn, streamlit). Nada de CSS/JS de terceiros ou componentes externos sem o Gustavo aprovar.
- A skill ajuda no **como** (tema, layout, interação, desempenho). **Não** escolhe o tipo de gráfico explanatório, não monta a história e não escreve nota analítica: isso é autoral.
- O que conta no bônus, segundo o enunciado (conferir em `_CONTEXTO_IA/01_REQUISITOS.md`): filtros dinâmicos interligados, seleção de variáveis/eixos, página da Parte Comum e animação do K-Means.
- Todo código feito com ajuda da skill continua marcado com `# [IA] <ferramenta> – <finalidade>` e a ferramenta entra em `docs/DECLARACAO_IA.md`.
