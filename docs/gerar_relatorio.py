"""Gera o relatorio tecnico completo em PDF na raiz do repositorio (relatorio.pdf).

# [IA] Gemini – diagramacao editorial reproduzivel em PDF com tipografia Lato e identidade visual Secao 2.1 (06_GUIDELINES)
# Compila integralmente os textos autorais da Parte Especifica (Gustavo) e da Parte Comum (Arthur Borges / Sacramento).

Execucao, a partir da raiz do repositorio:
    python docs/gerar_relatorio.py
"""

import io
from pathlib import Path
import pymupdf


ROOT = Path(__file__).resolve().parent.parent
OUT_ESP = ROOT / "out" / "parte_especifica"
OUT_COM = ROOT / "out" / "parte_comum" / "wine_quality"
DESTINO_PDF = ROOT / "relatorio.pdf"
WIN_FONTS = Path(r"C:\Windows\Fonts")
TEM_LATO = (WIN_FONTS / "Lato-Regular.ttf").exists() and (WIN_FONTS / "Lato-Bold.ttf").exists()
TEM_CONSOLAS = (WIN_FONTS / "consola.ttf").exists()

FONT_FACES = ""
if TEM_LATO:
    FONT_FACES += """
  @font-face { font-family: 'Lato'; src: url('Lato-Regular.ttf'); font-weight: normal; font-style: normal; }
  @font-face { font-family: 'Lato'; src: url('Lato-Bold.ttf'); font-weight: bold; font-style: normal; }
  @font-face { font-family: 'Lato'; src: url('Lato-Italic.ttf'); font-weight: normal; font-style: italic; }
  @font-face { font-family: 'Lato'; src: url('Lato-BoldItalic.ttf'); font-weight: bold; font-style: italic; }
"""
if TEM_CONSOLAS:
    FONT_FACES += """
  @font-face { font-family: 'Consolas'; src: url('consola.ttf'); font-weight: normal; font-style: normal; }
"""

FAMILIA_SANS = "'Lato', Helvetica, Arial, sans-serif" if TEM_LATO else "Helvetica, Arial, sans-serif"
FAMILIA_MONO = "'Consolas', Courier, monospace" if TEM_CONSOLAS else "Courier, monospace"


