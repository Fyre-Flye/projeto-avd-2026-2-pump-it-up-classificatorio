# Guia de Treino para Arguição, Variáveis e Pares Ao Vivo (Defesa 03/12/2026)

> **Regras oficiais da apresentação (enunciado AV2):**
> 1. Não haverá dataset surpresa.
> 2. Durante a defesa, a professora pode escolher **duas variáveis quaisquer do dataset do grupo** (mesmo que não destacadas nos slides) e pedir a **interpretação ao vivo da relação entre elas**.
> 3. **Qualquer integrante** pode ser questionado sobre **qualquer parte do projeto** (Comum ou Específica), e a resposta é **avaliada individualmente**.

Este guia foi montado para que **Gustavo, Arthur Borges e João Vitor do Sacramento** dominem 100% das variáveis, saibam interpretar qualquer par ao vivo usando o Dashboard Streamlit e tenham na ponta da língua as respostas técnicas sobre metodologia, código e limitações.

---

## PARTE 1: Protocolo de 15 Segundos ("A Professora Escolheu 2 Variáveis Ao Vivo")

Se a professora disser: *"Me mostre e interprete a relação entre a variável X e a variável Y"*, siga exatamente estes 4 passos sem travar:

1. **Classifique o par em voz alta (2 s):**
   - **Categórica × Categórica (ex.: `payment_type × quality_group`, `source_class × extraction_type_class`):** vá direto à **Aba 2 (Exploração Interativa)** do dashboard Streamlit -> seção **"Cruzamento livre de duas variáveis categóricas (Heatmap)"**, selecione Variável nas linhas = X e Variável nas colunas = Y!
   - **Categórica × `status_group` (ex.: `management_group × status_group`, `permit × status_group`):** na **Aba 2**, use o seletor **"Explorar qualquer variável categórica"** (já traz todas as 12 categóricas!).
   - **Numérica × `status_group` ou Numérica × Numérica:** relembre os achados da EDA abaixo (`idade_no_registro`, `population`, `amount_tsh`, `gps_height`, `longitude`, `latitude`) e, se precisar filtrar uma região ou tecnologia, use a sidebar do dashboard para conferir os KPIs na hora.
2. **Leia o padrão dominante, sem inventar causalidade (5 s):**
   - Sempre comece pelo que está visível no gráfico: *"No cruzamento de X com Y, observamos que a categoria A concentra..."*.
   - **NUNCA diga "X causa Y"**: use *"associa-se a"*, *"concentra maior taxa de inoperância"*, *"coocorre com"*.
3. **Verifique o tamanho da amostra (`n`) e o mecanismo MAR (4 s):**
   - Olhe o `n` dentro da célula do heatmap! Se `n < 100` (como `wind-powered` com `n = 59` ou `dam` em `waterpoint_type_group`), diga imediatamente: *"Vale a ressalva de que essa célula tem amostra pequena (`n = ...`), então não devemos generalizar sem cautela."*
   - Se envolver `population`, `construction_year`, `idade_no_registro` ou `gps_height`, lembre: *"~35% desses valores eram zeros MAR em 6 regiões e foram imputados em cascata; na análise de idade real usamos apenas `ausente_construction_year == 0` (`n = 38.674`)."*
4. **Conecte ao gestor público / pergunta de pesquisa (4 s):**
   - Feche com implicação prática: *"Para o gestor do Ministério de Águas, isso ajuda a priorizar inspeções em..."*

---

## PARTE 2: Colinha Completa das 31 Colunas da Base Limpa (Pump it Up)

> **Resumo da base:** `59.333 linhas × 31 colunas` (2011 a 2013, 0 `NaN`, 0 idades negativas, 0 altitudes negativas).  
> **Colunas descartadas da base bruta (41 -> 31):** `recorded_by` (constante), `num_private` (98,7% zeros, sem descrição oficial), `region_code` (inconsistente com `region`), `district_code` (coberto por `lga`/`region`), `wpt_name` (~37 mil categorias), `subvillage` (~19 mil), `scheme_name` (48,5% ausente, redundante com `scheme_management`), e as 9 irmãs redundantes (`extraction_type`, `extraction_type_group`, `quantity_group`, `payment`, `water_quality`, `source`, `source_type`, `waterpoint_type`, `management`).

