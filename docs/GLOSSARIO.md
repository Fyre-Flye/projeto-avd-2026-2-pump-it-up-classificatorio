# Glossário — Pump it Up e termos da EDA

Serve de consulta para a análise, o dashboard e a apresentação. É só tradução e definição de termos: **não interpreta os dados**.

## Como ler a coluna "Fonte"
| Marca | Significa |
| --- | --- |
| **DD** | Descrição oficial na [página de features do DrivenData](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/25/) |
| **Dados** | Fato que dá para conferir no arquivo `pump_it_up_train.csv` (ou no `eda.ipynb`) |
| **Slides** | Definição dada em aula (Aulas 9, 10, 14 e 26) |
| **Trad.** | Tradução literal do termo em inglês, sem fonte técnica |
| **Ext.** | Fonte externa (links no fim) |
| **?** | **A confirmar.** Não achei fonte; não use na apresentação sem conferir |

A página do DrivenData **não explica** as categorias (siglas de gestão, tipos de bomba etc.). Por isso muitos significados abaixo vêm de **Trad.** ou **Ext.**, e alguns ficam com **?**.

---

## 1. Variável-alvo: `status_group`
| Valor | Significado | Fonte |
| --- | --- | --- |
| `functional` | O ponto d'água funciona e não precisa de reparo | DD |
| `functional needs repair` | O ponto d'água funciona, mas precisa de reparo | DD |
| `non functional` | O ponto d'água não funciona | DD |

## 2. Colunas
| Coluna | Significado | Fonte |
| --- | --- | --- |
| `id` | Identificador da linha (único nas 59.400 linhas) | Dados |
| `amount_tsh` | "Total static head": quantidade de água disponível no ponto d'água. A página não informa a **unidade** | DD; unidade **?** |
| `date_recorded` | Data em que a linha foi registrada (anos 2002 a 2013 no arquivo) | DD, Dados |
| `funder` | Quem financiou o poço | DD |
| `gps_height` | Altitude do poço. A página não informa a unidade. Há valores negativos (1.496 linhas) | DD, Dados; unidade **?** |
| `installer` | Organização que instalou o poço | DD |
| `longitude`, `latitude` | Coordenadas GPS | DD |
| `wpt_name` | Nome do ponto d'água, se houver. O valor `none` aparece em 3.563 linhas | DD, Dados |
| `num_private` | **Sem descrição oficial** (campo em branco na página) | DD; significado **?** |
| `basin` | Bacia hidrográfica | DD (tradução: Trad.) |
| `subvillage`, `region`, `lga`, `ward` | Localização geográfica, de granularidade diferente. A página não define cada nível | DD; níveis **?** |
| `region_code`, `district_code` | Localização geográfica, codificada. Sete regiões têm mais de um `region_code` no arquivo (seção 1.2 da EDA) | DD, Dados |
| `population` | População ao redor do poço | DD |
| `public_meeting` | Verdadeiro/Falso. A página não diz o que significa | DD; significado **?** |
| `recorded_by` | Grupo que registrou a linha. Só tem um valor (`GeoData Consultants Ltd`) | DD, Dados |
| `scheme_management` | Quem opera o ponto d'água | DD |
| `scheme_name` | Quem opera o ponto d'água (a descrição oficial é igual à de `scheme_management`) | DD |
| `permit` | Se o ponto d'água tem permissão (licença) | DD |
| `construction_year` | Ano de construção do ponto d'água | DD |
| `extraction_type` | Tipo de extração que o ponto usa (nível mais detalhado) | DD |
| `extraction_type_group` | Idem, nível intermediário | DD, Dados |
| `extraction_type_class` | Idem, nível mais geral | DD, Dados |
| `management` | Como o ponto d'água é gerido (nível detalhado) | DD |
| `management_group` | Idem, nível agrupado | DD, Dados |
| `payment` | O que a água custa (nível detalhado) | DD |
| `payment_type` | Idem, com rótulos mais curtos | DD, Dados |
| `water_quality` | Qualidade da água (nível detalhado) | DD |
| `quality_group` | Idem, nível agrupado | DD, Dados |
| `quantity` | Quantidade de água | DD |
| `quantity_group` | Idem. Os valores são idênticos aos de `quantity` | DD, Dados |
| `source` | Fonte da água (nível detalhado) | DD |
| `source_type` | Idem, nível intermediário | DD, Dados |
| `source_class` | Idem, nível mais geral | DD, Dados |
| `waterpoint_type` | Tipo de ponto d'água (nível detalhado) | DD |
| `waterpoint_type_group` | Idem, nível agrupado | DD, Dados |

