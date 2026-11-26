"""Dashboard Interativo em Streamlit: Parte Especifica (Pump it Up) + Bonus Parte Comum (K-Means).

# [IA] Gemini – dashboard Streamlit 1.67 aplicando identidade visual RecifeView (Secao 2.1 de 06_GUIDELINES),
# skills de SKILL_DESIGN (fragments, segmented_control, pills, containers com borda), filtros dinamicos
# interligados, comparador lado a lado, animacao K-Means da Parte Comum e classificador auditavel

Execucao, a partir da raiz do repositorio:
    streamlit run src/parte_especifica/dashboard.py
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from data_loader import (
    COL_ALVO,
    COR_AZUL,
    COR_BORDA,
    COR_CINZA,
    COR_FONTE_NOTA,
    COR_LARANJA_ALERTA,
    COR_MARCA_CLARO,
    COR_MARCA_ESCURO,
    COR_MARCA_MARINHO,
    COR_MARCA_PRINCIPAL,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO,
    FAIXAS_IDADE_BINS,
    FAIXAS_IDADE_LABELS,
    GLOSSARIO_COLUNAS,
    ROTULOS_VARS_CAT,
    STATUS_CORES,
    STATUS_ORDEM,
    STATUS_ROTULO_PT,
    auditar_arvore,
    carregar_dados,
    carregar_tabelas_classificador,
    executar_kmeans_parte_comum,
    fmt_int,
    fmt_num,
    fmt_pct,
    gerar_resumo_markdown,
    treinar_classificadores,
)

# -----------------------------------------------------------------------------
# Configuracao de pagina e identidade visual oficial (Secao 2.1, RecifeView)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pump it Up: Monitoramento de Pontos d'Água (Tanzânia)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cabecalho oficial em azul-marinho (#062A5F) + caixa de Big Idea em azul-claro (#EAF2FF)
# Sem gradientes, sem sombras pesadas, sem emojis e sem eyebrow ALL-CAPS (06_GUIDELINES + SKILL_DESIGN)
st.html(
    """
    <style>
    .hero-header {
        background-color: #062A5F;
        color: #FFFFFF;
        padding: 1.25rem 1.5rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    .hero-title {
        color: #FFFFFF;
        font-size: 1.55rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
        line-height: 1.25;
    }
    .hero-subtitle {
        color: #EAF2FF;
        font-size: 0.92rem;
        margin: 0;
        line-height: 1.4;
    }
    .big-idea-card {
        background-color: #EAF2FF;
        border-left: 4px solid #0F62FE;
        padding: 1rem 1.25rem;
        border-radius: 4px;
        margin: 0.75rem 0 1.25rem 0;
    }
    .big-idea-heading {
        color: #0043CE;
        font-size: 0.92rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
    }
    .big-idea-body {
        color: #000000;
        font-size: 1.03rem;
        line-height: 1.5;
        margin: 0;
    }
    .chart-footnote {
        font-size: 0.80rem;
        color: #6F6F6F;
        margin-top: -0.35rem;
        margin-bottom: 0.85rem;
    }
    .filter-summary {
        background-color: #EAF2FF;
        color: #0043CE;
        font-size: 0.85rem;
        padding: 0.5rem 0.85rem;
        border-radius: 4px;
        border: 1px solid #C6D8FF;
        margin-bottom: 0.9rem;
    }
    </style>
    """
)


def aplicar_layout_base(fig, altura=420, margem_topo=60, margem_baixo=48):
    """Padroniza fundo branco, texto preto e grade horizontal discreta (#E0E0E0)."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="sans-serif", color=COR_TEXTO, size=12),
        height=altura,
        margin=dict(l=20, r=24, t=margem_topo, b=margem_baixo),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color=COR_TEXTO, bordercolor=COR_BORDA),
    )
    fig.update_xaxes(gridcolor="#E0E0E0", linecolor="#8D8D8D")
    fig.update_yaxes(gridcolor="#E0E0E0", linecolor="#8D8D8D")
    return fig


def exibir_rodape_grafico(texto):
    st.html(f'<p class="chart-footnote">{texto}</p>')


def inicializar_estado(idade_min, idade_max):
    defaults = {
        "f_regioes": [],
        "f_quantidades": [],
        "f_extracoes": [],
        "f_pagamentos": [],
        "f_idade": (int(idade_min), int(idade_max)),
        "f_ocultar_imp_idade": False,
        "seed_sorteio": 42,
    }
    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def limpar_filtros(idade_min, idade_max):
    st.session_state["f_regioes"] = []
    st.session_state["f_quantidades"] = []
    st.session_state["f_extracoes"] = []
    st.session_state["f_pagamentos"] = []
    st.session_state["f_idade"] = (int(idade_min), int(idade_max))
    st.session_state["f_ocultar_imp_idade"] = False


# -----------------------------------------------------------------------------
# Carga da base tratada (@st.cache_data)
# -----------------------------------------------------------------------------
df_total = carregar_dados()
df_metricas_csv, df_imp_csv = carregar_tabelas_classificador()

idade_min_global = int(df_total["idade_no_registro"].min())
idade_max_global = int(df_total["idade_no_registro"].max())
inicializar_estado(idade_min_global, idade_max_global)

# -----------------------------------------------------------------------------
# Sidebar em azul-claro (#EAF2FF): filtros dinamicos interligados + exportacao
# -----------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Filtros do painel")
    st.caption("Atualizam KPIs e gráficos da Parte Específica em tempo real.")

    regioes_opcoes = sorted(df_total["region"].unique().tolist())
    quant_opcoes = ["enough", "insufficient", "seasonal", "dry", "unknown"]
    ext_opcoes = df_total["extraction_type_class"].value_counts().index.tolist()
    pag_opcoes = df_total["payment_type"].value_counts().index.tolist()

    quant_sel = st.pills(
        "Disponibilidade de água (quantity)",
        options=quant_opcoes,
        selection_mode="multi",
        key="f_quantidades",
    )
    regioes_sel = st.multiselect(
        "Região (region)",
        options=regioes_opcoes,
        key="f_regioes",
        placeholder="Todas as 21 regiões",
    )
    ext_sel = st.multiselect(
        "Tecnologia de extração (extraction_type_class)",
        options=ext_opcoes,
        key="f_extracoes",
        placeholder="Todas as tecnologias",
    )
    pag_sel = st.multiselect(
        "Forma de pagamento (payment_type)",
        options=pag_opcoes,
        key="f_pagamentos",
        placeholder="Todas as formas",
    )
    idade_sel = st.slider(
        "Faixa de idade no registro (anos)",
        min_value=idade_min_global,
        max_value=idade_max_global,
        key="f_idade",
    )
    ocultar_imp_idade = st.toggle(
        "Ocultar ano de construção imputado (MAR)",
        key="f_ocultar_imp_idade",
        help="Oculta os 34,8% de registros cujo construction_year original era 0 (concentrados em 6 regiões).",
    )

    st.button(
        "Limpar filtros",
        on_click=limpar_filtros,
        args=(idade_min_global, idade_max_global),
        width="stretch",
    )

# Aplicacao dos filtros
mask = df_total["idade_no_registro"].between(idade_sel[0], idade_sel[1])
if regioes_sel:
    mask &= df_total["region"].isin(regioes_sel)
if quant_sel:
    mask &= df_total["quantity"].isin(quant_sel)
if ext_sel:
    mask &= df_total["extraction_type_class"].isin(ext_sel)
if pag_sel:
    mask &= df_total["payment_type"].isin(pag_sel)
if ocultar_imp_idade:
    mask &= df_total["ausente_construction_year"] == 0

df_filt = df_total[mask].copy()

filtros_ativos = {
    "Região": ", ".join(regioes_sel) if regioes_sel else "Todas (21)",
    "Disponibilidade de água": ", ".join(quant_sel) if quant_sel else "Todas",
    "Tecnologia de extração": ", ".join(ext_sel) if ext_sel else "Todas",
    "Forma de pagamento": ", ".join(pag_sel) if pag_sel else "Todas",
    "Faixa de idade": f"{idade_sel[0]} a {idade_sel[1]} anos",
    "Somente ano informado": "Sim" if ocultar_imp_idade else "Não",
}

with st.sidebar:
    st.divider()
    st.subheader("Exportação rápida")
    resumo_md = gerar_resumo_markdown(df_filt, df_total, filtros_ativos)
    st.download_button(
        label="Baixar resumo executivo (.md)",
        data=resumo_md.encode("utf-8"),
        file_name="resumo_recorte_pump_it_up.md",
        mime="text/markdown",
        width="stretch",
    )
    st.caption(f"Recorte ativo: {fmt_int(len(df_filt))} de {fmt_int(len(df_total))} pontos.")

# -----------------------------------------------------------------------------
# Cabecalho principal em azul-marinho (#062A5F) + faixa de filtros ativos
# -----------------------------------------------------------------------------
st.html(
    """
    <div class="hero-header">
        <div class="hero-title">Pump it Up: monitoramento operacional de pontos d'água na Tanzânia</div>
        <p class="hero-subtitle">
            Projeto Final AVD 2026.2 (Grupo 6) | Público-alvo: gestores do Ministério de Águas da Tanzânia |
            Base tratada DrivenData/Taarifa (2011 a 2013, n = 59.333)
        </p>
    </div>
    """
)

# Mostra barra discreta quando algum filtro esta ativo
partes_filtro = []
if regioes_sel:
    partes_filtro.append(f"Região: {', '.join(regioes_sel)}")
if quant_sel:
    partes_filtro.append(f"Água: {', '.join(quant_sel)}")
if ext_sel:
    partes_filtro.append(f"Tecnologia: {', '.join(ext_sel)}")
if pag_sel:
    partes_filtro.append(f"Pagamento: {', '.join(pag_sel)}")
if idade_sel != (idade_min_global, idade_max_global):
    partes_filtro.append(f"Idade: {idade_sel[0]} a {idade_sel[1]} anos")
if ocultar_imp_idade:
    partes_filtro.append("Somente ano de construção informado (sem MAR)")
if partes_filtro:
    st.html(f'<div class="filter-summary"><b>Filtros ativos:</b> {" | ".join(partes_filtro)}</div>')

if len(df_filt) == 0:
    st.warning(
        "Nenhum ponto d'água corresponde à combinação atual de filtros. Clique em 'Limpar filtros' na barra lateral.",
        title="Recorte vazio",
    )
    st.stop()