### 2.1 Variável-Alvo e Identificação / Tempo

| Coluna | Tipo | O que significa | Fatos-chave e números exatos |
| --- | --- | --- | --- |
| `status_group` | Alvo (3 classes) | Estado operacional do ponto d'água | `functional` 54,3% (32.226); `non functional` 38,4% (22.794); `functional needs repair` 7,3% (4.313). Forte desbalanceamento. |
| `id` | Identificador | Código único da bomba | 100% único; não entra no modelo preditivo. |
| `date_recorded` | Data | Data da vistoria/registro | 99,95% em 2011, 2012 e 2013 (31 linhas de 2002/2004 foram removidas). |
| `ano_registro` | Numérica derivada | Ano extraído de `date_recorded` | Apenas 2011, 2012 e 2013 na base limpa. |

### 2.2 Variáveis Quantitativas e Derivadas (7 colunas)

| Coluna | O que significa | Distribuição / Tratamento | Relação com `status_group` e outras variáveis |
| --- | --- | --- | --- |
| `amount_tsh` | *Total static head* (água disponível no ponto; unidade não informada no DD) | 70,0% zeros; assimetria altíssima (57,81); máx 350.000; 18,8% outliers IQR (mantidos). Zeros mantidos! | Forte separação: `amount_tsh == 0` tem **45,4%** de inoperantes contra **22,2%** quando `> 0`. Spearman com `longitude` = `-0,42`. |
| `gps_height` | Altitude do poço (unidade não informada no DD) | 34,4% zeros MAR imputados em cascata; 1.496 negativos no litoral ajustados para 0; assimetria baixa (-0,20). | Spearman forte com `longitude` (**`-0,63`**): o litoral leste da Tanzânia (maior longitude) tem altitude baixa e o interior oeste/norte tem planaltos mais altos. Importância RF: 2,90% (10º lugar). |
| `longitude` | Coordenada GPS leste-oeste | 3,1% zeros (1.812 linhas) imputados em cascata; assimetria -0,13. | Captura variação geográfica fina (4,64% importância no RF, 7º lugar). Leste/sul costeiro (Lindi, Mtwara) tem falhas muito maiores. |
| `latitude` | Coordenada GPS norte-sul | Pares com `longitude = 0` (~0) imputados em cascata; assimetria -0,25. | Complementa `longitude` (4,63% importância no RF, 8º lugar). |
| `population` | População ao redor do poço | 36,0% zeros MAR imputados em cascata; assimetria alta (10,99); máx 30.500; 7,4% outliers IQR (mantidos). | **Não separa funcionais de inoperantes:** mediana idêntica (**150 hab.**) em `functional` e `non functional` (200 em `needs repair`). |
| `construction_year` | Ano de construção do ponto | 34,9% zeros MAR imputados em cascata; assimetria moderada à esquerda (-0,73). | Base para `idade_no_registro`; bombas mais antigas falham muito mais. |
| `idade_no_registro` | Derivada: `ano_registro - construction_year` | 0 idades negativas na base limpa (as 9 originais caíram com o recorte 2011 a 2013). | **Forte separação (n = 38.674 reais):** mediana **9 anos** (`functional`), **14 anos** (`needs repair`), **18 anos** (`non functional`). Taxa NF vai de 23,9% (0 a 5 anos) a 60,8% (> 30 anos). |

### 2.3 Flags Binárias de Ausência MAR (4 colunas)

| Coluna | O que registra | Para que serve |
| --- | --- | --- |
| `ausente_population` | 1 se `population` era 0 na bruta (36,0%) | Preserva o sinal de ausência MAR e permite reverter para `NaN` antes do split do classificador (zero *data leakage*). |
| `ausente_construction_year` | 1 se `construction_year` era 0 (34,9%) | Usada para filtrar **apenas dados reais** (`== 0`, `n = 38.674`) na Explanatória 2A e reverter antes do split. |
| `ausente_gps_height` | 1 se `gps_height` era 0 (34,4%) | Coocorre 0,91 a 0,93 com as duas acima em 6 regiões (Dodoma, Kagera, Mbeya, Tabora, Shinyanga, Mwanza). |
| `ausente_coords` | 1 se `longitude == 0` (3,1%, 1.812 linhas) | Usada para omitir pontos imputados nos mapas geográficos (`n = 57.556` com GPS real). |