CSS_BASE = f"""
<style>
  {FONT_FACES}
  body {{
    font-family: {FAMILIA_SANS};
    font-size: 9.2pt;
    color: #000000;
    line-height: 1.44;
    margin: 0;
  }}
  /* Cabecalho da capa (azul-marinho Secao 2.1 + badge azul-principal) */
  .capa {{
    background-color: #062A5F;
    color: #FFFFFF;
    padding: 18pt 20pt 16pt 20pt;
    border-radius: 6pt;
    margin-bottom: 10pt;
  }}
  .capa-badge-tbl {{
    width: auto;
    border-collapse: collapse;
    margin: 0 0 7pt 0;
  }}
  .capa-badge-tbl td {{
    background-color: #0F62FE;
    color: #FFFFFF;
    font-size: 7.8pt;
    font-weight: bold;
    padding: 2.5pt 8.5pt;
    border: none;
    letter-spacing: 0.3pt;
  }}
  .capa h1 {{
    font-size: 17.5pt;
    color: #FFFFFF;
    margin: 0 0 4pt 0;
    padding: 0;
    line-height: 1.2;
  }}
  .capa .sub {{
    font-size: 9.6pt;
    color: #EAF2FF;
    margin: 0;
    line-height: 1.35;
  }}
  /* Cartao de metadados estilo editorial P5G8 */
  .meta-card {{
    background-color: #EAF2FF;
    border-left: 3.5pt solid #0F62FE;
    padding: 9pt 12pt;
    margin: 0 0 11pt 0;
    font-size: 8.6pt;
    line-height: 1.46;
  }}
  .meta-card table {{
    margin: 0;
    font-size: 8.5pt;
  }}
  .meta-card td {{
    border: none;
    padding: 1pt 6pt 1pt 0;
    vertical-align: top;
  }}
  .meta-lbl {{
    color: #0043CE;
    font-weight: bold;
    font-size: 7.6pt;
    letter-spacing: 0.4pt;
    margin-bottom: 2pt;
  }}
  h1 {{
    font-size: 13pt;
    color: #0F62FE;
    margin: 10pt 0 5pt 0;
    line-height: 1.22;
  }}
  h1.topo {{
    margin-top: 0;
  }}
  h2 {{
    font-size: 10.4pt;
    color: #062A5F;
    margin: 8.5pt 0 3.5pt 0;
    line-height: 1.25;
  }}
  h3 {{
    font-size: 9.5pt;
    color: #0043CE;
    margin: 6pt 0 3pt 0;
    line-height: 1.25;
  }}
  p {{
    margin: 2pt 0 5.5pt 0;
    text-align: left;
  }}
  ul {{
    margin: 2pt 0 6pt 14pt;
    padding: 0;
  }}
  li {{
    margin-bottom: 3pt;
  }}
  /* Faixa solida de destaque (contraste 5,0:1 branco sobre #0F62FE) */
  .banner-azul {{
    background-color: #0F62FE;
    color: #FFFFFF;
    padding: 8pt 11pt;
    border-radius: 5pt;
    margin: 5pt 0 8pt 0;
    font-size: 8.9pt;
    line-height: 1.42;
  }}
  .banner-azul b {{
    color: #FFFFFF;
  }}
  .box-azul {{
    background-color: #EAF2FF;
    border-left: 3.5pt solid #0F62FE;
    padding: 7pt 10pt;
    margin: 5pt 0 7pt 0;
    font-size: 8.9pt;
    line-height: 1.42;
  }}
  .box-azul .titulo-box {{
    color: #0043CE;
    font-weight: bold;
    font-size: 8.8pt;
    margin-bottom: 2pt;
  }}
  .nota-box {{
    background-color: #F7F9FC;
    border-left: 3pt solid #062A5F;
    padding: 6pt 9pt;
    margin: 2.5pt 0 8.5pt 0;
    font-size: 8.6pt;
    line-height: 1.4;
  }}
  .nota-box b {{
    color: #062A5F;
  }}
  .legenda {{
    font-size: 7.9pt;
    color: #6F6F6F;
    text-align: center;
    margin: 2pt 0 4.5pt 0;
    line-height: 1.32;
  }}
  .img-wrap {{
    text-align: center;
    margin: 4pt 0 2pt 0;
  }}
  /* Tabelas limpas estilo editorial (cabecalho #0F62FE, linhas sutis, sem grade pesada) */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6pt 0 8pt 0;
    font-size: 8.3pt;
  }}
  th {{
    background-color: #0F62FE;
    color: #FFFFFF;
    font-weight: bold;
    padding: 5pt 6pt;
    text-align: left;
    border: none;
  }}
  td {{
    border: none;
    border-bottom: 0.6pt solid #E5ECF6;
    padding: 4.5pt 6pt;
    text-align: left;
    vertical-align: top;
  }}
  tr.destaque td {{
    background-color: #EAF2FF;
  }}
  td.chave {{
    color: #062A5F;
    font-weight: bold;
  }}
  td.num, th.num {{
    text-align: right;
  }}
  table.fig-grid {{
    margin: 3pt 0 2pt 0;
  }}
  table.fig-grid td {{
    border: none;
    padding: 2pt 3pt;
    text-align: center;
    vertical-align: middle;
  }}
  table.split-cards {{
    margin: 4pt 0 7pt 0;
  }}
  table.split-cards td {{
    border: none;
    padding: 0;
    vertical-align: top;
  }}
  code {{
    font-family: {FAMILIA_MONO};
    font-size: 8.3pt;
    color: #0043CE;
  }}
</style>
"""


def criar_archive() -> pymupdf.Archive:
    arch = pymupdf.Archive()
    arch.add(str(ROOT))
    if TEM_LATO or TEM_CONSOLAS:
        arch.add(str(WIN_FONTS))
    return arch


def img_tag(caminho: Path, style: str) -> str:
    if not caminho.exists():
        return f"<p><i>[Imagem pendente: {caminho.name}]</i></p>"
    rel = caminho.relative_to(ROOT).as_posix()
    return f'<div class="img-wrap"><img src="{rel}" style="{style}"/></div>'


def wrap_page(body_html: str) -> str:
    return f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>{body_html}</body></html>'