# -----------------------------------------------------------------------------
# Barra de 5 KPIs dinamicos dentro de st.container(border=True) (Aula 22 + SKILL)
# -----------------------------------------------------------------------------
ref_func = (df_total[COL_ALVO] == "functional").mean() * 100
ref_nf = (df_total[COL_ALVO] == "non functional").mean() * 100
ref_rep = (df_total[COL_ALVO] == "functional needs repair").mean() * 100
ref_idade = df_total.loc[df_total["ausente_construction_year"] == 0, "idade_no_registro"].median()

n_filt = len(df_filt)
pct_base = n_filt / len(df_total) * 100
pct_func = (df_filt[COL_ALVO] == "functional").mean() * 100
pct_nf = (df_filt[COL_ALVO] == "non functional").mean() * 100
pct_rep = (df_filt[COL_ALVO] == "functional needs repair").mean() * 100
df_filt_idade_real = df_filt[df_filt["ausente_construction_year"] == 0]
med_idade_filt = df_filt_idade_real["idade_no_registro"].median() if len(df_filt_idade_real) > 0 else np.nan

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    with st.container(border=True):
        st.metric(
            "Pontos d'água no recorte",
            fmt_int(n_filt),
            delta=f"{fmt_pct(pct_base)} da base",
            delta_color="off",
        )
with k2:
    with st.container(border=True):
        diff_f = pct_func - ref_func
        st.metric(
            "Funcionais",
            fmt_pct(pct_func),
            delta=f"{fmt_num(diff_f, 1)} pp vs. nacional" if abs(diff_f) >= 0.05 else "Média nacional",
        )
with k3:
    with st.container(border=True):
        diff_nf = pct_nf - ref_nf
        st.metric(
            "Não funcionais",
            fmt_pct(pct_nf),
            delta=f"{fmt_num(diff_nf, 1)} pp vs. nacional" if abs(diff_nf) >= 0.05 else "Média nacional",
            delta_color="inverse",
        )
with k4:
    with st.container(border=True):
        diff_r = pct_rep - ref_rep
        st.metric(
            "Precisam de reparo",
            fmt_pct(pct_rep),
            delta=f"{fmt_num(diff_r, 1)} pp vs. nacional" if abs(diff_r) >= 0.05 else "Média nacional",
            delta_color="inverse",
        )
with k5:
    with st.container(border=True):
        if pd.notna(med_idade_filt):
            diff_id = med_idade_filt - ref_idade
            st.metric(
                "Idade mediana (reais)",
                f"{fmt_num(med_idade_filt, 0)} anos",
                delta=f"{fmt_num(diff_id, 0)} anos vs. nacional" if abs(diff_id) >= 0.5 else "Igual à nacional",
                delta_color="inverse",
            )
        else:
            st.metric("Idade mediana (reais)", "Sem dados", delta="100% MAR no recorte", delta_color="off")

# -----------------------------------------------------------------------------
# Navegacao principal em 5 abas
# -----------------------------------------------------------------------------
aba_explan, aba_expl, aba_clf, aba_comum, aba_ref = st.tabs([
    "Storytelling e Insights (Explanatória)",
    "Exploração Interativa (Exploratória)",
    "Classificador e Auditoria",
    "Parte Comum (K-Means Obesity)",
    "Glossário e Exportação",
])


