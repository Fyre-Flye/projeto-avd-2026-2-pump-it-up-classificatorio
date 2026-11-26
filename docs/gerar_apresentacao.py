"""Gera a apresentacao em PDF widescreen 16:9 (docs/APRESENTACAO_AVD_G6.pdf).

# [IA] Gemini – geracao de slides widescreen 16:9 em PDF (identidade visual Secao 2.1 de 06_GUIDELINES)
# Alinhada integralmente ao relatorio.pdf e as interpretacoes autorais da Parte Especifica,
# com espacos sinalizados para insercao dos graficos/metricas finais da Parte Comum pelo Arthur Borges.

Execucao, a partir da raiz do repositorio:
    python docs/gerar_apresentacao.py
"""

import io
from pathlib import Path
import pymupdf


ROOT = Path(__file__).resolve().parent.parent
OUT_ESP = ROOT / "out" / "parte_especifica"
OUT_COM = ROOT / "out" / "parte_comum" / "wine_quality"
DESTINO_PDF = ROOT / "docs" / "APRESENTACAO_AVD_G6.pdf"

SLIDE_W = 960.0
SLIDE_H = 540.0


CSS_BASE = """
<style>
  body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 13pt;
    color: #000000;
    line-height: 1.38;
    margin: 0;
    padding: 0;
  }
  .slide-header {
    border-bottom: 2pt solid #0F62FE;
    padding-bottom: 6pt;
    margin-bottom: 12pt;
  }
  .slide-kicker {
    font-size: 10pt;
    color: #0043CE;
    font-weight: bold;
    margin: 0 0 2pt 0;
  }
  h1 {
    font-size: 21pt;
    color: #062A5F;
    margin: 0;
    line-height: 1.18;
  }
  h2 {
    font-size: 14pt;
    color: #0F62FE;
    margin: 0 0 6pt 0;
  }
  p {
    margin: 0 0 8pt 0;
  }
  ul {
    margin: 4pt 0 6pt 18pt;
    padding: 0;
  }
  li {
    margin-bottom: 6pt;
  }
  table.layout {
    width: 100%;
    border-collapse: collapse;
    border: none;
  }
  table.layout td {
    border: none;
    vertical-align: top;
    padding: 0;
  }
  table.dados {
    width: 100%;
    border-collapse: collapse;
    font-size: 11pt;
    margin-top: 6pt;
  }
  table.dados th {
    background-color: #062A5F;
    color: #FFFFFF;
    padding: 6pt 8pt;
    text-align: left;
    border: 0.6pt solid #062A5F;
  }
  table.dados td {
    padding: 5.5pt 8pt;
    border: 0.6pt solid #E0E0E0;
  }
  table.dados tr:nth-child(even) td {
    background-color: #F4F4F4;
  }
  table.dados td.num, table.dados th.num {
    text-align: right;
  }
  .box-azul {
    background-color: #EAF2FF;
    border-left: 4pt solid #0F62FE;
    padding: 10pt 12pt;
    margin-bottom: 10pt;
  }
  .box-azul .titulo {
    color: #0043CE;
    font-weight: bold;
    font-size: 11.5pt;
    margin-bottom: 4pt;
  }
  .box-cinza {
    background-color: #F4F4F4;
    border: 0.8pt solid #E0E0E0;
    padding: 10pt 12pt;
    margin-bottom: 10pt;
  }
  .box-alerta {
    background-color: #FCF4D6;
    border-left: 4pt solid #8E6A00;
    padding: 10pt 12pt;
    margin-top: 8pt;
    font-size: 11.5pt;
  }
  .box-alerta .titulo {
    color: #8E6A00;
    font-weight: bold;
    margin-bottom: 4pt;
  }
  .kpi-num {
    font-size: 24pt;
    font-weight: bold;
    color: #062A5F;
    line-height: 1.1;
  }
  .kpi-num-laranja {
    font-size: 24pt;
    font-weight: bold;
    color: #D55E00;
    line-height: 1.1;
  }
  .kpi-num-azul {
    font-size: 24pt;
    font-weight: bold;
    color: #0F62FE;
    line-height: 1.1;
  }
  .kpi-lbl {
    font-size: 10.5pt;
    color: #525252;
    margin-top: 3pt;
  }
  .legenda {
    font-size: 9.8pt;
    color: #525252;
    margin-top: 4pt;
  }
  code {
    font-family: Courier, monospace;
    font-size: 11pt;
    background-color: #F4F4F4;
    padding: 1pt 3pt;
  }
</style>
"""