**Colunas "irmãs":** nas famílias acima, a coluna mais geral é só um agrupamento da mais detalhada (conferido na seção 1.1 da EDA).

---

## 3. Valores das categorias

### 3.1 Tipo de extração (`extraction_type`, `_group`, `_class`)
O `extraction_type_class` agrupa assim (conferido nos dados): `gravity`, `handpump`, `motorpump`, `submersible`, `rope pump`, `wind-powered` e `other`.

| Valor | Significado | Fonte |
| --- | --- | --- |
| `gravity` | Água que flui por gravidade | Trad. |
| `handpump` | Bomba manual | Trad. |
| `motorpump` | Motobomba (bomba com motor) | Trad. |
| `submersible` | Bomba submersa | Trad. |
| `rope pump` | Bomba de corda | Trad. |
| `wind-powered` / `windmill` | Movida a vento (cata-vento) | Trad. |
| `afridev` | Modelo de bomba manual de alavanca; elevação máxima recomendada de 45 m | Ext. |
| `nira/tanira` | Bomba manual Nira AF-85 (a Tanira seria a versão montada na Tanzânia) | Ext., conferir |
| `india mark ii`, `india mark iii` | Modelos de bomba manual da família India Mark | Ext. parcial |
| `swn 80` | Cabeçote de bomba manual para lençol freático de até cerca de 40 m (o `swn 81` serve aquíferos mais fundos, até cerca de 100 m) | Ext. |
| `mono` | Bomba de cavidade progressiva, com o elemento que bombeia abaixo do nível da água. No arquivo cai na classe `motorpump` | Ext., Dados |
| `ksb`, `cemo`, `climax`, `walimi`, `play pump`, `mkulima/shinyanga` | Nomes de modelos ou marcas. **Não achei fonte** | **?** |
| `other - ...` | Variações agrupadas como "outro" no nível detalhado (ex.: `other - rope pump` cai na classe `rope pump`) | Dados |

### 3.2 Gestão (`management`, `scheme_management`, `management_group`)
`management` e `scheme_management` usam os mesmos nomes (em minúsculas num e com inicial maiúscula no outro). `scheme_management` tem ainda o valor `SWC` e 3.878 faltantes.

| Valor | Significado | Fonte |
| --- | --- | --- |
| `VWC` | *Village Water Committee*: comitê de água da vila | Ext. |
| `WUA` | *Water Users Association*: associação de usuários de água | Ext. |
| `WUG` | *Water User Group*: grupo de usuários de água | Ext. |
| `Water Board` | Conselho de água. A diferença para `Water authority` não está documentada | Trad.; **?** |
| `Water authority` | Autoridade de água | Trad. |
| `Parastatal` | Entidade ligada ao Estado (paraestatal) | Trad. |
| `Private operator` | Operador privado | Trad. |
| `Company` | Empresa | Trad. |
| `Trust` | Entidade administradora (*trust*). O sentido exato aqui não está documentado | Trad.; **?** |
| `SWC` | **Não achei fonte** (só em `scheme_management`; 97 linhas) | **?** |
| `other - school` | Outro: escola (só em `management`) | Trad. |
| `unknown` | Desconhecido | Trad. |

**Agrupamento em `management_group` (conferido nos dados):**
- `user-group` (grupo de usuários): `vwc`, `wug`, `wua`, `water board`
- `commercial` (comercial): `company`, `private operator`, `trust`, `water authority`
- `parastatal`, `other` (inclui `other - school`) e `unknown`

### 3.3 Pagamento (`payment` e `payment_type`)
| `payment` | `payment_type` | Significado | Fonte |
| --- | --- | --- | --- |
| `never pay` | `never pay` | Nunca paga | Trad. |
| `pay per bucket` | `per bucket` | Paga por balde | Trad. |
| `pay monthly` | `monthly` | Paga mensalmente | Trad. |
| `pay annually` | `annually` | Paga anualmente | Trad. |
| `pay when scheme fails` | `on failure` | Paga quando o sistema falha | Trad. |
| `other` | `other` | Outro | Trad. |
| `unknown` | `unknown` | Desconhecido | Trad. |