# =============================================================================
# ABA 1: STORYTELLING E VISUALIZACOES EXPLANATORIAS (E1, E2A, E2B)
# =============================================================================
with aba_explan:
    st.subheader("Contexto e mensagem central para o gestor público")

    with st.container(border=True):
        c_perg, c_pub = st.columns([1.45, 1.0])
        with c_perg:
            st.markdown(
                "**Pergunta de pesquisa:** Quais características de um ponto d'água se associam ao seu estado "
                "operacional (funcional, precisando de reparo ou não funcional) e em que medida esses atributos "
                "permitem classificar corretamente bombas com necessidade de manutenção ou inoperantes?"
            )
        with c_pub:
            st.markdown(
                "**Público-alvo:** Gestores públicos do Ministério de Águas da Tanzânia, responsáveis por priorizar "
                "manutenção preventiva e escolher tecnologias mais confiáveis em campo."
            )

    st.html(
        """
        <div class="big-idea-card">
            <div class="big-idea-heading">Big Idea (Sujeito + Verbo + Ponto de Vista)</div>
            <p class="big-idea-body">
                Os pontos d'água da Tanzânia falham principalmente quando há escassez de água, quando são mais
                antigos ou quando usam tecnologias motorizadas em vez de sistemas mais simples (como gravidade e
                bombas manuais), que se mantêm mais funcionais mesmo quando há água disponível.
            </p>
        </div>
        """
    )

    # EXPLANATORIA 1
    with st.container(border=True):
        st.markdown("### Visualização Explanatória 1: Tecnologia de extração quando há água suficiente")
        sub_enough = df_filt[df_filt["quantity"] == "enough"].copy()

        if len(sub_enough) == 0:
            st.info(
                "Os filtros atuais excluíram os pontos com disponibilidade de água igual a 'enough'. "
                "Limpe ou ajuste o filtro de disponibilidade de água na barra lateral para ver este gráfico.",
                title="Sem registros com água suficiente neste recorte",
            )
        else:
            tab_e1 = (
                pd.crosstab(sub_enough["extraction_type_class"], sub_enough[COL_ALVO], normalize="index")
                .reindex(columns=STATUS_ORDEM, fill_value=0)
                .mul(100)
            )
            tab_e1["n"] = sub_enough["extraction_type_class"].value_counts()
            tab_e1 = tab_e1.sort_values("non functional", ascending=True)

            media_e1 = (sub_enough[COL_ALVO] == "non functional").mean() * 100
            destaque_cats = {"other", "wind-powered", "motorpump"}
            cores_e1 = [
                COR_LARANJA_ALERTA if cat in destaque_cats
                else ("#F0A070" if cat == "submersible" else COR_CINZA)
                for cat in tab_e1.index
            ]
            rotulos_ext = {
                "other": "other (outras / não especificadas)",
                "wind-powered": "wind-powered (eólica*)",
                "motorpump": "motorpump (motorizada)",
                "submersible": "submersible (submersível)",
                "rope pump": "rope pump (bomba de corda)",
                "handpump": "handpump (bomba manual)",
                "gravity": "gravity (gravidade)",
            }

            fig_e1 = go.Figure()
            fig_e1.add_trace(
                go.Bar(
                    y=[rotulos_ext.get(c, c) for c in tab_e1.index],
                    x=tab_e1["non functional"],
                    orientation="h",
                    marker_color=cores_e1,
                    text=[f"{fmt_pct(v)} (n = {fmt_int(n)})" for v, n in zip(tab_e1["non functional"], tab_e1["n"])],
                    textposition="outside",
                    customdata=np.stack([tab_e1["functional"], tab_e1["functional needs repair"], tab_e1["n"]], axis=-1),
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Não funcional: %{x:.1f}%<br>"
                        "Funcional: %{customdata[0]:.1f}%<br>"
                        "Precisa de reparo: %{customdata[1]:.1f}%<br>"
                        "Total no recorte: %{customdata[2]:,.0f}<extra></extra>"
                    ),
                )
            )
            fig_e1.add_vline(
                x=media_e1,
                line_dash="dash",
                line_color=COR_TEXTO_SECUNDARIO,
                line_width=1.3,
                annotation_text=f"Média (água suficiente): {fmt_pct(media_e1)}",
                annotation_position="top right",
                annotation_font=dict(size=11, color=COR_TEXTO),
            )
            fig_e1.update_layout(
                title=dict(
                    text="Mesmo com água suficiente, bombas motorizadas falham bem mais que gravidade e bombas manuais",
                    x=0.0,
                    font=dict(size=14.5),
                ),
                xaxis=dict(title="Taxa de pontos não funcionais (%)", range=[0, min(108, float(tab_e1["non functional"].max()) + 24)]),
                yaxis=dict(title="", automargin=True),
                showlegend=False,
            )
            aplicar_layout_base(fig_e1, altura=410, margem_topo=62, margem_baixo=44)
            st.plotly_chart(fig_e1, width="stretch")
            exibir_rodape_grafico(
                f"Fonte: DrivenData/Taarifa (Pump it Up) | 2011 a 2013 | Recorte quantity = enough dentro dos filtros ativos "
                f"(n = {fmt_int(len(sub_enough))}) | Pré-atentivos: cor por exceção (laranja vs. cinza) e ordenação por posição. "
                "*wind-powered possui amostra pequena."
            )

            col_t1, col_n1 = st.columns(2)
            with col_t1:
                with st.expander("Ver tabela alternativa (Explanatória 1)"):
                    tab_e1_show = tab_e1.iloc[::-1].copy()
                    tab_e1_show.columns = ["Funcional (%)", "Precisa reparo (%)", "Não funcional (%)", "Pontos (n)"]
                    st.dataframe(tab_e1_show.round(1), width="stretch")
            with col_n1:
                with st.expander("Nota analítica (Explanatória 1)"):
                    st.markdown(
                        "- **O que mostra:** percentual de pontos não funcionais por classe de extração restrito "
                        "somente aos pontos com água suficiente (`quantity = enough`, n = 33.150 na base limpa).\n"
                        "- **Insight:** mesmo com disponibilidade de água adequada, bombas motorizadas (`motorpump`, "
                        "45,9% inoperantes) e eólicas (`wind-powered`, 44,1%, amostra pequena de 59 registros) falham "
                        "muito mais que sistemas mecânicos simples como gravidade (`gravity`, 18,4%) e bombas manuais "
                        "(`handpump`, 23,5%). Tecnologias motorizadas tendem a depender de manutenção mais frequente e "
                        "especializada; já `other` (76,7%) aponta meios alternativos ou improvisados.\n"
                        "- **Por que este gráfico:** barra horizontal ordenada por taxa de falha, usando posição em eixo "
                        "comum (maior precisão perceptiva) e cor por exceção (laranja nas tecnologias críticas contra "
                        "cinza nos sistemas simples), além da linha de média do recorte."
                    )

    # EXPLANATORIA 2A
    with st.container(border=True):
        st.markdown("### Visualização Explanatória 2A: Efeito da idade na taxa de inoperância")
        val_idade = df_filt[df_filt["ausente_construction_year"] == 0].copy()

        if len(val_idade) == 0:
            st.info(
                "Os filtros atuais selecionaram apenas registros cujo ano de construção original estava ausente (MAR). "
                "Amplie a seleção regional para visualizar a relação real entre idade e inoperância.",
                title="Sem anos de construção reais neste recorte",
            )
        else:
            val_idade["faixa"] = pd.cut(
                val_idade["idade_no_registro"],
                bins=FAIXAS_IDADE_BINS,
                labels=FAIXAS_IDADE_LABELS,
            )
            tab_e2a = (
                pd.crosstab(val_idade["faixa"], val_idade[COL_ALVO], normalize="index")
                .reindex(index=FAIXAS_IDADE_LABELS, columns=STATUS_ORDEM, fill_value=0)
                .mul(100)
            )
            tab_e2a["n"] = val_idade["faixa"].value_counts().reindex(FAIXAS_IDADE_LABELS).fillna(0).astype(int)
            tab_e2a = tab_e2a[tab_e2a["n"] > 0]

            cores_e2a = [
                COR_LARANJA_ALERTA if faixa in {"21 a 30 anos", "Mais de 30 anos"}
                else ("#F0A070" if faixa == "16 a 20 anos" else COR_CINZA)
                for faixa in tab_e2a.index
            ]

            med_f_rec = val_idade.loc[val_idade[COL_ALVO] == "functional", "idade_no_registro"].median()
            med_nf_rec = val_idade.loc[val_idade[COL_ALVO] == "non functional", "idade_no_registro"].median()

            fig_e2a = go.Figure()
            fig_e2a.add_trace(
                go.Bar(
                    x=tab_e2a.index.tolist(),
                    y=tab_e2a["non functional"],
                    marker_color=cores_e2a,
                    text=[f"{fmt_pct(v)}<br>(n={fmt_int(n)})" for v, n in zip(tab_e2a["non functional"], tab_e2a["n"])],
                    textposition="outside",
                    name="Taxa de não funcionais",
                    customdata=np.stack([tab_e2a["functional"], tab_e2a["functional needs repair"], tab_e2a["n"]], axis=-1),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Não funcional: %{y:.1f}%<br>"
                        "Funcional: %{customdata[0]:.1f}%<br>"
                        "Precisa de reparo: %{customdata[1]:.1f}%<br>"
                        "Total na faixa: %{customdata[2]:,.0f}<extra></extra>"
                    ),
                )
            )
            fig_e2a.add_trace(
                go.Scatter(
                    x=tab_e2a.index.tolist(),
                    y=tab_e2a["non functional"],
                    mode="lines+markers",
                    line=dict(color=COR_TEXTO, width=2),
                    marker=dict(size=7, color=COR_TEXTO),
                    name="Tendência por faixa",
                    hoverinfo="skip",
                )
            )
            sub_med_txt = (
                f"Mediana no recorte: {fmt_num(med_f_rec, 0)} anos (funcionais) vs. "
                f"{fmt_num(med_nf_rec, 0)} anos (inoperantes)"
                if pd.notna(med_f_rec) and pd.notna(med_nf_rec)
                else "Evolução da taxa de pontos não funcionais conforme a idade da bomba"
            )
            fig_e2a.update_layout(
                title=dict(
                    text=f"Envelhecimento da rede: taxa de inoperância sobe com a idade ({sub_med_txt})",
                    x=0.0,
                    font=dict(size=14.2),
                ),
                xaxis=dict(title="Faixa de idade do ponto d'água no registro (idade_no_registro)"),
                yaxis=dict(title="Taxa de pontos não funcionais (%)", range=[0, min(105, float(tab_e2a["non functional"].max()) + 18)]),
                showlegend=False,
            )
            aplicar_layout_base(fig_e2a, altura=420, margem_topo=62, margem_baixo=50)
            st.plotly_chart(fig_e2a, width="stretch")
            exibir_rodape_grafico(
                f"Fonte: DrivenData/Taarifa (Pump it Up) | 2011 a 2013 | Somente registros com ano de construção informado "
                f"(ausente_construction_year = 0, n = {fmt_int(len(val_idade))}) | Pré-atentivos: cor laranja acima de 20 anos e linha de tendência."
            )

            col_t2a, col_n2a = st.columns(2)
            with col_t2a:
                with st.expander("Ver tabela alternativa (Explanatória 2A)"):
                    tab_e2a_show = tab_e2a.copy()
                    tab_e2a_show.columns = ["Funcional (%)", "Precisa reparo (%)", "Não funcional (%)", "Pontos (n)"]
                    st.dataframe(tab_e2a_show.round(1), width="stretch")
            with col_n2a:
                with st.expander("Nota analítica (Explanatória 2A)"):
                    st.markdown(
                        "- **O que mostra:** taxa de pontos não funcionais por faixa de idade (`idade_no_registro`), "
                        "considerando apenas os 38.674 registros com ano de construção informado (omitindo os 34,8% "
                        "ausentes sob mecanismo MAR).\n"
                        "- **Insight:** a idade separa claramente o estado operacional das bombas: a taxa de inoperância "
                        "sobe continuamente de 23,9% (0 a 5 anos) para 60,8% (mais de 30 anos), e a mediana de idade das "
                        "bombas quebradas (18 anos) é o dobro das funcionais (9 anos), com 14 anos nas que precisam de reparo.\n"
                        "- **Por que este gráfico:** barras em ordem cronológica combinadas a linha de tendência facilitam "
                        "enxergar a progressão contínua da falha com o envelhecimento, destacando em laranja as faixas acima de 20 anos."
                    )

    # EXPLANATORIA 2B
    with st.container(border=True):
        st.markdown("### Visualização Explanatória 2B: Desempenho preditivo e atributos mais influentes (Random Forest)")
        if df_metricas_csv.empty or df_imp_csv.empty:
            st.info("Os arquivos de métricas do classificador em out/parte_especifica/ não foram encontrados.")
        else:
            rf_cls = df_metricas_csv[
                (df_metricas_csv["modelo"] == "Random Forest") & (df_metricas_csv["classe"].isin(STATUS_ORDEM))
            ].copy()
            rf_cls["classe"] = pd.Categorical(rf_cls["classe"], categories=STATUS_ORDEM, ordered=True)
            rf_cls = rf_cls.sort_values("classe")

            c_left, c_right = st.columns(2)
            with c_left:
                fig_e2b_1 = go.Figure()
                rotulos_cls = [STATUS_ROTULO_PT[c] for c in rf_cls["classe"]]
                fig_e2b_1.add_trace(
                    go.Bar(
                        name="Precisão (%)",
                        x=rotulos_cls,
                        y=rf_cls["precisao"],
                        marker_color=[COR_CINZA, "#F5D08A", COR_CINZA],
                        text=[fmt_pct(v) for v in rf_cls["precisao"]],
                        textposition="outside",
                    )
                )
                fig_e2b_1.add_trace(
                    go.Bar(
                        name="Recall / Cobertura (%)",
                        x=rotulos_cls,
                        y=rf_cls["recall"],
                        marker_color=[COR_AZUL, COR_LARANJA_ALERTA, COR_AZUL],
                        text=[fmt_pct(v) for v in rf_cls["recall"]],
                        textposition="outside",
                    )
                )
                fig_e2b_1.update_layout(
                    barmode="group",
                    title=dict(
                        text="Random Forest (80,6% acurácia): gargalo de recall (27,0%) em 'Precisa de reparo'",
                        x=0.0,
                        font=dict(size=13.2),
                    ),
                    xaxis=dict(title="Situação real (status_group)"),
                    yaxis=dict(title="Desempenho no teste (%)", range=[0, 110]),
                    legend=dict(orientation="h", x=0.0, y=1.09),
                )
                aplicar_layout_base(fig_e2b_1, altura=420, margem_topo=82, margem_baixo=48)
                st.plotly_chart(fig_e2b_1, width="stretch")

            with c_right:
                # Grafico que nao mostra status_group -> cor de marca azul-principal (#0F62FE) vs cinza (#C6C6C6)
                top10 = df_imp_csv.head(10).iloc[::-1]
                destaque_vars = {"ward", "quantity", "extraction_type_class"}
                cores_imp = [COR_MARCA_PRINCIPAL if c in destaque_vars else COR_CINZA for c in top10["coluna"]]
                fig_e2b_2 = go.Figure()
                fig_e2b_2.add_trace(
                    go.Bar(
                        y=[f"{c} ({g})" for c, g in zip(top10["coluna"], top10["glossario"])],
                        x=top10["importancia_pct"],
                        orientation="h",
                        marker_color=cores_imp,
                        text=[fmt_pct(v) for v in top10["importancia_pct"]],
                        textposition="outside",
                        hovertemplate="<b>%{y}</b><br>Importância agregada: %{x:.2f}%<extra></extra>",
                    )
                )
                fig_e2b_2.update_layout(
                    title=dict(
                        text="Top 10 atributos mais relevantes no Random Forest",
                        x=0.0,
                        font=dict(size=13.2),
                    ),
                    xaxis=dict(title="Importância agregada (%)", range=[0, float(top10["importancia_pct"].max()) + 4.5]),
                    yaxis=dict(title="", automargin=True),
                    showlegend=False,
                )
                aplicar_layout_base(fig_e2b_2, altura=420, margem_topo=82, margem_baixo=48)
                st.plotly_chart(fig_e2b_2, width="stretch")

            exibir_rodape_grafico(
                "Fonte: DrivenData/Taarifa (Pump it Up) | RandomForestClassifier (200 árvores, hold-out 80/20 estratificado, "
                "teste n = 11.867, sem data leakage) | Pré-atentivos: laranja no recall da classe minoritária e azul de marca nos atributos-chave."
            )

            col_t2b, col_n2b = st.columns(2)
            with col_t2b:
                with st.expander("Ver tabela alternativa (Explanatória 2B)"):
                    st.dataframe(df_metricas_csv, width="stretch", hide_index=True)
            with col_n2b:
                with st.expander("Nota analítica (Explanatória 2B)"):
                    st.markdown(
                        "- **O que mostra:** Precisão e Recall por classe do `RandomForestClassifier` no conjunto de teste "
                        "estratificado (`n = 11.867`, sem data leakage) e o ranking das 10 variáveis mais importantes.\n"
                        "- **Insight:** o Random Forest atinge 80,58% de acurácia e separa bem bombas funcionais (recall "
                        "91,02%) e não funcionais (recall 75,96%), mas expõe o principal gargalo operacional na classe "
                        "minoritária `functional needs repair` (7,3% da base): precisão de 65,82%, porém recall baixo de "
                        "27,00%. As importâncias reforçam `quantity` (11,75%), `waterpoint_type_group` (5,08%) e "
                        "`extraction_type_class` (4,58%) junto aos sinais locais de `ward`, `funder`, `installer` e `lga`.\n"
                        "- **Por que este gráfico:** barras agrupadas com contraste de cor destacam imediatamente a queda "
                        "de recall na classe minoritária, enquanto o ranking horizontal ordenado organiza os atributos por relevância."
                    )


