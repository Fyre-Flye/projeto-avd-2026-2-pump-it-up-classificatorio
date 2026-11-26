"""Gera o relatorio tecnico completo em PDF na raiz do repositorio (relatorio.pdf).

# [IA] Gemini – diagramacao editorial reproduzivel em PDF (identidade visual Secao 2.1 de 06_GUIDELINES)
# Compila os textos autorais ja escritos pelo Gustavo na Parte Especifica e deixa blocos sinalizados
# para integracao final da Parte Comum pelo Arthur Borges.

Execucao, a partir da raiz do repositorio:
    python docs/gerar_relatorio.py
"""

import io
from pathlib import Path
import pymupdf


ROOT = Path(__file__).resolve().parent.parent
OUT_ESP = ROOT / "out" / "parte_especifica"
OUT_COM = ROOT / "out" / "parte_comum"
DESTINO_PDF = ROOT / "relatorio.pdf"


CSS_BASE = """
<style>
  body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9.3pt;
    color: #000000;
    line-height: 1.40;
    margin: 0;
  }
  .capa {
    background-color: #062A5F;
    color: #FFFFFF;
    padding: 20pt 20pt 16pt 20pt;
    margin-bottom: 12pt;
  }
  .capa h1 {
    font-size: 17pt;
    color: #FFFFFF;
    margin: 0 0 5pt 0;
    border: none;
    padding: 0;
    line-height: 1.22;
  }
  .capa .sub {
    font-size: 10pt;
    color: #EAF2FF;
    margin: 0 0 10pt 0;
  }
  .capa .meta {
    font-size: 8.8pt;
    color: #FFFFFF;
    border-top: 0.8pt solid #4589FF;
    padding-top: 7pt;
    line-height: 1.48;
  }
  h1 {
    font-size: 13pt;
    color: #062A5F;
    border-bottom: 1.4pt solid #0F62FE;
    padding-bottom: 3pt;
    margin: 10pt 0 6pt 0;
  }
  h1.topo {
    margin-top: 0;
  }
  h2 {
    font-size: 10.6pt;
    color: #0F62FE;
    margin: 9pt 0 4pt 0;
  }
  h3 {
    font-size: 9.6pt;
    color: #062A5F;
    margin: 6pt 0 3pt 0;
  }
  p {
    margin: 2pt 0 5.5pt 0;
    text-align: left;
  }
  ul {
    margin: 2pt 0 6pt 14pt;
    padding: 0;
  }
  li {
    margin-bottom: 3pt;
  }
  .box-azul {
    background-color: #EAF2FF;
    border-left: 3.5pt solid #0F62FE;
    padding: 7pt 10pt;
    margin: 6pt 0 8pt 0;
  }
  .box-azul .titulo-box {
    color: #0043CE;
    font-weight: bold;
    font-size: 9.2pt;
    margin-bottom: 2.5pt;
  }
  .box-alerta {
    background-color: #FCF4D6;
    border-left: 3.5pt solid #8E6A00;
    padding: 8pt 10pt;
    margin: 7pt 0 9pt 0;
    color: #000000;
    font-size: 9pt;
  }
  .box-alerta .titulo-alerta {
    color: #8E6A00;
    font-weight: bold;
    font-size: 9.3pt;
    margin-bottom: 3pt;
  }
  .nota-box {
    background-color: #F4F4F4;
    border-left: 3pt solid #8D8D8D;
    padding: 6pt 9pt;
    margin: 3pt 0 9pt 0;
    font-size: 8.8pt;
    line-height: 1.38;
  }
  .legenda {
    font-size: 8.1pt;
    color: #525252;
    text-align: center;
    margin: 2pt 0 5pt 0;
  }
  .img-wrap {
    text-align: center;
    margin: 4pt 0 2pt 0;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6pt 0 8pt 0;
    font-size: 8.4pt;
  }
  th, td {
    border: 0.5pt solid #E0E0E0;
    padding: 4pt 5.5pt;
    text-align: left;
  }
  th {
    background-color: #062A5F;
    color: #FFFFFF;
    font-weight: bold;
  }
  tr.par td {
    background-color: #F4F4F4;
  }
  td.num, th.num {
    text-align: right;
  }
  code {
    font-family: Courier, monospace;
    font-size: 8.4pt;
    background-color: #F4F4F4;
    padding: 0.5pt 2pt;
  }
</style>
"""


def img_tag(caminho: Path, style: str) -> str:
    if not caminho.exists():
        return f"<p><i>[Imagem pendente: {caminho.name}]</i></p>"
    rel = caminho.relative_to(ROOT).as_posix()
    return f'<div class="img-wrap"><img src="{rel}" style="{style}"/></div>'


def wrap_page(body_html: str) -> str:
    return f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>{body_html}</body></html>'