### 2.4 Variáveis Qualitativas de Baixa Cardinalidade (12 colunas -> One-Hot Encoding)

| Coluna | Principais categorias e volume | Relação com `status_group` (e destaques) |
| --- | --- | --- |
| `quantity` | `enough` (55,9%), `insufficient` (25,5%), `dry` (10,5%), `seasonal` (6,8%), `unknown` (1,3%) | **Maior separador operacional** (11,75% de importância no RF, 2º lugar): `dry` 96,9% NF, `unknown` 71,2% NF, `insufficient` 38,1% NF, `seasonal` 32,3% NF, `enough` 27,5% NF. |
| `extraction_type_class` | `gravity` (45,1%), `handpump` (27,7%), `other` (10,8%), `submersible` (10,4%), `motorpump` (5,0%), `rope pump` (0,8%), `wind-powered` (0,2%) | **Coração da Big Idea** (4,58% no RF, 9º lugar): em `enough`, `other` (76,7%), `motorpump` (45,9%) e `wind-powered` (44,1%, n=59) falham muito mais que `gravity` (18,4%) e `handpump` (23,5%). |
| `waterpoint_type_group` | `communal standpipe` (~58%), `hand pump` (~29%), `other` (~11%), `improved spring`, `cattle trough`, `dam` | 6º lugar em importância no RF (5,08%). `other` tem altíssima inoperância (~77%+); `improved spring` e `hand pump` têm altas taxas de funcionamento. |
| `payment_type` | `never pay` (42,7%), `per bucket` (~15%), `monthly` (~14%), `unknown` (~14%), `on failure` (~7%), `annually` (~6%), `other` (~2%) | `never pay` tem ~48% NF e `unknown` ~49% NF; já pagamento regular (`annually` ~18% NF, `monthly` ~23% NF, `per bucket` ~29% NF) associa-se a muito menos falhas (sugere fundo para manutenção). |
| `quality_group` | `good` (85,6%), `salty` (~8,7%), `unknown` (~3,2%), `milky`, `colored`, `fluoride` | Associação moderada no geral, mas `salty` sobe para **48,2% NF** e `unknown` para **84,1% NF** (contra 35,7% em `good`). |
| `source_class` | `groundwater` (77,1%), `surface` (22,4%), `unknown` (0,5%) | Água subterrânea (poços e nascentes) domina a rede; `unknown` tem taxa de falha elevada; `surface` associa-se bastante a `gravity`. |
| `management_group` | `user-group` (88,4%), `commercial` (~6,1%), `parastatal` (~3,0%), `other`, `unknown` | Forte concentração em gestão comunitária (`user-group`: VWC, WUG, WUA, Water Board); `unknown` tende a maior falha. |
| `scheme_management` | `VWC` (~62%), `WUG`, `Water authority`, `WUA`, `Water Board`, `Parastatal`, `Private operator`, `Company`, `desconhecido` (6,5% tratados) | Detalha quem opera; `VWC` (Village Water Committee) domina em volume; operadores dedicados como `Water Board` e `Private operator` costumam ter taxas funcionais acima da média. |
| `basin` | 9 bacias hidrográficas (`Lake Victoria`, `Pangani`, `Rufiji`, `Internal`, `Lake Tanganyika`, `Wami / Ruvu`, `Lake Nyasa`, `Ruvuma / Southern Coast`, `Lake Rukwa`) | Todas têm pelo menos 988 valores válidos nas numéricas MAR (por isso fechou a cascata `lga -> region -> basin`). Bacia `Ruvuma / Southern Coast` (sul litorâneo, onde ficam Lindi e Mtwara) tem as piores taxas. |
| `region` | 21 regiões administrativas da Tanzânia | Contraste extremo: **Iringa** (19,5% NF) e **Arusha** (26,3% NF) nos extremos positivos vs. **Lindi** (64,2% NF), **Mtwara** (62,4% NF) e **Tabora** (54,4% NF) nos piores. Também explica o mecanismo **MAR** (6 regiões com 88,6% a 100% de zeros). |
| `public_meeting` | `True`, `False`, `desconhecido` (5,6% tratados; significado exato não documentado no DD) | `True` é majoritário e apresenta menor taxa de inoperância do que `False` ou `desconhecido` (transparência: avisar que o DD não define o campo). |
| `permit` | `True`, `False`, `desconhecido` (5,1% tratados; se o ponto tem licença) | Pontos com `permit = True` tendem a apresentar taxa de funcionamento ligeiramente superior aos sem licença. |

