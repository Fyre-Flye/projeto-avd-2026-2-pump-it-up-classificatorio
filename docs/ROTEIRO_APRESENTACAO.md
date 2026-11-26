# Roteiro de Apresentação e Defesa (03/12/2026)

**Disciplina:** Análise e Visualização de Dados (AVD 2026.2, CESAR School)  
**Deck oficial:** `docs/APRESENTACAO_AVD_G6.pdf` (14 slides, formato 16:9)  
**Tempo-alvo total:** 11 a 12 minutos de fala (deixando margem confortável para demonstração ao vivo e arguição da professora).  
**Ordem dos apresentadores:** **1º Gustavo Henrique Cruz de Oliveira** -> **2º Arthur Borges** -> **3º João Vitor do Sacramento Bezerra da Cunha**.

---

## Visão geral da divisão de tempo

| Ordem | Integrante | Slides | Escopo na apresentação | Tempo estimado |
| --- | --- | --- | --- | --- |
| **1º** | **Gustavo Henrique Cruz de Oliveira** | Slides 1 a 9 | Abertura, Problema e Pergunta, Qualidade MAR, Exploratória, Big Idea, Explanatórias (Tecnologia, Idade, Classificador) e Demo Ao Vivo do Dashboard (Abas 1 a 3) | ~5 min 00 s |
| **2º** | **Arthur Borges** | Slides 10 a 12 | Parte Comum: Dataset Obesity, EDA e Padronização, K-Means em Duas Passadas (+ Demo da Aba 4 animada no Dashboard), Matrizes de Confusão e Métricas | ~3 min 30 s |
| **3º** | **João Vitor do Sacramento Bezerra da Cunha** | Slides 13 e 14 | Parte Comum: Discussão Crítica (Passada 1 vs. Passada 2 e granularidade das 7 classes), Conclusões Integradas, Limitações e Abertura para Arguição | ~2 min 30 s |

> **Regra de ouro da defesa:** qualquer integrante pode ser questionado sobre **qualquer parte** (Comum ou Específica) e sobre **qualquer par de variáveis** do dataset ao vivo. Todos devem treinar com `docs/GUIA_ARGUICAO_E_VARIAVEIS.md` antes do dia 03/12.

---

## Checklist pré-apresentação (5 minutos antes de começar)

1. Abrir o terminal na raiz do repositório e subir o dashboard localmente:
   ```powershell
   .venv\Scripts\streamlit.exe run src\parte_especifica\dashboard.py
   ```
2. Deixar duas janelas prontas lado a lado (ou em abas do navegador):
   - Aba 1: `docs/APRESENTACAO_AVD_G6.pdf` em tela cheia.
   - Aba 2: Dashboard Streamlit já carregado (`http://localhost:8501`) com o cache do classificador e do K-Means já aquecido (clique uma vez na Aba 3 e na Aba 4 antes de começar para o `@st.cache_resource` e `@st.cache_data` responderem instantaneamente!).
3. **Plano B sem internet:** se o Wi-Fi da sala cair, ativar o modo **"Offline (sem internet)"** no mapa da Aba 2 do dashboard e usar as figuras estáticas em `out/parte_especifica/` e `out/parte_comum/`.

---

## BLOCO 1: Gustavo Henrique Cruz de Oliveira (1º a falar | Slides 1 a 9 | ~5 min)

### Slide 1: Capa (~20 s)
- **Fala-chave:** "Bom dia/boa tarde, professora e turma. Somos o Grupo 6 (Gustavo, Arthur Borges e João Vitor do Sacramento). Vou iniciar apresentando a nossa Parte Específica, sobre os pontos d'água da Tanzânia no dataset *Pump it Up*, mostrar o dashboard ao vivo e depois passar para o Arthur e o João Vitor concluírem com a Parte Comum no dataset *Obesity*."