def montar_paginas() -> list[str]:
    """Monta paginas A4 independentes (evita quebras orfas e vazamento de estilo entre paginas)."""
    fig_mar_reg = img_tag(OUT_ESP / "02_ausencia_por_regiao.png", "width:84%;")
    fig_expl_1 = img_tag(OUT_ESP / "07_expl_01_distribuicao_status.png", "width:56%;")
    fig_expl_2 = img_tag(OUT_ESP / "07_expl_02_status_por_categoria.png", "width:83%;")
    fig_expl_3 = img_tag(OUT_ESP / "07_expl_03_contraste_regional_mapa.png", "width:96%;")
    fig_expl_4 = img_tag(OUT_ESP / "07_expl_04_heatmap_quantity_extraction.png", "width:78%;")
    fig_explan_1 = img_tag(OUT_ESP / "08_explan_01_tecnologia_com_agua.png", "width:74%;")
    fig_explan_2a = img_tag(OUT_ESP / "08_explan_02a_idade_vs_falha.png", "width:72%;")
    fig_explan_2b = img_tag(OUT_ESP / "08_explan_02b_classificador_metricas.png", "width:98%;")
    fig_cm_clf = img_tag(OUT_ESP / "06_matriz_confusao_modelos.png", "width:94%;")
    fig_ob_cls = img_tag(OUT_COM / "02_distribuicao_classes.png", "width:78%;")

    # ------------------------------------------------------------------
    # PAGINA 1: CAPA + SECAO 1 + SECAO 2
    # ------------------------------------------------------------------
    p1 = wrap_page("""
<div class="capa">
  <h1>Relatório Técnico: Agrupamento, EDA e Dashboard Interativo</h1>
  <div class="sub">Avaliação II (AV2) de Análise e Visualização de Dados (AVD) | Grupo 6</div>
  <div class="meta">
    <b>Instituição:</b> CESAR School | <b>Período:</b> 2026.2 | <b>Professora:</b> Maira Lira<br/>
    <b>Parte Específica (Pump it Up: Data Mining the Water Table):</b> Gustavo Henrique Cruz de Oliveira<br/>
    <b>Parte Comum (Obesity, UCI 544) e Integração Final:</b> João Vitor do Sacramento Bezerra da Cunha; Arthur Borges<br/>
    <b>Data de entrega:</b> 26/11/2026 | <b>Apresentação e Defesa:</b> 03/12/2026
  </div>
</div>

<h1>1. Resumo Executivo</h1>
<p>
  Este relatório apresenta a análise técnica desenvolvida pelo Grupo 6 para o Projeto Final de Análise e Visualização de
  Dados (AVD). O trabalho integra duas frentes complementares: a <b>Parte Específica</b>, dedicada à exploração,
  tratamento, storytelling, modelagem preditiva e construção de dashboard interativo em Streamlit sobre os pontos d'água
  da Tanzânia (dataset <i>Pump it Up</i>, DrivenData/Taarifa, 59.400 registros brutos e 59.333 após limpeza), e a
  <b>Parte Comum</b>, voltada à análise exploratória, padronização e agrupamento não supervisionado com K-Means em duas
  passadas sobre o dataset <i>Obesity</i> (UCI 544, 2.111 registros e 7 classes).
</p>
<p>
  Na Parte Específica, os achados respondem integralmente à pergunta de pesquisa formulada para gestores do Ministério de
  Águas da Tanzânia. Quase metade da rede inspecionada entre 2011 e 2013 está inoperante (38,4%) ou requer reparo (7,3%),
  contra 54,3% de pontos funcionais. A falha das bombas associa-se fortemente à escassez hídrica (96,9% de inoperância em
  pontos secos), mas também ocorre onde há água suficiente: bombas motorizadas (<code>motorpump</code>, 45,9% inoperantes)
  falham 2,5 vezes mais que sistemas por gravidade (<code>gravity</code>, 18,4%). Além disso, a taxa de inoperância cresce
  de 23,9% em bombas de 0 a 5 anos para 60,8% acima de 30 anos. Um classificador <code>RandomForestClassifier</code>
  treinado sem vazamento de dados alcançou 80,58% de acurácia no teste (n = 11.867), superando a Árvore de Decisão baseline
  (75,33%) e expondo o gargalo operacional da classe minoritária <code>functional needs repair</code> (precisão de 65,82%,
  porém recall de 27,00%).
</p>

<h1>2. Parte Específica: Pergunta de Pesquisa, Público-Alvo e Dados</h1>
<h2>2.1 Pergunta de pesquisa e público-alvo</h2>
<div class="box-azul">
  <div class="titulo-box">Público-alvo definido</div>
  Gestores públicos do Ministério de Águas da Tanzânia, interessados em priorizar manutenção preventiva, alocar equipes em
  campo e identificar bombas quebradas ou com necessidade de reparo.
</div>
<div class="box-azul">
  <div class="titulo-box">Pergunta de pesquisa</div>
  "Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de reparo ou não
  funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas com necessidade de
  manutenção ou inoperantes?"
</div>

<h2>2.2 Origem e estrutura do dataset</h2>
<p>
  A base provém da competição <i>Pump it Up: Data Mining the Water Table</i> (DrivenData), construída com registros da
  plataforma Taarifa e do Ministério da Água da Tanzânia. O arquivo bruto (<code>data/parte_especifica/raw/pump_it_up_train.csv</code>)
  contém <b>59.400 linhas e 41 colunas</b> (40 atributos explicativos e a variável-alvo multiclasse <code>status_group</code>),
  combinando variáveis quantitativas e qualitativas de baixa e alta cardinalidade. As definições completas de colunas e
  categorias estão documentadas em <code>docs/GLOSSARIO.md</code>; colunas sem documentação oficial (como
  <code>num_private</code>) foram descartadas na etapa de limpeza.
</p>
""")

    # ------------------------------------------------------------------
    # PAGINA 2: SECAO 3.1 + 3.2 (MAR + FIGURA 1)
    # ------------------------------------------------------------------
    p2 = wrap_page(f"""
<h1 class="topo">3. Parte Específica: Análise Exploratória (EDA), Qualidade e Tratamento</h1>
<h2>3.1 Análise estrutural e cardinalidade</h2>
<p>
  Não foram encontrados identificadores (<code>id</code>) repetidos nem linhas inteiramente idênticas considerando todas as
  41 colunas, mas a verificação ignorando <code>id</code> revelou <b>36 registros duplicados</b> nas demais 40 colunas,
  removidos na etapa de tratamento. A análise de estrutura também identificou colunas irrelevantes ou inconsistentes:
  <code>recorded_by</code> assume valor único (<code>GeoData Consultants Ltd</code>) em 100% da base; <code>region_code</code>
  apresenta mapeamento inconsistente com <code>region</code> (sete regiões aparecem associadas a mais de um código); e sete
  famílias de atributos repetem a mesma informação em níveis diferentes de detalhe (por exemplo,
  <code>extraction_type</code>, <code>extraction_type_group</code> e <code>extraction_type_class</code>).
</p>
<p>
  Nas variáveis nominais de alta cardinalidade (<code>wpt_name</code> com 37.400 categorias, <code>subvillage</code> com
  19.287, <code>installer</code> com 2.145 e <code>funder</code> com 1.897), padronizar espaços e caixa baixa com
  <code>strip().lower()</code> reduziu duplicidades de digitação em <code>installer</code> (de 2.145 para 1.935) e
  <code>scheme_name</code> (de 2.695 para 2.576). Para evitar explosão dimensional no One-Hot Encoding, optou-se por descartar
  identificadores quase únicos (<code>wpt_name</code>, <code>subvillage</code>) e aplicar <b>Target Encoding</b> às quatro
  nominais de alta cardinalidade mantidas (<code>lga</code>, <code>ward</code>, <code>funder</code> e <code>installer</code>)
  dentro de um <code>Pipeline</code> ajustado exclusivamente no conjunto de treino.
</p>

<h2>3.2 Dados ausentes, mecanismo MAR e imputação em cascata</h2>
<p>
  Além dos valores <code>NaN</code> explícitos (<code>scheme_name</code> com 48,5%, <code>scheme_management</code> com 6,5%,
  <code>installer</code> com 6,2%, <code>funder</code> com 6,1%, <code>public_meeting</code> com 5,6% e <code>permit</code>
  com 5,1%), a inspeção de domínio detectou zeros estruturais que escondem ausência real: <code>population</code> (36,0%),
  <code>construction_year</code> (34,9%), <code>gps_height</code> (34,4%) e coordenadas GPS zeradas (3,1%, equivalentes a
  1.812 linhas com <code>longitude = 0</code> e <code>latitude</code> próxima de zero).
</p>
<p>
  Os indicadores de ausência de <code>population</code>, <code>construction_year</code> e <code>gps_height</code> apresentam
  coocorrência de <b>0,91 a 0,93</b> entre si e concentram-se entre <b>88,6% e 100% em seis regiões</b> (Dodoma, Kagera,
  Mbeya, Tabora, Shinyanga e Mwanza), enquanto as outras 15 regiões ficam abaixo de 7,3% (Figura 1). Como a ausência depende
  da variável observável <code>region</code>, descarta-se MCAR e caracteriza-se o mecanismo <b>MAR (Missing At Random)</b>
  (Aula 09).
</p>
{fig_mar_reg}
<div class="legenda">Figura 1: Percentual de ausência (NaN e zeros suspeitos) por região na base bruta (n = 59.400), evidenciando o mecanismo MAR concentrado em 6 regiões. Fonte: DrivenData/Taarifa (2002 a 2013).</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 3: DECISAO DE IMPUTACAO + 3.3 + TABELA 1 + 4.1 STORYTELLING
    # ------------------------------------------------------------------
    p3 = wrap_page("""
<p>
  Remover essas linhas eliminaria cerca de um terço da base e apagaria quase 100% de seis regiões inteiras. Por isso, os
  zeros suspeitos foram convertidos em <code>NaN</code>, preservando-se quatro flags binárias (<code>ausente_population</code>,
  <code>ausente_construction_year</code>, <code>ausente_gps_height</code> e <code>ausente_coords</code>) antes da imputação.
  Como quatro regiões (Dodoma, Kagera, Mbeya e Tabora) possuem zero registros válidos nessas três numéricas, adotou-se
  <b>imputação agrupada em cascata pela mediana</b> seguindo a hierarquia <code>lga -&gt; region -&gt; basin</code> (todas
  as nove bacias hidrográficas possuem ao menos 988 valores válidos). Já <code>amount_tsh</code> foi mantida com
  <code>0</code> (70,0% zeros), pois imputar 70% de uma coluna deformaria a distribuição e a diferença entre
  <code>amount_tsh == 0</code> (45,4% inoperantes) e <code>&gt; 0</code> (22,2% inoperantes) carrega forte sinal. As
  categóricas com <code>NaN</code>, <code>'0'</code> ou <code>'-'</code> receberam a categoria explícita
  <code>"desconhecido"</code>.
</p>

<h2>3.3 Recorte temporal, outliers e conferência antes vs. depois</h2>
<p>
  Em <code>date_recorded</code>, 99,95% das coletas ocorreram entre 2011 e 2013; apenas 31 registros residuais eram de 2002 e
  2004 e concentravam todas as 9 inconsistências de idade negativa (<code>construction_year &gt; ano_registro</code>), motivo
  pelo qual foram descartados. Os 1.496 registros com altitude negativa (<code>gps_height &lt; 0</code>, mediana de -18 m e
  mínimo de -90 m) concentram-se nas cinco regiões litorâneas (Pwani, Mtwara, Lindi, Dar es Salaam e Tanga), indicando erro
  vertical de GPS próximo ao nível do mar; eles foram corrigidos para <code>0</code> após a imputação dos zeros originais,
  sem perda de linhas. Outliers positivos de <code>amount_tsh</code> (18,8% pelo IQR, máx. 350.000) e <code>population</code>
  (7,4% pelo IQR, máx. 30.500) foram mantidos por serem plausíveis no domínio e não prejudicarem modelos baseados em árvores.
</p>

<table>
  <thead>
    <tr>
      <th>Métrica de conferência</th>
      <th class="num">Base bruta</th>
      <th class="num">Base tratada</th>
      <th>Decisão aplicada na Seção 6 da EDA</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Linhas</td><td class="num">59.400</td><td class="num">59.333</td><td>Remoção de 36 duplicadas (sem id) e 31 registros de 2002/2004</td></tr>
    <tr class="par"><td>Colunas</td><td class="num">41</td><td class="num">31</td><td>Descarte de 16 redundantes/irrelevantes; adição de flags e derivadas</td></tr>
    <tr><td>NaN explícitos</td><td class="num">46.743</td><td class="num">0</td><td>Categóricas preenchidas com "desconhecido"</td></tr>
    <tr class="par"><td>Zeros suspeitos (pop / year / gps / lon)</td><td class="num">64.340</td><td class="num">0</td><td>Flags ausente_* salvas + imputação em cascata (lga -&gt; region -&gt; basin)</td></tr>
    <tr><td>Idades negativas (construction_year &gt; ano)</td><td class="num">9</td><td class="num">0</td><td>Eliminadas no recorte temporal de 2011 a 2013</td></tr>
    <tr class="par"><td>Altitudes negativas (gps_height &lt; 0)</td><td class="num">1.496</td><td class="num">0</td><td>Ajustadas para 0 (litoral) após imputação dos zeros originais</td></tr>
  </tbody>
</table>

<h1>4. Parte Específica: Storytelling e Visualizações</h1>
<h2>4.1 Raciocínio do Storytelling (da Exploratória à Explanatória)</h2>
<p>
  <b>Público-alvo e linguagem:</b> voltado a gestores públicos do Ministério de Águas da Tanzânia, o storytelling traduz os
  achados da EDA em linguagem objetiva, com percentuais em pt-BR, rótulos diretos e paleta acessível a daltonismo
  (Okabe-Ito: azul <code>#0072B2</code> para funcional, amarelo <code>#E69F00</code> para precisa de reparo e laranja
  <code>#D55E00</code> para não funcional; azul de marca <code>#0F62FE</code> apenas em gráficos que não exibem
  <code>status_group</code>).
</p>
<p>
  <b>O que nasceu da exploração:</b> a EDA mostrou que a falha de uma bomba não se limita à seca da fonte. Mesmo quando há
  água suficiente (<code>quantity = enough</code>), sistemas motorizados falham muito mais que soluções mecânicas simples;
  além disso, a inoperância aumenta continuamente com a idade da infraestrutura e apresenta forte contraste territorial entre
  regiões. A modelagem supervisionada confirmou esses sinais e revelou o principal gargalo operacional na detecção da classe
  minoritária <code>functional needs repair</code>.
</p>
<div class="box-azul">
  <div class="titulo-box">Big Idea (Sujeito + Verbo + Ponto de Vista, Aula 06)</div>
  Os pontos d'água da Tanzânia falham principalmente quando há escassez de água, quando são mais antigos ou quando usam
  tecnologias motorizadas em vez de sistemas mais simples (como gravidade e bombas manuais), que se mantêm mais funcionais
  mesmo quando há água disponível.
</div>
<p>
  <b>Atributos pré-atentivos aplicados:</b> <b>cor por exceção</b> (categorias de contexto em cinza <code>#C6C6C6</code>
  contra destaque em laranja <code>#D55E00</code> nos grupos críticos e azul <code>#0F62FE</code> nos atributos-chave),
  <b>posição em eixo comum</b> com ordenação explícita por taxa ou cronologia, e <b>anotações diretas</b> com linhas de
  referência.
</p>
""")

    # ------------------------------------------------------------------
    # PAGINA 4: EXPLORATORIAS 1 E 2
    # ------------------------------------------------------------------
    p4 = wrap_page(f"""
<h2 style="margin-top:0;">4.2 Visualizações Exploratórias (4 gráficos) e Notas Analíticas</h2>

<h3>Exploratória 1: Distribuição da situação operacional (status_group)</h3>
{fig_expl_1}
<div class="legenda">Figura 2: Contagem e percentual das três classes de status_group na base tratada (n = 59.333).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Mostra a distribuição das três classes de <code>status_group</code> (32.226 funcionais, 54,3%;
  22.794 não funcionais, 38,4%; e 4.313 precisando de reparo, 7,3%). O insight principal é o forte desbalanceamento da base e
  o fato de 45,7% dos pontos já apresentarem falha ou necessidade de reparo; como a classe minoritária soma apenas 7,3%,
  avaliar o classificador apenas pela acurácia global esconderia falhas nessa classe. Escolheu-se o gráfico de barras verticais
  com eixo Y em zero e rótulos diretos por ser a forma mais precisa para comparar contagens entre poucas categorias nominais.
</div>

<h3>Exploratória 2: Situação operacional por variáveis categóricas principais</h3>
{fig_expl_2}
<div class="legenda">Figura 3: Proporção de status_group em quantity, extraction_type_class, waterpoint_type_group e payment_type (n = 59.333).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Compara a composição proporcional de <code>status_group</code> nas quatro qualitativas de maior
  destaque (no dashboard Streamlit o usuário alterna entre todas as 12 categóricas). Em <code>quantity</code>, pontos secos
  (<code>dry</code>, 97% inoperantes) e desconhecidos (<code>unknown</code>, 71%) lideram as falhas; em
  <code>payment_type</code>, <code>never pay</code> concentra 42,7% dos registros e apresenta 48% de inoperância (contra 18%
  em pagamento anual e 23% mensal). Barras horizontais 100% empilhadas foram escolhidas para acomodar rótulos longos sem
  inclinação e comparar proporções entre categorias de volumes muito distintos.
</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 5: EXPLORATORIAS 3 E 4
    # ------------------------------------------------------------------
    p5 = wrap_page(f"""
<h3 style="margin-top:0;">Exploratória 3: Contraste regional e distribuição geográfica</h3>
{fig_expl_3}
<div class="legenda">Figura 4: Ranking ordenado de taxa de inoperância nas 21 regiões (n = 59.333) e distribuição espacial com GPS real (n = 57.556).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Reúne o ranking de percentual não funcional por região frente à média nacional (38,4%) e a posição
  geográfica das bombas com coordenadas reais (omitindo pontos imputados). Evidencia-se forte disparidade territorial: Iringa
  (19,5% inoperantes; 78,2% funcionais) e Arusha (26,3% inoperantes) lideram o desempenho positivo, enquanto Lindi (64,2%),
  Mtwara (62,4%) e Tabora (54,4%) superam metade dos pontos inoperantes. A combinação de barra horizontal ordenada com mapa
  responde simultaneamente ao ranking exato e à concentração espacial.
</div>

<h3>Exploratória 4: Cruzamento multivariado entre disponibilidade de água e tecnologia</h3>
{fig_expl_4}
<div class="legenda">Figura 5: Mapa de calor de % não funcional cruzando quantity e extraction_type_class (exclui unknown e other, n = 52.305).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Cruza disponibilidade hídrica e tecnologia de extração exibindo taxa de inoperância e tamanho de
  amostra (<code>n</code>) em cada célula. Enquanto a coluna <code>dry</code> concentra 90% a 100% de falha em qualquer
  tecnologia, a coluna <code>enough</code> revela o contraste que origina a análise explanatória: <code>motorpump</code>
  (45,9%) e <code>wind-powered</code> (44,1%, n = 59) falham muito mais que <code>gravity</code> (18,4%) e
  <code>handpump</code> (23,5%). O mapa de calor com escala sequencial (<code>YlOrRd</code>) permite inspecionar padrões
  combinados entre duas variáveis qualitativas sem poluição visual.
</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 6: EXPLANATORIAS 1 E 2A
    # ------------------------------------------------------------------
    p6 = wrap_page(f"""
<h2 style="margin-top:0;">4.3 Visualizações Explanatórias (3 gráficos) e Notas Analíticas</h2>
<p>
  Embora o enunciado solicite o mínimo de duas visualizações explanatórias, optou-se por apresentar três visuais
  complementares que cobrem integralmente os dois eixos da Big Idea (tecnologia com água disponível e idade da rede) e a
  segunda metade da pergunta de pesquisa (capacidade preditiva do classificador).
</p>

<h3>Explanatória 1: Tecnologia de extração quando há água suficiente</h3>
{fig_explan_1}
<div class="legenda">Figura 6: Taxa de inoperância por extraction_type_class restrita a pontos com quantity = enough (n = 33.150).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Mostra a taxa de pontos não funcionais por tecnologia apenas onde há água suficiente
  (<code>quantity = enough</code>, média do recorte de 27,5%). Mesmo com água disponível, <code>motorpump</code> (45,9%)
  falha 2,5 vezes mais (+27,4 pontos percentuais) que <code>gravity</code> (18,4%), e <code>wind-powered</code> (44,1%, com
  ressalva de amostra pequena, n = 59) acompanha essa tendência, ficando <code>submersible</code> (33,0%) em nível
  intermediário. Tecnologias motorizadas dependem de manutenção especializada, enquanto <code>other</code> (76,7%) sugere
  soluções improvisadas. Barra horizontal ordenada com cor por exceção destaca imediatamente a tese ao gestor.
</div>

<h3>Explanatória 2A: Envelhecimento da rede vs. taxa de inoperância</h3>
{fig_explan_2a}
<div class="legenda">Figura 7: Taxa de pontos não funcionais por faixa de idade real (somente ausente_construction_year = 0, n = 38.674).</div>
<div class="nota-box">
  <b>Nota analítica:</b> Exibe o percentual de pontos inoperantes em seis faixas de idade, usando apenas os 38.674 registros
  com ano de construção informado (omitindo os 34,8% imputados por MAR). Diferentemente da população ao redor (mediana
  idêntica de 150 habitantes em funcionais e quebradas), a idade separa claramente o estado operacional: a falha sobe
  monotonicamente de 23,9% (0 a 5 anos) para 48,3% (21 a 30 anos) e chega a 60,8% acima de 30 anos, com mediana de 18 anos nas
  bombas inoperantes contra 9 anos nas funcionais.
</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 7: EXPLANATORIA 2B + SECAO 5.1 + TABELA 2
    # ------------------------------------------------------------------
    p7 = wrap_page(f"""
<h3 style="margin-top:0;">Explanatória 2B: Desempenho preditivo e top atributos do Random Forest</h3>
{fig_explan_2b}
<div class="legenda">Figura 8: Precisão e Recall por classe (teste n = 11.867) e Top 10 atributos mais relevantes no RandomForestClassifier.</div>
<div class="nota-box">
  <b>Nota analítica:</b> Responde diretamente à segunda metade da pergunta de pesquisa, mostrando Precisão e Recall por classe
  no teste (acurácia global de 80,58%) e as 10 variáveis de maior importância agregada no <code>RandomForestClassifier</code>.
  O modelo separa bem bombas funcionais (recall 91,02%) e inoperantes (precisão 84,42%, recall 75,96%), mas expõe o gargalo
  operacional na classe minoritária <code>functional needs repair</code> (precisão de 65,82%, porém recall de apenas 27,00%).
  As importâncias confirmam <code>quantity</code> (11,8%), <code>waterpoint_type_group</code> (5,1%) e
  <code>extraction_type_class</code> (4,6%) junto aos sinais locais e de gestão em alta cardinalidade (<code>ward</code>,
  <code>funder</code>, <code>installer</code>, <code>lga</code>).
</div>

<h1>5. Classificador Supervisionado e Dashboard Interativo</h1>
<h2>5.1 Pipeline sem data leakage e comparação entre modelos</h2>
<p>
  Em <code>src/parte_especifica/classificador.ipynb</code>, o CSV limpo teve seus valores imputados revertidos para
  <code>NaN</code> via flags <code>ausente_*</code> antes da divisão estratificada 80/20 (treino n = 47.466; teste
  n = 11.867; <code>random_state = 42</code>). Tanto a imputação em cascata (<code>ImputadorCascata</code>) quanto o
  <code>ColumnTransformer</code> (<code>OneHotEncoder</code> nas 12 categóricas de baixa cardinalidade e
  <code>TargetEncoder(smooth="auto")</code> nas 4 de alta cardinalidade) foram encapsulados no <code>Pipeline</code> e
  ajustados apenas sobre <code>X_train</code>, eliminando vazamento de dados (Aula 26).
</p>

<table>
  <thead>
    <tr>
      <th>Modelo</th>
      <th>Classe / Agregado</th>
      <th class="num">Acurácia (%)</th>
      <th class="num">Precisão (%)</th>
      <th class="num">Recall (%)</th>
      <th class="num">F1 (%)</th>
      <th class="num">Suporte</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Árvore de Decisão (baseline)</td><td>functional</td><td class="num">75,33</td><td class="num">76,04</td><td class="num">85,28</td><td class="num">80,39</td><td class="num">6.445</td></tr>
    <tr class="par"><td>Árvore de Decisão (baseline)</td><td>functional needs repair</td><td class="num">75,33</td><td class="num">47,35</td><td class="num">26,88</td><td class="num">34,29</td><td class="num">863</td></tr>
    <tr><td>Árvore de Decisão (baseline)</td><td>non functional</td><td class="num">75,33</td><td class="num">77,42</td><td class="num">70,45</td><td class="num">73,77</td><td class="num">4.559</td></tr>
    <tr class="par"><td><b>Árvore de Decisão (baseline)</b></td><td><b>Média Macro (3 classes)</b></td><td class="num"><b>75,33</b></td><td class="num"><b>66,93</b></td><td class="num"><b>60,87</b></td><td class="num"><b>62,82</b></td><td class="num"><b>11.867</b></td></tr>
    <tr><td>Random Forest (200 árvores)</td><td>functional</td><td class="num">80,58</td><td class="num">79,15</td><td class="num">91,02</td><td class="num">84,67</td><td class="num">6.445</td></tr>
    <tr class="par"><td>Random Forest (200 árvores)</td><td>functional needs repair</td><td class="num">80,58</td><td class="num">65,82</td><td class="num">27,00</td><td class="num">38,29</td><td class="num">863</td></tr>
    <tr><td>Random Forest (200 árvores)</td><td>non functional</td><td class="num">80,58</td><td class="num">84,42</td><td class="num">75,96</td><td class="num">79,97</td><td class="num">4.559</td></tr>
    <tr class="par"><td><b>Random Forest (200 árvores)</b></td><td><b>Média Macro (3 classes)</b></td><td class="num"><b>80,58</b></td><td class="num"><b>76,46</b></td><td class="num"><b>64,66</b></td><td class="num"><b>67,64</b></td><td class="num"><b>11.867</b></td></tr>
  </tbody>
</table>
""")

    # ------------------------------------------------------------------
    # PAGINA 8: FIGURA 9 + TRADE-OFF + 5.2 DASHBOARD STREAMLIT
    # ------------------------------------------------------------------
    p8 = wrap_page(f"""
{fig_cm_clf}
<div class="legenda">Figura 9: Matrizes de confusão lado a lado (Árvore de Decisão baseline vs. Random Forest) no conjunto de teste (n = 11.867).</div>

<p>
  O <code>RandomForestClassifier</code> superou o baseline em todas as métricas (+5,25 pontos percentuais em acurácia e +4,82
  pp em Macro F1). Na prática operacional do Ministério de Águas, observa-se um trade-off claro: o Random Forest oferece maior
  acurácia para triagem em larga escala, enquanto a Árvore de Decisão permite auditar passo a passo cada regra percorrida
  (<code>decision_path</code>) até a decisão final, recurso integrado à demonstração ao vivo no dashboard.
</p>

<h2>5.2 Dashboard Interativo em Streamlit e Recursos de Bônus Visual/UX</h2>
<p>
  O aplicativo em <code>src/parte_especifica/dashboard.py</code> (apoiado por <code>data_loader.py</code> com separação
  estrita entre <code>@st.cache_data</code> para dados e <code>@st.cache_resource</code> para modelos, e tema oficial em
  <code>.streamlit/config.toml</code>) adota a identidade visual limpa do projeto (azul marinho <code>#062A5F</code>, azul
  principal <code>#0F62FE</code>, destaque claro <code>#EAF2FF</code> e paleta Okabe-Ito para <code>status_group</code>) e
  organiza toda a experiência em cinco abas interligadas pelos filtros globais da barra lateral:
</p>
<ul>
  <li><b>Aba 1 (Storytelling e Insights):</b> apresenta a Big Idea em destaque e as três visualizações explanatórias interativas com notas analíticas expansíveis.</li>
  <li><b>Aba 2 (Exploração Interativa):</b> reúne as quatro visualizações exploratórias, seletor livre de qualquer uma das 12 variáveis categóricas, <b>heatmap livre de duas variáveis</b> (preparado para testes ao vivo na arguição), mapa Carto Positron com opção offline, <b>Comparador lado a lado de duas regiões</b> e diagnóstico do mecanismo MAR.</li>
  <li><b>Aba 3 (Classificador e Auditoria):</b> exibe as matrizes de confusão e métricas, permite sortear 3 bombas reais do teste (alternando entre Cartões e Tabela), mostra mapa e probabilidades previstas, abre a <b>trilha passo a passo <code>decision_path</code></b> da Árvore de Decisão e inclui um simulador de bomba via <code>st.form</code>.</li>
  <li><b>Aba 4 (Parte Comum: K-Means Obesity):</b> permite ajustar <code>k</code> livre da Passada 1, inspecionar a curva do Método do Cotovelo e reproduzir a <b>animação interativa de transição entre Passada 1 e Passada 2 em PCA 2D</b>, junto às matrizes de confusão e métricas por classe.</li>
  <li><b>Aba 5 (Glossário e Exportação):</b> glossário pesquisável de colunas/termos e download direto do recorte filtrado em CSV e do resumo executivo em Markdown.</li>
</ul>
<div class="box-azul">
  <div class="titulo-box">Boas práticas de UX/UI e desempenho aplicadas</div>
  Uso de controles nativos modernos do Streamlit (<code>st.pills</code>, <code>st.segmented_control</code>,
  <code>st.container(border=True)</code> e <code>@st.fragment</code> para isolamento de reexecuções), barra de resumo dos
  filtros ativos com botão de limpeza rápida e contraste superior a 4,5:1 em todos os textos.
</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 9: SECAO 6 (PARTE COMUM) + SECAO 7 (LIMITACOES E REFERENCIAS)
    # ------------------------------------------------------------------
    p9 = wrap_page(f"""
<h1 class="topo">6. Parte Comum: EDA e Agrupamento K-Means (Obesity, UCI 544)</h1>
<p>
  O grupo selecionou o dataset <b>Obesity</b> (UCI Machine Learning Repository, id = 544,
  <code>data/parte_comum/obesity/ObesityDataSet_raw_and_data_sinthetic.csv</code>), composto por <b>2.111 registros e 17
  colunas</b> (8 atributos numéricos: <code>Age</code>, <code>Height</code>, <code>Weight</code>, <code>FCVC</code>,
  <code>NCP</code>, <code>CH2O</code>, <code>FAF</code>, <code>TUE</code>; 8 atributos qualitativos; e a variável de classe
  <code>NObeyesdad</code> com <b>7 níveis de peso/obesidade</b>). Não há valores nulos, há 24 linhas duplicadas e cerca de
  77% dos dados são sintéticos (SMOTE), conforme documentação da UCI.
</p>

{fig_ob_cls}
<div class="legenda">Figura 10: Distribuição das 7 classes originais de NObeyesdad no dataset Obesity (n = 2.111). Fonte: UCI (id = 544).</div>

<h2>6.1 Por que padronizar antes do K-Means (Aula 14)</h2>
<p>
  O algoritmo K-Means agrupa observações minimizando a soma das distâncias euclidianas ao quadrado até os centroides. Como as
  variáveis numéricas de <i>Obesity</i> possuem escalas muito distintas (<code>Weight</code> varia entre 39 kg e 173 kg
  enquanto <code>Height</code> varia entre 1,45 m e 1,98 m e <code>TUE</code> entre 0 e 2), rodar o K-Means sem padronização
  faria o peso dominar quase completamente o cálculo de distância. Aplicar <code>StandardScaler</code> (média 0 e desvio padrão
  1) antes do agrupamento garante que todas as variáveis numéricas contribuam em igualdade de escala. A coluna
  <code>NObeyesdad</code> nunca entra no treinamento do K-Means.
</p>

<div class="box-alerta">
  <div class="titulo-alerta">INTEGRAÇÃO PENDENTE (ARTHUR BORGES): Resultados finais e discussão crítica da Parte Comum</div>
  Os notebooks <code>notebooks/parte_comum/eda.ipynb</code> (pilares distribucional, relacional e outliers) e
  <code>notebooks/parte_comum/kmeans_metricas.ipynb</code> (Passada 1 com k livre via Cotovelo, Passada 2 com k = 7, gráficos
  dos clusters, mapeamento cluster -&gt; classe majoritária, matrizes de confusão e métricas por classe) estão sob conclusão do
  integrante Arthur Borges. Após rodar os notebooks e salvar as figuras em <code>out/parte_comum/</code>, substituir este
  quadro em <code>docs/gerar_relatorio.py</code> adicionando uma página com:
  <ul>
    <li><b>6.2 EDA completa do Obesity:</b> correlações/boxplots com <code>NObeyesdad</code> e decisão sobre outliers e 24 duplicadas.</li>
    <li><b>6.3 K-Means (Passada 1 vs. Passada 2):</b> gráfico do Método do Cotovelo, justificativa de k livre e visualização dos grupos.</li>
    <li><b>6.4 Matrizes de confusão e métricas por classe:</b> mapeamento cluster -&gt; classe, matrizes retangular e 7×7, acurácia, precisão e recall (<code>zero_division=0</code>).</li>
    <li><b>6.5 Discussão crítica autoral (1,0 pt):</b> coerência entre Passada 1 e Passada 2 e análise crítica da granularidade das 7 classes originais.</li>
  </ul>
</div>

<h1>7. Limitações e Referências</h1>
<p>
  <b>Limitações principais:</b> (i) 34,8% dos pontos do <i>Pump it Up</i> não possuem ano de construção real (mecanismo MAR em
  seis regiões), exigindo imputação para modelagem e exclusão desses casos na Explanatória 2A; (ii) amostras pequenas como
  <code>wind-powered</code> (n = 59 em <code>enough</code>) exigem cautela; (iii) <code>functional needs repair</code> (7,3%)
  manteve recall de 27,00% no Random Forest, pedindo vistorias preventivas complementares; (iv) unidades de
  <code>amount_tsh</code> e <code>gps_height</code> não são detalhadas no DrivenData; e (v) ~77% da base <i>Obesity</i> é
  gerada sinteticamente via SMOTE.
</p>
<p>
  <b>Referências:</b> DrivenData, <i>Pump it Up: Data Mining the Water Table</i> (Taarifa / Ministério da Água da Tanzânia);
  UCI Machine Learning Repository, <i>Estimation of Obesity Levels</i> (id = 544); Knaflic, C. N., <i>Storytelling com Dados</i>;
  Tufte, E. R., <i>The Visual Display of Quantitative Information</i>; Slides das Aulas 01 a 26 de AVD (2026.2, Prof. Maira
  Lira, CESAR School).
</p>
""")

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9]


def gerar_pdf():
    paginas = montar_paginas()
    mediabox = pymupdf.paper_rect("a4")
    where = mediabox + (40, 36, -40, -36)
    bio = io.BytesIO()
    writer = pymupdf.DocumentWriter(bio)

    for idx, html in enumerate(paginas, start=1):
        story = pymupdf.Story(html=html, archive=str(ROOT))
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        if more:
            print(f"[AVISO] Pagina {idx} do relatorio teve conteudo excedente; verifique o layout.")
        story.draw(dev)
        writer.end_page()
    writer.close()

    doc = pymupdf.open("pdf", bio.getvalue())
    total = len(doc)
    for idx, page in enumerate(doc):
        if idx == 0:
            continue
        rodape = f"Projeto Final AVD 2026.2 (Grupo 6)  |  Página {idx + 1} de {total}"
        page.insert_text(
            (40, mediabox.height - 18),
            rodape,
            fontsize=8,
            fontname="helv",
            color=(0.43, 0.43, 0.43),
        )
    doc.save(str(DESTINO_PDF), garbage=4, deflate=True, deflate_images=True, clean=True)
    doc.close()
    print(f"Relatorio gerado com sucesso: {DESTINO_PDF} ({total} paginas, {DESTINO_PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    gerar_pdf()