### 2.5 Variáveis Qualitativas de Alta Cardinalidade (4 colunas -> Target Encoding)

| Coluna | Cardinalidade aproximada | Papel no modelo (Random Forest) | O que saber explicar |
| --- | --- | --- | --- |
| `ward` | ~2.092 divisões locais (abaixo de `lga`) | **1º lugar em importância (16,73%)** | Captura o microcontexto local (qualidade da gestão e manutenção na comunidade). Alta cardinalidade exige **Target Encoding dentro do Pipeline** só no treino! |
| `funder` | ~1.897 financiadores (padronizados `strip().lower()`) | **3º lugar em importância (10,11%)** | Maior financiador é `government of tanzania`. Diferentes ONGs/órgãos financiam tecnologias e padrões construtivos muito distintos. |
| `installer` | ~1.935 instaladores (após limpeza de 2.145) | **4º lugar em importância (9,64%)** | Maior instalador é `dwe` (31,2% dos válidos). Indica qualidade da execução técnica e padronização de peças. |
| `lga` | ~125 autoridades locais (distritos, abaixo de `region`) | **5º lugar em importância (8,31%)** | Primeiro nível da imputação em cascata (`lga -> region -> basin`) e forte preditor geográfico-administrativo. |

---

## PARTE 3: Colinha das 13 Variáveis da Parte Comum (Wine Quality Combinado, UCI 186)

> **Resumo da base:** `6.497 linhas × 13 colunas` (4.898 brancos, 75,39%; 1.599 tintos, 24,61%), 0 nulos, 1.177 duplicatas completas (18,12%, mantidas por falta de identificador individual).  
> **Escalas muito diferentes -> obrigatório `StandardScaler` nas 11 numéricas + `wine_type_red` antes do K-Means!**

| Coluna | Tipo | Significado (Cortez et al., 2009 / UCI 186) | Papel no K-Means e na EDA |
| --- | --- | --- | --- |
| `quality` | Alvo ordinal (7 classes: 3 a 9) | Nota sensorial atribuída por especialistas | **NUNCA entra no treino do K-Means.** Notas 5 (32,91%) e 6 (43,65%) somam 76,56%; nota 9 tem só 5 vinhos. |
| `wine_type` | Categórica (`white`, `red`) | Tipo de vinho | Convertida em `wine_type_red` (0/1) padronizada no K-Means; nos tintos a moda é nota 5 (42,59%) e nos brancos é nota 6 (44,88%). |
| `alcohol` | Numérica (% vol.) | Teor alcoólico | **Maior correlação positiva com `quality`** (+0,44 Pearson / +0,45 Spearman); mediana sobe de 9,60 (nota 5) -> 10,50 (nota 6) -> 11,40 (nota 7). |
| `density` | Numérica (g/cm³) | Densidade do vinho (~0,99 a 1,00) | Forte correlação negativa com `alcohol` (-0,69) e com `quality` (-0,31); positiva com `residual sugar` (+0,55). |
| `volatile acidity` | Numérica (g/dm³) | Acidez volátil (ácido acético; excesso dá gosto de vinagre) | Correlação negativa com `quality` (-0,27); média cai de ~0,517 (nota 3) para ~0,289 (nota 7). 5,80% outliers IQR. |
| `chlorides` | Numérica (g/dm³) | Cloretos (teor de sal) | Escala pequena (milésimos); associação negativa com `quality` (-0,20 Pearson / -0,30 Spearman). |
| `fixed acidity` | Numérica (g/dm³) | Acidez fixa (ácido tartárico) | 5,49% outliers IQR; associação moderada com `density` (+0,46). |
| `citric acid` | Numérica (g/dm³) | Ácido cítrico (frescor) | 151 valores iguais a 0 (medições reais, não nulos); maior taxa de outliers IQR global (7,83%). |
| `residual sugar` | Numérica (g/dm³) | Açúcar residual pós-fermentação | Forte diferença entre tipos (9,69% outliers IQR nos tintos vs. 0,14% nos brancos); correlaciona +0,55 com `density`. |
| `free sulfur dioxide` | Numérica (mg/dm³) | Dióxido de enxofre livre (antioxidante) | Forte correlação com `total sulfur dioxide` (+0,72 Pearson / +0,74 Spearman). |
| `total sulfur dioxide` | Numérica (mg/dm³) | Dióxido de enxofre total (centenas de mg/dm³) | **Maior amplitude numérica**; dominaria o K-Means sem `StandardScaler`. Bem mais alto em vinhos brancos. |
| `pH` | Numérica | Escala de acidez (~2,7 a 4,0) | Correlação muito baixa com `quality` (+0,02); negativa com `citric acid` (-0,33) e `fixed acidity` (-0,25). |
| `sulphates` | Numérica (g/dm³) | Sulfatos (aditivo que contribui para SO₂) | Correlação positiva com `chlorides` (+0,40); associação linear muito fraca com `quality` (+0,04). |