### Slide 2: Problema, Público-Alvo e Pergunta de Pesquisa (~35 s)
- **Fala-chave:** "Nosso público-alvo são os **gestores do Ministério de Águas da Tanzânia**, que precisam decidir onde priorizar manutenção preventiva e alocação de equipes. Nossa pergunta de pesquisa tem duas partes: quais características de um ponto d'água se associam ao seu estado operacional (`functional`, `functional needs repair` ou `non functional`) e em que medida esses atributos permitem classificar bombas que precisam de reparo ou estão inoperantes."
- **Destacar nos cartões:** `59.333` pontos após limpeza, `45,7%` fora do estado ideal (`38,4%` quebrados + `7,3%` precisando de reparo), `21` regiões e `80,6%` de acurácia no modelo final.

### Slide 3: Qualidade dos Dados, Mecanismo MAR e Tratamento (~45 s)
- **Fala-chave:** "Antes de modelar, a EDA revelou zeros disfarçados de dados ausentes em cerca de um terço da base: `population` (36,0%), `construction_year` (34,9%) e `gps_height` (34,4%). Eles ocorrem juntos nas mesmas linhas (correlação de 0,91 a 0,93) e se concentram entre **88,6% e 100% em seis regiões** (Dodoma, Kagera, Mbeya, Tabora, Shinyanga e Mwanza)."
- **Ponto teórico obrigatório:** "Como a ausência depende de uma variável observável (`region`), caracterizamos **MAR (Missing At Random)**. Apagar essas linhas eliminaria seis regiões inteiras; por isso salvamos flags `ausente_*` e imputamos pela mediana em cascata `lga -> region -> basin`. Também removemos 36 duplicadas, 31 registros antigos de 2002/2004 que concentravam todas as 9 idades negativas e corrigimos 1.496 altitudes negativas de GPS no litoral para zero. Fechamos a base limpa com **59.333 × 31 e zero nulos**."

### Slide 4: Visualizações Exploratórias 1 e 2 (~35 s)
- **Fala-chave:** "Na distribuição do alvo, chamamos atenção para o desbalanceamento: `functional needs repair` tem só **7,3%** (4.313 bombas), então olhar apenas acurácia no classificador seria enganoso. Nas categóricas, `quantity = dry` lidera a inoperância com **97%**, e `payment_type = never pay` concentra 42,7% dos pontos com **48%** de falha, muito acima de quem paga mensalmente (23%) ou anualmente (18%)."

### Slide 5: Visualizações Exploratórias 3 e 4 (~35 s)
- **Fala-chave:** "No recorte territorial, existe um abismo entre regiões: **Iringa** tem só 19,5% de falhas e **Arusha** 26,3%, enquanto **Lindi** chega a **64,2%** e **Mtwara** a **62,4%**. Cruzando `quantity` com `extraction_type_class` no heatmap à direita, nasce o insight central do nosso storytelling: mesmo olhando só a coluna `enough` (onde há água suficiente), a taxa de falha varia drasticamente conforme a tecnologia."

### Slide 6: Storytelling, Big Idea e Explanatória 1 (~45 s)
- **Fala-chave:** Ler a **Big Idea** com clareza: *"Os pontos d'água da Tanzânia falham principalmente quando há escassez de água, quando são mais antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como gravidade e bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível."*
- **Apontar no gráfico:** "Isolando os **33.150 pontos com água suficiente**, `motorpump` chega a **45,9%** de inoperância (2,5 vezes a taxa de `gravity`, que é 18,4%, uma diferença de +27,4 pontos percentuais). Sistemas simples como gravidade e bomba manual (23,5%) exigem menos manutenção especializada. Ressaltamos com transparência que `wind-powered` (44,1%) tem amostra pequena (`n = 59`)."

### Slide 7: Explanatória 2A (Envelhecimento da Rede) (~35 s)
- **Fala-chave:** "No segundo eixo da Big Idea, filtramos apenas os **38.674 pontos com ano de construção real** (sem os imputados por MAR). Enquanto a população ao redor não diferencia bombas funcionais de quebradas (mediana igual de 150 habitantes), a **idade** separa claramente: a falha sobe de **23,9%** (0 a 5 anos) para **60,8%** acima de 30 anos, com mediana de **18 anos** nas inoperantes contra **9 anos** nas funcionais."