# =============================================================================
# ABA 2: EXPLORACAO INTERATIVA (4 EXPLORATORIAS + COMPARADOR LADO A LADO)
# =============================================================================
@st.fragment
def secao_exploratoria_categorica(df_base):
    """Fragmento isolado para selecao interativa de variavel categorica (SKILL Streamlit 1.67)."""
    st.markdown("#### Exploratória 2: Situação por variável categórica (seletor interativo)")
    ctrl_a, ctrl_b, ctrl_c = st.columns([1.45, 0.9, 0.9], vertical_alignment="bottom")
    with ctrl_a:
        var_cat = st.selectbox(
            "Variável categórica",
            options=list(ROTULOS_VARS_CAT.keys()),
            format_func=lambda k: ROTULOS_VARS_CAT[k],
            index=0,
            key="expl2_var_cat",
        )
    with ctrl_b:
        modo_e2 = st.segmented_control(
            "Escala",
            options=["Proporção (%)", "Contagem"],
            default="Proporção (%)",
            key="expl2_modo",
        ) or "Proporção (%)"
    with ctrl_c:
        ord_e2 = st.segmented_control(
            "Ordenar por",
            options=["Volume (n)", "% Inoperante"],
            default="Volume (n)",
            key="expl2_ordem",
        ) or "Volume (n)"

    tab_abs = pd.crosstab(df_base[var_cat], df_base[COL_ALVO]).reindex(columns=STATUS_ORDEM, fill_value=0)
    tab_pct = tab_abs.div(tab_abs.sum(axis=1), axis=0).mul(100)
    tab_pct["n"] = tab_abs.sum(axis=1)

    ordem_idx = (
        tab_pct.sort_values("n", ascending=True).index
        if ord_e2 == "Volume (n)"
        else tab_pct.sort_values("non functional", ascending=True).index
    )

    tab_plot = tab_pct.loc[ordem_idx] if modo_e2 == "Proporção (%)" else tab_abs.loc[ordem_idx]
    rotulos_y = [f"{cat} (n={fmt_int(tab_pct.loc[cat, 'n'])})" for cat in ordem_idx]

    fig_x2 = go.Figure()
    for st_val in STATUS_ORDEM:
        vals_s = tab_plot[st_val].values
        fig_x2.add_trace(
            go.Bar(
                y=rotulos_y,
                x=vals_s,
                orientation="h",
                name=STATUS_ROTULO_PT[st_val],
                marker_color=STATUS_CORES[st_val],
                hovertemplate=(
                    "<b>%{y}</b><br>" + STATUS_ROTULO_PT[st_val] +
                    (": %{x:.1f}%" if modo_e2 == "Proporção (%)" else ": %{x:,.0f}") +
                    "<extra></extra>"
                ),
            )
        )

    fig_x2.update_layout(
        barmode="stack",
        title=dict(text=f"Situação por {ROTULOS_VARS_CAT[var_cat]}", x=0.0, font=dict(size=13.5)),
        xaxis=dict(
            title="% dos pontos d'água na categoria" if modo_e2 == "Proporção (%)" else "Número de pontos d'água",
            range=[0, 100] if modo_e2 == "Proporção (%)" else None,
        ),
        yaxis=dict(title="", automargin=True),
        legend=dict(orientation="h", x=0.0, y=1.12, title=""),
    )
    altura_x2 = max(380, min(620, 32 * len(ordem_idx) + 120))
    aplicar_layout_base(fig_x2, altura=altura_x2, margem_topo=75, margem_baixo=45)
    st.plotly_chart(fig_x2, width="stretch")
    exibir_rodape_grafico(f"Fonte: DrivenData/Taarifa | 2011 a 2013 | n = {fmt_int(len(df_base))}")

    with st.expander("Tabela e Nota analítica (Exploratória 2)"):
        tab_show_e2 = tab_pct.loc[ordem_idx[::-1]].copy()
        tab_show_e2.columns = ["Funcional (%)", "Precisa reparo (%)", "Não funcional (%)", "Pontos (n)"]
        st.dataframe(tab_show_e2.round(1), width="stretch")
        st.markdown(
            "**Nota analítica:** Compara a distribuição proporcional (ou absoluta) da situação operacional dentro "
            "de cada categoria selecionada. Em `quantity`, pontos secos (`dry`, 96,9% inoperantes) e desconhecidos "
            "(`unknown`, 71,2%) concentram as maiores falhas; em `payment_type`, o predomínio de `never pay` (42,7% "
            "da base) também se associa a maior inoperância (48%). Barras 100% empilhadas facilitam comparar proporções "
            "entre categorias com volumes muito diferentes."
        )


@st.fragment
def secao_heatmap_multivariado(df_base):
    """Fragmento isolado para heatmap de quaisquer 2 variaveis categoricas (Bonus UX + arguicao)."""
    st.markdown("#### Exploratória 4: Cruzamento multivariado entre duas variáveis (Heatmap livre)")
    hm_c1, hm_c2, hm_c3, hm_c4 = st.columns([1.1, 1.1, 1.0, 0.9], vertical_alignment="bottom")
    vars_hm = [
        "extraction_type_class",
        "quantity",
        "waterpoint_type_group",
        "payment_type",
        "quality_group",
        "source_class",
        "management_group",
        "basin",
        "region",
        "faixa_idade",
    ]
    with hm_c1:
        var_lin = st.selectbox("Variável nas linhas", options=vars_hm, index=0, key="hm_var_lin")
    with hm_c2:
        var_col = st.selectbox("Variável nas colunas", options=vars_hm, index=1, key="hm_var_col")
    with hm_c3:
        alvo_hm = st.selectbox(
            "Métrica exibida na célula",
            options=STATUS_ORDEM[::-1],
            format_func=lambda s: f"% {STATUS_ROTULO_PT[s]}",
            index=0,
            key="hm_alvo",
        )
    with hm_c4:
        ocultar_ruido_hm = st.checkbox("Ocultar unknown e other", value=True, key="hm_ocultar_ruido")

    if var_lin == var_col:
        st.warning("Selecione duas variáveis diferentes para montar o cruzamento multivariado.")
        return

    sub_hm = df_base.copy()
    if ocultar_ruido_hm:
        sub_hm = sub_hm[
            (~sub_hm[var_lin].isin(["unknown", "other", "Other", "desconhecido"]))
            & (~sub_hm[var_col].isin(["unknown", "other", "Other", "desconhecido"]))
        ]

    if len(sub_hm) == 0:
        st.info("Sem registros suficientes após aplicar o filtro do heatmap.")
        return

    pv_pct = pd.crosstab(sub_hm[var_lin], sub_hm[var_col], values=(sub_hm[COL_ALVO] == alvo_hm), aggfunc="mean") * 100
    pv_n = pd.crosstab(sub_hm[var_lin], sub_hm[var_col])

    lin_ord = (
        [f for f in FAIXAS_IDADE_LABELS if f in pv_pct.index]
        if var_lin == "faixa_idade"
        else sub_hm[var_lin].value_counts().index.tolist()
    )
    if var_col == "quantity":
        col_ord = [q for q in ["enough", "insufficient", "seasonal", "dry", "unknown"] if q in pv_pct.columns]
    elif var_col == "faixa_idade":
        col_ord = [f for f in FAIXAS_IDADE_LABELS if f in pv_pct.columns]
    else:
        col_ord = sub_hm[var_col].value_counts().index.tolist()

    pv_pct = pv_pct.reindex(index=lin_ord, columns=col_ord)
    pv_n = pv_n.reindex(index=lin_ord, columns=col_ord).fillna(0).astype(int)

    text_mat = [
        [
            f"{fmt_pct(pv_pct.loc[r, c])}<br>(n={fmt_int(pv_n.loc[r, c])})"
            if pd.notna(pv_pct.loc[r, c]) and pv_n.loc[r, c] > 0
            else "-"
            for c in pv_pct.columns
        ]
        for r in pv_pct.index
    ]

    escala_hm = "YlOrRd" if alvo_hm == "non functional" else ("Blues" if alvo_hm == "functional" else "YlOrBr")
    fig_hm = go.Figure(
        data=go.Heatmap(
            z=pv_pct.values,
            x=pv_pct.columns.tolist(),
            y=pv_pct.index.tolist(),
            text=text_mat,
            texttemplate="%{text}",
            textfont=dict(size=10),
            colorscale=escala_hm,
            zmin=0,
            zmax=100,
            colorbar=dict(title=f"% {STATUS_ROTULO_PT[alvo_hm]}"),
            hovertemplate="<b>%{y} x %{x}</b><br>Taxa: %{z:.1f}%<extra></extra>",
        )
    )
    fig_hm.update_layout(
        title=dict(text=f"% de pontos '{STATUS_ROTULO_PT[alvo_hm]}': {var_lin} vs. {var_col}", x=0.0, font=dict(size=14)),
        xaxis=dict(title=var_col, side="bottom"),
        yaxis=dict(title=var_lin, autorange="reversed", automargin=True),
    )
    altura_hm = max(420, min(720, 46 * len(pv_pct.index) + 140))
    aplicar_layout_base(fig_hm, altura=altura_hm, margem_topo=60, margem_baixo=55)
    st.plotly_chart(fig_hm, width="stretch")
    exibir_rodape_grafico(
        f"Fonte: DrivenData/Taarifa | 2011 a 2013 | n = {fmt_int(len(sub_hm))} | "
        f"{'Exclui unknown/other' if ocultar_ruido_hm else 'Inclui todas as categorias'}"
    )

    with st.expander("Tabela numérica e Nota analítica (Exploratória 4)"):
        st.dataframe(pv_pct.round(1), width="stretch")
        st.markdown(
            "**Nota analítica:** Cruza duas variáveis categóricas exibindo o percentual da situação escolhida e o volume "
            "`n` em cada célula. No cruzamento padrão (`extraction_type_class` x `quantity`), pontos secos falham em "
            "quase todas as tecnologias (90% a 100%), mas na coluna `enough` aparece o contraste que originou a "
            "Explanatória 1 (`motorpump` com 45,9% vs. `gravity` com 18,4%). O mapa de calor é o formato mais direto "
            "para detectar padrões combinados entre duas variáveis qualitativas."
        )