def montar_paginas() -> list[str]:
    """Monta 10 paginas A4 independentes com ritmo editorial limpo e zero vazamento entre paginas."""
    fig_mar_reg = img_tag(OUT_ESP / "02_ausencia_por_regiao.png", "width:82%;")
    fig_expl_1 = img_tag(OUT_ESP / "07_expl_01_distribuicao_status.png", "width:54%;")
    fig_expl_2 = img_tag(OUT_ESP / "07_expl_02_status_por_categoria.png", "width:80%;")
    fig_expl_3 = img_tag(OUT_ESP / "07_expl_03_contraste_regional_mapa.png", "width:95%;")
    fig_expl_4 = img_tag(OUT_ESP / "07_expl_04_heatmap_quantity_extraction.png", "width:76%;")
    fig_explan_1 = img_tag(OUT_ESP / "08_explan_01_tecnologia_com_agua.png", "width:72%;")
    fig_explan_2a = img_tag(OUT_ESP / "08_explan_02a_idade_vs_falha.png", "width:70%;")
    fig_explan_2b = img_tag(OUT_ESP / "08_explan_02b_classificador_metricas.png", "width:96%;")
    fig_cm_clf = img_tag(OUT_ESP / "06_matriz_confusao_modelos.png", "width:92%;")

    # ------------------------------------------------------------------
    # PAGINA 1: CAPA EDITORIAL + SECAO 1 + SECAO 2
    # ------------------------------------------------------------------
    p1 = wrap_page("""
<div class="capa">
  <table class="capa-badge-tbl"><tr><td>AV2 · GRUPO 06 · CESAR SCHOOL 2026.2</td></tr></table>
  <h1>Relatório Técnico: Agrupamento, EDA e Dashboard Interativo</h1>
  <div class="sub">Análise e Visualização de Dados (AVD) · Parte Específica (Pump it Up) e Parte Comum (Wine Quality, UCI 186)</div>
</div>

<div class="meta-card">
  <table>
    <tr>
      <td style="width:58%; padding-right:10pt;">
        <div class="meta-lbl">EQUIPE E ESCOPO</div>
        <b>Parte Específica (Pump it Up):</b> Gustavo Henrique Cruz de Oliveira<br/>
        <b>Parte Comum (Wine Quality, UCI 186):</b> Arthur de Assis Borges; João Vitor do Sacramento Bezerra da Cunha
      </td>
      <td style="width:42%;">
        <div class="meta-lbl">INFORMAÇÕES DA ENTREGA</div>
        <b>Professora:</b> Maira Lira (CESAR School)<br/>
        <b>Entrega:</b> 26/11/2026 · <b>Defesa:</b> 03/12/2026
      </td>
    </tr>
  </table>
</div>

<h1>1. Resumo Executivo</h1>
<div class="banner-azul">
  <b>Síntese em uma frase:</b> na Tanzânia (59.333 pontos d'água), quase metade da rede está inoperante (38,4%) ou requer
  reparo (7,3%), com falhas concentradas na escassez hídrica, no envelhecimento acima de 20 anos e em bombas motorizadas mesmo
  onde há água suficiente; em <i>Wine Quality</i> (6.497 vinhos), o K-Means evidencia que 7 notas sensoriais desbalanceadas não
  formam 7 agrupamentos naturais isolados.
</div>
<p>
  Este relatório documenta a análise técnica do Grupo 6 em duas frentes complementares. A <b>Parte Específica</b> cobre EDA,
  tratamento de ausência MAR, storytelling, modelagem preditiva sem <i>data leakage</i> e dashboard interativo em Streamlit
  sobre o dataset <i>Pump it Up</i> (DrivenData/Taarifa, 59.400 registros brutos e 59.333 tratados entre 2011 e 2013). A
  <b>Parte Comum</b> aplica EDA nos quatro pilares, padronização com <code>StandardScaler</code> e K-Means em duas passadas
  (<code>k = 3</code> livre vs. <code>k = 7</code> fixo) sobre o dataset <i>Wine Quality</i> combinado (UCI 186, 6.497
  amostras em 7 notas de 3 a 9).
</p>
<p>
  Na Parte Específica, mesmo quando há água suficiente (<code>quantity = enough</code>), bombas motorizadas
  (<code>motorpump</code>, 45,9% inoperantes) falham 2,5 vezes mais que sistemas por gravidade (<code>gravity</code>, 18,4%),
  e a inoperância sobe de 23,9% (0 a 5 anos) para 60,8% acima de 30 anos. O classificador <code>RandomForestClassifier</code>
  alcançou <b>80,58% de acurácia</b> no teste (n = 11.867), superando a Árvore de Decisão baseline (75,33%) e expondo o gargalo
  operacional na classe minoritária <code>functional needs repair</code> (precisão de 65,82%, recall de 27,00%).
</p>

<h1>2. Parte Específica: Pergunta de Pesquisa, Público-Alvo e Dados</h1>
<table class="split-cards">
  <tr>
    <td style="width:45%; padding-right:8pt;">
      <div class="box-azul" style="margin:0;">
        <div class="titulo-box">Público-alvo definido</div>
        Gestores públicos do Ministério de Águas da Tanzânia, interessados em priorizar manutenção preventiva, alocar equipes
        em campo e identificar bombas quebradas ou com necessidade de reparo.
      </div>
    </td>
    <td style="width:55%;">
      <div class="box-azul" style="margin:0;">
        <div class="titulo-box">Pergunta de pesquisa</div>
        "Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de reparo ou não
        funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas com necessidade de
        manutenção ou inoperantes?"
      </div>
    </td>
  </tr>
</table>

<h2>2.1 Origem e estrutura do dataset</h2>
<p>
  A base provém da competição <i>Pump it Up: Data Mining the Water Table</i> (DrivenData), reunindo vistorias da plataforma
  Taarifa e do Ministério da Água da Tanzânia. O arquivo bruto (<code>data/parte_especifica/raw/pump_it_up_train.csv</code>)
  possui <b>59.400 linhas e 41 colunas</b> (40 atributos explicativos e o alvo multiclasse <code>status_group</code>),
  combinando variáveis quantitativas e qualitativas de baixa e alta cardinalidade. As definições completas de colunas constam
  em <code>docs/GLOSSARIO.md</code>; colunas sem documentação oficial (como <code>num_private</code>) foram descartadas na
  etapa de limpeza.
</p>
""")

    # ------------------------------------------------------------------
    # PAGINA 2: SECAO 3.1 + 3.2 (MAR + FIGURA 1)
    # ------------------------------------------------------------------
    p2 = wrap_page(f"""
<h1 class="topo">3. Parte Específica: EDA, Qualidade dos Dados e Tratamento</h1>
<h2>3.1 Análise estrutural e cardinalidade</h2>
<p>
  Não foram encontrados identificadores (<code>id</code>) repetidos nem linhas inteiramente idênticas nas 41 colunas, mas a
  verificação ignorando <code>id</code> revelou <b>36 registros duplicados</b> nas demais 40 colunas, removidos no tratamento.
  A auditoria estrutural também identificou colunas irrelevantes ou inconsistentes: <code>recorded_by</code> assume valor único
  (<code>GeoData Consultants Ltd</code>) em 100% da base; <code>region_code</code> diverge de <code>region</code> (sete
  regiões aparecem com mais de um código); e sete famílias repetem a mesma informação em níveis diferentes de detalhe (como
  <code>extraction_type</code>, <code>extraction_type_group</code> e <code>extraction_type_class</code>).
</p>
<p>
  Nas nominais de alta cardinalidade (<code>wpt_name</code> com 37.400 categorias, <code>subvillage</code> com 19.287,
  <code>installer</code> com 2.145 e <code>funder</code> com 1.897), normalizar texto com <code>strip().lower()</code> reduziu
  duplicidades em <code>installer</code> (2.145 para 1.935) e <code>scheme_name</code> (2.695 para 2.576). Para evitar explosão
  dimensional no One-Hot Encoding, descartaram-se identificadores quase únicos (<code>wpt_name</code>, <code>subvillage</code>)
  e aplicou-se <b>Target Encoding</b> às quatro nominais de alta cardinalidade mantidas (<code>lga</code>, <code>ward</code>,
  <code>funder</code> e <code>installer</code>) dentro de um <code>Pipeline</code> ajustado exclusivamente no treino.
</p>

<h2>3.2 Dados ausentes, mecanismo MAR e imputação em cascata</h2>
<p>
  Além dos valores <code>NaN</code> explícitos (<code>scheme_name</code> 48,5%, <code>scheme_management</code> 6,5%,
  <code>installer</code> 6,2%, <code>funder</code> 6,1%, <code>public_meeting</code> 5,6% e <code>permit</code> 5,1%), a
  inspeção de domínio detectou zeros estruturais que escondem ausência real: <code>population</code> (36,0%),
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
<div class="legenda">Figura 1: Percentual de ausência (NaN e zeros suspeitos) por região na base bruta (n = 59.400), evidenciando o mecanismo MAR em 6 regiões. Fonte: DrivenData/Taarifa (2002 a 2013).</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 3: IMPUTACAO + 3.3 + TABELA 1 + 4.1 STORYTELLING
    # ------------------------------------------------------------------
    p3 = wrap_page("""
<p style="margin-top:0;">
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
  2004 e concentravam todas as 9 inconsistências de idade negativa (<code>construction_year &gt; ano_registro</code>), sendo
  descartados. Os 1.496 registros com altitude negativa (<code>gps_height &lt; 0</code>, mediana de -18 m e mínimo de -90 m)
  concentram-se nas cinco regiões litorâneas (Pwani, Mtwara, Lindi, Dar es Salaam e Tanga), indicando erro vertical de GPS
  próximo ao nível do mar; eles foram corrigidos para <code>0</code> após a imputação dos zeros originais, sem perda de
  linhas. Outliers positivos de <code>amount_tsh</code> (18,8% IQR, máx. 350.000) e <code>population</code> (7,4% IQR, máx.
  30.500) foram mantidos por serem plausíveis no domínio e não prejudicarem modelos baseados em árvores.
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
    <tr><td class="chave">Linhas</td><td class="num">59.400</td><td class="num">59.333</td><td>Remoção de 36 duplicadas (sem id) e 31 registros de 2002/2004</td></tr>
    <tr><td class="chave">Colunas</td><td class="num">41</td><td class="num">31</td><td>Descarte de 16 redundantes/irrelevantes; adição de flags e derivadas</td></tr>
    <tr><td class="chave">NaN explícitos</td><td class="num">46.743</td><td class="num">0</td><td>Categóricas preenchidas com "desconhecido"</td></tr>
    <tr><td class="chave">Zeros suspeitos (pop / year / gps / lon)</td><td class="num">64.340</td><td class="num">0</td><td>Flags ausente_* salvas + imputação em cascata (lga -&gt; region -&gt; basin)</td></tr>
    <tr><td class="chave">Idades negativas (construction_year &gt; ano)</td><td class="num">9</td><td class="num">0</td><td>Eliminadas no recorte temporal de 2011 a 2013</td></tr>
    <tr><td class="chave">Altitudes negativas (gps_height &lt; 0)</td><td class="num">1.496</td><td class="num">0</td><td>Ajustadas para 0 (litoral) após imputação dos zeros originais</td></tr>
  </tbody>
</table>

<h1>4. Parte Específica: Storytelling e Visualizações</h1>
<h2>4.1 Raciocínio do Storytelling (da Exploratória à Explanatória)</h2>
<p>
  <b>Público-alvo e linguagem:</b> voltado a gestores do Ministério de Águas da Tanzânia, o storytelling traduz os achados em
  linguagem direta, com percentuais em pt-BR, rótulos diretos e paleta acessível a daltonismo (Okabe-Ito: azul
  <code>#0072B2</code> para funcional, amarelo <code>#E69F00</code> para precisa de reparo e laranja <code>#D55E00</code> para
  não funcional; azul de marca <code>#0F62FE</code> apenas em gráficos sem <code>status_group</code>).
</p>
<p>
  <b>O que nasceu da exploração:</b> a falha de uma bomba não se limita à seca da fonte. Mesmo quando há água suficiente
  (<code>quantity = enough</code>), sistemas motorizados falham muito mais que soluções mecânicas simples; além disso, a
  inoperância cresce continuamente com a idade e varia fortemente entre regiões. A modelagem supervisionada confirmou esses
  sinais e expôs o principal gargalo operacional na detecção da classe minoritária <code>functional needs repair</code>.
</p>
<div class="banner-azul">
  <b>Big Idea (Sujeito + Verbo + Ponto de Vista, Aula 06):</b> Os pontos d'água da Tanzânia falham principalmente quando há
  escassez de água, quando são mais antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como
  gravidade e bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível.
</div>
<p>
  <b>Atributos pré-atentivos aplicados:</b> <b>cor por exceção</b> (contexto em cinza <code>#C6C6C6</code> contra destaque em
  laranja <code>#D55E00</code> nos grupos críticos e azul <code>#0F62FE</code> nos atributos-chave), <b>posição em eixo
  comum</b> com ordenação explícita por taxa ou cronologia, e <b>anotações diretas</b> com linhas de referência.
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
  Em <code>src/parte_especifica/classificador.ipynb</code>, os valores imputados no CSV limpo foram revertidos para
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
    <tr><td>Árvore de Decisão (baseline)</td><td>functional needs repair</td><td class="num">75,33</td><td class="num">47,35</td><td class="num">26,88</td><td class="num">34,29</td><td class="num">863</td></tr>
    <tr><td>Árvore de Decisão (baseline)</td><td>non functional</td><td class="num">75,33</td><td class="num">77,42</td><td class="num">70,45</td><td class="num">73,77</td><td class="num">4.559</td></tr>
    <tr class="destaque"><td class="chave">Árvore de Decisão (baseline)</td><td class="chave">Média Macro (3 classes)</td><td class="num"><b>75,33</b></td><td class="num"><b>66,93</b></td><td class="num"><b>60,87</b></td><td class="num"><b>62,82</b></td><td class="num"><b>11.867</b></td></tr>
    <tr><td>Random Forest (200 árvores)</td><td>functional</td><td class="num">80,58</td><td class="num">79,15</td><td class="num">91,02</td><td class="num">84,67</td><td class="num">6.445</td></tr>
    <tr><td>Random Forest (200 árvores)</td><td>functional needs repair</td><td class="num">80,58</td><td class="num">65,82</td><td class="num">27,00</td><td class="num">38,29</td><td class="num">863</td></tr>
    <tr><td>Random Forest (200 árvores)</td><td>non functional</td><td class="num">80,58</td><td class="num">84,42</td><td class="num">75,96</td><td class="num">79,97</td><td class="num">4.559</td></tr>
    <tr class="destaque"><td class="chave">Random Forest (200 árvores)</td><td class="chave">Média Macro (3 classes)</td><td class="num"><b>80,58</b></td><td class="num"><b>76,46</b></td><td class="num"><b>64,66</b></td><td class="num"><b>67,64</b></td><td class="num"><b>11.867</b></td></tr>
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
  <code>.streamlit/config.toml</code>) adota a identidade visual limpa do projeto (azul-marinho <code>#062A5F</code>, azul
  principal <code>#0F62FE</code>, destaque claro <code>#EAF2FF</code> e paleta Okabe-Ito para <code>status_group</code>) e
  organiza toda a experiência em cinco abas interligadas pelos filtros globais da barra lateral:
</p>
<table>
  <thead>
    <tr>
      <th style="width:24%;">Aba do Dashboard</th>
      <th>Recursos principais e apoio à decisão</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="chave">1. Storytelling e Insights</td><td>Apresenta a Big Idea em destaque e as três visualizações explanatórias interativas com notas analíticas expansíveis.</td></tr>
    <tr><td class="chave">2. Exploração Interativa</td><td>Quatro exploratórias, seletor livre das 12 categóricas, <b>heatmap livre de 2 variáveis</b> (pronto para arguição), mapa Carto Positron com opção offline, <b>Comparador lado a lado de 2 regiões</b> e diagnóstico MAR.</td></tr>
    <tr><td class="chave">3. Classificador e Auditoria</td><td>Matrizes de confusão e métricas, sorteio de 3 bombas reais do teste (Cartões ou Tabela), mapa e probabilidades previstas, <b>trilha passo a passo <code>decision_path</code></b> da Árvore e simulador via <code>st.form</code>.</td></tr>
    <tr><td class="chave">4. K-Means Wine Quality</td><td>Ajuste do <code>k</code> livre da Passada 1 (padrão 3), curva do Cotovelo e <b>animação interativa da transição Passada 1 para Passada 2 em PCA 2D</b>, junto às matrizes de confusão e métricas por nota.</td></tr>
    <tr><td class="chave">5. Glossário e Exportação</td><td>Glossário pesquisável de colunas e download direto do recorte filtrado em CSV e do resumo executivo em Markdown.</td></tr>
  </tbody>
</table>
<div class="box-azul">
  <div class="titulo-box">Boas práticas de UX/UI e desempenho aplicadas</div>
  Uso de controles nativos modernos do Streamlit (<code>st.pills</code>, <code>st.segmented_control</code>,
  <code>st.container(border=True)</code> e <code>@st.fragment</code> para isolamento de reexecuções), barra de resumo dos
  filtros ativos com botão de limpeza rápida e contraste superior a 4,5:1 em todos os textos.
</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 9: SECAO 6 (PARTE COMUM - WINE QUALITY: EDA, PADRONIZACAO E PASSADAS)
    # ------------------------------------------------------------------
    p9 = wrap_page("""
<h1 class="topo">6. Parte Comum: EDA e Agrupamento K-Means (Wine Quality, UCI 186)</h1>
<h2>6.1 Estrutura, qualidade dos dados e principais achados da EDA</h2>
<p>
  A Parte Comum analisa a base combinada <b>Wine Quality</b> (Cortez et al., 2009; UCI id = 186;
  <code>data/parte_comum/wine_quality/winequality-combined.csv</code>), com <b>6.497 amostras e 13 colunas</b>: 11 atributos
  físico-químicos numéricos, o tipo de vinho (<code>wine_type</code>: 4.898 brancos, 75,39%; 1.599 tintos, 24,61%) e a
  variável de classe ordinal <code>quality</code>, com <b>7 notas reais (3 a 9)</b>. Não há valores nulos; os 151 zeros em
  <code>citric acid</code> são medições válidas. Foram identificadas <b>1.177 duplicatas completas</b> (18,12%; 240 tintos e
  937 brancos), mantidas junto aos valores sinalizados pelo critério IQR (maior incidência global em <code>citric acid</code>
  com 7,83%, <code>volatile acidity</code> com 5,80% e <code>fixed acidity</code> com 5,49%) por ausência de identificador
  individual que comprove repetição indevida.
</p>
<p>
  As notas concentram-se fortemente no centro: <b>notas 5 (32,91%) e 6 (43,65%) somam 76,56%</b> da base, enquanto os extremos
  são raros (30 vinhos na nota 3 e apenas 5 na nota 9). Na análise relacional, o teor alcoólico é o atributo mais associado
  positivamente à qualidade (Pearson +0,44; Spearman +0,45; mediana sobe de 9,60 na nota 5 para 10,50 na nota 6 e 11,40 na
  nota 7), enquanto <code>density</code> (-0,31), <code>volatile acidity</code> (-0,27) e <code>chlorides</code> (-0,20) têm
  associação negativa; destacam-se ainda <code>free</code> × <code>total sulfur dioxide</code> (+0,72) e <code>density</code> ×
  <code>alcohol</code> (-0,69).
</p>

<h2>6.2 Por que padronizar antes do K-Means (Aula 14)</h2>
<p>
  O K-Means agrupa observações pela distância euclidiana até os centroides. Como os 11 atributos físico-químicos têm escalas
  muito distintas (<code>total sulfur dioxide</code> atinge centenas de mg/dm³, enquanto <code>density</code> varia em torno
  de 0,99 a 1,00 e <code>chlorides</code> em milésimos), rodar o algoritmo sem padronização faria variáveis de grande amplitude
  dominarem o agrupamento. Aplicou-se <code>StandardScaler</code> (média 0 e desvio padrão 1) às 11 variáveis numéricas e ao
  indicador binário <code>wine_type_red</code>, mantendo <code>quality</code> estritamente fora do treino.
</p>

<table class="fig-grid">
  <tr>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/distribuicao_quality.png" style="width:98%;"/></td>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/metodo_cotovelo.png" style="width:98%;"/></td>
  </tr>
</table>
<div class="legenda">Figura 10: Distribuição das 7 notas reais de quality (esq.) e curva de inércia do Método do Cotovelo para k = 2 a 10 (dir., n = 6.497).</div>

<h2>6.3 K-Means em duas passadas: Passada 1 (k = 3 livre) vs. Passada 2 (k = 7 fixo)</h2>
<p>
  Na curva do Método do Cotovelo (Figura 10), a maior redução relativa de inércia ocorre de k = 2 (56.403,48) para k = 3
  (45.875,74; queda de 18,67%), suavizando a partir de k = 4 (10,21%, 6,60% e 5,50%). Adotou-se <b>k = 3 na Passada 1</b>
  (Silhouette 0,2523; Davies-Bouldin 1,4196) e <b>k = 7 na Passada 2</b> (= 7 notas reais; inércia 34.418,18; Silhouette
  0,1822; Davies-Bouldin 1,5977). A Figura 11 projeta os grupos em PCA 2D (PC1 = 31,74% e PC2 = 21,07%, somando 52,82% da
  variância).
</p>

<table class="fig-grid">
  <tr>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/clusters_livre.png" style="width:98%;"/></td>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/clusters_fixo.png" style="width:98%;"/></td>
  </tr>
</table>
<div class="legenda">Figura 11: Projeção PCA 2D dos clusters e centroides do K-Means na Passada 1 (k = 3, esq.) e na Passada 2 (k = 7, dir.).</div>
""")

    # ------------------------------------------------------------------
    # PAGINA 10: SECAO 6.4 + 6.5 (MATRIZES, METRICAS, DISCUSSAO) + SECAO 7
    # ------------------------------------------------------------------
    p10 = wrap_page("""
<h2 style="margin-top:0;">6.4 Mapeamento cluster -&gt; nota majoritária, matrizes de confusão e métricas</h2>
<p>
  Cada cluster foi associado à nota real de <code>quality</code> mais frequente em seu interior. Na <b>Passada 1 (k = 3)</b>,
  os clusters 0 e 1 mapearam para a nota 6 e o cluster 2 para a nota 5. Na <b>Passada 2 (k = 7)</b>, os clusters 0, 1 e 5
  mapearam para a nota 5 e os clusters 2, 3, 4 e 6 para a nota 6. Em ambas as passadas, <b>apenas as notas 5 e 6</b> aparecem
  como classe majoritária; as notas 3, 4, 7, 8 e 9 não lideram nenhum cluster e recebem precisão e recall de 0,0%
  (<code>zero_division=0</code>).
</p>

<table class="fig-grid">
  <tr>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/matriz_confusao_livre.png" style="width:94%;"/></td>
    <td style="width:50%;"><img src="out/parte_comum/wine_quality/matriz_confusao_fixo.png" style="width:94%;"/></td>
  </tr>
</table>
<div class="legenda">Figura 12: Matrizes de confusão entre nota real e nota mapeada na Passada 1 (k = 3, esq.) e na Passada 2 (k = 7, dir., n = 6.497).</div>

<table>
  <thead>
    <tr>
      <th>Passada</th>
      <th class="num">k</th>
      <th class="num">Inércia</th>
      <th class="num">Coincidência</th>
      <th class="num">Macro F1</th>
      <th class="num">Nota 5 (Prec / Rec)</th>
      <th class="num">Nota 6 (Prec / Rec)</th>
      <th>Notas 3, 4, 7, 8 e 9</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="chave">Passada 1 (k livre)</td>
      <td class="num">3</td>
      <td class="num">45.875,74</td>
      <td class="num">44,47%</td>
      <td class="num">13,37%</td>
      <td class="num">42,87% / 31,90%</td>
      <td class="num">44,99% / 77,82%</td>
      <td>0,0% (sem cluster)</td>
    </tr>
    <tr class="destaque">
      <td class="chave">Passada 2 (k fixo)</td>
      <td class="num"><b>7</b></td>
      <td class="num"><b>34.418,18</b></td>
      <td class="num"><b>45,67%</b></td>
      <td class="num"><b>14,69%</b></td>
      <td class="num"><b>46,74% / 53,32%</b></td>
      <td class="num"><b>45,02% / 64,42%</b></td>
      <td>0,0% (sem cluster)</td>
    </tr>
  </tbody>
</table>

<h2>6.5 Discussão crítica (Passada 1 vs. Passada 2 e granularidade das 7 notas)</h2>
<div class="box-azul">
  <div class="titulo-box">Síntese crítica da Parte Comum</div>
  A Passada 1 (k = 3) apresenta melhor coesão interna (Silhouette 0,2523 vs. 0,1822 em k = 7), enquanto a Passada 2 (k = 7)
  eleva a coincidência global em apenas +1,20 ponto percentual (de 44,47% para 45,67%, pouco acima da frequência da classe
  majoritária 6 sozinha, que já soma 43,65% da base). As sete notas não correspondem a sete agrupamentos naturais isolados:
  a qualidade sensorial é ordinal e fortemente desbalanceada, e amostras com notas vizinhas (5, 6 e 7) possuem composições
  físico-químicas muito próximas. Além disso, incluir <code>wine_type_red</code> favorece a separação por tipo de vinho
  (tinto vs. branco) em vez de qualidade. Logo, o K-Means revela perfis físico-químicos, mas não substitui um classificador
  supervisionado para prever notas sensoriais finas.
</div>

<h1>7. Limitações e Referências</h1>
<p>
  <b>Limitações principais:</b> (i) 34,8% dos pontos do <i>Pump it Up</i> não possuem ano de construção real (mecanismo MAR em
  seis regiões), exigindo imputação para modelagem e exclusão desses casos na Explanatória 2A; (ii) amostras pequenas como
  <code>wind-powered</code> (n = 59 em <code>enough</code>) exigem cautela; (iii) <code>functional needs repair</code> (7,3%)
  manteve recall de 27,00% no Random Forest, pedindo vistorias preventivas complementares; (iv) unidades de
  <code>amount_tsh</code> e <code>gps_height</code> não são detalhadas no DrivenData; e (v) em <i>Wine Quality</i>, 18,12%
  das linhas são duplicatas completas mantidas por falta de identificador e a inclusão de <code>wine_type_red</code> influencia
  os centroides do K-Means.
</p>
<p>
  <b>Referências:</b> DrivenData, <i>Pump it Up: Data Mining the Water Table</i> (Taarifa / Ministério da Água da Tanzânia);
  Cortez et al. (2009), <i>Modeling wine preferences by data mining from physicochemical properties</i> (UCI id = 186);
  Knaflic, C. N., <i>Storytelling com Dados</i>; Tufte, E. R., <i>The Visual Display of Quantitative Information</i>; Slides
  das Aulas 01 a 26 de AVD (2026.2, Prof. Maira Lira, CESAR School).
</p>
""")

    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


def gerar_pdf():
    paginas = montar_paginas()
    arch = criar_archive()
    mediabox = pymupdf.paper_rect("a4")
    where_p1 = mediabox + (42, 32, -42, -36)
    where_int = mediabox + (42, 46, -42, -36)

    bio = io.BytesIO()
    writer = pymupdf.DocumentWriter(bio)

    for idx, html in enumerate(paginas, start=1):
        story = pymupdf.Story(html=html, archive=arch)
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where_p1 if idx == 1 else where_int)
        if more:
            print(f"[AVISO] Pagina {idx} do relatorio teve conteudo excedente; verifique o layout.")
        story.draw(dev)
        writer.end_page()
    writer.close()

    # Cabecalho discreto (pags 2..N) e rodape editorial com numeracao azul estilo P5G8
    doc = pymupdf.open("pdf", bio.getvalue())
    total = len(doc)
    font_reg = str(WIN_FONTS / "Lato-Regular.ttf") if TEM_LATO else None
    font_bold = str(WIN_FONTS / "Lato-Bold.ttf") if TEM_LATO else None

    for idx, page in enumerate(doc):
        if TEM_LATO:
            page.insert_font(fontname="lato_r", fontfile=font_reg)
            page.insert_font(fontname="lato_b", fontfile=font_bold)
            fn_r, fn_b = "lato_r", "lato_b"
        else:
            fn_r, fn_b = "helv", "hebo"

        if idx > 0:
            # Cabecalho discreto estilo N6 P5G8 com alinhamento exato na margem direita
            page.insert_text(
                (42, 26),
                "AVD · Grupo 6",
                fontsize=9.0,
                fontname=fn_b,
                color=(15 / 255, 98 / 255, 254 / 255),
            )
            hdr_dir = "Relatório Técnico · Pump it Up & Wine Quality"
            w_hdr = pymupdf.get_text_length(hdr_dir, fontname="helv", fontsize=7.8) if not TEM_LATO else pymupdf.Font(fontfile=font_reg).text_length(hdr_dir, fontsize=7.8)
            page.insert_text(
                (mediabox.width - 42 - w_hdr, 26),
                hdr_dir,
                fontsize=7.8,
                fontname=fn_r,
                color=(111 / 255, 111 / 255, 111 / 255),
            )
            sh = page.new_shape()
            sh.draw_line((42, 33), (mediabox.width - 42, 33))
            sh.finish(color=(229 / 255, 236 / 255, 246 / 255), width=0.7)
            sh.commit(overlay=True)

        # Rodape limpo com numero de pagina azul em negrito alinhado a margem direita
        page.insert_text(
            (42, mediabox.height - 17),
            "CESAR School · 2026.2 · Análise e Visualização de Dados (AVD)",
            fontsize=7.6,
            fontname=fn_r,
            color=(111 / 255, 111 / 255, 111 / 255),
        )
        num_txt = f"{idx + 1}"
        w_num = pymupdf.get_text_length(num_txt, fontname="hebo", fontsize=8.2) if not TEM_LATO else pymupdf.Font(fontfile=font_bold).text_length(num_txt, fontsize=8.2)
        page.insert_text(
            (mediabox.width - 42 - w_num, mediabox.height - 17),
            num_txt,
            fontsize=8.2,
            fontname=fn_b,
            color=(15 / 255, 98 / 255, 254 / 255),
        )

    doc.save(str(DESTINO_PDF), garbage=4, deflate=True, deflate_images=True, clean=True)
    doc.close()
    print(f"Relatorio gerado com sucesso: {DESTINO_PDF} ({total} paginas, {DESTINO_PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    gerar_pdf()