### 3.4 Quantidade de água (`quantity`)
`enough` (suficiente), `insufficient` (insuficiente), `dry` (seco), `seasonal` (sazonal) e `unknown` (desconhecido). Fonte: Trad. A página não define o critério de cada categoria (**?**).

### 3.5 Qualidade da água (`water_quality`, `quality_group`)
| Valor | Significado | Fonte |
| --- | --- | --- |
| `soft` | Água "mole" (baixa dureza). No `quality_group` vira `good` | Trad., Dados |
| `salty` | Salgada | Trad. |
| `milky` | Leitosa (esbranquiçada) | Trad. |
| `coloured` / `colored` | Com cor | Trad. |
| `fluoride` | Com flúor | Trad. |
| `salty abandoned`, `fluoride abandoned` | Provavelmente "abandonado" por causa do sal ou do flúor. Caem em `salty` e `fluoride` no `quality_group` | Trad.; **?** |
| `unknown` | Desconhecida | Trad. |

### 3.6 Fonte da água (`source`, `source_type`, `source_class`)
| Valor | Significado | Fonte |
| --- | --- | --- |
| `spring` | Nascente | Trad. |
| `shallow well` | Poço raso | Trad. |
| `borehole` | Poço tubular profundo (furo perfurado) | Trad. |
| `river` / `lake` | Rio / lago (viram `river/lake` no `source_type`) | Trad., Dados |
| `rainwater harvesting` | Captação de água da chuva | Trad. |
| `dam` | Represa | Trad. |
| `machine dbh`, `hand dtw` | Siglas não explicadas. Ambas viram `borehole`. Talvez: poço perfurado a máquina e a mão | **?** |
| `groundwater` / `surface` | Água subterrânea / superficial (classe mais geral) | Trad. |

Conferido nos dados: `spring`, `shallow well` e `borehole` são `groundwater`; `dam`, `rainwater harvesting` e `river/lake` são `surface`; `other` e `unknown` ficam como `unknown`.

### 3.7 Tipo de ponto d'água (`waterpoint_type`, `waterpoint_type_group`)
| Valor | Significado | Fonte |
| --- | --- | --- |
| `communal standpipe` | Torneira ou chafariz comunitário | Trad. |
| `communal standpipe multiple` | Idem, com várias torneiras (no grupo, vira `communal standpipe`) | Trad., Dados |
| `hand pump` | Bomba manual | Trad. |
| `improved spring` | Nascente protegida ou melhorada | Trad. |
| `cattle trough` | Bebedouro de gado | Trad. |
| `dam` | Represa | Trad. |
| `other` | Outro | Trad. |

### 3.8 Outras colunas com poucas categorias
- **`basin`** (bacia hidrográfica): `Lake Victoria`, `Pangani`, `Rufiji`, `Internal`, `Lake Tanganyika`, `Wami / Ruvu`, `Lake Nyasa`, `Ruvuma / Southern Coast` e `Lake Rukwa`. (Trad. dos termos; o que é a bacia `Internal` é **?**.)
- **`region`:** as 21 regiões da Tanzânia presentes no arquivo (Arusha, Dar es Salaam, Dodoma, Iringa, Kagera, Kigoma, Kilimanjaro, Lindi, Manyara, Mara, Mbeya, Morogoro, Mtwara, Mwanza, Pwani, Rukwa, Ruvuma, Shinyanga, Singida, Tabora e Tanga).

---

## 4. Termos de estatística e de análise de dados
Definições do jeito que foram dadas em aula.