@st.fragment
def secao_comparador_regioes(df_base_total):
    """Bonus UX: comparacao lado a lado de duas regioes da Tanzania."""
    st.markdown("#### Comparador lado a lado entre duas regiões (Bônus UX)")
    regioes_disp = sorted(df_base_total["region"].unique().tolist())
    idx_a = regioes_disp.index("Iringa") if "Iringa" in regioes_disp else 0
    idx_b = regioes_disp.index("Lindi") if "Lindi" in regioes_disp else min(1, len(regioes_disp) - 1)

    sel1, sel2 = st.columns(2)
    with sel1:
        reg_a = st.selectbox("Região A (referência)", options=regioes_disp, index=idx_a, key="comp_reg_a")
    with sel2:
        reg_b = st.selectbox("Região B (comparação)", options=regioes_disp, index=idx_b, key="comp_reg_b")

    df_a = df_base_total[df_base_total["region"] == reg_a]
    df_b = df_base_total[df_base_total["region"] == reg_b]

    col_a, col_b = st.columns(2)
    for col_box, nome_r, sub_r in [(col_a, reg_a, df_a), (col_b, reg_b, df_b)]:
        with col_box:
            with st.container(border=True):
                nf_r = (sub_r[COL_ALVO] == "non functional").mean() * 100
                fn_r = (sub_r[COL_ALVO] == "functional").mean() * 100
                rp_r = (sub_r[COL_ALVO] == "functional needs repair").mean() * 100
                dry_r = (sub_r["quantity"] == "dry").mean() * 100
                top_ext = sub_r["extraction_type_class"].mode().iloc[0]

                st.markdown(f"**{nome_r}** (n = {fmt_int(len(sub_r))})")
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Funcionais", fmt_pct(fn_r))
                mc2.metric("Não funcionais", fmt_pct(nf_r))
                mc3.metric("Poços secos", fmt_pct(dry_r))
                st.caption(f"Precisam de reparo: {fmt_pct(rp_r)} | Tecnologia predominante: {top_ext}")

    # Grafico comparativo direto de status_group lado a lado
    df_comp_plot = pd.DataFrame([
        {
            "Região": nome_r,
            "Situação": STATUS_ROTULO_PT[s],
            "status_raw": s,
            "Percentual (%)": (sub_r[COL_ALVO] == s).mean() * 100,
        }
        for nome_r, sub_r in [(reg_a, df_a), (reg_b, df_b)]
        for s in STATUS_ORDEM
    ])
    fig_comp = go.Figure()
    for s in STATUS_ORDEM:
        sub_s = df_comp_plot[df_comp_plot["status_raw"] == s]
        fig_comp.add_trace(
            go.Bar(
                name=STATUS_ROTULO_PT[s],
                x=sub_s["Região"],
                y=sub_s["Percentual (%)"],
                marker_color=STATUS_CORES[s],
                text=[fmt_pct(v) for v in sub_s["Percentual (%)"]],
                textposition="outside",
            )
        )
    fig_comp.update_layout(
        barmode="group",
        title=dict(text=f"Comparação direta de situação operacional: {reg_a} vs. {reg_b}", x=0.0, font=dict(size=13.5)),
        yaxis=dict(title="Percentual na região (%)", range=[0, 100]),
        xaxis=dict(title=""),
        legend=dict(orientation="h", x=0.0, y=1.12, title=""),
    )
    aplicar_layout_base(fig_comp, altura=340, margem_topo=68, margem_baixo=40)
    st.plotly_chart(fig_comp, width="stretch")
    exibir_rodape_grafico(
        f"Fonte: DrivenData/Taarifa | 2011 a 2013 | {reg_a} (n = {fmt_int(len(df_a))}) vs. {reg_b} (n = {fmt_int(len(df_b))})"
    )


with aba_expl:
    st.subheader("Exploração interativa do comportamento dos dados")
    st.caption("As 4 visualizações exploratórias respondem aos filtros da barra lateral.")

    c_e1, c_e2 = st.columns([0.9, 1.35])
    with c_e1:
        with st.container(border=True):
            st.markdown("#### Exploratória 1: Distribuição da situação operacional")
            cont_st = df_filt[COL_ALVO].value_counts().reindex(STATUS_ORDEM).fillna(0).astype(int)
            pct_st = cont_st / len(df_filt) * 100

            fig_x1 = go.Figure()
            fig_x1.add_trace(
                go.Bar(
                    x=[STATUS_ROTULO_PT[s] for s in STATUS_ORDEM],
                    y=cont_st.values,
                    marker_color=[STATUS_CORES[s] for s in STATUS_ORDEM],
                    text=[f"{fmt_int(n)}<br>({fmt_pct(p)})" for n, p in zip(cont_st.values, pct_st.values)],
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>Pontos d'água: %{y:,.0f}<extra></extra>",
                )
            )
            fig_x1.update_layout(
                title=dict(text="Distribuição de status_group no recorte", x=0.0, font=dict(size=13.5)),
                xaxis=dict(title="Situação operacional"),
                yaxis=dict(title="Número de pontos d'água", range=[0, float(cont_st.max()) * 1.24 if cont_st.max() > 0 else 1]),
                showlegend=False,
            )
            aplicar_layout_base(fig_x1, altura=440, margem_topo=55, margem_baixo=48)
            st.plotly_chart(fig_x1, width="stretch")
            exibir_rodape_grafico(f"Fonte: DrivenData/Taarifa | 2011 a 2013 | n = {fmt_int(len(df_filt))}")

            with st.expander("Tabela e Nota analítica (Exploratória 1)"):
                st.dataframe(
                    pd.DataFrame({
                        "Situação": [STATUS_ROTULO_PT[s] for s in STATUS_ORDEM],
                        "Pontos (n)": cont_st.values,
                        "Proporção (%)": pct_st.round(2).values,
                    }),
                    width="stretch",
                    hide_index=True,
                )
                st.markdown(
                    "**Nota analítica:** Mostra a contagem e a proporção das três classes de `status_group`. "
                    "A base é fortemente desbalanceada (54,3% funcionais, 38,4% não funcionais e apenas 7,3% precisando de reparo), "
                    "o que exige acompanhar precisão, recall e F1 por classe além da acurácia. "
                    "Gráfico de barras verticais escolhido por comparar diretamente o volume de categorias nominais com eixo partindo do zero."
                )

    with c_e2:
        with st.container(border=True):
            secao_exploratoria_categorica(df_filt)

    # EXPLORATORIA 3: Ranking regional + Mapa
    with st.container(border=True):
        st.markdown("#### Exploratória 3: Contraste regional e distribuição geográfica")
        m_ctrl1, m_ctrl2 = st.columns([1.2, 1.0], vertical_alignment="bottom")
        with m_ctrl1:
            amostra_mapa = st.slider(
                "Máximo de pontos exibidos no mapa (amostra com seed = 42)",
                min_value=2000,
                max_value=15000,
                value=6000,
                step=1000,
            )
        with m_ctrl2:
            usar_mapa_osm = st.toggle(
                "Usar mapa base cartográfico (Carto Positron)",
                value=True,
                help="Desligue caso esteja offline para exibir dispersão simples de longitude x latitude.",
            )

        col_reg, col_map = st.columns([1.0, 1.2])
        with col_reg:
            tab_reg = (
                pd.crosstab(df_filt["region"], df_filt[COL_ALVO], normalize="index")
                .reindex(columns=STATUS_ORDEM, fill_value=0)
                .mul(100)
            )
            tab_reg["n"] = df_filt["region"].value_counts()
            tab_reg = tab_reg.sort_values("non functional", ascending=True)
            media_reg = (df_filt[COL_ALVO] == "non functional").mean() * 100

            fig_reg = go.Figure()
            fig_reg.add_trace(
                go.Bar(
                    y=[f"{r} (n={fmt_int(n)})" for r, n in zip(tab_reg.index, tab_reg["n"])],
                    x=tab_reg["non functional"],
                    orientation="h",
                    marker_color=COR_LARANJA_ALERTA,
                    text=[fmt_pct(v) for v in tab_reg["non functional"]],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Não funcional: %{x:.1f}%<extra></extra>",
                )
            )
            fig_reg.add_vline(
                x=media_reg,
                line_dash="dash",
                line_color=COR_TEXTO,
                annotation_text=f"Média: {fmt_pct(media_reg)}",
                annotation_position="bottom right",
            )
            fig_reg.update_layout(
                title=dict(text="Taxa de inoperância (%) por região", x=0.0, font=dict(size=13.5)),
                xaxis=dict(title="% de pontos não funcionais", range=[0, min(105, float(tab_reg["non functional"].max()) + 16)]),
                yaxis=dict(title="", automargin=True),
                showlegend=False,
            )
            aplicar_layout_base(fig_reg, altura=520, margem_topo=55, margem_baixo=44)
            st.plotly_chart(fig_reg, width="stretch")

        with col_map:
            geo = df_filt[df_filt["ausente_coords"] == 0].copy()
            if len(geo) == 0:
                st.info("Não há pontos com coordenadas GPS reais neste recorte.")
            else:
                geo_plot = geo.sample(n=amostra_mapa, random_state=42) if len(geo) > amostra_mapa else geo
                geo_plot["situacao_pt"] = geo_plot[COL_ALVO].map(STATUS_ROTULO_PT)
                cores_pt = {STATUS_ROTULO_PT[k]: v for k, v in STATUS_CORES.items()}

                if usar_mapa_osm:
                    fig_map = px.scatter_map(
                        geo_plot,
                        lat="latitude",
                        lon="longitude",
                        color="situacao_pt",
                        color_discrete_map=cores_pt,
                        category_orders={"situacao_pt": [STATUS_ROTULO_PT[s] for s in STATUS_ORDEM]},
                        hover_name="region",
                        hover_data={
                            "lga": True,
                            "quantity": True,
                            "extraction_type_class": True,
                            "idade_no_registro": True,
                            "latitude": ":.3f",
                            "longitude": ":.3f",
                            "situacao_pt": False,
                        },
                        zoom=4.8,
                        center=dict(lat=float(geo_plot["latitude"].median()), lon=float(geo_plot["longitude"].median())),
                        map_style="carto-positron",
                        opacity=0.65,
                    )
                    fig_map.update_traces(marker=dict(size=5))
                else:
                    fig_map = px.scatter(
                        geo_plot,
                        x="longitude",
                        y="latitude",
                        color="situacao_pt",
                        color_discrete_map=cores_pt,
                        category_orders={"situacao_pt": [STATUS_ROTULO_PT[s] for s in STATUS_ORDEM]},
                        hover_name="region",
                        hover_data={"lga": True, "quantity": True, "extraction_type_class": True, "situacao_pt": False},
                        opacity=0.55,
                    )
                    fig_map.update_traces(marker=dict(size=4))
                    fig_map.update_xaxes(title="Longitude")
                    fig_map.update_yaxes(title="Latitude")

                fig_map.update_layout(
                    title=dict(
                        text=f"Mapa geográfico ({fmt_int(len(geo_plot))} de {fmt_int(len(geo))} pontos com GPS real)",
                        x=0.0,
                        font=dict(size=13.5),
                    ),
                    legend=dict(orientation="h", x=0.0, y=1.08, title=""),
                )
                aplicar_layout_base(fig_map, altura=520, margem_topo=70, margem_baixo=20)
                st.plotly_chart(fig_map, width="stretch")

        exibir_rodape_grafico(
            f"Fonte: DrivenData/Taarifa | 2011 a 2013 | Ranking: n = {fmt_int(len(df_filt))}; "
            f"Mapa (ausente_coords = 0): n = {fmt_int(len(df_filt[df_filt['ausente_coords'] == 0]))}"
        )
        with st.expander("Tabela regional e Nota analítica (Exploratória 3)"):
            tab_reg_show = tab_reg.iloc[::-1].copy()
            tab_reg_show.columns = ["Funcional (%)", "Precisa reparo (%)", "Não funcional (%)", "Pontos (n)"]
            st.dataframe(tab_reg_show.round(1), width="stretch")
            st.markdown(
                "**Nota analítica:** Reúne o ranking ordenado das 21 regiões administrativas por percentual de pontos "
                "não funcionais e a distribuição espacial das bombas com coordenadas reais (`ausente_coords = 0`). "
                "Há forte contraste territorial entre regiões como Iringa (19,5% inoperantes) e Arusha (26,3%) frente a "
                "Lindi (64,2%), Mtwara (62,4%) e Tabora (54,4%). A combinação de barras horizontais ordenadas com mapa "
                "permite ao gestor comparar o ranking exato e localizar concentrações críticas no território."
            )

    # EXPLORATORIA 4 (fragmento isolado)
    with st.container(border=True):
        secao_heatmap_multivariado(df_filt)

    # COMPARADOR LADO A LADO DE DUAS REGIOES (Bonus UX)
    with st.container(border=True):
        secao_comparador_regioes(df_total)

    # Extra recolhido: diagnostico de qualidade MAR por regiao
    with st.expander("Diagnóstico de qualidade da base: mecanismo de ausência MAR por região"):
        cols_flags = ["ausente_population", "ausente_construction_year", "ausente_gps_height", "ausente_coords"]
        mar_reg = df_filt.groupby("region")[cols_flags].mean().mul(100)
        mar_reg = mar_reg.sort_values("ausente_construction_year", ascending=False)
        fig_mar = px.imshow(
            mar_reg.round(1),
            text_auto=".1f",
            color_continuous_scale="YlOrRd",
            zmin=0,
            zmax=100,
            labels=dict(x="Indicador de ausência original", y="Região", color="% ausente"),
            aspect="auto",
        )
        fig_mar.update_layout(
            title=dict(text="Percentual de zeros suspeitos originais por região (evidência de MAR)", x=0.0, font=dict(size=13.5))
        )
        aplicar_layout_base(fig_mar, altura=520, margem_topo=55, margem_baixo=44)
        st.plotly_chart(fig_mar, width="stretch")
        exibir_rodape_grafico(
            f"Fonte: DrivenData/Taarifa | 2011 a 2013 | Flags binárias ausente_* salvas antes da imputação em cascata (n = {fmt_int(len(df_filt))})"
        )