### Slide 8: Explanatória 2B (Classificador Sem Data Leakage) (~40 s)
- **Fala-chave:** "Para responder à segunda parte da pergunta, treinamos uma Árvore de Decisão baseline e um Random Forest com 200 árvores, revertendo os valores imputados via `ausente_*` **antes** do split estratificado 80/20 para garantir zero *data leakage*, com `ImputadorCascata`, `OneHotEncoder` e `TargetEncoder` dentro do `Pipeline`."
- **Destacar o achado operacional:** "O Random Forest atingiu **80,58%** de acurácia e **67,64%** de Macro F1 no teste, acertando 91% das funcionais e 76% das inoperantes, mas expôs o principal gargalo: recall de apenas **27,0%** na classe minoritária `functional needs repair`. Nas importâncias, além de `quantity` e tecnologia, atributos de localização e gestão de alta cardinalidade (`ward`, `funder`, `installer`, `lga`) pesam fortemente. Na prática, o Random Forest serve para triagem em escala e a Árvore para auditoria passo a passo."

### Slide 9: Demonstração Ao Vivo do Dashboard Streamlit (~50 s)
- **Ações exatas na tela (alternar para o navegador em `localhost:8501`):**
  1. Mostrar o cabeçalho, a Big Idea e os **5 KPIs dinâmicos** no topo; selecionar rapidamente `Lindi` na sidebar para provar a reatividade e clicar em **"Limpar filtros"**.
  2. Abrir a **Aba 2 (Exploração Interativa)**: mostrar o **Comparador lado a lado de duas regiões** (Iringa vs. Lindi) e apontar o **Heatmap livre de 2 variáveis** (avisando à professora que ele está pronto para qualquer cruzamento na arguição).
  3. Abrir a **Aba 3 (Classificador e Auditoria)**: mostrar uma das 3 bombas sorteadas do teste com as probabilidades do Random Forest e expandir a tabela **`decision_path`** da Árvore.
- **Frase de passagem para o Arthur Borges:** "Para integrar o projeto inteiro num só lugar, colocamos também uma aba interativa do K-Means da Parte Comum. Passo agora a palavra para o Arthur apresentar o dataset *Obesity*, a padronização e o agrupamento em duas passadas."

---

## BLOCO 2: Arthur Borges (2º a falar | Slides 10 a 12 | ~3 min 30 s)

### Slide 10: Parte Comum: Dataset Obesity, EDA e Padronização (~1 min)
- **Fala-chave:** "Obrigado, Gustavo. Na Parte Comum, trabalhamos com o dataset **Obesity** (UCI 544): **2.111 registros e 17 colunas** (8 numéricas, 8 categóricas e o alvo `NObeyesdad` com **7 níveis** de peso e obesidade). Não há valores nulos, encontramos 24 linhas duplicadas e a própria documentação da UCI informa que cerca de 77% dos dados foram gerados sinteticamente via SMOTE."
- **Explicar a padronização (ponto obrigatório da rubrica):** "Antes de rodar o K-Means, aplicamos `StandardScaler` nas variáveis numéricas. Como o K-Means minimiza distância euclidiana, variáveis em escalas grandes como `Weight` (39 a 173 kg) esmagariam variáveis como `Height` (1,45 a 1,98 m) ou `TUE` (0 a 2). Padronizar para média 0 e desvio padrão 1 coloca todos os atributos em pé de igualdade, e mantemos a coluna `NObeyesdad` estritamente fora do treino."

### Slide 11: K-Means em Duas Passadas + Demo da Aba 4 (~1 min 15 s)
- **Fala-chave:** "Executamos o K-Means em **duas passadas**. Na **Passada 1**, testamos `k` de 2 a 10 e analisamos a curva de inércia pelo Método do Cotovelo para escolher o `k` livre mais coerente com a geometria dos dados. Na **Passada 2**, fixamos `k = 7`, igual ao número real de classes de `NObeyesdad`."
- **Ação rápida na tela (se estiver com o Dashboard aberto):** abrir a **Aba 4 (Parte Comum: K-Means Obesity)** e apertar **Play** no gráfico animado em PCA 2D mostrando visualmente os pontos migrando dos clusters da Passada 1 para os 7 clusters da Passada 2. *(Se o tempo estiver apertado, apresentar direto nos gráficos do Slide 11.)*

