"""Gera a apresentacao em PDF widescreen 16:9 (docs/APRESENTACAO_AVD_G6.pdf).

# [IA] Gemini / Claude Code – script auxiliar de diagramacao editorial offline em PDF 16:9 (tipografia Montserrat e identidade visual Secao 2.1)
# Alinhada integralmente ao relatorio.pdf, a Parte Especifica (Pump it Up) e a Parte Comum (Wine Quality, UCI 186).

Execucao, a partir da raiz do repositorio:
    python docs/gerar_apresentacao.py
"""

import io
from pathlib import Path
# Biblioteca auxiliar usada apenas para diagramacao offline HTML -> PDF (nao usada na analise nem no dashboard).
import pymupdf


ROOT = Path(__file__).resolve().parent.parent
OUT_ESP = ROOT / "out" / "parte_especifica"
OUT_COM = ROOT / "out" / "parte_comum" / "wine_quality"
DESTINO_PDF = ROOT / "docs" / "APRESENTACAO_AVD_G6.pdf"
WIN_FONTS = Path(r"C:\Windows\Fonts")
DIR_FONTES = ROOT / "src" / "parte_especifica" / "static" / "fonts"
TEM_MONTSERRAT = all((DIR_FONTES / f"Montserrat-{p}.ttf").exists() for p in ("Regular", "Bold", "SemiBold", "Italic"))
TEM_CONSOLAS = (WIN_FONTS / "consola.ttf").exists()

SLIDE_W = 960.0
SLIDE_H = 540.0
MARGEM_X = 46.0
AZUL = (15 / 255, 98 / 255, 254 / 255)
CINZA_NOTA = (111 / 255, 111 / 255, 111 / 255)

FONT_FACES = ""
if TEM_MONTSERRAT:
    FONT_FACES += """
  @font-face { font-family: 'Montserrat'; src: url('src/parte_especifica/static/fonts/Montserrat-Regular.ttf'); font-weight: normal; font-style: normal; }
  @font-face { font-family: 'Montserrat'; src: url('src/parte_especifica/static/fonts/Montserrat-Bold.ttf'); font-weight: bold; font-style: normal; }
  @font-face { font-family: 'Montserrat'; src: url('src/parte_especifica/static/fonts/Montserrat-Italic.ttf'); font-weight: normal; font-style: italic; }
  @font-face { font-family: 'MontserratSB'; src: url('src/parte_especifica/static/fonts/Montserrat-SemiBold.ttf'); font-weight: normal; font-style: normal; }
  @font-face { font-family: 'MontserratSB'; src: url('src/parte_especifica/static/fonts/Montserrat-Bold.ttf'); font-weight: bold; font-style: normal; }
"""
if TEM_CONSOLAS:
    FONT_FACES += """
  @font-face { font-family: 'Consolas'; src: url('consola.ttf'); font-weight: normal; font-style: normal; }
"""

FAMILIA_SANS = "'Montserrat', Helvetica, Arial, sans-serif" if TEM_MONTSERRAT else "Helvetica, Arial, sans-serif"
FAMILIA_SB = "'MontserratSB', Helvetica, Arial, sans-serif" if TEM_MONTSERRAT else "Helvetica, Arial, sans-serif"
FAMILIA_MONO = "'Consolas', Courier, monospace" if TEM_CONSOLAS else "Courier, monospace"