# =============================================================================
# ABA 3: CLASSIFICADOR E AUDITORIA (ISOLADO EM FRAGMENT)
# =============================================================================
@st.fragment
def secao_demo_classificador(bundle, df_base_total):
    """Fragmento isolado para sorteio ao vivo de 3 bombas, mapa, probabilidades e auditoria decision_path."""
    pipe_dt = bundle["pipe_dt"]
    pipe_rf = bundle["pipe_rf"]
    X_test = bundle["X_test"]
    y_test = bundle["y_test"]

    st.markdown("### Teste ao vivo em bombas reais do conjunto de teste")
    st.write(
        "Sorteie 3 bombas reais que nunca foram vistas durante o treinamento e compare a previsão e as probabilidades "
        "do Random Forest com a trilha auditável de decisões da Árvore de Decisão."
    )

    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1.2, 1.0, 1.15, 1.0], vertical_alignment="bottom")
    with ctrl1:
        modelo_demo = st.selectbox(
            "Modelo para avaliação",
            options=["Ambos", "Random Forest", "Arvore de Decisao"],
            index=0,
            key="clf_modelo_demo",
        )
    with ctrl2:
        modo_vis = st.segmented_control(
            "Exibição das fichas",
            options=["Cartões", "Tabela"],
            default="Cartões",
            key="clf_modo_vis",
        ) or "Cartões"
    with ctrl3:
        uma_por_classe = st.checkbox("Garantir 1 bomba de cada classe", value=True, key="clf_uma_por_classe")
    with ctrl4:
        if st.button("Sortear 3 novas bombas", width="stretch", type="primary", key="btn_sortear_bombas"):
            st.session_state["seed_sorteio"] += 1

    seed_atual = st.session_state["seed_sorteio"]
    if uma_por_classe:
        indices_sort = [y_test[y_test == cls].sample(1, random_state=seed_atual).index[0] for cls in STATUS_ORDEM]
    else:
        indices_sort = list(X_test.sample(3, random_state=seed_atual).index)

    X_amostra = X_test.loc[indices_sort]
    y_amostra = y_test.loc[indices_sort]
    ficha_sort = df_base_total.loc[indices_sort].copy()

    mapa_pipes = {"Arvore de Decisao": pipe_dt, "Random Forest": pipe_rf}
    escolhidos = list(mapa_pipes.keys()) if modelo_demo == "Ambos" else [modelo_demo]

    registros_pred = []
    for nome_m in escolhidos:
        pipe_m = mapa_pipes[nome_m]
        preds_m = pipe_m.predict(X_amostra)
        probs_m = pipe_m.predict_proba(X_amostra)
        idx_ord = [list(pipe_m.classes_).index(c) for c in STATUS_ORDEM]

        for k, (idx_r, real_c, pred_c, prob_v) in enumerate(zip(indices_sort, y_amostra, preds_m, probs_m), start=1):
            p_ord = prob_v[idx_ord] * 100
            registros_pred.append({
                "bomba": f"Bomba #{k}",
                "id": int(df_base_total.loc[idx_r, "id"]),
                "modelo": nome_m,
                "classe_real": real_c,
                "classe_prevista": pred_c,
                "acertou": "Acertou" if pred_c == real_c else "Errou",
                "prob_func": round(float(p_ord[0]), 1),
                "prob_rep": round(float(p_ord[1]), 1),
                "prob_nf": round(float(p_ord[2]), 1),
            })

    df_pred_demo = pd.DataFrame(registros_pred)

    if modo_vis == "Cartões":
        cards_cols = st.columns(3)
        for k, (col_c, idx_r) in enumerate(zip(cards_cols, indices_sort), start=1):
            row_f = df_base_total.loc[idx_r]
            sub_p = df_pred_demo[df_pred_demo["bomba"] == f"Bomba #{k}"]
            with col_c:
                with st.container(border=True):
                    st.markdown(f"**Bomba #{k} (ID {int(row_f['id'])})**")
                    st.caption(f"{row_f['region']} | {row_f['lga']} | {row_f['ward']}")
                    st.markdown(
                        f"Situação real: **{STATUS_ROTULO_PT[row_f[COL_ALVO]]}**  \n"
                        f"Água (`quantity`): {row_f['quantity']}  \n"
                        f"Extração: {row_f['extraction_type_class']}  \n"
                        f"Tipo: {row_f['waterpoint_type_group']}  \n"
                        f"Idade: {int(row_f['idade_no_registro'])} anos | Pagamento: {row_f['payment_type']}  \n"
                        f"Financiador: {row_f['funder']}"
                    )
                    st.divider()
                    for _, rp in sub_p.iterrows():
                        cor_tag = "#198038" if rp["acertou"] == "Acertou" else "#DA1E28"
                        bg_tag = "#DEFBE6" if rp["acertou"] == "Acertou" else "#FFF1F1"
                        st.html(
                            f"<div style='font-size:0.86rem; margin-bottom:4px;'>"
                            f"<b>{rp['modelo']}:</b> {STATUS_ROTULO_PT[rp['classe_prevista']]} "
                            f"<span style='background:{bg_tag}; color:{cor_tag}; font-weight:700; "
                            f"padding:1px 6px; border-radius:3px;'>{rp['acertou']}</span></div>"
                        )
    else:
        cols_ficha_tab = [
            "id", "region", "lga", "ward", "quantity", "extraction_type_class",
            "waterpoint_type_group", "idade_no_registro", "payment_type", COL_ALVO,
        ]
        tab_f = ficha_sort[cols_ficha_tab].copy()
        tab_f.insert(0, "bomba", [f"Bomba #{k}" for k in range(1, 4)])
        st.dataframe(tab_f, width="stretch", hide_index=True)

    g_prob_col, g_map_col = st.columns([1.35, 0.95])
    with g_prob_col:
        fig_probs = make_subplots(
            rows=1,
            cols=3,
            subplot_titles=[
                f"Bomba #{k} (real: {STATUS_ROTULO_PT[y_amostra.iloc[k - 1]]})" for k in range(1, 4)
            ],
            shared_yaxes=True,
        )
        cores_modelos = {"Arvore de Decisao": COR_CINZA, "Random Forest": COR_MARCA_PRINCIPAL}
        rot_curto = ["Funcional", "Reparo", "Não func."]

        for k in range(1, 4):
            sub_k = df_pred_demo[df_pred_demo["bomba"] == f"Bomba #{k}"]
            for _, rm in sub_k.iterrows():
                vals_p = [rm["prob_func"], rm["prob_rep"], rm["prob_nf"]]
                fig_probs.add_trace(
                    go.Bar(
                        x=rot_curto,
                        y=vals_p,
                        name=rm["modelo"],
                        marker_color=cores_modelos[rm["modelo"]],
                        text=[f"{v:.0f}%" for v in vals_p],
                        textposition="outside",
                        showlegend=(k == 1),
                        legendgroup=rm["modelo"],
                    ),
                    row=1,
                    col=k,
                )
        fig_probs.update_yaxes(range=[0, 118], title_text="Probabilidade (%)", col=1)
        fig_probs.update_layout(
            barmode="group",
            title=dict(text=f"Probabilidades previstas nas 3 bombas reais (seed = {seed_atual})", x=0.0, font=dict(size=13.5)),
            legend=dict(orientation="h", x=0.32, y=1.18, title=""),
        )
        aplicar_layout_base(fig_probs, altura=365, margem_topo=85, margem_baixo=40)
        st.plotly_chart(fig_probs, width="stretch")

    with g_map_col:
        ficha_map = ficha_sort.copy()
        ficha_map["rotulo"] = [f"Bomba #{k} (ID {int(i)})" for k, i in enumerate(ficha_map["id"], start=1)]
        ficha_map["situacao_pt"] = ficha_map[COL_ALVO].map(STATUS_ROTULO_PT)
        cores_pt = {STATUS_ROTULO_PT[k]: v for k, v in STATUS_CORES.items()}
        fig_m3 = px.scatter_map(
            ficha_map,
            lat="latitude",
            lon="longitude",
            color="situacao_pt",
            color_discrete_map=cores_pt,
            hover_name="rotulo",
            hover_data={"region": True, "lga": True, "quantity": True, "extraction_type_class": True, "situacao_pt": False},
            zoom=4.5,
            center=dict(lat=-6.3, lon=34.9),
            map_style="carto-positron",
        )
        fig_m3.update_traces(marker=dict(size=13))
        fig_m3.update_layout(
            title=dict(text="Localização das 3 bombas sorteadas", x=0.0, font=dict(size=13.5)),
            legend=dict(orientation="h", x=0.0, y=1.12, title=""),
        )
        aplicar_layout_base(fig_m3, altura=365, margem_topo=70, margem_baixo=20)
        st.plotly_chart(fig_m3, width="stretch")

    if "Arvore de Decisao" in escolhidos:
        with st.expander("Auditoria da Árvore de Decisão: trilha real de perguntas da raiz até a folha", expanded=True):
            trilhas = {}
            finais = {}
            max_p = 0
            for k, idx_r in enumerate(indices_sort, start=1):
                regras, _, n_folha = auditar_arvore(pipe_dt, X_amostra.loc[[idx_r]])
                row_dt = df_pred_demo[
                    (df_pred_demo["bomba"] == f"Bomba #{k}") & (df_pred_demo["modelo"] == "Arvore de Decisao")
                ].iloc[0]
                col_n = f"Bomba #{k} (ID {row_dt['id']} | {row_dt['acertou']})"
                trilhas[col_n] = regras
                finais[col_n] = (
                    f"Prevista: {STATUS_ROTULO_PT[row_dt['classe_prevista']]} "
                    f"(real: {STATUS_ROTULO_PT[row_dt['classe_real']]}, folha n={n_folha})"
                )
                max_p = max(max_p, len(regras))

            dados_aud = {
                cn: rg + ["-"] * (max_p - len(rg)) + [finais[cn]]
                for cn, rg in trilhas.items()
            }
            df_aud = pd.DataFrame(dados_aud, index=[f"Passo {p}" for p in range(1, max_p + 1)] + ["Decisão na folha"])
            st.dataframe(df_aud, width="stretch")