| Termo | Significado | Fonte |
| --- | --- | --- |
| **EDA** | *Exploratory Data Analysis*: investigar e visualizar os dados de forma sistemática. Os pilares são estrutural, distribucional, relacional e detecção de outliers | Slides (Aulas 9 e 10) |
| **Dado ausente** | Valor que falta. Pode vir como vazio (`NaN`) ou "disfarçado", como um zero ou um código sem sentido | Slides (Aula 9); Dados |
| **MCAR** | *Missing Completely At Random*: a chance de faltar é a mesma para todas as instâncias; não há viés | Slides (Aula 9) |
| **MAR** | *Missing At Random*: a ausência está ligada a algo que **podemos observar**; há viés, mas dá para corrigir | Slides (Aula 9) |
| **MNAR** | *Missing Not At Random*: a ausência depende do **próprio valor** da variável; há viés e não dá para corrigir | Slides (Aula 9) |
| **Imputação** | Preencher valores faltantes (com média, mediana ou moda, ou considerando outras variáveis) | Slides (Aula 9) |
| **Outlier** | Valor muito afastado do restante. A aula separa em estatístico, de domínio (viola regra de negócio ou condição física) e erro de dado | Slides (Aula 9) |
| **Quartis (Q1, Q3)** | Valores que dividem os dados ordenados em quatro partes iguais | Slides (Aula 10) |
| **IQR** | Intervalo interquartil: `Q3 − Q1`. É a base do boxplot | Slides (Aula 10) |
| **Regra do 1,5 × IQR** | Critério usado na EDA para marcar outliers: valores abaixo de `Q1 − 1,5·IQR` ou acima de `Q3 + 1,5·IQR` | Convenção do boxplot; código no `eda.ipynb` |
| **Média / mediana / moda** | Média: soma dividida por n (sensível a outliers). Mediana: valor central após ordenar. Moda: valor mais frequente | Slides (Aula 10) |
| **Assimetria** | Medida do quanto a distribuição é torta para um lado. Na aula: abaixo de 0,5, razoável; entre 0,5 e 1, moderada; acima de 1, alta | Slides (Aula 10) |
| **Boxplot** | Gráfico de caixa, baseado no IQR | Slides (Aula 10) |
| **Correlação de Pearson** | Mede relação **linear**; sensível a outliers | Slides (Aula 10) |
| **Correlação de Spearman** | Mede relação **monotônica** (os valores sobem ou descem juntos, sem precisar ser em linha reta); boa para dados ordinais | Slides (Aula 10) |
| **Variável quantitativa / qualitativa** | Quantitativa: medida em números. Qualitativa: categorias (nominal, sem ordem; ordinal, com ordem) | Slides (Aulas 10 e 26) |
| **Cardinalidade** | Número de categorias distintas de uma variável qualitativa. "Alta cardinalidade" é, por exemplo, `wpt_name` (cerca de 37 mil) | Slides (Aula 26); Dados |
| **Padronização** | Reescala para média 0 e variância 1 (`StandardScaler`) | Slides (Aula 14) |
| **Normalização** | Reescala para um intervalo, em geral [0, 1] (`MinMaxScaler`) | Slides (Aula 14) |
| **Encoding** | Converter variáveis categóricas em números: *label*, *one-hot*, *dummy*, *target*, *frequency* e *hash* | Slides (Aula 26) |
| **Data leakage** | Vazamento de dados: usar informação do teste no treino, o que infla o desempenho. Ex.: normalizar antes de dividir treino e teste | Slides (Aula 26) |
| **Matriz de confusão** | Tabela que cruza a classe real com a prevista; base de acurácia, precisão e recall | Slides (Aula 26) |
| **Acurácia / precisão / recall / F1** | Acurácia: acertos sobre o total. Precisão: dos que o modelo marcou como positivos, quantos eram. Recall: dos positivos reais, quantos o modelo achou. F1: média harmônica de precisão e recall | Slides (Aula 26) |

---

## 5. Pendências (marcadas com **?**)
Para a apresentação, vale confirmar antes de usar:
1. Unidade de `amount_tsh` e de `gps_height`.
2. O que é `num_private`.
3. O que significam `public_meeting`, `lga` e `ward` (níveis administrativos).
4. As siglas `SWC`, `machine dbh` e `hand dtw`, e os modelos `ksb`, `cemo`, `climax`, `walimi`, `play pump` e `mkulima/shinyanga`.
5. A diferença entre `Water Board` e `Water authority`, e o sentido de `Trust` e de `abandoned` nas categorias de qualidade.
6. O que é a bacia `Internal`.

Fontes externas usadas: [glossário de uma dissertação da Mzumbe University](https://scholar.mzumbe.ac.tz/bitstreams/11735b7f-763d-4647-b894-54354a12d377/download) (VWC, WUA, WUG), [lista de organizações comunitárias no relatório da JICA](https://www2.jica.go.jp/en/evaluation/pdf/2012_0804000_4_f.pdf), [RWSN, bombas manuais](https://rural-water-supply.net/en/sustainable-groundwater-management/handpump-technologies), [pôster WEDC sobre a Afridev](https://wedc-knowledge.lboro.ac.uk/resources/posters/P042_The_Afridev_handpump.pdf) e [bomba Nira AF-85](https://rural-water-supply.net/fr/implementation/proprietary-handpumps/nira-af-85-pump).