CSS_BASE = f"""
<style>
  {FONT_FACES}
  body {{
    font-family: {FAMILIA_SANS};
    font-size: 12.4pt;
    color: #111111;
    line-height: 1.38;
    margin: 0;
    padding: 0;
  }}
  .slide-header {{ margin-bottom: 15pt; }}
  .slide-kicker {{
    font-family: {FAMILIA_SB};
    font-size: 9.6pt;
    color: #0F62FE;
    margin: 0 0 5pt 0;
  }}
  h1 {{
    font-size: 23pt;
    font-weight: bold;
    color: #000000;
    margin: 0;
    line-height: 1.16;
  }}
  h2 {{
    font-size: 13.6pt;
    font-weight: bold;
    color: #0F62FE;
    margin: 0 0 7pt 0;
  }}
  p {{ margin: 0 0 7pt 0; }}
  b {{ font-weight: bold; }}
  ul, ol {{ margin: 2pt 0 4pt 15pt; padding: 0; }}
  li {{ margin-bottom: 7pt; }}
  table.layout {{ width: 100%; border-collapse: collapse; border: none; }}
  table.layout td {{ border: none; vertical-align: top; padding: 0; }}
  /* Tabela no estilo do slide de AA: cabecalho azul, primeira coluna em azul, linhas finas */
  table.dados {{ width: 100%; border-collapse: collapse; font-size: 10.6pt; margin-top: 8pt; }}
  table.dados th {{
    background-color: #0F62FE;
    color: #FFFFFF;
    padding: 7pt 9pt;
    text-align: left;
    border: none;
    font-weight: bold;
  }}
  table.dados td {{ padding: 7pt 9pt; border: none; border-bottom: 0.8pt solid #E0E0E0; }}
  table.dados tr.destaque td {{ background-color: #EAF2FF; }}
  table.dados td.chave {{ color: #0F62FE; font-weight: bold; }}
  table.dados td.num, table.dados th.num {{ text-align: right; }}
  /* Faixa azul solida (a "Ideia central" do slide de AA) */
  .banner-azul {{
    background-color: #0F62FE;
    color: #FFFFFF;
    padding: 11pt 16pt;
    margin-bottom: 10pt;
    line-height: 1.4;
  }}
  .banner-azul .titulo {{ color: #FFFFFF; font-weight: bold; font-size: 11pt; margin-bottom: 3pt; }}
  .box-azul {{
    background-color: #EAF2FF;
    padding: 12pt 15pt;
    margin-bottom: 10pt;
  }}
  .box-azul .titulo {{ color: #0F62FE; font-weight: bold; font-size: 11.4pt; margin-bottom: 4pt; }}
  .box-suave {{
    background-color: #F4F7FB;
    border: 0.8pt solid #E0E0E0;
    padding: 11pt 14pt;
    margin-bottom: 10pt;
  }}
  /* Cartoes de numero (o "1.999.000" do slide de AA) */
  .kpi-card-azul {{ background-color: #0F62FE; color: #FFFFFF; padding: 13pt 15pt; }}
  .kpi-card-laranja {{ background-color: #D55E00; color: #FFFFFF; padding: 13pt 15pt; }}
  .kpi-card-claro {{ background-color: #EAF2FF; padding: 13pt 15pt; }}
  .kpi-num-branco {{ font-size: 28pt; font-weight: bold; color: #FFFFFF; line-height: 1.05; }}
  .kpi-lbl-branco {{ font-size: 10.2pt; color: #FFFFFF; margin-top: 5pt; line-height: 1.32; }}
  .kpi-num {{ font-size: 26pt; font-weight: bold; color: #0F62FE; line-height: 1.05; }}
  .kpi-num-azul {{ font-size: 26pt; font-weight: bold; color: #0F62FE; line-height: 1.05; }}
  .kpi-lbl {{ font-size: 10.2pt; color: #525252; margin-top: 5pt; line-height: 1.32; }}
  .legenda {{ font-size: 9.4pt; color: #6F6F6F; margin-top: 5pt; line-height: 1.32; }}
  code {{ font-family: {FAMILIA_MONO}; font-size: 0.9em; color: #0043CE; }}
  .banner-azul code, .kpi-card-azul code {{ color: #FFFFFF; }}
</style>
"""


def criar_archive() -> pymupdf.Archive:
    arch = pymupdf.Archive()
    arch.add(str(ROOT))
    if TEM_CONSOLAS:
        arch.add(str(WIN_FONTS))
    return arch


def img_rel(caminho: Path, style: str) -> str:
    if not caminho.exists():
        return '<div class="box-azul"><div class="titulo">Imagem pendente</div>Arquivo não encontrado: ' + caminho.name + "</div>"
    rel = caminho.relative_to(ROOT).as_posix()
    return f'<img src="{rel}" style="{style}"/>'