@st.fragment
def secao_simulador_bomba(bundle, df_base_total):
    """Fragmento isolado para o formulario de simulacao ilustrativa."""
    pipe_dt = bundle["pipe_dt"]
    pipe_rf = bundle["pipe_rf"]
    X_test = bundle["X_test"]

    with st.expander("Simular classificação para um perfil de ponto d'água (simulação ilustrativa)"):
        st.caption(
            "Os demais atributos não escolhidos assumem o valor mediano ou modal da base tratada. "
            "Resultado ilustrativo para apoio à decisão operacional."
        )
        with st.form("form_simulador"):
            s1, s2, s3 = st.columns(3)
            with s1:
                sim_reg = st.selectbox("Região (region)", sorted(df_base_total["region"].unique().tolist()))
                sim_q = st.selectbox("Disponibilidade de água (quantity)", ["enough", "insufficient", "seasonal", "dry", "unknown"])
            with s2:
                sim_ext = st.selectbox("Tecnologia de extração", df_base_total["extraction_type_class"].value_counts().index.tolist())
                sim_wpt = st.selectbox("Tipo de ponto d'água", df_base_total["waterpoint_type_group"].value_counts().index.tolist())
            with s3:
                sim_pag = st.selectbox("Forma de pagamento", df_base_total["payment_type"].value_counts().index.tolist())
                sim_idade = st.slider("Idade estimada (anos)", 0, 50, 12)

            rodar_sim = st.form_submit_button("Simular classificação", type="primary")

        if rodar_sim:
            linha_sim = dict(bundle["perfil_base"])
            sub_r = df_base_total[df_base_total["region"] == sim_reg]
            linha_sim["region"] = sim_reg
            linha_sim["basin"] = str(sub_r["basin"].mode().iloc[0])
            linha_sim["lga"] = str(sub_r["lga"].mode().iloc[0])
            linha_sim["ward"] = str(sub_r["ward"].mode().iloc[0])
            linha_sim["longitude"] = float(sub_r["longitude"].median())
            linha_sim["latitude"] = float(sub_r["latitude"].median())
            linha_sim["gps_height"] = float(sub_r["gps_height"].median())
            linha_sim["quantity"] = sim_q
            linha_sim["extraction_type_class"] = sim_ext
            linha_sim["waterpoint_type_group"] = sim_wpt
            linha_sim["payment_type"] = sim_pag
            linha_sim["ano_registro"] = 2013
            linha_sim["construction_year"] = float(2013 - sim_idade)
            linha_sim["ausente_construction_year"] = 0
            linha_sim["ausente_gps_height"] = 0
            linha_sim["ausente_population"] = 0
            linha_sim["ausente_coords"] = 0

            X_sim = pd.DataFrame([linha_sim])[X_test.columns]
            pred_rf_s = pipe_rf.predict(X_sim)[0]
            prob_rf_s = pipe_rf.predict_proba(X_sim)[0]
            idx_ord_s = [list(pipe_rf.classes_).index(c) for c in STATUS_ORDEM]
            p_rf_ord = prob_rf_s[idx_ord_s] * 100

            pred_dt_s = pipe_dt.predict(X_sim)[0]
            regras_sim, _, n_folha_s = auditar_arvore(pipe_dt, X_sim)

            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.metric("Previsão Random Forest", STATUS_ROTULO_PT[pred_rf_s])
                st.write(
                    f"Probabilidades: Funcional {fmt_pct(p_rf_ord[0])} | "
                    f"Precisa de reparo {fmt_pct(p_rf_ord[1])} | "
                    f"Não funcional {fmt_pct(p_rf_ord[2])}"
                )
            with r_col2:
                st.metric("Previsão Árvore de Decisão", STATUS_ROTULO_PT[pred_dt_s])
                st.caption(f"Trilha com {len(regras_sim)} regras até folha com {n_folha_s} exemplos de treino.")
            st.dataframe(
                pd.DataFrame({"Passo": [f"Passo {i}" for i in range(1, len(regras_sim) + 1)], "Regra aplicada": regras_sim}),
                width="stretch",
                hide_index=True,
            )


with aba_clf:
    st.subheader("Classificador supervisionado e auditoria passo a passo")
    st.caption(
        "Pipelines reproduzidos de src/parte_especifica/classificador.ipynb (split 80/20 estratificado, "
        "imputação em cascata e Target Encoding ajustados somente no treino para evitar data leakage)."
    )

    bundle = treinar_classificadores()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric("Acurácia Árvore (baseline)", fmt_pct(bundle["acc_dt"], 2))
    with m2:
        with st.container(border=True):
            st.metric(
                "Acurácia Random Forest",
                fmt_pct(bundle["acc_rf"], 2),
                delta=f"+{fmt_num(bundle['acc_rf'] - bundle['acc_dt'], 2)} pp",
            )
    with m3:
        with st.container(border=True):
            st.metric("Conjunto de teste (20%)", fmt_int(len(bundle["X_test"])), delta="Estratificado", delta_color="off")
    with m4:
        with st.container(border=True):
            st.metric("Árvores no Random Forest", "200", delta="min_samples_leaf = 2", delta_color="off")

    with st.container(border=True):
        c_cm1, c_cm2 = st.columns(2)
        rotulos_cm = [STATUS_ROTULO_PT[s] for s in STATUS_ORDEM]
        escala_azul_marca = [[0.0, "#EAF2FF"], [0.35, "#A6C8FF"], [0.7, "#4589FF"], [0.9, "#0F62FE"], [1.0, "#062A5F"]]
        for col_box, nome_m, cm_mat in [
            (c_cm1, "Árvore de Decisão (baseline)", bundle["cm_dt"]),
            (c_cm2, "Random Forest (200 árvores)", bundle["cm_rf"]),
        ]:
            cm_pct = cm_mat / cm_mat.sum(axis=1, keepdims=True) * 100
            txt_cm = [
                [f"{fmt_pct(cm_pct[i, j])}<br>(n={fmt_int(cm_mat[i, j])})" for j in range(3)]
                for i in range(3)
            ]
            fig_cm = go.Figure(
                data=go.Heatmap(
                    z=cm_pct,
                    x=rotulos_cm,
                    y=rotulos_cm,
                    text=txt_cm,
                    texttemplate="%{text}",
                    colorscale=escala_azul_marca,
                    zmin=0,
                    zmax=100,
                    showscale=False,
                    hovertemplate="Real: %{y}<br>Prevista: %{x}<br>Recall na linha: %{z:.1f}%<extra></extra>",
                )
            )
            fig_cm.update_layout(
                title=dict(text=f"Matriz de confusão (% por classe real): {nome_m}", x=0.0, font=dict(size=13)),
                xaxis=dict(title="Classe prevista"),
                yaxis=dict(title="Classe real", autorange="reversed"),
            )
            aplicar_layout_base(fig_cm, altura=360, margem_topo=50, margem_baixo=48)
            with col_box:
                st.plotly_chart(fig_cm, width="stretch")

        exibir_rodape_grafico(
            "Fonte: DrivenData/Taarifa (Pump it Up) | Avaliação exclusiva no conjunto de teste (n = 11.867, random_state = 42)"
        )

    with st.container(border=True):
        secao_demo_classificador(bundle, df_total)

    secao_simulador_bomba(bundle, df_total)


