# Storytelling e Notas Analíticas (Parte Específica: Pump it Up)

> **Status:** Rascunho estruturado para revisão final do Gustavo antes de gerar `relatorio.pdf`.
> Os itens 1 a 4 do Storytelling compilam exclusivamente o que o aluno já escreveu na EDA (`0.1`, `7.1`), no Classificador (`6.1`) e na Big Idea. Os campos de **Insight** e **Justificativa** das Notas Analíticas estão marcados como `[AUTORAL]` para o Gustavo revisar/escrever com suas próprias palavras (regra do enunciado: notas analíticas são 100% autorais).

---

## 1. Storytelling: da Exploratória à Explanatória (Seção 3 do enunciado)

### 1.1 Público-alvo
Gestores públicos do Ministério de Águas da Tanzânia, responsáveis por priorizar manutenção preventiva, alocar recursos em campo e identificar bombas quebradas ou em risco de falha. Por ser um público de gestão, a comunicação evita jargão estatístico pesado, adota termos consistentes em português (ponto d'água, situação operacional, região), rótulos diretos com percentuais no padrão pt-BR e gráficos de leitura imediata orientados à decisão.

### 1.2 O que foi encontrado na exploração
Na EDA da base tratada de 59.333 pontos d'água (registros de 2011 a 2013, após remover 36 duplicadas e 31 linhas residuais de 2002 e 2004), identificou-se uma variável-alvo desbalanceada: 54,3% funcionais (`functional`), 38,4% não funcionais (`non functional`) e apenas 7,3% precisando de reparo (`functional needs repair`). Os fatores mais associados ao estado operacional foram:

- **Disponibilidade de água (`quantity`):** pontos secos (`dry`) chegam a 96,9% de inoperância.
- **Tecnologia de extração (`extraction_type_class`):** mesmo quando há água suficiente (`quantity = enough`, n = 33.150), sistemas motorizados (`motorpump`, 45,9% não funcionais), eólicos (`wind-powered`, 44,1%, com amostra pequena n = 59) e categorias não especificadas (`other`, 76,7%) falham muito mais do que sistemas mecânicos simples como gravidade (`gravity`, 18,4%), bombas manuais (`handpump`, 23,5%) e bombas de corda (`rope pump`, 23,8%), ficando `submersible` em patamar intermediário (33,0%).
- **Idade do ponto d'água (`idade_no_registro`):** considerando apenas os 38.674 registros com ano de construção informado (excluindo os 34,8% ausentes sob mecanismo MAR concentrado em 6 regiões), a taxa de inoperância cresce de 23,9% na faixa de 0 a 5 anos para 60,8% acima de 30 anos. A mediana de idade das bombas quebradas é de 18 anos, o dobro das funcionais (9 anos), com 14 anos nas que precisam de reparo.
- **Contraste regional (`region`, `lga`, `ward`):** forte disparidade geográfica entre regiões com maior funcionalidade (como Iringa e Arusha) frente a regiões críticas (como Lindi, Mtwara e Tabora). Por outro lado, a população ao redor não separou bombas funcionais de quebradas (mediana de 150 em ambos os grupos).
- **Validação preditiva (classificador extra):** o `RandomForestClassifier` (200 árvores, sem data leakage) atingiu 80,58% de acurácia global e 67,64% de Macro F1 no teste (n = 11.867), superando o baseline `DecisionTreeClassifier` (75,33% de acurácia e 62,82% de Macro F1). O modelo confirmou `ward` (16,73%), `quantity` (11,75%), `funder` (10,11%), `installer` (9,64%), `lga` (8,31%), `waterpoint_type_group` (5,08%) e `extraction_type_class` (4,58%) entre os sinais mais fortes, mas revelou o gargalo operacional na classe minoritária `functional needs repair` (precisão de 65,82%, porém recall de apenas 27,00%).

### 1.3 Que história os dados contam (Big Idea)
**Formato da Aula 06 (`[Sujeito + Verbo + Ponto de Vista]`):**

> **Os pontos d'água da Tanzânia** *(sujeito)* **falham principalmente** *(verbo)* **quando há escassez de água, quando são mais antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como gravidade e bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível** *(ponto de vista)*.

### 1.4 Por que essa mensagem é a mais relevante para o público definido
Porque mostra ao gestor do Ministério de Águas que uma bomba parada não decorre apenas de fonte seca: mesmo onde há água suficiente, a escolha e a sustentação técnica de tecnologias motorizadas e o envelhecimento acima de 20 anos elevam fortemente a taxa de falha. Combinado ao contraste regional e ao classificador supervisionado (com Random Forest para triagem em escala e Árvore de Decisão para auditoria transparente das regras), o gestor passa a ter base objetiva para priorizar manutenção preventiva e planejar novos investimentos em infraestrutura hídrica.

### 1.5 Técnicas pré-atentivas usadas nas visualizações explanatórias
- **Cor por exceção (contraste):** paleta fixa acessível a daltonismo (Okabe-Ito), mantendo categorias/faixas de contexto em cinza neutro (`#C6C6C6`) e aplicando laranja de alerta (`#D55E00`) apenas nos grupos críticos da história (tecnologias motorizadas/eólicas com água suficiente na Explanatória 1; bombas com mais de 20 anos na Explanatória 2A; gargalo de recall da classe `functional needs repair` na Explanatória 2B) e azul (`#0072B2`) nos atributos-chave do classificador.
- **Posição e ordenação:** barras ordenadas por taxa de falha (Explanatória 1), por ordem cronológica de idade (Explanatória 2A) e por importância decrescente (Explanatória 2B), explorando a posição em eixo comum (maior precisão perceptiva, Aula 06).
- **Anotações diretas e linha de referência:** rótulos de percentual e `n` direto nas barras, linha tracejada de média do recorte e caixas curtas com a comparação direta (ex.: razão entre `motorpump` e `gravity`, medianas de 9 vs. 18 anos, recall de 27,0%).

---

## 2. Notas Analíticas das Visualizações (Seção 6 do enunciado)

> **Instrução para o Gustavo:** amanhã, revise as 4 exploratórias e decida se mantém **as 3 explanatórias (E1 + E2A + E2B)** ou escolhe 2 delas (o enunciado pede *mínimo* de 2 explanatórias, então manter as 3 é 100% permitido e responde tanto aos 2 eixos da Big Idea quanto à 2ª parte da pergunta de pesquisa). Preencha/valide os campos `[AUTORAL]` abaixo e copie para `relatorio.pdf` (e para os expanders de `dashboard.py`).

### Visualização Exploratória 1: Distribuição da situação operacional (`07_expl_01_distribuicao_status.png`)
- **O que está sendo mostrado:** contagem absoluta e percentual das três classes de `status_group` na base tratada (`n = 59.333`, 2011 a 2013): `functional` (32.226; 54,3%), `non functional` (22.794; 38,4%) e `functional needs repair` (4.313; 7,3%).
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

### Visualização Exploratória 2: Situação operacional por variáveis categóricas (`07_expl_02_status_por_categoria.png`)
- **O que está sendo mostrado:** proporção percentual (barras 100% empilhadas) das três classes de `status_group` por categoria em `quantity`, `extraction_type_class`, `waterpoint_type_group` e `payment_type` (`n = 59.333`). No dashboard Streamlit, o usuário pode alternar entre todas as 12 categóricas e entre proporção (%) e contagem absoluta.
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

### Visualização Exploratória 3: Contraste regional e distribuição geográfica (`07_expl_03_contraste_regional_mapa.png`)
- **O que está sendo mostrado:** à esquerda, ranking horizontal ordenado da taxa de inoperância (`% non functional`) nas 21 regiões administrativas (`n = 59.333`) com linha de média nacional (38,4%); à direita, mapa geográfico de `longitude` e `latitude` colorido por `status_group` apenas nos registros com GPS real (`ausente_coords = 0`, `n = 57.556`).
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

### Visualização Exploratória 4: Heatmap multivariado `quantity x extraction_type_class` (`07_expl_04_heatmap_quantity_extraction.png`)
- **O que está sendo mostrado:** matriz de calor cruzando disponibilidade de água (`quantity`) e tecnologia de extração (`extraction_type_class`), exibindo em cada célula o percentual de bombas `non functional` e o número de observações (`n`), excluindo `unknown` e `other` (`n = 52.305`). No dashboard, o usuário pode escolher qualquer par de variáveis categóricas.
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

---

### Visualização Explanatória 1: Tecnologia de extração com água suficiente (`08_explan_01_tecnologia_com_agua.png`)
- **O que está sendo mostrado:** ranking horizontal da taxa de inoperância (`% non functional`) por `extraction_type_class` restrito apenas aos pontos com água suficiente (`quantity = enough`, `n = 33.150`), com linha de referência da média do recorte e destaque de cor nas tecnologias mais críticas (`other`, `wind-powered`, `motorpump`) contra cinza nas mecânicas simples (`gravity`, `handpump`, `rope pump`).
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

### Visualização Explanatória 2A: Envelhecimento da rede vs. taxa de inoperância (`08_explan_02a_idade_vs_falha.png`)
- **O que está sendo mostrado:** taxa de pontos `non functional` em seis faixas de `idade_no_registro` (de 0 a 5 anos até mais de 30 anos), usando somente os 38.674 registros com `construction_year` informado (excluindo os 34,8% MAR), com destaque em laranja nas faixas acima de 20 anos e anotação das medianas (9 anos funcionais vs. 18 anos inoperantes).
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`

### Visualização Explanatória 2B: Desempenho do classificador e top atributos (`08_explan_02b_classificador_metricas.png`)
- **O que está sendo mostrado:** à esquerda, Precisão e Recall por classe do `RandomForestClassifier` no conjunto de teste (`n = 11.867`, acurácia global 80,58%), destacando em laranja o recall de 27,0% em `functional needs repair`; à direita, ranking das 10 variáveis mais importantes no modelo, destacando `ward`, `quantity` e `extraction_type_class`. Responde diretamente à segunda metade da pergunta de pesquisa.
- **Insight extraído:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
- **Por que esse tipo de visualização foi escolhido:** `> [AUTORAL - escrever/confirmar pelo Gustavo]`