def img_rel(caminho: Path, style: str) -> str:
    if not caminho.exists():
        return '<div class="box-alerta"><div class="titulo">Imagem pendente</div>Arquivo nao encontrado: ' + caminho.name + "</div>"
    rel = caminho.relative_to(ROOT).as_posix()
    return f'<img src="{rel}" style="{style}"/>'


def montar_slides() -> list[tuple[str, str]]:
    """Retorna lista de tuplas (tipo, html). tipo in {'capa', 'conteudo'}."""
    slides: list[tuple[str, str]] = []

    # ------------------------------------------------------------------
    # SLIDE 1: CAPA (desenhada sobre fundo azul-marinho #062A5F)
    # ------------------------------------------------------------------
    s1 = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>
    <style>
      body { font-family: Helvetica, Arial, sans-serif; color: #FFFFFF; margin: 0; }
      .tag { font-size: 12pt; color: #A6C8FF; font-weight: bold; margin-bottom: 14pt; }
      h1 { font-size: 32pt; color: #FFFFFF; line-height: 1.18; margin: 0 0 14pt 0; }
      .sub { font-size: 16pt; color: #EAF2FF; line-height: 1.35; margin: 0 0 28pt 0; }
      .linha { border-top: 2pt solid #0F62FE; margin: 0 0 18pt 0; width: 120pt; }
      .meta { font-size: 12.5pt; color: #FFFFFF; line-height: 1.65; }
      .meta b { color: #A6C8FF; }
    </style></head><body>
      <div class="tag">Avaliação II (AV2) | Análise e Visualização de Dados (AVD) | Grupo 6</div>
      <h1>Agrupamento, EDA e Dashboard Interativo</h1>
      <div class="sub">
        Parte Específica: Pontos d'Água da Tanzânia (Pump it Up, DrivenData)<br/>
        Parte Comum: Qualidade de Vinhos e Agrupamento K-Means (Wine Quality, UCI 186)
      </div>
      <div class="linha"></div>
      <div class="meta">
        <b>Integrantes:</b> Gustavo Henrique Cruz de Oliveira | Arthur Borges | João Vitor do Sacramento Bezerra da Cunha<br/>
        <b>Instituição:</b> CESAR School (2026.2) | <b>Professora:</b> Maira Lira<br/>
        <b>Apresentação e Defesa:</b> 03/12/2026
      </div>
    </body></html>"""
    slides.append(("capa", s1))

    # ------------------------------------------------------------------
    # SLIDE 2: PROBLEMA, PUBLICO-ALVO E PERGUNTA DE PESQUISA
    # ------------------------------------------------------------------
    s2 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Pump it Up (Tanzânia)</div>
        <h1>Problema, Público-Alvo e Pergunta de Pesquisa</h1>
      </div>
      <div class="box-azul">
        <div class="titulo">Pergunta de Pesquisa</div>
        <p style="font-size:14.5pt; margin:0; color:#000000;">
          "Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de
          reparo ou não funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas
          com necessidade de manutenção ou inoperantes?"
        </p>
      </div>
      <table class="layout" style="margin-top:12pt;">
        <tr>
          <td style="width:52%; padding-right:16pt;">
            <h2>Público-Alvo e Contexto</h2>
            <ul>
              <li><b>Gestores do Ministério de Águas da Tanzânia</b>, responsáveis por priorizar manutenção preventiva e alocação de equipes em campo.</li>
              <li><b>Fonte:</b> DrivenData / Taarifa e Ministério da Água da Tanzânia (registros de 2011 a 2013 na base tratada).</li>
              <li><b>Alvo multiclasse (<code>status_group</code>):</b> <code>functional</code>, <code>functional needs repair</code> e <code>non functional</code>.</li>
            </ul>
          </td>
          <td style="width:48%;">
            <table class="layout">
              <tr>
                <td style="width:50%; padding:0 6pt 10pt 0;">
                  <div class="box-cinza"><div class="kpi-num">59.333</div><div class="kpi-lbl">Pontos d'água na base limpa (31 colunas)</div></div>
                </td>
                <td style="width:50%; padding:0 0 10pt 6pt;">
                  <div class="box-cinza"><div class="kpi-num-laranja">45,7%</div><div class="kpi-lbl">Inoperantes (38,4%) ou precisam de reparo (7,3%)</div></div>
                </td>
              </tr>
              <tr>
                <td style="width:50%; padding:0 6pt 0 0;">
                  <div class="box-cinza"><div class="kpi-num-azul">21</div><div class="kpi-lbl">Regiões administrativas analisadas</div></div>
                </td>
                <td style="width:50%; padding:0 0 0 6pt;">
                  <div class="box-cinza"><div class="kpi-num">80,6%</div><div class="kpi-lbl">Acurácia do Random Forest no teste (n = 11.867)</div></div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s2))

    # ------------------------------------------------------------------
    # SLIDE 3: QUALIDADE DOS DADOS, MECANISMO MAR E TRATAMENTO
    # ------------------------------------------------------------------
    s3 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: EDA e Tratamento</div>
        <h1>Ausência Concentrada em 6 Regiões (MAR) e Limpeza Sem Perda de Cobertura</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:57%; padding-right:14pt;">
            {img_rel(OUT_ESP / "02_ausencia_por_regiao.png", "width:100%; max-height:365pt;")}
            <div class="legenda">Zeros suspeitos em population (36,0%), construction_year (34,9%) e gps_height (34,4%) na base bruta (n = 59.400).</div>
          </td>
          <td style="width:43%;">
            <div class="box-azul">
              <div class="titulo">Mecanismo MAR (Aula 09)</div>
              Coocorrência de <b>0,91 a 0,93</b> entre as três colunas, concentrada em <b>88,6% a 100%</b> em 6 regiões (Dodoma, Kagera, Mbeya, Tabora, Shinyanga e Mwanza).
            </div>
            <ul>
              <li><b>Decisão:</b> não remover 1/3 da base; salvar flags <code>ausente_*</code> e aplicar imputação em cascata pela mediana (<code>lga -&gt; region -&gt; basin</code>).</li>
              <li><b>Limpeza:</b> removidas 36 duplicadas (sem <code>id</code>) e 31 linhas de 2002/2004 (todas as 9 idades negativas); 1.496 altitudes negativas no litoral ajustadas para 0.</li>
              <li><b>Resultado final:</b> <b>59.333 × 31</b>, <b>0 NaNs</b>, 0 idades/altitudes negativas.</li>
            </ul>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s3))

    # ------------------------------------------------------------------
    # SLIDE 4: EXPLORATORIA 1 E 2 (CLASSES E CATEGORICAS)
    # ------------------------------------------------------------------
    s4 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Visualizações Exploratórias (1 e 2)</div>
        <h1>Quase Metade da Rede Falha e a Disponibilidade de Água Lidera o Risco</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:43%; padding-right:10pt;">
            {img_rel(OUT_ESP / "07_expl_01_distribuicao_status.png", "width:100%; max-height:320pt;")}
            <div class="box-cinza" style="margin-top:8pt; font-size:11pt;">
              <b>Desbalanceamento:</b> <code>functional needs repair</code> soma apenas <b>7,3%</b> (4.313 pontos), exigindo Precisão, Recall e F1 por classe.
            </div>
          </td>
          <td style="width:57%;">
            {img_rel(OUT_ESP / "07_expl_02_status_por_categoria.png", "width:100%; max-height:320pt;")}
            <div class="box-cinza" style="margin-top:8pt; font-size:11pt;">
              <b>Principais sinais:</b> pontos secos (<code>dry</code>) chegam a <b>97%</b> de falha; <code>never pay</code> (42,7% da rede) tem <b>48%</b> de inoperância contra 18% no pagamento anual.
            </div>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s4))

    # ------------------------------------------------------------------
    # SLIDE 5: EXPLORATORIA 3 E 4 (REGIONAL + HEATMAP)
    # ------------------------------------------------------------------
    s5 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Visualizações Exploratórias (3 e 4)</div>
        <h1>Forte Desigualdade Territorial e Contraste Entre Água e Tecnologia</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:55%; padding-right:10pt;">
            {img_rel(OUT_ESP / "07_expl_03_contraste_regional_mapa.png", "width:100%; max-height:315pt;")}
            <div class="box-cinza" style="margin-top:8pt; font-size:11pt;">
              <b>Extremos regionais:</b> Iringa (<b>19,5%</b> inoperantes) e Arusha (<b>26,3%</b>) vs. Lindi (<b>64,2%</b>), Mtwara (<b>62,4%</b>) e Tabora (<b>54,4%</b>).
            </div>
          </td>
          <td style="width:45%;">
            {img_rel(OUT_ESP / "07_expl_04_heatmap_quantity_extraction.png", "width:100%; max-height:315pt;")}
            <div class="box-azul" style="margin-top:8pt; font-size:11pt;">
              <b>Ponte para a Explanatória:</b> na coluna <code>enough</code>, a falha muda drasticamente conforme a tecnologia de extração.
            </div>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s5))

    # ------------------------------------------------------------------
    # SLIDE 6: BIG IDEA + EXPLANATORIA 1 (TECNOLOGIA COM AGUA)
    # ------------------------------------------------------------------
    s6 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Storytelling e Visualização Explanatória 1</div>
        <h1>Mesmo com Água Suficiente, Bombas Motorizadas Falham 2,5x Mais</h1>
      </div>
      <div class="box-azul" style="padding:7pt 12pt; margin-bottom:8pt;">
        <div class="titulo" style="margin-bottom:2pt;">Big Idea</div>
        <span style="font-size:11.5pt;">Os pontos d'água da Tanzânia falham principalmente quando há escassez de água, quando são mais antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como gravidade e bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível.</span>
      </div>
      <table class="layout">
        <tr>
          <td style="width:68%; padding-right:12pt;">
            {img_rel(OUT_ESP / "08_explan_01_tecnologia_com_agua.png", "width:100%; max-height:315pt;")}
          </td>
          <td style="width:32%;">
            <h2>Destaque em <code>enough</code></h2>
            <ul style="font-size:11.5pt;">
              <li><b><code>motorpump</code>:</b> <b>45,9%</b> inoperantes (n = 1.539), +27,4 pp acima de <code>gravity</code>.</li>
              <li><b><code>gravity</code> e <code>handpump</code>:</b> apenas <b>18,4%</b> e <b>23,5%</b> de falha.</li>
              <li><b><code>other</code>:</b> <b>76,7%</b> de falha (soluções improvisadas).</li>
              <li><b>Ressalva:</b> <code>wind-powered</code> (44,1%) tem amostra pequena (n = 59).</li>
            </ul>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s6))

    # ------------------------------------------------------------------
    # SLIDE 7: EXPLANATORIA 2A (ENVELHECIMENTO DA REDE)
    # ------------------------------------------------------------------
    s7 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Visualização Explanatória 2A</div>
        <h1>A Idade da Bomba Separa o Risco: Falha Sobe de 23,9% para 60,8%</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:66%; padding-right:14pt;">
            {img_rel(OUT_ESP / "08_explan_02a_idade_vs_falha.png", "width:100%; max-height:365pt;")}
          </td>
          <td style="width:34%;">
            <div class="box-cinza">
              <div class="kpi-num-laranja">18 anos</div>
              <div class="kpi-lbl">Mediana de idade das bombas inoperantes (o dobro dos <b>9 anos</b> das funcionais)</div>
            </div>
            <ul style="font-size:12pt;">
              <li><b>Rigor metodológico:</b> apenas os <b>38.674</b> pontos com ano real informado (sem os 34,8% imputados por MAR).</li>
              <li><b>Contraste com <code>population</code>:</b> população ao redor tem mediana idêntica (150 hab.) em funcionais e quebradas.</li>
              <li><b>Ação prática:</b> priorizar vistorias preventivas em sistemas acima de 20 anos.</li>
            </ul>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s7))

    # ------------------------------------------------------------------
    # SLIDE 8: EXPLANATORIA 2B (CLASSIFICADOR)
    # ------------------------------------------------------------------
    s8 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica: Visualização Explanatória 2B (Classificador Sem Data Leakage)</div>
        <h1>Random Forest Atinge 80,6% no Teste, mas Expõe Gargalo em Reparo</h1>
      </div>
      <div style="text-align:center;">
        {img_rel(OUT_ESP / "08_explan_02b_classificador_metricas.png", "width:74%;")}
      </div>
      <table class="dados" style="margin-top:6pt; font-size:9.8pt;">
        <thead>
          <tr>
            <th style="padding:4.5pt 7pt;">Modelo (split 80/20 estratificado, teste n = 11.867)</th>
            <th class="num" style="padding:4.5pt 7pt;">Acurácia</th>
            <th class="num" style="padding:4.5pt 7pt;">Macro F1</th>
            <th class="num" style="padding:4.5pt 7pt;">Recall functional</th>
            <th class="num" style="padding:4.5pt 7pt;">Recall needs repair</th>
            <th class="num" style="padding:4.5pt 7pt;">Precisão / Recall NF</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding:4.5pt 7pt;">Árvore de Decisão (baseline auditável, <code>max_depth=15</code>)</td>
            <td class="num" style="padding:4.5pt 7pt;">75,33%</td>
            <td class="num" style="padding:4.5pt 7pt;">62,82%</td>
            <td class="num" style="padding:4.5pt 7pt;">85,28%</td>
            <td class="num" style="padding:4.5pt 7pt;">26,88%</td>
            <td class="num" style="padding:4.5pt 7pt;">77,42% / 70,45%</td>
          </tr>
          <tr>
            <td style="padding:4.5pt 7pt;"><b>Random Forest (200 árvores, Target + One-Hot no Pipeline)</b></td>
            <td class="num" style="padding:4.5pt 7pt;"><b>80,58%</b></td>
            <td class="num" style="padding:4.5pt 7pt;"><b>67,64%</b></td>
            <td class="num" style="padding:4.5pt 7pt;"><b>91,02%</b></td>
            <td class="num" style="padding:4.5pt 7pt;"><b>27,00%</b></td>
            <td class="num" style="padding:4.5pt 7pt;"><b>84,42% / 75,96%</b></td>
          </tr>
        </tbody>
      </table>
    </body></html>"""
    slides.append(("conteudo", s8))

    # ------------------------------------------------------------------
    # SLIDE 9: DEMO AO VIVO DO DASHBOARD STREAMLIT
    # ------------------------------------------------------------------
    s9 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Demonstração Ao Vivo: Streamlit + Bônus Visual/UX</div>
        <h1>Dashboard Interativo: 5 Abas Conectadas e Recursos de Apoio à Decisão</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:52%; padding-right:14pt;">
            <div class="box-azul">
              <div class="titulo">Roteiro da Demo (<code>streamlit run src/parte_especifica/dashboard.py</code>)</div>
              <ol style="margin:4pt 0 0 18pt; padding:0; font-size:12pt;">
                <li style="margin-bottom:5pt;"><b>Filtros globais + KPIs dinâmicos:</b> filtrar <code>Lindi</code> e <code>enough</code> e observar o recálculo instantâneo.</li>
                <li style="margin-bottom:5pt;"><b>Aba 2 (Exploração):</b> usar o <b>Comparador lado a lado de duas regiões</b> (Iringa vs. Lindi) e o <b>Heatmap livre de 2 variáveis</b> (pronto para arguição!).</li>
                <li style="margin-bottom:5pt;"><b>Aba 3 (Classificador):</b> sortear 3 bombas reais e abrir a trilha <code>decision_path</code> da Árvore.</li>
                <li style="margin-bottom:0;"><b>Aba 4 (Parte Comum):</b> reproduzir a <b>animação interativa Passada 1 -&gt; Passada 2</b> do K-Means em PCA 2D.</li>
              </ol>
            </div>
          </td>
          <td style="width:48%;">
            <h2>Bônus de UX/UI Aplicados</h2>
            <ul style="font-size:12pt;">
              <li>Identidade visual limpa (RecifeView + Okabe-Ito) com contraste acima de 4,5:1 e zero poluição visual.</li>
              <li>Controles nativos modernos (<code>st.pills</code>, <code>st.segmented_control</code>, <code>@st.fragment</code>) com zero reexecução desnecessária.</li>
              <li>Cache separado: <code>@st.cache_data</code> para tabelas e <code>@st.cache_resource</code> para modelos.</li>
              <li><b>Plano B offline:</b> opção de mapa sem internet e figuras estáticas prontas em <code>out/parte_especifica/</code>.</li>
            </ul>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s9))

    # ------------------------------------------------------------------
    # SLIDE 10: PARTE COMUM - DATASET WINE QUALITY, EDA E PADRONIZACAO
    # ------------------------------------------------------------------
    s10 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Wine Quality Combinado (UCI 186)</div>
        <h1>Wine Quality: Notas Concentradas em 5 e 6 e Escalas Muito Distintas</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:52%; padding-right:14pt;">
            {img_rel(OUT_COM / "distribuicao_quality.png", "width:100%;")}
            <div class="legenda">Distribuição das 7 notas reais (3 a 9) em Wine Quality (n = 6.497; 4.898 brancos e 1.599 tintos).</div>
          </td>
          <td style="width:48%;">
            <h2>Estrutura, EDA e Padronização</h2>
            <ul style="font-size:11.8pt;">
              <li><b>6.497 × 13</b> (11 físico-químicas + <code>wine_type</code> + <code>quality</code>), 0 nulos, 1.177 duplicatas (18,12%, mantidas).</li>
              <li><b>Desbalanceamento:</b> notas <b>5 (32,9%)</b> e <b>6 (43,7%)</b> somam <b>76,6%</b>; nota 9 tem só 5 vinhos.</li>
              <li><b>Relacional:</b> <code>alcohol</code> (+0,44) sobe com a nota; <code>density</code> (-0,31) e <code>volatile acidity</code> (-0,27) caem.</li>
              <li><b><code>StandardScaler</code> obrigatório:</b> sem padronizar, <code>total sulfur dioxide</code> dominaria <code>density</code> e <code>chlorides</code> na distância euclidiana. <code>quality</code> fica fora do treino.</li>
            </ul>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s10))

    # ------------------------------------------------------------------
    # SLIDE 11: PARTE COMUM - K-MEANS EM DUAS PASSADAS
    # ------------------------------------------------------------------
    s11 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Agrupamento Não Supervisionado (K-Means)</div>
        <h1>K-Means em Duas Passadas: Cotovelo (k = 3) vs. k Fixo = 7</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:33%; padding-right:8pt;">
            {img_rel(OUT_COM / "metodo_cotovelo.png", "width:100%;")}
            <div class="legenda">Cotovelo em k = 3 (-18,7% de inércia de k=2 para k=3).</div>
          </td>
          <td style="width:33.5%; padding-right:8pt;">
            {img_rel(OUT_COM / "clusters_livre.png", "width:100%;")}
            <div class="legenda">Passada 1 (k = 3, PCA 2D = 52,8% var.).</div>
          </td>
          <td style="width:33.5%;">
            {img_rel(OUT_COM / "clusters_fixo.png", "width:100%;")}
            <div class="legenda">Passada 2 (k = 7 = notas 3 a 9).</div>
          </td>
        </tr>
      </table>
      <div class="box-azul" style="margin-top:10pt; font-size:11.5pt;">
        <div class="titulo">Comparação das Passadas (Aba 4 do Dashboard anima esta transição ao vivo)</div>
        Passada 1 (<b>k = 3</b>): inércia <b>45.875,7</b>, Silhouette <b>0,252</b> e Davies-Bouldin <b>1,420</b>.
        Passada 2 (<b>k = 7</b>): inércia cai para <b>34.418,2</b>, mas Silhouette cai para <b>0,182</b> e Davies-Bouldin piora para <b>1,598</b>.
      </div>
    </body></html>"""
    slides.append(("conteudo", s11))

    # ------------------------------------------------------------------
    # SLIDE 12: PARTE COMUM - MATRIZES DE CONFUSAO E METRICAS
    # ------------------------------------------------------------------
    s12 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Avaliação dos Clusters Frente às Notas Reais</div>
        <h1>Apenas Notas 5 e 6 Dominam Clusters; Ganho de k = 7 É de +1,2 pp</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:46%; padding-right:10pt; text-align:center;">
            {img_rel(OUT_COM / "matriz_confusao_livre.png", "width:84%;")}
            <div class="legenda">Passada 1 (k = 3): coincidência 44,47% | Macro F1 13,37%.</div>
          </td>
          <td style="width:46%; text-align:center;">
            {img_rel(OUT_COM / "matriz_confusao_fixo.png", "width:84%;")}
            <div class="legenda">Passada 2 (k = 7): coincidência 45,67% | Macro F1 14,69%.</div>
          </td>
        </tr>
      </table>
      <table class="dados" style="margin-top:6pt; font-size:10pt;">
        <thead>
          <tr>
            <th>Passada</th>
            <th class="num">Coincidência</th>
            <th class="num">Macro F1</th>
            <th class="num">Nota 5 (Prec / Rec)</th>
            <th class="num">Nota 6 (Prec / Rec)</th>
            <th>Notas 3, 4, 7, 8 e 9</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Passada 1 (k = 3 livre)</td>
            <td class="num">44,47%</td>
            <td class="num">13,37%</td>
            <td class="num">42,87% / 31,90%</td>
            <td class="num">44,99% / 77,82%</td>
            <td>0,0% (<code>zero_division=0</code>)</td>
          </tr>
          <tr>
            <td><b>Passada 2 (k = 7 fixo)</b></td>
            <td class="num"><b>45,67%</b></td>
            <td class="num"><b>14,69%</b></td>
            <td class="num"><b>46,74% / 53,32%</b></td>
            <td class="num"><b>45,02% / 64,42%</b></td>
            <td>0,0% (<code>zero_division=0</code>)</td>
          </tr>
        </tbody>
      </table>
    </body></html>"""
    slides.append(("conteudo", s12))

    # ------------------------------------------------------------------
    # SLIDE 13: PARTE COMUM - DISCUSSAO CRITICA
    # ------------------------------------------------------------------
    s13 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Discussão Crítica (Wine Quality)</div>
        <h1>7 Notas Sensoriais Não Formam 7 Grupos Naturais no Espaço Químico</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:50%; padding-right:12pt;">
            <div class="box-azul">
              <div class="titulo">1. Passada 1 (k = 3) vs. Passada 2 (k = 7)</div>
              <ul style="font-size:11.8pt; margin-bottom:0;">
                <li><b>Coesão interna:</b> k = 3 entrega grupos mais limpos (Silhouette 0,252 vs. 0,182).</li>
                <li><b>Coincidência limitada:</b> passar para k = 7 eleva a taxa em só +1,20 pp (44,47% -&gt; 45,67%), pouco acima da nota 6 sozinha (43,65%).</li>
              </ul>
            </div>
          </td>
          <td style="width:50%;">
            <div class="box-cinza">
              <div class="titulo" style="font-weight:bold; color:#062A5F; margin-bottom:4pt;">2. Granularidade das 7 notas originais</div>
              <ul style="font-size:11.8pt; margin-bottom:0;">
                <li><b>Qualidade ordinal e desbalanceada:</b> notas 5 e 6 concentram 76,6% dos vinhos e têm química parecida.</li>
                <li><b>Efeito do tipo de vinho:</b> incluir <code>wine_type_red</code> puxa o agrupamento para composição (tinto vs. branco) mais do que para nota.</li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
      <div class="box-azul" style="margin-top:8pt; font-size:12pt;">
        <div class="titulo">Conclusão metodológica</div>
        K-Means descobre perfis físico-químicos naturais, mas <b>não substitui um classificador supervisionado</b> para distinguir notas sensoriais vizinhas (como 5, 6 e 7).
      </div>
    </body></html>"""
    slides.append(("conteudo", s13))

    # ------------------------------------------------------------------
    # SLIDE 14: CONCLUSAO INTEGRADA, LIMITACOES E ARGUICAO
    # ------------------------------------------------------------------
    s14 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Fechamento Integrado do Grupo 6</div>
        <h1>Conclusões, Limitações e Próximos Passos</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:53%; padding-right:14pt;">
            <h2>Principais Entregas e Respostas</h2>
            <ul style="font-size:12pt;">
              <li><b>Pump it Up:</b> escassez hídrica, envelhecimento da bomba (&gt; 20 anos) e tecnologias motorizadas concentram as falhas; o Random Forest (80,6%) apoia a triagem e a Árvore (75,3%) oferece auditoria transparente.</li>
              <li><b>Dashboard Streamlit:</b> reúne storytelling, exploração livre (inclusive de quaisquer 2 variáveis ao vivo), auditoria do classificador e transição animada do K-Means.</li>
              <li><b>Wine Quality (K-Means):</b> evidencia o papel do <code>StandardScaler</code> e por que 7 notas sensoriais desbalanceadas não viram 7 clusters puros.</li>
            </ul>
          </td>
          <td style="width:47%;">
            <div class="box-cinza">
              <h2 style="margin-bottom:4pt;">Limitações Transparentes</h2>
              <ul style="font-size:11.5pt; margin-bottom:0;">
                <li><b>MAR em 6 regiões:</b> 34,8% sem ano de construção real (excluídos da análise de idade).</li>
                <li><b>Classe minoritária:</b> recall de 27,0% em <code>functional needs repair</code> pede inspeção preventiva complementar.</li>
                <li><b>Amostras pequenas e unidades:</b> cautela com <code>wind-powered</code> (n = 59) e unidades não declaradas (<code>amount_tsh</code>, <code>gps_height</code>).</li>
                <li><b>Wine Quality:</b> 18,1% de duplicatas mantidas e influência de <code>wine_type_red</code> nos centroides.</li>
              </ul>
            </div>
            <div class="box-azul" style="margin-top:8pt; margin-bottom:0;">
              <div class="titulo">Obrigado! Abertos para perguntas e testes ao vivo no Dashboard.</div>
              Repositório GitHub: <code>projeto-avd-2026-2-pump-it-up-classificatorio</code>
            </div>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s14))

    return slides


def gerar_apresentacao():
    slides = montar_slides()
    mediabox = pymupdf.Rect(0, 0, SLIDE_W, SLIDE_H)
    bio = io.BytesIO()
    writer = pymupdf.DocumentWriter(bio)

    for idx, (tipo, html) in enumerate(slides, start=1):
        dev = writer.begin_page(mediabox)
        if tipo == "capa":
            where = pymupdf.Rect(58, 105, SLIDE_W - 58, SLIDE_H - 50)
        else:
            where = pymupdf.Rect(38, 28, SLIDE_W - 38, SLIDE_H - 36)
        story = pymupdf.Story(html=html, archive=str(ROOT))
        more, _ = story.place(where)
        if more:
            print(f"[AVISO] Slide {idx} teve conteudo excedente; verifique o layout.")
        story.draw(dev)
        writer.end_page()

    writer.close()

    # Pos-processamento vetorial: fundo marinho na capa + barra/rodape nos demais slides
    doc = pymupdf.open("pdf", bio.getvalue())
    total = len(doc)
    for idx, page in enumerate(doc):
        if idx == 0:
            # Fundo azul-marinho atras do texto da capa
            shape = page.new_shape()
            shape.draw_rect(mediabox)
            shape.finish(fill=(6 / 255, 42 / 255, 95 / 255), color=None)
            # Faixa vertical de destaque azul-principal na borda esquerda
            shape.draw_rect(pymupdf.Rect(0, 0, 14, SLIDE_H))
            shape.finish(fill=(15 / 255, 98 / 255, 254 / 255), color=None)
            shape.commit(overlay=False)
        else:
            # Linha sutil de rodape + numeracao
            shape = page.new_shape()
            shape.draw_line((38, SLIDE_H - 28), (SLIDE_W - 38, SLIDE_H - 28))
            shape.finish(color=(224 / 255, 224 / 255, 224 / 255), width=0.8)
            shape.commit(overlay=True)
            page.insert_text(
                (38, SLIDE_H - 13),
                "Projeto Final AVD 2026.2 | Grupo 6 | CESAR School",
                fontsize=8.5,
                fontname="helv",
                color=(0.43, 0.43, 0.43),
            )
            page.insert_text(
                (SLIDE_W - 88, SLIDE_H - 13),
                f"Slide {idx + 1} / {total}",
                fontsize=8.5,
                fontname="helv",
                color=(0.43, 0.43, 0.43),
            )

    doc.save(str(DESTINO_PDF), garbage=4, deflate=True, deflate_images=True, clean=True)
    doc.close()
    print(f"Apresentacao gerada com sucesso: {DESTINO_PDF} ({total} slides, {DESTINO_PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    gerar_apresentacao()
