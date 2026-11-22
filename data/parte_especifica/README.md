# Dados — Parte Específica (Pump it Up)

## Origem
- **Competição:** [Pump it Up: Data Mining the Water Table (DrivenData)](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/)
- **Dados originais:** [Taarifa](http://taarifa.org/) e Ministério da Água da Tanzânia.
- **Tarefa:** classificar `status_group` em `functional`, `functional needs repair` ou `non functional`.

## Arquivos
| Pasta | Conteúdo | Versionado? |
| --- | --- | --- |
| `raw/pump_it_up_train.csv` | Conjunto de treino com valores e rótulos unificados: 59.400 linhas × 41 colunas (40 atributos + `status_group`). Nunca é editado à mão. | Sim |
| `clean/` | Dataset tratado, exportado na última etapa de `src/parte_especifica/eda.ipynb`. O dashboard lê **só** desta pasta. | Sim |

O CSV unificado foi montado juntando, pela coluna `id`, os dois arquivos oficiais do DrivenData: *Training set values* e *Training set labels*.

## Como baixar de novo (o DrivenData exige cadastro)
1. Crie uma conta gratuita em <https://www.drivendata.org/> e faça login.
2. Abra a competição: <https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/>.
3. Entre na competição pelo botão da página e aceite as regras.
4. Na área de download de dados, baixe **Training set values** e **Training set labels** (CSV).
5. Junte os dois arquivos pela coluna `id` e salve como `raw/pump_it_up_train.csv`:

```python
import pandas as pd

valores = pd.read_csv("training_set_values.csv")   # nome do arquivo baixado
rotulos = pd.read_csv("training_set_labels.csv")
df = valores.merge(rotulos, on="id", how="inner")
df.to_csv("data/parte_especifica/raw/pump_it_up_train.csv", index=False)
```

O *Test set values* da competição não tem rótulos e não é usado neste projeto.

## Dicionário de variáveis (descrição oficial do DrivenData, traduzida)
| Coluna | Descrição |
| --- | --- |
| `amount_tsh` | Total static head: quantidade de água disponível no ponto |
| `date_recorded` | Data de registro da linha |
| `funder` | Quem financiou o poço |
| `gps_height` | Altitude do poço |
| `installer` | Organização que instalou o poço |
| `longitude`, `latitude` | Coordenadas GPS |
| `wpt_name` | Nome do ponto de água, se houver |
| `num_private` | (sem descrição oficial) |
| `basin` | Bacia hidrográfica |
| `subvillage`, `region`, `region_code`, `district_code`, `lga`, `ward` | Localização geográfica |
| `population` | População ao redor do poço |
| `public_meeting` | Verdadeiro/Falso |
| `recorded_by` | Grupo que registrou a linha |
| `scheme_management` | Quem opera o ponto de água |
| `scheme_name` | Quem opera o ponto de água |
| `permit` | Se o ponto de água tem licença |
| `construction_year` | Ano de construção |
| `extraction_type`, `extraction_type_group`, `extraction_type_class` | Tipo de extração usado |
| `management`, `management_group` | Como o ponto de água é gerido |
| `payment`, `payment_type` | Quanto a água custa |
| `water_quality`, `quality_group` | Qualidade da água |
| `quantity`, `quantity_group` | Quantidade de água |
| `source`, `source_type`, `source_class` | Fonte da água |
| `waterpoint_type`, `waterpoint_type_group` | Tipo de ponto de água |
| `status_group` | **Rótulo**: `functional`, `functional needs repair`, `non functional` |