---

## PARTE 4: Matriz de 14 Pares de Variáveis Mais Prováveis na Arguição Ao Vivo

Treine explicar cada par abaixo em 20 segundos (e lembre que os pares categóricos podem ser abertos em 3 segundos na **Aba 2 -> Heatmap livre de 2 variáveis**!):

1. **`quantity × extraction_type_class` (Pump it Up):** Em `dry`, todas as tecnologias falham (90% a 100%). Em `enough`, `motorpump` (45,9%) e `other` (76,7%) falham muito mais que `gravity` (18,4%) e `handpump` (23,5%). É a ponte direta da Exploratória para a Explanatória.
2. **`idade_no_registro × status_group` (Pump it Up):** Nos 38.674 pontos sem imputação MAR, a falha sobe continuamente de 23,9% (0 a 5 anos) para 60,8% (> 30 anos); mediana 9 anos (`functional`), 14 (`needs repair`), 18 (`non functional`).
3. **`population × status_group` (Pump it Up):** Contraste importante: **não separa bem** funcionais de inoperantes (mediana 150 hab. nas duas; 200 em `needs repair`), provando que maior demanda populacional ao redor não é, sozinha, o fator principal de quebra.
4. **`amount_tsh × status_group` (Pump it Up):** 70% dos valores são zero, e mantivemos o zero justamente porque `amount_tsh == 0` tem **45,4%** de inoperância contra **22,2%** quando `> 0`.
5. **`gps_height × longitude` (Pump it Up):** Única correlação numérica de Spearman forte na base (**`-0,63`**). Reflete a geografia física da Tanzânia: altitudes mais baixas (inclusive os 1.496 registros negativos corrigidos para 0) ficam no litoral leste (maiores longitudes), enquanto o interior oeste/norte tem planaltos mais elevados.
6. **`region × ausente_construction_year` (ou `ausente_population`, `ausente_gps_height`):** Prova do mecanismo **MAR**: 6 regiões (Dodoma, Kagera, Mbeya, Tabora, Shinyanga, Mwanza) concentram 88,6% a 100% dos zeros suspeitos, contra < 7,3% nas outras 15 regiões.
7. **`payment_type × status_group` (Pump it Up):** `never pay` (42,7% da rede) tem ~48% de inoperância, enquanto pontos com cobrança regular (`annually` ~18%, `monthly` ~23%, `per bucket` ~29%) falham bem menos, indício de que arrecadação recorrente financia reparos.
8. **`quality_group × status_group` (Pump it Up):** Água `good` (85,6% da base) tem 35,7% de falha; água `salty` sobe para **48,2%** (corrosão/abandono) e `unknown` dispara para **84,1%**.
9. **`source_class × extraction_type_class` (Pump it Up):** Abrir no Heatmap da Aba 2! `surface` (rios, lagos, nascentes superficiais) associa-se muito a `gravity`, enquanto `groundwater` (poços rasos e tubulares) concentra `handpump`, `submersible` e `motorpump`.
10. **`waterpoint_type_group × extraction_type_class` (Pump it Up):** Forte alinhamento físico: `hand pump` coincide com `handpump`; `communal standpipe` (chafarizes comunitários) é alimentado sobretudo por `gravity`, `submersible` e `motorpump`; a categoria `other` acumula alta inoperância nos dois lados.
11. **`region × quantity` (Pump it Up):** Abrir no Heatmap da Aba 2! Mostra se a alta inoperância de regiões críticas como **Lindi (64,2%)** e **Mtwara (62,4%)** vem apenas de fontes secas (`dry`) ou também de falhas onde há água (`enough`/`insufficient`).
12. **`ward × region` (ou `funder × installer`) (Pump it Up):** Relação hierárquica/organizacional. `ward` fica dentro de `lga` que fica dentro de `region`; `ward`, `funder`, `installer` e `lga` lideram as importâncias do Random Forest (Top 5 junto com `quantity`), mostrando que contexto local e quem financiou/construiu pesam muito no funcionamento.
13. **`alcohol × density` e `alcohol × quality` (Wine Quality):** O teor alcoólico tem forte correlação negativa com a densidade (`-0,69` Pearson / `-0,70` Spearman, pois o etanol é menos denso que água e açúcar) e é o principal associado positivo com a nota `quality` (`+0,44`; mediana sobe de 9,60 na nota 5 para 10,50 na 6 e 11,40 na 7).
14. **`free sulfur dioxide × total sulfur dioxide` e `wine_type × quality` (Wine Quality):** Os dois dióxidos de enxofre têm a maior correlação da base (`+0,72` Pearson / `+0,74` Spearman) e são muito mais altos nos vinhos brancos; nos tintos a nota mais frequente é 5 (42,59%), enquanto nos brancos é 6 (44,88%).