def montar_slides() -> list[tuple[str, str]]:
    """Retorna lista de tuplas (tipo, html). tipo in {'capa', 'conteudo'}."""
    slides: list[tuple[str, str]] = []

    # ------------------------------------------------------------------
    # SLIDE 1: CAPA (fundo azul-principal da Secao 2.1 + tipografia Montserrat)
    # ------------------------------------------------------------------
    s1 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>
    <style>
      {FONT_FACES}
      body {{ font-family: {FAMILIA_SANS}; color: #FFFFFF; margin: 0; }}
      .kicker {{ font-family: {FAMILIA_SB}; font-size: 11pt; color: #FFFFFF; margin: 0 0 16pt 0; }}
      h1 {{ font-size: 40pt; font-weight: bold; color: #FFFFFF; line-height: 1.1; margin: 0 0 18pt 0; }}
      .sub {{ font-size: 15pt; color: #FFFFFF; line-height: 1.5; margin: 0 0 54pt 0; }}
      .meta {{ font-size: 10.6pt; color: #FFFFFF; line-height: 1.6; }}
      .meta b {{ font-weight: bold; }}
    </style></head><body>
      <div class="kicker">Avaliação II (AV2) · AVD 2026.2 · Grupo 06</div>
      <h1>Agrupamento, EDA e<br/>Dashboard Interativo</h1>
      <div class="sub">
        <b>Parte Específica:</b> Pontos d'Água da Tanzânia (Pump it Up, DrivenData)<br/>
        <b>Parte Comum:</b> Qualidade de Vinhos e K-Means (Wine Quality, UCI 186)
      </div>
      <div class="meta">
        <b>Integrantes:</b> Gustavo Henrique Cruz de Oliveira · Arthur de Assis Borges · João Vitor do Sacramento Bezerra da Cunha<br/>
        <b>Instituição:</b> CESAR School · <b>Professora:</b> Maira Lira · <b>Defesa:</b> 03/12/2026
      </div>
    </body></html>"""
    slides.append(("capa", s1))

    # ------------------------------------------------------------------
    # SLIDE 2: PROBLEMA, PUBLICO-ALVO E PERGUNTA DE PESQUISA
    # ------------------------------------------------------------------
    s2 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Específica · Pump it Up (Tanzânia)</div>
        <h1>Problema, Público-Alvo e Pergunta de Pesquisa</h1>
      </div>
      <div class="box-azul">
        <div class="titulo">Pergunta de Pesquisa</div>
        <p style="font-size:13.6pt; margin:0; color:#000000; line-height:1.38;">
          "Quais características de um ponto d'água se associam ao seu estado operacional (funcional, precisando de
          reparo ou não funcional) e em que medida esses atributos permitem classificar/identificar corretamente bombas
          com necessidade de manutenção ou inoperantes?"
        </p>
      </div>
      <table class="layout" style="margin-top:10pt;">
        <tr>
          <td style="width:416pt; padding-right:18pt;">
            <h2>Público-Alvo e Contexto</h2>
            <ul>
              <li><b>Gestores do Ministério de Águas da Tanzânia</b>, responsáveis por priorizar manutenção preventiva e alocação de equipes em campo.</li>
              <li><b>Fonte:</b> DrivenData / Taarifa e Ministério da Água da Tanzânia (registros de 2011 a 2013 na base tratada).</li>
              <li><b>Alvo multiclasse (<code>status_group</code>):</b> <code>functional</code>, <code>functional needs repair</code> e <code>non functional</code>.</li>
            </ul>
          </td>
          <td style="width:434pt;">
            <table class="layout">
              <tr>
                <td style="width:210pt; padding:0 7pt 11pt 0;">
                  <div class="kpi-card-claro"><div class="kpi-num">59.333</div><div class="kpi-lbl">Pontos d'água na base limpa (31 colunas)</div></div>
                </td>
                <td style="width:210pt; padding:0 0 11pt 7pt;">
                  <div class="kpi-card-laranja"><div class="kpi-num-branco">45,7%</div><div class="kpi-lbl-branco">Inoperantes (38,4%) ou precisam de reparo (7,3%)</div></div>
                </td>
              </tr>
              <tr>
                <td style="width:210pt; padding:0 7pt 0 0;">
                  <div class="kpi-card-claro"><div class="kpi-num-azul">21</div><div class="kpi-lbl">Regiões administrativas da Tanzânia</div></div>
                </td>
                <td style="width:210pt; padding:0 0 0 7pt;">
                  <div class="kpi-card-azul"><div class="kpi-num-branco">80,6%</div><div class="kpi-lbl-branco">Acurácia do Random Forest no teste (n = 11.867)</div></div>
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
        <div class="slide-kicker">Parte Específica · EDA e Tratamento</div>
        <h1>Ausência Concentrada em 6 Regiões (MAR) e Limpeza Sem Perda de Cobertura</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:364pt; padding-right:18pt;">
            {img_rel(OUT_ESP / "02_ausencia_por_regiao.png", "width:352pt; height:306pt;")}
            <div class="legenda">Zeros suspeitos em population (36,0%), construction_year (34,9%) e gps_height (34,4%) na base bruta (n = 59.400).</div>
          </td>
          <td style="width:486pt;">
            <div class="box-azul">
              <div class="titulo">Mecanismo MAR (Aula 09)</div>
              Coocorrência de <b>0,91 a 0,93</b> entre as três colunas, concentrada em <b>88,6% a 100%</b> em 6 regiões (Dodoma, Kagera, Mbeya, Tabora, Shinyanga e Mwanza).
            </div>
            <ul>
              <li><b>Decisão:</b> não remover 1/3 da base; salvar flags <code>ausente_*</code> e imputar pela mediana em cascata (<code>lga -&gt; region -&gt; basin</code>).</li>
              <li><b>Limpeza:</b> removidas 36 duplicadas (sem <code>id</code>) e 31 linhas de 2002/2004 (todas as 9 idades negativas); 1.496 altitudes negativas no litoral ajustadas para 0.</li>
              <li><b>Base limpa:</b> <b>59.333 × 31</b>, <b>0 NaNs</b>, 0 idades ou altitudes negativas.</li>
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
        <div class="slide-kicker">Parte Específica · Visualizações Exploratórias (1 e 2)</div>
        <h1>Quase Metade da Rede Falha e a Disponibilidade de Água Lidera o Risco</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:361pt; padding-right:12pt;">
            {img_rel(OUT_ESP / "07_expl_01_distribuicao_status.png", "width:360pt;")}
            <div class="box-suave" style="margin-top:8pt; font-size:10.8pt;">
              <b>Desbalanceamento:</b> <code>functional needs repair</code> soma só <b>7,3%</b> (4.313 pontos), exigindo Precisão, Recall e F1 por classe.
            </div>
          </td>
          <td style="width:495pt;">
            {img_rel(OUT_ESP / "07_expl_02_status_por_categoria.png", "width:440pt;")}
            <div class="box-suave" style="margin-top:8pt; font-size:10.8pt;">
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
        <div class="slide-kicker">Parte Específica · Visualizações Exploratórias (3 e 4)</div>
        <h1>Forte Desigualdade Territorial e Contraste Entre Água e Tecnologia</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:465pt; padding-right:12pt;">
            {img_rel(OUT_ESP / "07_expl_03_contraste_regional_mapa.png", "width:460pt;")}
            <div class="box-suave" style="margin-top:8pt; font-size:10.8pt;">
              <b>Extremos regionais:</b> Iringa (<b>19,5%</b> inoperantes) e Arusha (<b>26,3%</b>) vs. Lindi (<b>64,2%</b>), Mtwara (<b>62,4%</b>) e Tabora (<b>54,4%</b>).
            </div>
          </td>
          <td style="width:391pt;">
            {img_rel(OUT_ESP / "07_expl_04_heatmap_quantity_extraction.png", "width:384pt;")}
            <div class="box-azul" style="margin-top:8pt; font-size:10.8pt;">
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
        <div class="slide-kicker">Parte Específica · Storytelling e Visualização Explanatória 1</div>
        <h1>Mesmo com Água Suficiente, Bombas Motorizadas Falham 2,5x Mais</h1>
      </div>
      <div class="banner-azul" style="padding:8pt 13pt; margin-bottom:10pt; font-size:11.2pt;">
        <b>Big Idea:</b> Os pontos d'água da Tanzânia falham principalmente quando há escassez de água, quando são mais antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como gravidade e bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível.
      </div>
      <table class="layout">
        <tr>
          <td style="width:583pt; padding-right:16pt;">
            {img_rel(OUT_ESP / "08_explan_01_tecnologia_com_agua.png", "width:578pt;")}
          </td>
          <td style="width:269pt;">
            <h2>Destaque em água suficiente</h2>
            <ul>
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
        <div class="slide-kicker">Parte Específica · Visualização Explanatória 2A</div>
        <h1>A Idade da Bomba Separa o Risco: Falha Sobe de 23,9% para 60,8%</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:574pt; padding-right:16pt;">
            {img_rel(OUT_ESP / "08_explan_02a_idade_vs_falha.png", "width:568pt;")}
          </td>
          <td style="width:278pt;">
            <div class="kpi-card-laranja" style="margin-bottom:12pt;">
              <div class="kpi-num-branco">18 anos</div>
              <div class="kpi-lbl-branco">Mediana de idade das bombas inoperantes, o dobro dos <b>9 anos</b> nas funcionais</div>
            </div>
            <ul>
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
        <div class="slide-kicker">Parte Específica · Visualização Explanatória 2B (Classificador Sem Data Leakage)</div>
        <h1>Random Forest Atinge 80,6% no Teste, mas Expõe Gargalo em Reparo</h1>
      </div>
      <div style="text-align:center;">
        {img_rel(OUT_ESP / "08_explan_02b_classificador_metricas.png", "width:680pt;")}
      </div>
      <table class="dados" style="margin-top:6pt; font-size:9.6pt;">
        <thead>
          <tr>
            <th>Modelo (split 80/20 estratificado, teste n = 11.867)</th>
            <th class="num">Acurácia</th>
            <th class="num">Macro F1</th>
            <th class="num">Recall functional</th>
            <th class="num">Recall needs repair</th>
            <th class="num">Precisão / Recall NF</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="chave">Árvore de Decisão (baseline auditável, <code>max_depth=15</code>)</td>
            <td class="num">75,33%</td>
            <td class="num">62,82%</td>
            <td class="num">85,28%</td>
            <td class="num">26,88%</td>
            <td class="num">77,42% / 70,45%</td>
          </tr>
          <tr class="destaque">
            <td class="chave">Random Forest (200 árvores, Target + One-Hot no Pipeline)</td>
            <td class="num"><b>80,58%</b></td>
            <td class="num"><b>67,64%</b></td>
            <td class="num"><b>91,02%</b></td>
            <td class="num"><b>27,00%</b></td>
            <td class="num"><b>84,42% / 75,96%</b></td>
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
        <div class="slide-kicker">Demonstração ao vivo · Dashboard Streamlit</div>
        <h1>Dashboard Interativo: 5 Abas Conectadas e Recursos de Apoio à Decisão</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:444pt; padding-right:16pt;">
            <div class="box-azul">
              <div class="titulo">Roteiro da Demo ao Vivo (Streamlit)</div>
              <p style="font-size:10pt; margin:0 0 7pt 0; color:#525252;">Comando: <code>streamlit run src/parte_especifica/dashboard.py</code></p>
              <ol style="margin:3pt 0 0 18pt; padding:0; font-size:11.5pt;">
                <li style="margin-bottom:6pt;"><b>Filtros globais + KPIs dinâmicos:</b> filtrar <code>Lindi</code> e <code>enough</code> e observar o recálculo instantâneo.</li>
                <li style="margin-bottom:6pt;"><b>Aba 2 (Exploração):</b> usar o <b>Comparador lado a lado de 2 regiões</b> (Iringa vs. Lindi) e o <b>Heatmap livre de 2 variáveis</b> (pronto para a arguição).</li>
                <li style="margin-bottom:6pt;"><b>Aba 3 (Classificador):</b> sortear 3 bombas reais e abrir a trilha <code>decision_path</code> da Árvore.</li>
                <li style="margin-bottom:0;"><b>Aba 4 (Parte Comum):</b> reproduzir a <b>animação interativa Passada 1 -&gt; Passada 2</b> do K-Means em PCA 2D.</li>
              </ol>
            </div>
          </td>
          <td style="width:408pt;">
            <h2>Recursos de Interação e Desempenho</h2>
            <ul>
              <li>Identidade visual limpa (RecifeView Seção 2.1 + Okabe-Ito) com contraste acima de 4,5:1 e zero poluição visual.</li>
              <li>Controles nativos modernos (<code>st.pills</code>, <code>st.segmented_control</code>, <code>@st.fragment</code>) com isolamento de reexecuções.</li>
              <li>Cache separado: <code>@st.cache_data</code> para tabelas e <code>@st.cache_resource</code> para pipelines treinados.</li>
              <li><b>Plano B offline:</b> opção de mapa sem internet e figuras estáticas prontas em <code>out/parte_especifica/</code>.</li>
            </ul>
          </td>
        </tr>
      </table>
      <div class="banner-azul" style="margin-top:16pt; margin-bottom:0; font-size:11.6pt;">
        <b>Pronto para a arguição ao vivo:</b> qualquer par de variáveis categóricas do dataset pode ser cruzado em 3 segundos
        no Heatmap livre da Aba 2, e todos os filtros da sidebar recalculam KPIs e gráficos instantaneamente.
      </div>
    </body></html>"""
    slides.append(("conteudo", s9))

    # ------------------------------------------------------------------
    # SLIDE 10: PARTE COMUM - DATASET WINE QUALITY, EDA E PADRONIZACAO
    # ------------------------------------------------------------------
    s10 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum · Wine Quality Combinado (UCI 186)</div>
        <h1>Wine Quality: Notas Concentradas em 5 e 6 e Escalas Muito Distintas</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:485pt; padding-right:18pt;">
            {img_rel(OUT_COM / "distribuicao_quality.png", "width:482pt;")}
            <div class="legenda">Distribuição das 7 notas reais (3 a 9) em Wine Quality (n = 6.497; 4.898 brancos e 1.599 tintos).</div>
          </td>
          <td style="width:365pt;">
            <h2>Estrutura, EDA e Padronização</h2>
            <ul>
              <li><b>6.497 × 13</b> (11 físico-químicas + <code>wine_type</code> + <code>quality</code>), 0 nulos, 1.177 duplicatas (18,12%, mantidas).</li>
              <li><b>Desbalanceamento:</b> notas <b>5 (32,9%)</b> e <b>6 (43,7%)</b> somam <b>76,6%</b>; nota 9 tem apenas 5 vinhos.</li>
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
        <div class="slide-kicker">Parte Comum · Agrupamento Não Supervisionado (K-Means)</div>
        <h1>K-Means em Duas Passadas: Cotovelo (k = 3) vs. k Fixo = 7</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:282pt; padding-right:7pt;">
            {img_rel(OUT_COM / "metodo_cotovelo.png", "width:282pt;")}
            <div class="legenda">Cotovelo em k = 3 (-18,7% de inércia de k = 2 para k = 3).</div>
          </td>
          <td style="width:282pt; padding-right:7pt;">
            {img_rel(OUT_COM / "clusters_livre.png", "width:282pt;")}
            <div class="legenda">Passada 1 (k = 3, PCA 2D = 52,8% var.).</div>
          </td>
          <td style="width:289pt;">
            {img_rel(OUT_COM / "clusters_fixo.png", "width:282pt;")}
            <div class="legenda">Passada 2 (k = 7 = notas 3 a 9).</div>
          </td>
        </tr>
      </table>
      <div class="banner-azul" style="margin-top:12pt; margin-bottom:0; font-size:11.4pt;">
        <b>Comparação das Passadas (Aba 4 do Dashboard anima esta transição ao vivo):</b>
        Passada 1 (<b>k = 3</b>) atinge inércia <b>45.875,7</b>, Silhouette <b>0,252</b> e Davies-Bouldin <b>1,420</b>;
        Passada 2 (<b>k = 7</b>) reduz inércia para <b>34.418,2</b>, mas Silhouette cai para <b>0,182</b> e Davies-Bouldin piora para <b>1,598</b>.
      </div>
    </body></html>"""
    slides.append(("conteudo", s11))

    # ------------------------------------------------------------------
    # SLIDE 12: PARTE COMUM - MATRIZES DE CONFUSAO E METRICAS
    # ------------------------------------------------------------------
    s12 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Parte Comum · Avaliação dos Clusters Frente às Notas Reais</div>
        <h1>Apenas Notas 5 e 6 Dominam Clusters; Ganho de k = 7 É de +1,2 pp</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:407pt; padding-right:10pt; text-align:center;">
            {img_rel(OUT_COM / "matriz_confusao_livre.png", "width:340pt;")}
          </td>
          <td style="width:417pt; text-align:center;">
            {img_rel(OUT_COM / "matriz_confusao_fixo.png", "width:340pt;")}
          </td>
        </tr>
      </table>
      <table class="dados" style="margin-top:8pt; font-size:10pt;">
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
            <td class="chave">Passada 1 (k = 3 livre)</td>
            <td class="num">44,47%</td>
            <td class="num">13,37%</td>
            <td class="num">42,87% / 31,90%</td>
            <td class="num">44,99% / 77,82%</td>
            <td>0,0% (<code>zero_division=0</code>)</td>
          </tr>
          <tr class="destaque">
            <td class="chave">Passada 2 (k = 7 fixo)</td>
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
        <div class="slide-kicker">Parte Comum · Discussão Crítica (Wine Quality)</div>
        <h1>7 Notas Sensoriais Não Formam 7 Grupos Naturais no Espaço Químico</h1>
      </div>
      <table class="layout" style="margin-top:6pt;">
        <tr>
          <td style="width:422pt; padding-right:12pt;">
            <div class="box-azul" style="min-height:195pt;">
              <div class="titulo">1. Passada 1 (k = 3) vs. Passada 2 (k = 7)</div>
              <ul style="margin-bottom:0;">
                <li><b>Coesão interna superior:</b> <code>k = 3</code> entrega grupos mais coesos (Silhouette <b>0,252</b> vs. <b>0,182</b>; Davies-Bouldin <b>1,420</b> vs. <b>1,598</b>).</li>
                <li><b>Ganho marginal limitado:</b> forçar <code>k = 7</code> eleva a coincidência em apenas <b>+1,20 pp</b> (44,47% -&gt; 45,67%), pouco acima da frequência da nota 6 sozinha (43,65%).</li>
              </ul>
            </div>
          </td>
          <td style="width:434pt;">
            <div class="box-suave" style="min-height:195pt;">
              <div style="font-weight:bold; color:#062A5F; font-size:11pt; margin-bottom:5pt;">2. Granularidade das 7 notas originais</div>
              <ul style="margin-bottom:0;">
                <li><b>Qualidade ordinal e desbalanceada:</b> notas 5 e 6 concentram <b>76,6%</b> dos vinhos e compartilham perfis físico-químicos muito próximos entre vizinhos.</li>
                <li><b>Efeito do tipo de vinho:</b> incluir <code>wine_type_red</code> puxa os centroides para separar composição (tinto vs. branco) mais do que nota sensorial.</li>
              </ul>
            </div>
          </td>
        </tr>
      </table>
      <div class="banner-azul" style="margin-top:12pt; margin-bottom:14pt; font-size:12.2pt;">
        <b>Conclusão metodológica:</b> o K-Means descobre perfis físico-químicos naturais, mas não substitui um classificador
        supervisionado para distinguir notas sensoriais finas (como 5, 6 e 7).
      </div>
      <table class="layout">
        <tr>
          <td style="width:281pt; padding-right:8pt;">
            <div class="kpi-card-claro"><div class="kpi-num-azul">0,252 vs. 0,182</div><div class="kpi-lbl">Silhouette cai quando forçamos k = 7</div></div>
          </td>
          <td style="width:281pt; padding-right:8pt;">
            <div class="kpi-card-claro"><div class="kpi-num">+1,20 pp</div><div class="kpi-lbl">Ganho marginal em coincidência (44,47% -&gt; 45,67%)</div></div>
          </td>
          <td style="width:289pt;">
            <div class="kpi-card-claro"><div class="kpi-num">76,6%</div><div class="kpi-lbl">Amostras concentradas nas notas 5 e 6</div></div>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s13))

    # ------------------------------------------------------------------
    # SLIDE 14: CONCLUSAO INTEGRADA, LIMITACOES E ARGUICAO
    # ------------------------------------------------------------------
    s14 = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"/>{CSS_BASE}</head><body>
      <div class="slide-header">
        <div class="slide-kicker">Fechamento integrado · Grupo 06</div>
        <h1>Conclusões, Limitações e Próximos Passos</h1>
      </div>
      <table class="layout">
        <tr>
          <td style="width:435pt; padding-right:16pt;">
            <h2>Principais Entregas e Respostas</h2>
            <ul>
              <li><b>Pump it Up:</b> escassez hídrica, envelhecimento da bomba (&gt; 20 anos) e tecnologias motorizadas concentram as falhas; o Random Forest (80,6%) apoia triagem em escala e a Árvore (75,3%) oferece auditoria transparente.</li>
              <li><b>Dashboard Streamlit:</b> reúne storytelling, exploração livre (inclusive de quaisquer 2 variáveis ao vivo), auditoria do classificador e transição animada do K-Means.</li>
              <li><b>Wine Quality (K-Means):</b> evidencia o papel do <code>StandardScaler</code> e por que 7 notas sensoriais desbalanceadas não viram 7 clusters puros.</li>
            </ul>
          </td>
          <td style="width:417pt;">
            <div class="box-suave">
              <h2 style="margin-bottom:5pt;">Limitações Transparentes</h2>
              <ul style="margin-bottom:0;">
                <li><b>MAR em 6 regiões:</b> 34,8% sem ano real (excluídos da análise de idade).</li>
                <li><b>Classe minoritária:</b> recall de 27,0% em <code>functional needs repair</code> pede inspeção preventiva complementar.</li>
                <li><b>Amostras e unidades:</b> cautela com <code>wind-powered</code> (n = 59) e unidades não declaradas (<code>amount_tsh</code>, <code>gps_height</code>).</li>
                <li><b>Wine Quality:</b> 18,1% de duplicatas mantidas e efeito de <code>wine_type_red</code> nos centroides.</li>
              </ul>
            </div>
            <div class="banner-azul" style="margin-top:8pt; margin-bottom:0;">
              <div class="titulo">Obrigado! Abertos para perguntas e testes ao vivo no Dashboard.</div>
              <span style="font-size:10.5pt;">Repositório GitHub: <code>projeto-avd-2026-2-pump-it-up-classificatorio</code></span>
            </div>
          </td>
        </tr>
      </table>
    </body></html>"""
    slides.append(("conteudo", s14))

    return slides


def gerar_apresentacao():
    slides = montar_slides()
    arch = criar_archive()
    mediabox = pymupdf.Rect(0, 0, SLIDE_W, SLIDE_H)
    bio = io.BytesIO()
    writer = pymupdf.DocumentWriter(bio)

    for idx, (tipo, html) in enumerate(slides, start=1):
        dev = writer.begin_page(mediabox)
        if tipo == "capa":
            where = pymupdf.Rect(64, 112, SLIDE_W - 64, SLIDE_H - 40)
        else:
            where = pymupdf.Rect(MARGEM_X, 34, SLIDE_W - MARGEM_X, SLIDE_H - 40)
        story = pymupdf.Story(html=html, archive=arch)
        more, _ = story.place(where)
        if more:
            print(f"[AVISO] Slide {idx} teve conteudo excedente; verifique o layout.")
        story.draw(dev)
        writer.end_page()

    writer.close()

    doc = pymupdf.open("pdf", bio.getvalue())
    total = len(doc)
    font_reg = str(DIR_FONTES / "Montserrat-Regular.ttf") if TEM_MONTSERRAT else None

    for idx, page in enumerate(doc):
        if TEM_MONTSERRAT:
            page.insert_font(fontname="mont_r", fontfile=font_reg)
            fn_r = "mont_r"
            largura = pymupdf.Font(fontfile=font_reg).text_length
        else:
            fn_r = "helv"
            largura = lambda txt, fontsize: pymupdf.get_text_length(txt, fontname="helv", fontsize=fontsize)

        if idx == 0:
            # Capa: fundo azul-principal inteiro (identidade da Secao 2.1, como a capa do slide de AA)
            shape = page.new_shape()
            shape.draw_rect(mediabox)
            shape.finish(fill=AZUL, color=None)
            shape.commit(overlay=False)
        else:
            # Rodape minimo: nome do trabalho a esquerda e numero a direita, em cinza
            page.insert_text(
                (MARGEM_X, SLIDE_H - 16),
                "Projeto Final AVD 2026.2 · Grupo 6 · CESAR School",
                fontsize=7.6,
                fontname=fn_r,
                color=CINZA_NOTA,
            )
            num_txt = f"{idx + 1}"
            page.insert_text(
                (SLIDE_W - MARGEM_X - largura(num_txt, fontsize=7.6), SLIDE_H - 16),
                num_txt,
                fontsize=7.6,
                fontname=fn_r,
                color=CINZA_NOTA,
            )

    doc.save(str(DESTINO_PDF), garbage=4, deflate=True, deflate_images=True, clean=True)
    doc.close()
    print(f"Apresentacao gerada com sucesso: {DESTINO_PDF} ({total} slides, {DESTINO_PDF.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    gerar_apresentacao()
