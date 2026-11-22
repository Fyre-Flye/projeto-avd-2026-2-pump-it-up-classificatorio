# 03 — Parte Específica: Pump it Up (responsável: Gustavo)

## Dataset
- **Fonte:** [DrivenData — Pump it Up: Data Mining the Water Table](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/). Dados da Taarifa e do Ministério da Água da Tanzânia.
- **Arquivo:** `data/parte_especifica/raw/pump_it_up_train.csv`, com 59.400 linhas × 41 colunas (40 atributos + `status_group`).
- **Tarefa:** classificação multiclasse de `status_group`:
  - `functional`: funciona e não precisa de reparo (54,3%)
  - `non functional`: não funciona (38,4%)
  - `functional needs repair`: funciona, mas precisa de reparo (7,3%, classe minoritária)
- Registros de 2002 a 2013. Há 33 qualitativas e 7 quantitativas, segundo a planilha da prof.
- **Status: dataset APROVADO pela professora.**

## Comentários da professora (planilha da turma, aba Datasets). Todos precisam ser tratados na EDA.
1. **Faltantes explícitos:** `scheme_name` 48,5%, `scheme_management` 6,5%, `installer` 6,2%, `funder` 6,1%, `public_meeting` 5,6%, `permit` 5,1%, `subvillage` 0,6%.
2. **Zeros que escondem faltantes:** `population` 36,0%, `construction_year` 34,9%, `gps_height` 34,4%, `longitude = 0` 3,1% (1.812 linhas, com `latitude ≈ 0` nas mesmas). `installer`/`funder` com `'0'` ou `'-'` (~780).
3. **Mecanismo de ausência:** os zeros de `gps_height`, `construction_year` e `population` ocorrem **nas mesmas linhas** (correlação de 0,91 a 0,93 entre os indicadores) e se concentram em **algumas regiões** (Shinyanga, Mbeya, Kagera, Mwanza). A ausência depende da região, o que a prof considera ótimo para discutir o mecanismo.
4. **Descartes a avaliar:** `num_private` (98,7% zeros), `recorded_by` (valor único).
5. **Colunas redundantes:** `extraction_type`/`_group`/`_class`, `quantity`/`quantity_group`, `payment`/`payment_type` (e também `source`/`_type`/`_class`, `waterpoint_type`/`_group`, `water_quality`/`quality_group`, `management`/`management_group`).
6. **Alta cardinalidade:** `wpt_name` (~37 mil), `subvillage` (~19 mil), `installer` (~2,1 mil), `funder` (~1,9 mil).
7. **Outliers (IQR):** `amount_tsh` 18,8% (70% zeros, máximo de 350 mil), `population` 7,4% (máximo de 30.500).
8. **Correlações numéricas modestas:** após tratar os zeros, só `gps_height × longitude` (−0,63) e `amount_tsh × longitude` (−0,42) passam de 0,4 (Spearman).
9. **Incluir no repo as instruções de download** (o DrivenData exige cadastro), já feito em `data/parte_especifica/README.md`.

## Pergunta de pesquisa e público-alvo (decisão do Gustavo, em construção)
- Pergunta de partida: *"Can you predict which water pumps are faulty?"*. A formulação final sai depois da EDA.
- Ainda **não decidido**: treinar um classificador (Aulas 25 e 26) ou responder só pela EDA. Não assuma nenhum dos dois.
- **Público-alvo:** gestor público (ex.: Ministério da Água da Tanzânia) interessado em priorizar manutenção e identificar bombas quebradas ou que precisam de reparo.

## Arquivos
| Onde | O quê |
| --- | --- |
| `src/parte_especifica/eda.ipynb` | EDA do Pump it Up |
| `src/parte_especifica/dashboard.py` | app Streamlit (`streamlit run src/parte_especifica/dashboard.py`) |
| `data/parte_especifica/clean/` | CSV tratado exportado pela EDA; o dashboard lê só daqui |
| `out/parte_especifica/` | figuras e tabelas |