### Slide 12: Mapeamento Cluster -> Classe, Matrizes e Métricas (~1 min 15 s)
- **Fala-chave:** "Para comparar os clusters com as classes reais sem vazar rótulos no treino, mapeamos cada cluster à classe majoritária de `NObeyesdad` dentro dele. Montamos a **matriz de confusão** (retangular na Passada 1, quadrada 7×7 na Passada 2) e calculamos acurácia de coincidência, precisão e recall por classe usando `zero_division=0` para classes que não dominam nenhum cluster."
- **Destacar números reais do `kmeans_metricas.ipynb`:** citar a acurácia de coincidência de cada passada e apontar quais classes foram melhor separadas (geralmente extremos como `Obesity_Type_III` e `Insufficient_Weight`) e quais tiveram recall baixo ou zero.
- **Frase de passagem para o João Vitor do Sacramento:** "Com os números das duas passadas comparados, passo a palavra para o João Vitor trazer nossa discussão crítica sobre a granularidade das 7 classes e o fechamento integrado do projeto."

---

## BLOCO 3: João Vitor do Sacramento Bezerra da Cunha (3º a falar | Slides 13 e 14 | ~2 min 30 s)

### Slide 13: Discussão Crítica da Parte Comum (~1 min 20 s)
- **Fala-chave:** "Obrigado, Arthur. Na nossa discussão crítica, respondemos às duas perguntas centrais da Parte Comum:"
  1. **Passada 1 vs. Passada 2:** comparar diretamente se os grupos da Passada 1 (`k` livre) são mais limpos e coerentes do que forçar `k = 7`. Explicar que, embora `k = 7` aumente o número de partições e permita capturar mais classes, ele fragmenta regiões densas onde os perfis de hábitos e medidas corporais se misturam.
  2. **Granularidade das 7 classes:** destacar que `NObeyesdad` divide um espectro contínuo de IMC e hábitos em 7 faixas muito próximas (por exemplo, `Overweight_Level_I`, `Overweight_Level_II` e `Obesity_Type_I`). Como o K-Means não vê a fórmula do IMC nem os rótulos, ele distingue bem os extremos (`Insufficient_Weight` e `Obesity_Type_III`), mas confunde faixas intermediárias contíguas, mostrando que a fronteira entre essas 7 classes é mais médica/normativa do que um agrupamento geométrico isolado nos dados.

### Slide 14: Conclusões Integradas, Limitações e Encerramento (~1 min 10 s)
- **Fala-chave:** "Para fechar integrando as duas frentes: na Parte Específica (*Pump it Up*), respondemos ao gestor público mostrando que escassez hídrica, bombas com mais de 20 anos e tecnologias motorizadas concentram as falhas, e entregamos um dashboard com Random Forest (80,6%) e Árvore auditável para apoiar decisões em campo. Na Parte Comum (*Obesity*), comprovamos na prática a importância da padronização antes do K-Means e os limites do agrupamento não supervisionado diante de 7 rótulos finos."
- **Destacar transparência nas limitações:** "Registramos quatro limitações claras: a ausência MAR em 6 regiões da Tanzânia (34,8% sem ano real), o recall baixo (27,0%) em `functional needs repair`, amostras pequenas como `wind-powered` (`n = 59`) e o fato de cerca de 77% do dataset *Obesity* ser sintético via SMOTE."
- **Fechamento:** "Muito obrigado, professora! Todo o código, notebooks, relatório e dashboard estão no repositório, e estamos à disposição para responder às perguntas e testar quaisquer duas variáveis ao vivo no dashboard."

---

## Notas de ensaio rápido (antes de 03/12)
- **Cronometragem:** fazer pelo menos 1 ensaio cronometrado pelos três juntos (Gustavo 5 min, Arthur 3 min 30 s, Sacramento 2 min 30 s = 11 min).
- **Troca de microfone sem pausas:** treinar as duas frases de transição (Gustavo -> Arthur no fim do Slide 9; Arthur -> Sacramento no fim do Slide 12).
- **Consistência de números:** assim que Arthur Borges terminar `kmeans_metricas.ipynb` e atualizar `docs/gerar_relatorio.py` e `docs/gerar_apresentacao.py`, conferir se todos os números ditos nos Slides 11, 12 e 13 batem 100% com o `relatorio.pdf`.