# =============================================================================
# ABA 4: PARTE COMUM (K-MEANS OBESITY + ANIMACAO DE TRANSICAO - BONUS +1,0)
# =============================================================================
@st.fragment
def secao_parte_comum_kmeans():
    """Bonus Visual/UX (+1,0): pagina da Parte Comum e animacao de transicao Passada 1 -> Passada 2 do K-Means."""
    st.subheader("Parte Comum: Agrupamento K-Means no dataset Obesity (Bônus Visual/UX)")
    st.caption(
        "Dataset UCI 544 (Obesity, 2.111 registros e 7 classes em NObeyesdad). "
        "Padronização com StandardScaler nas 8 variáveis numéricas, curva do Cotovelo e transição animada entre as duas passadas (PCA 2D)."
    )

    k_escolhido = st.slider(
        "Valor de k para a Passada 1 (k livre sugerido pelo Método do Cotovelo)",
        min_value=2,
        max_value=10,
        value=4,
        key="kmeans_k_livre",
    )

    res_km = executar_kmeans_parte_comum(k_livre=k_escolhido)
    if res_km is None:
        st.warning("Arquivo data/parte_comum/obesity/ObesityDataSet_raw_and_data_sinthetic.csv não encontrado.")
        return

    p1 = res_km["passada_1"]
    p2 = res_km["passada_2"]

    km1, km2, km3, km4 = st.columns(4)
    with km1:
        with st.container(border=True):
            st.metric("Registros Obesity", fmt_int(res_km["n_linhas"]), delta=f"{res_km['n_classes']} classes reais", delta_color="off")
    with km2:
        with st.container(border=True):
            st.metric(f"Coincidência Passada 1 (k = {p1['k']})", fmt_pct(p1["acc"], 1))
    with km3:
        with st.container(border=True):
            st.metric(
                f"Coincidência Passada 2 (k = {p2['k']})",
                fmt_pct(p2["acc"], 1),
                delta=f"{fmt_num(p2['acc'] - p1['acc'], 1)} pp vs. Passada 1",
            )
    with km4:
        with st.container(border=True):
            st.metric("Variância explicada (PCA 2D)", fmt_pct(float(res_km["var_exp"].sum()), 1), delta="PC1 + PC2", delta_color="off")

    c_cot, c_anim = st.columns([0.95, 1.35])
    with c_cot:
        with st.container(border=True):
            df_cot = res_km["df_cotovelo"]
            cores_cot = [
                COR_MARCA_PRINCIPAL if k_v in {k_escolhido, res_km["n_classes"]} else COR_CINZA
                for k_v in df_cot["k"]
            ]
            fig_cot = go.Figure()
            fig_cot.add_trace(
                go.Scatter(
                    x=df_cot["k"],
                    y=df_cot["inercia"],
                    mode="lines+markers",
                    line=dict(color=COR_MARCA_PRINCIPAL, width=2.2),
                    marker=dict(size=10, color=cores_cot, line=dict(width=1.2, color=COR_TEXTO)),
                    hovertemplate="k = %{x}<br>Inércia (WCSS): %{y:,.1f}<extra></extra>",
                )
            )
            fig_cot.add_vline(
                x=k_escolhido,
                line_dash="dash",
                line_color=COR_MARCA_PRINCIPAL,
                annotation_text=f"k livre = {k_escolhido}",
                annotation_position="top right",
            )
            fig_cot.add_vline(
                x=res_km["n_classes"],
                line_dash="dot",
                line_color=COR_TEXTO_SECUNDARIO,
                annotation_text=f"k fixo = {res_km['n_classes']}",
                annotation_position="bottom right",
            )
            fig_cot.update_layout(
                title=dict(text="Método do Cotovelo (k = 2 a 10, StandardScaler)", x=0.0, font=dict(size=13.5)),
                xaxis=dict(title="Número de clusters (k)", dtick=1),
                yaxis=dict(title="Inércia (WCSS)"),
                showlegend=False,
            )
            aplicar_layout_base(fig_cot, altura=460, margem_topo=58, margem_baixo=48)
            st.plotly_chart(fig_cot, width="stretch")
            exibir_rodape_grafico(
                f"Fonte: UCI Machine Learning Repository (id = 544) | StandardScaler em 8 variáveis numéricas | n = {fmt_int(res_km['n_linhas'])}"
            )

    with c_anim:
        with st.container(border=True):
            df_anim = res_km["df_anim"]
            # Paleta qualitativa acessivel (Okabe-Ito + tons de marca) para ate 10 clusters
            paleta_clusters = [
                "#0F62FE", "#D55E00", "#009E73", "#E69F00", "#56B4E9",
                "#CC79A7", "#062A5F", "#6F6F6F", "#198038", "#8E6A00",
            ]
            fig_anim = px.scatter(
                df_anim,
                x="PC1",
                y="PC2",
                animation_frame="Passada",
                animation_group="id_ponto",
                color="Cluster",
                color_discrete_sequence=paleta_clusters,
                hover_data={
                    "Classe real": True,
                    "Classe mapeada": True,
                    "Peso (kg)": ":.1f",
                    "Altura (m)": ":.2f",
                    "id_ponto": False,
                    "Passada": False,
                },
                opacity=0.72,
            )
            fig_anim.update_traces(marker=dict(size=6))
            fig_anim.update_layout(
                title=dict(
                    text=f"Transição animada dos clusters em PCA 2D: Passada 1 (k = {p1['k']}) para Passada 2 (k = {p2['k']})",
                    x=0.0,
                    font=dict(size=13.5),
                ),
                xaxis=dict(title=f"PC1 ({fmt_pct(res_km['var_exp'][0])} da variância)"),
                yaxis=dict(title=f"PC2 ({fmt_pct(res_km['var_exp'][1])} da variância)"),
                legend=dict(title="Cluster", orientation="v"),
            )
            aplicar_layout_base(fig_anim, altura=460, margem_topo=58, margem_baixo=60)
            st.plotly_chart(fig_anim, width="stretch")
            exibir_rodape_grafico(
                "Use o botão Play abaixo do gráfico ou alterne o slider para visualizar a reatribuição dos pontos entre as duas passadas do K-Means."
            )

    with st.container(border=True):
        st.markdown("#### Matrizes de confusão (Cluster mapeado x Classe real) e métricas por passada")
        st.caption(
            "O K-Means não vê os rótulos reais durante o treino; a taxa de coincidência mede apenas o quanto os "
            "grupos descobertos coincidem com as classes originais de NObeyesdad (notebooks completos em notebooks/parte_comum/)."
        )
        tab_p1, tab_p2 = st.columns(2)
        with tab_p1:
            st.markdown(f"**Passada 1 (k = {p1['k']} livre) | Coincidência global: {fmt_pct(p1['acc'])}**")
            st.dataframe(p1["cm_df"], width="stretch")
            with st.expander(f"Ver precisão, recall e F1 por classe (Passada 1, k = {p1['k']})"):
                st.dataframe(p1["df_met"], width="stretch", hide_index=True)
        with tab_p2:
            st.markdown(f"**Passada 2 (k = {p2['k']} fixo) | Coincidência global: {fmt_pct(p2['acc'])}**")
            st.dataframe(p2["cm_df"], width="stretch")
            with st.expander(f"Ver precisão, recall e F1 por classe (Passada 2, k = {p2['k']})"):
                st.dataframe(p2["df_met"], width="stretch", hide_index=True)


with aba_comum:
    secao_parte_comum_kmeans()


# =============================================================================
# ABA 5: GLOSSARIO E EXPORTACAO
# =============================================================================
with aba_ref:
    st.subheader("Glossário das colunas tratadas e exportação de dados")
    busca_col = st.text_input("Buscar coluna ou significado", placeholder="Ex.: quantity, ward, idade, MAR...")

    linhas_glos = []
    for col in df_total.columns:
        if col == "faixa_idade":
            continue
        desc = GLOSSARIO_COLUNAS.get(col, "Sem descrição")
        exemplos = ", ".join([str(v) for v in df_total[col].dropna().unique()[:4]])
        if (not busca_col) or (busca_col.lower() in col.lower()) or (busca_col.lower() in desc.lower()):
            linhas_glos.append({
                "Coluna": col,
                "Significado": desc,
                "Tipo": str(df_total[col].dtype),
                "Valores únicos": int(df_total[col].nunique()),
                "Exemplos": exemplos,
            })

    st.dataframe(pd.DataFrame(linhas_glos), width="stretch", hide_index=True)

    st.divider()
    st.subheader("Exportar dados e resumo do recorte atual")
    ex1, ex2 = st.columns(2)
    with ex1:
        csv_bytes = df_filt.drop(columns=["faixa_idade"], errors="ignore").to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Baixar CSV filtrado ({fmt_int(len(df_filt))} linhas)",
            data=csv_bytes,
            file_name="pump_it_up_recorte_filtrado.csv",
            mime="text/csv",
            width="stretch",
        )
    with ex2:
        st.download_button(
            label="Baixar resumo executivo (.md)",
            data=resumo_md.encode("utf-8"),
            file_name="resumo_recorte_pump_it_up.md",
            mime="text/markdown",
            width="stretch",
        )
