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
| **2º** | **Arthur Borges** | Slides 10 a 12 | Parte Comum: Dataset Wine Quality (UCI 186), EDA e Padronização, K-Means em Duas Passadas (`k = 3` vs. `k = 7` + Demo da Aba 4 animada), Matrizes de Confusão e Métricas | ~3 min 30 s |
| **3º** | **João Vitor do Sacramento Bezerra da Cunha** | Slides 13 e 14 | Parte Comum: Discussão Crítica (`k = 3` vs. `k = 7` e granularidade das 7 notas sensoriais), Conclusões Integradas, Limitações e Abertura para Arguição | ~2 min 30 s |

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
3. **Plano B sem internet:** se o Wi-Fi da sala cair, desligar a chave **"Usar mapa base cartográfico (Carto Positron)"** na Exploratória 3 (Aba 2) do dashboard e usar as figuras estáticas em `out/parte_especifica/` e `out/parte_comum/`.

---

## BLOCO 1: Gustavo Henrique Cruz de Oliveira (1º a falar | Slides 1 a 9 | ~5 min)

### Slide 1: Capa (~20 s)
- **Fala-chave:** "Bom dia/boa tarde, professora e turma. Somos o Grupo 6 (Gustavo, Arthur Borges e João Vitor do Sacramento). Vou iniciar apresentando a nossa Parte Específica, sobre os pontos d'água da Tanzânia no dataset *Pump it Up*, mostrar o dashboard ao vivo e depois passar para o Arthur e o João Vitor concluírem com a Parte Comum no dataset *Wine Quality*."

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
- **Frase de passagem para o Arthur Borges:** "Para integrar o projeto inteiro num só lugar, colocamos também uma aba interativa do K-Means da Parte Comum. Passo agora a palavra para o Arthur apresentar o dataset *Wine Quality*, a padronização e o agrupamento em duas passadas."

---

## BLOCO 2: Arthur Borges (2º a falar | Slides 10 a 12 | ~3 min 30 s)

### Slide 10: Parte Comum: Dataset Wine Quality, EDA e Padronização (~1 min)
- **Fala-chave:** "Obrigado, Gustavo. Na Parte Comum, trabalhamos com a base combinada **Wine Quality** (UCI 186, Cortez et al., 2009): **6.497 amostras e 13 colunas** (11 atributos físico-químicos, `wine_type` com 4.898 brancos e 1.599 tintos, e a nota `quality` em **7 classes de 3 a 9**). Não há nulos e mantivemos as 1.177 duplicatas (18,12%) por ausência de identificador único. As notas **5 (32,9%) e 6 (43,7%)** somam **76,6%** da base, enquanto a nota 9 tem apenas 5 vinhos; o teor alcoólico (`+0,44`) é a variável mais associada à nota."
- **Explicar a padronização (ponto obrigatório da rubrica):** "Antes de rodar o K-Means, aplicamos `StandardScaler` nas 11 numéricas e no indicador binário `wine_type_red`. Como o K-Means usa distância euclidiana, variáveis em centenas como `total sulfur dioxide` dominariam variáveis em milésimos como `chlorides` ou `density` (0,99 a 1,00). A coluna `quality` fica estritamente fora do treino."

### Slide 11: K-Means em Duas Passadas + Demo da Aba 4 (~1 min 15 s)
- **Fala-chave:** "Executamos o K-Means em **duas passadas**. Na **Passada 1**, o Método do Cotovelo mostra a maior queda de inércia de `k = 2` (56.403) para **`k = 3` (45.876, -18,7%)**, suavizando depois; por isso escolhemos **`k = 3`** (Silhouette 0,252; Davies-Bouldin 1,420). Na **Passada 2**, fixamos **`k = 7`**, igual às 7 notas reais (inércia cai para 34.418, mas Silhouette cai para 0,182 e Davies-Bouldin piora para 1,598)."
- **Ação rápida na tela (se estiver com o Dashboard aberto):** abrir a **Aba 4 (Parte Comum: K-Means)** e apertar **Play** no gráfico animado em PCA 2D (52,8% da variância) mostrando a transição dos 3 clusters para os 7 clusters.

