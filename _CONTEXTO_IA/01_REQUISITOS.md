# 01 — Requisitos do enunciado (resumo fiel)

Fonte: *Projeto Final: Agrupamento, EDA e Dashboard Interativo*, AVD 2026.2 (para estudantes não matriculados em Teoria dos Grafos). Este resumo segue o PDF. Em caso de dúvida, vale o PDF: `Requisitos/Projeto_Final_AVD_2026_2_SEM_MARCADOR.pdf`. A versão `COM_MARCADOR` mostra a divisão do grupo: **azul = Parte Comum (Sacramento)**, **verde = Parte Específica (Gustavo)**.

## Grupo 6
| Integrante | Situação | Parte |
| --- | --- | --- |
| Gustavo Henrique Cruz de Oliveira | ativo | Parte Específica (Pump it Up) |
| João Vitor do Sacramento Bezerra da Cunha | ativo | Parte Comum (Wine Quality ou Obesity, a escolher) |
| Arthur Borges | sem contribuição até o momento | — |
| Luiz Felipe Cruz Braz | reprovado por falta | — |

O enunciado pede grupos de 4, mas o grupo segue com 2 integrantes ativos.

## Requisitos técnicos
- Python 3.11+; libs permitidas: pandas, numpy, matplotlib, seaborn, plotly, scikit-learn (incluindo KMeans), streamlit.
- Dashboard final em **Streamlit**.
- Parte Comum pode ser feita em **notebook Jupyter** (opção escolhida pelo grupo).

## Entrega (GitHub, só o link vai para o Classroom)
O repositório deve conter:
- Código-fonte completo (EDA, agrupamento, dashboard).
- Datasets das duas partes (ou script/instruções de download).
- README com instalação e execução.
- **Relatório em PDF** com a análise técnica completa das duas partes (`relatorio.pdf` na raiz).
- **Declaração de Uso de IA assinada por todos**: `docs/DECLARACAO_IA.pdf`, obrigatória mesmo sem uso de IA.
- **Matriz de contribuição**.
- Todos os integrantes precisam ter **commits** no repositório.

## Calendário
| Etapa | Data |
| --- | --- |
| Checkpoint do dataset específico | 27/10/2026 (aprovado) |
| Acompanhamentos em sala | 17/11, 19/11, 24/11 |
| **Entrega** (todos postam no Classroom) | **26/11/2026** |
| **Apresentação** | **03/12/2026** |

## Parte Comum: EDA e Agrupamento (Wine Quality ou Obesity)
1. **EDA, 4 pilares:** estrutural (tipos, dimensões), distribucional (cada variável), relacional (todas as variáveis, incluindo a classe), outliers (identificar, discutir, tratar ou justificar não tratar).
2. **Padronização:** padronizar/normalizar as numéricas antes do agrupamento e explicar no relatório por que isso é necessário para o K-Means.
3. **K-Means em duas passadas:**
   - Passada 1, k livre: rodar para um intervalo de k (sugestão 2 a 10), escolher k pelo **Método do Cotovelo** e visualizar os grupos.
   - Passada 2, k fixo: k = número real de classes do dataset; visualizar os grupos.
4. **Métricas e matriz de confusão (para cada passada):** mapear cada cluster para a classe real **majoritária** dentro dele; montar a matriz de confusão rótulo mapeado × rótulo real (pode ser retangular na Passada 1 e é quadrada na Passada 2); calcular **acurácia, precisão e recall por classe** a partir da matriz.
5. **Discussão crítica (no relatório):** comparar Passada 1 × Passada 2 (qual gerou grupos mais coerentes?) e discutir se a granularidade das classes faz sentido (ex.: notas 5 e 6 do vinho são distinguíveis pelos dados?).

> O K-Means não vê os rótulos. A "acurácia" mede o quanto os grupos não supervisionados coincidem com as classes conhecidas, e não o acerto de uma previsão.

## Parte Específica: Exploração, Storytelling e Dashboard (Pump it Up)
1. **Pergunta de pesquisa** (hipótese).
2. **EDA, 4 pilares.** Faltantes **não podem ser simplesmente removidos**: discutir o mecanismo de ausência e justificar o tratamento. Outliers avaliados, discutidos e tratados/excluídos com justificativa.
3. **Storytelling:** definir o público-alvo; registrar o raciocínio (o que se encontrou, que história os dados contam, por que é a mensagem mais relevante, qual atributo pré-atentivo destaca a mensagem: cor, tamanho, posição).
4. **Visualizações (mínimo 6):** 4 exploratórias + 2 explanatórias, e pelo menos 1 responde diretamente à pergunta. Todas com título, legenda e eixos; tipo coerente com o dado; pizza/radar só com justificativa forte.
5. **Dashboard Streamlit:** reúne a exploração e as explanatórias, com hierarquia, legibilidade e cores adequadas.
6. **Notas analíticas** para cada visualização: o que mostra, qual insight, por que esse gráfico. **Autorais, IA proibida.**

## Rubrica (10,0 + até 1,0 de bônus)
| Parte | Critério | Pts | O que será observado |
| --- | --- | --- | --- |
| Comum | EDA (4 pilares) | 1,5 | tipos, qualidade (faltantes, inconsistências, outliers), distribuições, relações |
| Comum | K-Means + métricas | 1,5 | padronização correta; duas passadas; mapeamento cluster→classe; matriz; acurácia/precisão/recall corretos |
| Comum | Discussão crítica | 1,0 | k do cotovelo × k fixo; granularidade das classes; raciocínio no relatório |
| Específica | Exploração | 1,5 | qualidade, mecanismo de ausência, tratamento justificado, relações multivariadas com a pergunta |
| Específica | Storytelling | 1,5 | explanatória nasce da exploratória; história coerente com o público |
| Específica | Boas práticas visuais + dashboard | 2,0 | gráfico adequado, pré-atentivos justificados, título/legenda/eixos, organização e usabilidade, sem distorções |
| Específica | Notas analíticas e relatório | 1,0 | nota autoral por visualização; resposta à pergunta |

**Bônus Visual/UX (+1,0):** filtros interligados, seleção de variáveis/eixos pelo usuário, comparação lado a lado, **animação de transição entre as passadas do K-Means da Parte Comum**, **página da Parte Comum no dashboard**, exportação de relatório pelo dashboard.

## Regras da apresentação
- Não há dataset surpresa.
- A professora pode escolher **duas variáveis do dataset do grupo** e pedir a interpretação da relação ao vivo.
- **Qualquer integrante** pode ser questionado sobre **qualquer parte** (Comum ou Específica). A avaliação é individual.

## Uso de IA generativa (texto do enunciado, resumido)
- **Permitido (com registro):** dúvidas conceituais; entender erros/depurar código do grupo; apoio com pandas, scikit-learn e Streamlit; revisão de ortografia e clareza.
- **Proibido:** gerar análises, discussões, conclusões ou notas analíticas; pedir que a IA interprete gráficos, escolha o tipo de gráfico ou monte a história; entregar trecho que ninguém do grupo saiba explicar.
- **Obrigatório:** marcar no código `# [IA] <ferramenta> – <finalidade>` e entregar a declaração assinada.
- Uso não declarado, declaração ausente ou código/análise que o grupo não sabe explicar: **nota ZERO**.

## Dicas do enunciado
- Comece pela EDA da Parte Comum: entender o dado vem primeiro.
- O k do cotovelo pode não bater com o número de classes. Isso não é erro, é um resultado a discutir.
- Documente tudo no relatório: decisões de tratamento, escolha de k, leitura da matriz de confusão, raciocínio do storytelling.