---

## PARTE 5: Banco de 20 Perguntas Difíceis da Professora (Conceitos, Decisões e Código)

### A. Qualidade dos Dados e EDA (Pump it Up)

**1. Por que vocês classificaram a ausência como MAR e não MCAR nem MNAR?**  
- **MCAR** exige que a chance de faltar seja igual em toda a base. Aqui não é: a ausência concentra-se entre 88,6% e 100% em 6 regiões e fica abaixo de 7,3% nas outras 15. Como conseguimos explicar a ausência por uma variável **observada** no dataset (`region`), trata-se de **MAR (Missing At Random)** (Aula 09). Seria MNAR apenas se a falta dependesse do próprio valor faltante (ex.: omitir o ano só porque a bomba é velha).

**2. Por que não imputaram simplesmente pela mediana da `region`? Por que cascata `lga -> region -> basin`?**  
- Porque **4 regiões inteiras** (Dodoma, Kagera, Mbeya e Tabora) têm **ZERO valores válidos** (100% zeros suspeitos) em `population`, `construction_year` e `gps_height`! Imputar só por `region` deixaria essas 4 regiões com `NaN`. Como todas as 9 bacias hidrográficas (`basin`) têm pelo menos 988 valores válidos, a cascata `lga -> region -> basin` preserva granularidade local onde existe dado e cai para `basin` apenas onde a região inteira está vazia.

**3. Por que mantiveram os zeros de `amount_tsh` se ele tem 70% de zeros?**  
- Primeiro, imputar 70% de uma coluna deformaria completamente a distribuição. Segundo, testamos na EDA: `amount_tsh == 0` tem **45,4%** de `non functional`, contra **22,2%** quando `amount_tsh > 0`. O zero carrega forte sinal informativo sobre o estado do ponto.

**4. Por que não removeram os outliers de `amount_tsh` (18,8%) e `population` (7,4%)?**  
- Porque não são erros impossíveis de domínio (uma cidade/vila densa pode atender 10 mil pessoas num ponto comunitário), e tanto a Árvore de Decisão quanto o Random Forest fazem cortes por limiar e são **robustos a outliers numéricos**. Nas visualizações compensamos usando mediana e escala logarítmica. Já as 9 idades negativas e as 1.496 altitudes negativas no litoral eram **erros de dado/domínio**, por isso foram tratados.

**5. Por que a Explanatória 2A (Idade vs. Falha) tem `n = 38.674` e não `59.333`?**  
- Por rigor metodológico: 34,8% dos registros tiveram `construction_year` imputado por causa do MAR nas 6 regiões. Se incluíssemos os imputados no gráfico de idade, criaríamos picos artificiais nas medianas das bacias. Usando a flag `ausente_construction_year == 0`, mostramos apenas bombas com idade real informada.

### B. Classificador e Código Crítico (Pump it Up)