### Slide 12: Mapeamento Cluster -> Nota, Matrizes e Métricas (~1 min 15 s)
- **Fala-chave:** "Mapeando cada cluster à nota majoritária de `quality`, vemos um resultado muito revelador: tanto em **`k = 3` (44,47% de coincidência, Macro F1 13,37%)** quanto em **`k = 7` (45,67%, ganho de só +1,20 pp, Macro F1 14,69%)**, **apenas as notas 5 e 6** dominam clusters; as notas 3, 4, 7, 8 e 9 ficam com precisão e recall de 0,0% (`zero_division=0`)."
- **Frase de passagem para o João Vitor do Sacramento:** "Com essas métricas comparadas, passo a palavra para o João Vitor trazer nossa discussão crítica sobre a coerência das duas passadas, a granularidade das 7 notas e o fechamento do projeto."

---

## BLOCO 3: João Vitor do Sacramento Bezerra da Cunha (3º a falar | Slides 13 e 14 | ~2 min 30 s)

### Slide 13: Discussão Crítica da Parte Comum (~1 min 20 s)
- **Fala-chave:** "Obrigado, Arthur. Na nossa discussão crítica, respondemos às duas perguntas centrais da Parte Comum:"
  1. **Passada 1 (`k = 3`) vs. Passada 2 (`k = 7`):** o agrupamento com `k = 3` tem melhor coesão interna (Silhouette 0,252 contra 0,182), enquanto forçar `k = 7` traz ganho marginal de apenas +1,20 ponto percentual (45,67%), muito perto dos 43,65% que a nota 6 sozinha já representa na base.
  2. **Granularidade das 7 notas:** a nota sensorial é ordinal e fortemente desbalanceada; vinhos de notas vizinhas (5, 6 e 7) têm perfis químicos muito parecidos. Além disso, incluir `wine_type_red` tende a separar tintos de brancos mais do que notas de qualidade. Logo, o K-Means revela perfis físico-químicos, mas não substitui um classificador supervisionado para prever notas finas.

### Slide 14: Conclusões Integradas, Limitações e Encerramento (~1 min 10 s)
- **Fala-chave:** "Para fechar integrando as duas frentes: na Parte Específica (*Pump it Up*), respondemos ao gestor público mostrando que escassez hídrica, bombas com mais de 20 anos e tecnologias motorizadas concentram as falhas, e entregamos um dashboard com Random Forest (80,6%) e Árvore auditável para apoiar decisões em campo. Na Parte Comum (*Wine Quality*), comprovamos na prática a importância do `StandardScaler` e os limites do K-Means diante de 7 notas sensoriais desbalanceadas."
- **Destacar transparência nas limitações:** "Registramos quatro limitações claras: a ausência MAR em 6 regiões da Tanzânia (34,8% sem ano real), o recall baixo (27,0%) em `functional needs repair`, amostras pequenas como `wind-powered` (`n = 59`) e, no *Wine Quality*, a manutenção de 18,1% de duplicatas e a influência de `wine_type_red` nos centroides."
- **Fechamento:** "Muito obrigado, professora! Todo o código, notebooks, relatório e dashboard estão no repositório, e estamos à disposição para responder às perguntas e testar quaisquer duas variáveis ao vivo no dashboard."

---

## Notas de ensaio rápido (antes de 03/12)
- **Cronometragem:** fazer pelo menos 1 ensaio cronometrado pelos três juntos (Gustavo 5 min, Arthur 3 min 30 s, Sacramento 2 min 30 s = 11 min).
- **Troca de microfone sem pausas:** treinar as duas frases de transição (Gustavo -> Arthur no fim do Slide 9; Arthur -> Sacramento no fim do Slide 12).
- **Consistência verificada:** todos os números acima já estão 100% alinhados entre `notebooks/parte_comum/kmeans_metricas.ipynb`, `relatorio.pdf`, `docs/APRESENTACAO_AVD_G6.pdf` e a Aba 4 do Dashboard Streamlit.
