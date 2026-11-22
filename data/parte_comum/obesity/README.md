# Dados — Parte Comum: Obesity

- **Fonte:** UCI Machine Learning Repository, [Estimation of Obesity Levels Based On Eating Habits and Physical Condition (id 544)](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition). Licença CC BY 4.0, segundo a página da UCI.
- **Artigo de apresentação:** F. Mendoza Palechor e A. De la Hoz Manotas. *Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico*. Data in Brief, 2019. <https://doi.org/10.1016/j.dib.2019.104344>
- **Citação do dataset:** *Estimation of Obesity Levels Based On Eating Habits and Physical Condition* [Dataset]. (2019). UCI Machine Learning Repository. <https://doi.org/10.24432/C5H31Z>
- **Arquivo:** `ObesityDataSet_raw_and_data_sinthetic.csv`, o arquivo original do zip da UCI, sem alterações. Tem 2.111 linhas × 17 colunas, separador `,`.
- **Classe:** `NObeyesdad`, com 7 classes: `Insufficient_Weight`, `Normal_Weight`, `Overweight_Level_I`, `Overweight_Level_II`, `Obesity_Type_I`, `Obesity_Type_II`, `Obesity_Type_III`. A página da UCI chama essa variável de "NObesity".

## Origem dos dados (texto da página da UCI)
- Pessoas do México, do Peru e da Colômbia.
- **77% dos dados foram gerados sinteticamente** com a ferramenta Weka e o filtro SMOTE. Os outros 23% foram coletados diretamente de usuários por uma plataforma web.

## Colunas
| Coluna | Tipo no arquivo | Descrição (página da UCI) |
| --- | --- | --- |
| `Gender` | texto | Gênero (`Female`, `Male`) |
| `Age` | número | Idade |
| `Height` | número | Altura (m) |
| `Weight` | número | Peso (kg) |
| `family_history_with_overweight` | texto (yes/no) | Algum familiar teve ou tem sobrepeso? |
| `FAVC` | texto (yes/no) | Come alimentos muito calóricos com frequência? |
| `FCVC` | número | Costuma comer verduras nas refeições? |
| `NCP` | número | Quantas refeições principais faz por dia? |
| `CAEC` | texto | Come algo entre as refeições? (`no`, `Sometimes`, `Frequently`, `Always`) |
| `SMOKE` | texto (yes/no) | Fuma? |
| `CH2O` | número | (sem descrição na página da UCI; ver o artigo) |
| `SCC` | texto (yes/no) | (sem descrição na página da UCI; ver o artigo) |
| `FAF` | número | (sem descrição na página da UCI; ver o artigo) |
| `TUE` | número | (sem descrição na página da UCI; ver o artigo) |
| `CALC` | texto | (sem descrição na página da UCI; ver o artigo). Valores: `no`, `Sometimes`, `Frequently`, `Always` |
| `MTRANS` | texto | (sem descrição na página da UCI; ver o artigo). Valores: `Automobile`, `Bike`, `Motorbike`, `Public_Transportation`, `Walking` |
| `NObeyesdad` | texto | **Classe** (nível de obesidade) |

Fatos verificados no arquivo: não há valores nulos e existem 24 linhas duplicadas. As colunas `FCVC`, `NCP`, `CH2O`, `FAF` e `TUE` são numéricas e têm valores fracionários: entre 30% e 61% das linhas, conforme a coluna.

Download manual, se precisar: na página da UCI, clique em *Download* e extraia o CSV nesta pasta.