**6. Como vocês garantiram que não houve *data leakage* se o classificador lê o CSV limpo que já estava imputado?**  
- **Pergunta clássica de código!** Em `src/parte_especifica/classificador.ipynb` (e `data_loader.py`), usamos as 4 flags `ausente_*` salvas na EDA para **reverter para `NaN`** todos os valores previamente imputados **ANTES** do `train_test_split(stratify=y, random_state=42)`. Depois, o `ImputadorCascata` (transformador customizado herdando `BaseEstimator, TransformerMixin`) aprende as medianas de `lga`/`region`/`basin` **apenas no `fit(X_train)`** e aplica no `transform(X_test)` dentro do `Pipeline`. O mesmo vale para o `TargetEncoder`.

**7. Por que usaram `OneHotEncoder` em 12 colunas e `TargetEncoder` nas 4 de alta cardinalidade?**  
- Aplicar `OneHotEncoder` em `ward` (~2.092), `installer` (~1.935), `funder` (~1.897) e `lga` (~125) criaria mais de 6.000 colunas binárias esparsas (maldição da dimensionalidade e árvores lentas/fragmentadas). O `TargetEncoder` (Aula 26) resume cada categoria na taxa suavizada da classe no **treino** (evitando leakage com validação cruzada interna + smoothing), mantendo alta performance com baixa dimensionalidade.

**8. Por que o `RandomForest` venceu a Árvore de Decisão, e por que manter a Árvore no projeto?**  
- Uma única Árvore tem alta variância e depende de divisões gananciosas locais (75,33% de acurácia, Macro F1 62,82%). O Random Forest combina **200 árvores** treinadas em amostras bootstrap com subconjuntos aleatórios de atributos, reduzindo variância e elevando a acurácia para **80,58%** (Macro F1 67,64%). Mantivemos a Árvore como **baseline** e pela **auditabilidade**: no dashboard, o gestor vê exatamente o caminho de regras (`decision_path`) de cada bomba.

**9. Como funciona a tabela `decision_path` na Aba 3 do dashboard?**  
- A função `auditar_arvore_instancia()` em `data_loader.py` passa uma única linha pelo pré-processador do Pipeline, chama `arvore.decision_path(X_proc)` para obter os índices dos nós percorridos da raiz até a folha e traduz cada condição (`feature <= limiar` ou `> limiar`), mostrando a distribuição de classes em cada nó até a decisão final.

**10. Por que o recall de `functional needs repair` ficou em apenas 27,00% mesmo com 80,58% de acurácia global?**  
- Porque `functional needs repair` é fortemente minoritária (**7,3%** da base) e fica semanticamente no meio-termo entre `functional` e `non functional` (uma bomba que ainda fornece água, mas tem desgaste mecânico difícil de capturar apenas em metadados cadastrais). Como a maioria dos falsos negativos cai em `functional`, o modelo tem boa precisão (65,82% quando alerta reparo), mas baixo recall (deixa passar 73% das que precisam de reparo). Isso prova por que olhar só acurácia global engana!

**11. Qual a diferença entre `@st.cache_data` e `@st.cache_resource` no seu `data_loader.py`?**  
- `@st.cache_data` faz cache de **dados serializáveis** (DataFrames como `pump_it_up_clean.csv`, CSVs de métricas e o resultado do K-Means), retornando cópias seguras a cada chamada. `@st.cache_resource` faz cache de **objetos compartilhados/não serializáveis pesados** em memória, como os Pipelines treinados do `DecisionTreeClassifier` e `RandomForestClassifier`, evitando retreinar 200 árvores a cada clique de filtro!

**12. Para que serve `@st.fragment` no `dashboard.py`?**  
- O decorator `@st.fragment` isola seções interativas (como o seletor de categórica, o heatmap livre, o comparador de 2 regiões, o sorteio de 3 bombas e o slider de `k` do K-Means) para que alterar um controle dentro daquela aba **reexecute apenas aquele fragmento**, deixando o dashboard muito mais rápido e sem recarregar a página inteira.

### C. Storytelling e Visualização

