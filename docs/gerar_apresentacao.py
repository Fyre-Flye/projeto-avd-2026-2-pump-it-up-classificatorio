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
OUT_COM = ROOT / "out" / "parte_comum"
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
        Parte Comum: Níveis de Obesidade e Agrupamento K-Means (Obesity, UCI 544)
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
    # SLIDE 10: PARTE COMUM - DATASET OBESITY, EDA E PADRONIZACAO
    # ------------------------------------------------------------------
    s10 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Obesity (UCI 544)</div>
        <h1>Dataset Obesity: 7 Classes Equilibradas e Necessidade de Padronização</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:54%; padding-right:14pt;">
            {img_rel(OUT_COM / "02_distribuicao_classes.png", "width:100%; max-height:335pt;")}
            <div class="legenda">Distribuição das 7 classes de NObeyesdad no dataset Obesity (n = 2.111, UCI id = 544).</div>
          </td>
          <td style="width:46%;">
            <h2>Estrutura e Escalas</h2>
            <ul style="font-size:12pt;">
              <li><b>2.111 registros × 17 colunas</b> (8 numéricas, 8 categóricas e classe <code>NObeyesdad</code>), 0 nulos, 24 duplicadas e ~77% sintéticos (SMOTE).</li>
              <li><b>Por que padronizar (<code>StandardScaler</code>)?</b> K-Means usa distância euclidiana. <code>Weight</code> varia de 39 a 173 kg enquanto <code>Height</code> varia de 1,45 a 1,98 m e <code>TUE</code> de 0 a 2.</li>
              <li>Sem padronização, <code>Weight</code> dominaria os centroides. A classe <code>NObeyesdad</code> fica fora do treino.</li>
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
        <h1>K-Means em Duas Passadas: Método do Cotovelo vs. k Fixo = 7</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:50%; padding-right:12pt;">
            <div class="box-azul">
              <div class="titulo">Passada 1: Escolha livre de k (2 a 10)</div>
              Curva de inércia (Método do Cotovelo) sobre as variáveis numéricas padronizadas para identificar o número natural de grupos sem olhar os rótulos.
            </div>
          </td>
          <td style="width:50%;">
            <div class="box-cinza">
              <div class="titulo" style="font-weight:bold; color:#062A5F; margin-bottom:4pt;">Passada 2: k fixo = 7 classes reais</div>
              Agrupamento forçado com k = 7 para confrontar diretamente os clusters encontrados pelo algoritmo com os 7 níveis oficiais de <code>NObeyesdad</code>.
            </div>
          </td>
        </tr>
      </table>
      <div class="box-alerta">
        <div class="titulo">INTEGRAÇÃO ARTHUR BORGES (inserir figuras de out/parte_comum/ antes da defesa)</div>
        Após concluir <code>notebooks/parte_comum/kmeans_metricas.ipynb</code>, substitua este quadro em
        <code>docs/gerar_apresentacao.py</code> pelas imagens finais do <b>Método do Cotovelo</b> e da
        <b>visualização comparativa dos clusters (Passada 1 vs. Passada 2)</b> e rode <code>python docs/gerar_apresentacao.py</code>.
        (Na demo ao vivo, a <b>Aba 4 do Dashboard Streamlit</b> já executa e anima essa transição em PCA 2D.)
      </div>
    </body></html>"""
    slides.append(("conteudo", s11))

    # ------------------------------------------------------------------
    # SLIDE 12: PARTE COMUM - MATRIZES DE CONFUSAO E METRICAS
    # ------------------------------------------------------------------
    s12 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Avaliação dos Clusters Frente às Classes Reais</div>
        <h1>Mapeamento Cluster -&gt; Classe Majoritária, Matrizes e Métricas</h1>
      </div>
      <ul style="font-size:12.5pt;">
        <li><b>Regra de avaliação:</b> cada cluster recebe o rótulo da classe <code>NObeyesdad</code> mais frequente dentro dele; em seguida calculam-se <b>matriz de confusão</b> (retangular na Passada 1, 7×7 na Passada 2), <b>acurácia de coincidência</b>, <b>precisão</b> e <b>recall</b> por classe (<code>zero_division=0</code>).</li>
        <li><b>Cuidado conceitual:</b> essa "acurácia" não mede previsão supervisionada, mas o grau de coincidência entre os grupos naturais nos dados e a rotulagem original.</li>
      </ul>
      <div class="box-alerta">
        <div class="titulo">INTEGRAÇÃO ARTHUR BORGES (inserir matrizes e tabela final de out/parte_comum/)</div>
        Inserir aqui as imagens das matrizes de confusão (Passada 1 e Passada 2) e os valores exatos de acurácia global,
        precisão e recall por classe gerados em <code>notebooks/parte_comum/kmeans_metricas.ipynb</code>, mantendo 100%
        de consistência com a Seção 6.4 do <code>relatorio.pdf</code>.
      </div>
    </body></html>"""
    slides.append(("conteudo", s12))

    # ------------------------------------------------------------------
    # SLIDE 13: PARTE COMUM - DISCUSSAO CRITICA
    # ------------------------------------------------------------------
    s13 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum: Discussão Crítica</div>
        <h1>Coerência entre Passadas e Granularidade das 7 Classes de Obesidade</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:50%; padding-right:12pt;">
            <div class="box-azul">
              <div class="titulo">1. Passada 1 (k livre) vs. Passada 2 (k = 7)</div>
              Avaliar qual escolha formou grupos mais compactos e coerentes e se forçar 7 clusters realmente separa melhor os perfis físicos e hábitos de vida.
            </div>
          </td>
          <td style="width:50%;">
            <div class="box-cinza">
              <div class="titulo" style="font-weight:bold; color:#062A5F; margin-bottom:4pt;">2. Granularidade das classes originais</div>
              Discutir se níveis contíguos de IMC (como <i>Overweight Level I</i>, <i>Overweight Level II</i> e <i>Obesity Type I</i>) formam fronteiras reais nos dados ou se sobrepõem no espaço numérico.
            </div>
          </td>
        </tr>
      </table>
      <div class="box-alerta">
        <div class="titulo">INTEGRAÇÃO ARTHUR BORGES / SACRAMENTO (conclusão autoral da Parte Comum)</div>
        Substituir este aviso por 3 bullets autorais resumindo os números exatos e a conclusão crítica escrita na
        Seção 6.5 do <code>relatorio.pdf</code> (ex.: quais classes tiveram recall 0% na Passada 1 e quais se confundiram na Passada 2).
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
              <li><b>Obesity (K-Means):</b> evidencia na prática o impacto da padronização e o limite de recuperar 7 rótulos finos sem supervisão.</li>
            </ul>
          </td>
          <td style="width:47%;">
            <div class="box-cinza">
              <h2 style="margin-bottom:4pt;">Limitações Transparentes</h2>
              <ul style="font-size:11.5pt; margin-bottom:0;">
                <li><b>MAR em 6 regiões:</b> 34,8% sem ano de construção real (excluídos da análise de idade).</li>
                <li><b>Classe minoritária:</b> recall de 27,0% em <code>functional needs repair</code> pede inspeção preventiva complementar.</li>
                <li><b>Amostras pequenas e unidades:</b> cautela com <code>wind-powered</code> (n = 59) e unidades não declaradas (<code>amount_tsh</code>, <code>gps_height</code>).</li>
                <li><b>Obesity sintético:</b> ~77% dos registros vêm de SMOTE (UCI).</li>
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