**13. Qual a diferença entre visualização exploratória e explanatória no projeto de vocês?**  
- As **4 exploratórias** mostram o panorama dos dados para investigação aberta (distribuição do alvo, 4 categóricas, ranking/mapa das 21 regiões, heatmap completo `quantity × extraction`). As **3 explanatórias** têm uma **tese específica** (ligada à Big Idea e à pergunta de pesquisa), usam **cor por exceção** (cinza `#C6C6C6` para contexto, laranja `#D55E00` para o foco crítico), ordenação intencional e anotações diretas para guiar o olhar do gestor.

**14. Por que vocês escolheram essas cores específicas no relatório e no dashboard?**  
- Combinamos a identidade visual limpa da marca (`#062A5F` marinho para cabeçalhos/capa, `#0F62FE` azul principal para elementos sem `status_group`, fundo branco) com a **paleta Okabe-Ito** fixa para `status_group` (`#0072B2` funcional, `#E69F00` precisa de reparo, `#D55E00` não funcional), que é segura para pessoas com daltonismo e nunca mistura o significado de alerta com a cor de marca.

### D. Parte Comum (Wine Quality e K-Means)

**15. Por que o K-Means exige padronização (`StandardScaler`) no dataset *Wine Quality*?**  
- Porque o K-Means atribui pontos ao centroide mais próximo usando **distância euclidiana**. Em *Wine Quality*, `total sulfur dioxide` chega a centenas de mg/dm³, enquanto `density` varia em torno de 0,99 a 1,00 e `chlorides` fica em milésimos. Sem `StandardScaler`, o dióxido de enxofre esmagaria todas as demais variáveis. Padronizar para média 0 e desvio padrão 1 equilibra os 11 atributos físico-químicos + `wine_type_red`.

**16. Por que a coluna `quality` não pode entrar no K-Means?**  
- Porque K-Means é **aprendizado não supervisionado**: o objetivo é testar se os atributos físico-químicos sozinhos recuperam os 7 níveis de nota. Incluir `quality` no treino seria vazamento de rótulo (*label leakage*) e invalidaria o experimento.

**17. Como vocês escolheram `k = 3` na Passada 1 (Método do Cotovelo)?**  
- Rodamos K-Means para `k = 2` até `k = 10` e plotamos a **inércia** (WCSS). A maior queda percentual acontece de `k = 2` (56.403,5) para **`k = 3` (45.875,7; -18,67%)**; a partir daí as quedas desaceleram (`-10,21%`, `-6,60%`, `-5,50%`). O ponto de inflexão ("cotovelo") em `k = 3` equilibra coesão (Silhouette 0,252 vs. 0,182 em `k = 7`) e parcimônia.

**18. O que significa "acurácia", "precisão" e "recall" no K-Means e por que 5 notas tiveram recall 0%?**  
- Não é acurácia preditiva supervisionada, mas **coincidência** entre cada cluster (rotulado pela nota mais frequente nele) e a nota real. Como as notas 5 (32,91%) e 6 (43,65%) representam **76,56%** da base, todos os clusters tanto em `k = 3` (coincidência **44,47%**) quanto em `k = 7` (**45,67%**) tiveram 5 ou 6 como maioria. As notas 3, 4, 7, 8 e 9 nunca dominaram nenhum cluster, ficando com precisão e recall 0,0% (`zero_division=0`).

**19. Por que forçar `k = 7` quase não melhorou a coincidência (+1,20 pp)?**  
- Porque as 7 notas sensoriais não formam 7 "ilhas" geométricas separadas no espaço físico-químico: a qualidade é **ordinal**, as classes são muito desbalanceadas (nota 6 sozinha já dá 43,65%) e vinhos de notas vizinhas (5, 6 e 7) têm composição química muito próxima. Além disso, incluir `wine_type_red` puxa os centroides para separar tintos de brancos mais do que notas.

**20. O que vocês fariam diferente se tivessem mais tempo ou outro ciclo de projeto?**  
- (1) Na Parte Específica: testar ajuste de limiar de probabilidade ou `class_weight="balanced"` para elevar o recall de `functional needs repair` (hoje 27,0%) sem destruir a precisão, e coletar dados de campo nas 6 regiões com ausência MAR.  
- (2) Na Parte Comum: rodar a análise de sensibilidade do K-Means **sem** `wine_type_red` e **sem** as 1.177 duplicatas (18,12%) para isolar o efeito da composição pura sobre a qualidade, e comparar tinto vs. branco separadamente.
