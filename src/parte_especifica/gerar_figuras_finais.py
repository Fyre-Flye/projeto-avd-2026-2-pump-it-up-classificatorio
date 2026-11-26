"""Gera e salva em out/parte_especifica/ as figuras estaticas limpas para o relatorio PDF e slides.

# [IA] Gemini – geracao reproduzivel das 4 visualizacoes exploratorias e 3 explanatorias (E1, E2A, E2B) no padrao 06_GUIDELINES

Execucao, a partir da raiz do repositorio:
    python src/parte_especifica/gerar_figuras_finais.py
"""

import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def obter_raiz():
    atual = Path(__file__).resolve()
    for pai in [atual.parent] + list(atual.parents):
        if (pai / "requirements.txt").exists():
            return pai
    return Path.cwd()


ROOT = obter_raiz()
CLEAN_PATH = ROOT / "data" / "parte_especifica" / "clean" / "pump_it_up_clean.csv"
OUT_DIR = ROOT / "out" / "parte_especifica"
METRICAS_PATH = OUT_DIR / "06_metricas_classificadores.csv"
IMPORTANCIA_PATH = OUT_DIR / "06_importancia_features.csv"

COL_ALVO = "status_group"
STATUS_ORDEM = ["functional", "functional needs repair", "non functional"]
STATUS_ROTULO_PT = {
    "functional": "Funcional",
    "functional needs repair": "Precisa de reparo",
    "non functional": "Não funcional",
}
STATUS_CORES = {
    "functional": "#0072B2",
    "functional needs repair": "#E69F00",
    "non functional": "#D55E00",
}
COR_CINZA = "#C6C6C6"
COR_TEXTO = "#111827"
COR_SUBTEXTO = "#4B5563"
COR_GRADE = "#E5E7EB"


def fmt_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


def fmt_pct(v, casas=1):
    return f"{v:.{casas}f}%".replace(".", ",")


def fmt_num(v, casas=1):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def configurar_estilo():
    plt.rcParams.update({
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "savefig.facecolor": "#FFFFFF",
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "text.color": COR_TEXTO,
        "axes.labelcolor": COR_TEXTO,
        "xtick.color": COR_TEXTO,
        "ytick.color": COR_TEXTO,
        "axes.edgecolor": "#9CA3AF",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def salvar_fig(fig, nome):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destino = OUT_DIR / f"{nome}.png"
    for tentativa in range(5):
        try:
            fig.savefig(destino, dpi=150, bbox_inches="tight", facecolor="#FFFFFF")
            print(f"Salvo: {destino.relative_to(ROOT)}")
            plt.close(fig)
            return
        except OSError:
            if tentativa == 4:
                raise
            time.sleep(0.5)


def adicionar_rodape(fig, texto, y=-0.04):
    fig.text(0.01, y, texto, fontsize=8.5, color=COR_SUBTEXTO, ha="left")


def gerar_expl_01_distribuicao_status(df):
    """Exploratoria 1: distribuicao da situacao dos pontos d'agua (status_group)."""
    cont = df[COL_ALVO].value_counts().reindex(STATUS_ORDEM)
    pct = cont / len(df) * 100

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    x = np.arange(len(STATUS_ORDEM))
    cores = [STATUS_CORES[s] for s in STATUS_ORDEM]
    rotulos = [STATUS_ROTULO_PT[s] for s in STATUS_ORDEM]

    barras = ax.bar(x, cont.values, width=0.55, color=cores, zorder=3)
    ax.grid(axis="y", color=COR_GRADE, linestyle="--", linewidth=0.7, zorder=0)
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos, fontsize=11, fontweight="bold")
    ax.set_ylabel("Número de pontos d'água", fontsize=10.5)
    ax.set_ylim(0, cont.max() * 1.18)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_int(v)))

    for barra, n_val, p_val in zip(barras, cont.values, pct.values):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + cont.max() * 0.025,
            f"{fmt_int(n_val)}\n({fmt_pct(p_val)})",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color=COR_TEXTO,
        )

    ax.set_title(
        "Distribuição da situação operacional dos pontos d'água (status_group)",
        loc="left",
        fontsize=12.5,
        fontweight="bold",
        pad=14,
    )
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | Base tratada (2011 a 2013) | n = {fmt_int(len(df))}",
        y=-0.06,
    )
    fig.tight_layout()
    salvar_fig(fig, "07_expl_01_distribuicao_status")


def gerar_expl_02_status_por_categoria(df):
    """Exploratoria 2: situacao operacional por 4 variaveis categoricas principais."""
    cols = [
        ("quantity", "Disponibilidade de água (quantity)"),
        ("extraction_type_class", "Tecnologia de extração (extraction_type_class)"),
        ("waterpoint_type_group", "Tipo de ponto d'água (waterpoint_type_group)"),
        ("payment_type", "Forma de pagamento (payment_type)"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14.5, 9.2))
    for ax, (col, titulo) in zip(axes.flat, cols):
        tab = pd.crosstab(df[col], df[COL_ALVO], normalize="index").reindex(columns=STATUS_ORDEM, fill_value=0) * 100
        counts = df[col].value_counts()
        tab = tab.loc[counts.index].iloc[::-1]
        y_labels = [f"{cat} (n={fmt_int(counts[cat])})" for cat in tab.index]
        y_pos = np.arange(len(tab))

        esq = np.zeros(len(tab))
        for st_val in STATUS_ORDEM:
            vals = tab[st_val].values
            ax.barh(
                y_pos,
                vals,
                left=esq,
                height=0.68,
                color=STATUS_CORES[st_val],
                label=STATUS_ROTULO_PT[st_val],
                zorder=3,
            )
            for idx_b, (v, l_pos) in enumerate(zip(vals, esq)):
                if v >= 13:
                    ax.text(
                        l_pos + v / 2,
                        y_pos[idx_b],
                        fmt_pct(v, 0),
                        ha="center",
                        va="center",
                        fontsize=8.2,
                        color="#FFFFFF" if st_val != "functional needs repair" else COR_TEXTO,
                        fontweight="bold",
                    )
            esq += vals

        ax.set_yticks(y_pos)
        ax.set_yticklabels(y_labels, fontsize=9)
        ax.set_xlim(0, 100)
        ax.set_xlabel("% dos pontos d'água na categoria", fontsize=9.5)
        ax.set_title(titulo, loc="left", fontsize=11, fontweight="bold", pad=8)
        ax.grid(axis="x", color=COR_GRADE, linestyle="--", linewidth=0.6, zorder=0)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=3,
        bbox_to_anchor=(0.5, 0.995),
        frameon=False,
        fontsize=10.5,
    )
    fig.suptitle(
        "Situação operacional dos pontos d'água por variáveis categóricas principais",
        fontsize=13.5,
        fontweight="bold",
        y=1.035,
    )
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | Base tratada (2011 a 2013) | n = {fmt_int(len(df))} | Ordenado por volume (n)",
        y=-0.02,
    )
    fig.tight_layout(rect=[0, 0.01, 1, 0.95])
    salvar_fig(fig, "07_expl_02_status_por_categoria")


def gerar_expl_03_contraste_regional_mapa(df):
    """Exploratoria 3: ranking regional de inoperancia lado a lado com mapa geografico."""
    tab_reg = pd.crosstab(df["region"], df[COL_ALVO], normalize="index").reindex(columns=STATUS_ORDEM, fill_value=0) * 100
    n_reg = df["region"].value_counts()
    tab_reg = tab_reg.sort_values("non functional", ascending=True)
    media_nac = (df[COL_ALVO] == "non functional").mean() * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7.6), gridspec_kw={"width_ratios": [1.05, 1.15]})

    # Painel esquerdo: ranking regional ordenado
    y_pos = np.arange(len(tab_reg))
    vals = tab_reg["non functional"].values
    ax1.barh(y_pos, vals, height=0.72, color=STATUS_CORES["non functional"], alpha=0.88, zorder=3)
    ax1.axvline(media_nac, color=COR_TEXTO, linestyle="--", linewidth=1.1, zorder=4)
    ax1.text(
        media_nac + 0.8,
        0.5,
        f"Média nacional: {fmt_pct(media_nac)}",
        fontsize=8.8,
        color=COR_TEXTO,
        fontweight="bold",
        va="bottom",
    )
    for yp, v in zip(y_pos, vals):
        ax1.text(v + 0.7, yp, fmt_pct(v), va="center", ha="left", fontsize=8.5, color=COR_TEXTO)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f"{r} (n={fmt_int(n_reg[r])})" for r in tab_reg.index], fontsize=8.8)
    ax1.set_xlim(0, max(vals) + 12)
    ax1.set_xlabel("% de pontos não funcionais na região", fontsize=10)
    ax1.set_title("Taxa de inoperância por região (21 regiões)", loc="left", fontsize=11.5, fontweight="bold", pad=10)
    ax1.grid(axis="x", color=COR_GRADE, linestyle="--", linewidth=0.6, zorder=0)

    # Painel direito: mapa geografico (apenas coordenadas reais, sem imputadas)
    geo = df[df["ausente_coords"] == 0]
    for st_val in STATUS_ORDEM:
        sub = geo[geo[COL_ALVO] == st_val]
        ax2.scatter(
            sub["longitude"],
            sub["latitude"],
            s=2.2,
            alpha=0.38 if st_val != "functional needs repair" else 0.55,
            color=STATUS_CORES[st_val],
            label=STATUS_ROTULO_PT[st_val],
            rasterized=True,
        )
    ax2.set_xlabel("Longitude", fontsize=10)
    ax2.set_ylabel("Latitude", fontsize=10)
    ax2.set_title(
        f"Distribuição geográfica por situação (coordenadas reais, n = {fmt_int(len(geo))})",
        loc="left",
        fontsize=11.5,
        fontweight="bold",
        pad=10,
    )
    ax2.grid(color=COR_GRADE, linestyle="--", linewidth=0.5)
    leg = ax2.legend(loc="lower left", frameon=True, facecolor="#FFFFFF", edgecolor="#D1D5DB", fontsize=9.5, markerscale=4.5)
    for lh in leg.legend_handles:
        lh.set_alpha(1.0)

    fig.suptitle(
        "Contraste regional e distribuição geográfica da situação operacional",
        fontsize=13.5,
        fontweight="bold",
        y=1.01,
    )
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | Base tratada (2011 a 2013) | Ranking: n = {fmt_int(len(df))}; Mapa sem coords imputadas: n = {fmt_int(len(geo))}",
        y=-0.03,
    )
    fig.tight_layout()
    salvar_fig(fig, "07_expl_03_contraste_regional_mapa")


def gerar_expl_04_heatmap_quantity_extraction(df):
    """Exploratoria 4: heatmap multivariado quantity x extraction_type_class (limpo)."""
    sub = df[(df["quantity"] != "unknown") & (df["extraction_type_class"] != "other")].copy()
    ordem_q = ["enough", "insufficient", "seasonal", "dry"]
    ordem_e = sub["extraction_type_class"].value_counts().index.tolist()

    pv_pct = pd.crosstab(sub["extraction_type_class"], sub["quantity"], values=(sub[COL_ALVO] == "non functional"), aggfunc="mean") * 100
    pv_n = pd.crosstab(sub["extraction_type_class"], sub["quantity"])
    pv_pct = pv_pct.reindex(index=ordem_e, columns=ordem_q)
    pv_n = pv_n.reindex(index=ordem_e, columns=ordem_q).fillna(0).astype(int)

    annot = pd.DataFrame(index=ordem_e, columns=ordem_q, dtype=object)
    for r in ordem_e:
        for c in ordem_q:
            v = pv_pct.loc[r, c]
            n_val = pv_n.loc[r, c]
            annot.loc[r, c] = f"{fmt_pct(v)}\n(n={fmt_int(n_val)})" if pd.notna(v) else "sem dados"

    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    sns.heatmap(
        pv_pct,
        annot=annot,
        fmt="",
        cmap="YlOrRd",
        vmin=0,
        vmax=100,
        linewidths=0.8,
        linecolor="#FFFFFF",
        cbar_kws={"label": "% de pontos não funcionais"},
        annot_kws={"fontsize": 9},
        ax=ax,
    )
    ax.set_xlabel("Disponibilidade de água (quantity)", fontsize=10.5)
    ax.set_ylabel("Tecnologia de extração (extraction_type_class)", fontsize=10.5)
    ax.set_title(
        "Taxa de pontos não funcionais: disponibilidade de água vs. tecnologia de extração",
        loc="left",
        fontsize=12,
        fontweight="bold",
        pad=14,
    )
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | 2011 a 2013 | Exclui unknown e other | n = {fmt_int(len(sub))}",
        y=-0.06,
    )
    fig.tight_layout()
    salvar_fig(fig, "07_expl_04_heatmap_quantity_extraction")


def gerar_explan_01_tecnologia_com_agua(df):
    """Explanatoria 1 (Big Idea eixo 1): com agua suficiente, tecnologias motorizadas/complexas falham bem mais."""
    sub = df[df["quantity"] == "enough"].copy()
    tab = pd.crosstab(sub["extraction_type_class"], sub[COL_ALVO], normalize="index").reindex(columns=STATUS_ORDEM, fill_value=0) * 100
    counts = sub["extraction_type_class"].value_counts()
    tab["n"] = counts
    tab = tab.sort_values("non functional", ascending=True)

    media_recorte = (sub[COL_ALVO] == "non functional").mean() * 100
    destaque_cats = {"other", "wind-powered", "motorpump"}
    cores = [
        STATUS_CORES["non functional"] if cat in destaque_cats
        else ("#F0A070" if cat == "submersible" else COR_CINZA)
        for cat in tab.index
    ]

    rotulos_pt = {
        "other": "other (outras / não especificadas)",
        "wind-powered": "wind-powered (bomba eólica*)",
        "motorpump": "motorpump (bomba motorizada)",
        "submersible": "submersible (submersível)",
        "rope pump": "rope pump (bomba de corda)",
        "handpump": "handpump (bomba manual)",
        "gravity": "gravity (gravidade)",
    }

    fig, ax = plt.subplots(figsize=(10.6, 5.9))
    y_pos = np.arange(len(tab))
    vals = tab["non functional"].values

    barras = ax.barh(y_pos, vals, height=0.60, color=cores, zorder=3)
    ax.axvline(media_recorte, color=COR_SUBTEXTO, linestyle="--", linewidth=1.1, alpha=0.65, zorder=2)
    ax.text(
        media_recorte + 0.8,
        len(tab) - 0.35,
        f"Média em pontos com água suficiente: {fmt_pct(media_recorte)}",
        fontsize=9,
        color=COR_TEXTO,
        fontweight="bold",
        va="bottom",
        ha="left",
        bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.9),
        zorder=5,
    )

    for idx_b, (barra, cat) in enumerate(zip(barras, tab.index)):
        v = tab.loc[cat, "non functional"]
        n_v = tab.loc[cat, "n"]
        em_foco = cat in destaque_cats
        ax.text(
            v + 1.1,
            barra.get_y() + barra.get_height() / 2,
            f"{fmt_pct(v)}  (n = {fmt_int(n_v)})",
            va="center",
            ha="left",
            fontsize=9.6,
            fontweight="bold" if em_foco else "normal",
            color=STATUS_CORES["non functional"] if em_foco else COR_TEXTO,
            bbox=dict(boxstyle="square,pad=0.12", facecolor="#FFFFFF", edgecolor="none", alpha=0.88),
            zorder=5,
        )

    # Anotacao comparativa direta motorpump vs gravity (posicionada em area livre a direita)
    v_motor = tab.loc["motorpump", "non functional"]
    v_grav = tab.loc["gravity", "non functional"]
    diff_pp = v_motor - v_grav
    ax.annotate(
        f"Motorpump falha {fmt_num(v_motor / v_grav, 1)}x mais que gravidade\n(+{fmt_num(diff_pp, 1)} pontos percentuais)",
        xy=(v_motor + 21.5, list(tab.index).index("motorpump") - 0.05),
        xytext=(57, 1.85),
        fontsize=9.2,
        fontweight="bold",
        color=STATUS_CORES["non functional"],
        bbox=dict(boxstyle="round,pad=0.42", facecolor="#FFF7ED", edgecolor=STATUS_CORES["non functional"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=STATUS_CORES["non functional"], lw=1.3, connectionstyle="arc3,rad=0.22"),
        zorder=6,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels([rotulos_pt.get(c, c) for c in tab.index], fontsize=10)
    ax.set_xlim(0, 99)
    ax.set_ylim(-0.6, len(tab) + 0.15)
    ax.set_xlabel("Taxa de pontos não funcionais (%)", fontsize=10.5)
    ax.grid(axis="x", color=COR_GRADE, linestyle="--", linewidth=0.7, zorder=0)

    fig.suptitle(
        "Mesmo com água suficiente, bombas motorizadas falham mais que o dobro de sistemas por gravidade",
        x=0.02,
        ha="left",
        fontsize=12.8,
        fontweight="bold",
        y=0.99,
    )
    ax.set_title(
        "Taxa de inoperância (% non functional) por tecnologia de extração somente em pontos com quantity = enough",
        loc="left",
        fontsize=10,
        color=COR_SUBTEXTO,
        pad=12,
    )
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | 2011 a 2013 | Recorte quantity = enough (n = {fmt_int(len(sub))}) | *wind-powered tem amostra pequena (n = 59)",
        y=-0.05,
    )
    fig.tight_layout(rect=[0, 0.01, 1, 0.94])
    salvar_fig(fig, "08_explan_01_tecnologia_com_agua")


def gerar_explan_02a_idade_vs_falha(df):
    """Explanatoria 2A (Big Idea eixo 2): envelhecimento das bombas eleva fortemente a taxa de inoperancia."""
    val = df[df["ausente_construction_year"] == 0].copy()
    bins = [-1, 5, 10, 15, 20, 30, 100]
    labels = ["0 a 5 anos", "6 a 10 anos", "11 a 15 anos", "16 a 20 anos", "21 a 30 anos", "Mais de 30 anos"]
    val["faixa"] = pd.cut(val["idade_no_registro"], bins=bins, labels=labels)

    tab = pd.crosstab(val["faixa"], val[COL_ALVO], normalize="index").reindex(index=labels, columns=STATUS_ORDEM, fill_value=0) * 100
    counts = val["faixa"].value_counts().reindex(labels)

    med_func = val.loc[val[COL_ALVO] == "functional", "idade_no_registro"].median()
    med_nf = val.loc[val[COL_ALVO] == "non functional", "idade_no_registro"].median()

    cores = [COR_CINZA, COR_CINZA, COR_CINZA, "#F0A070", STATUS_CORES["non functional"], STATUS_CORES["non functional"]]

    fig, ax = plt.subplots(figsize=(10.2, 5.4))
    x = np.arange(len(labels))
    vals = tab["non functional"].values

    barras = ax.bar(x, vals, width=0.58, color=cores, zorder=3)
    ax.plot(x, vals, color=COR_TEXTO, marker="o", linewidth=1.6, markersize=5, zorder=4)
    ax.grid(axis="y", color=COR_GRADE, linestyle="--", linewidth=0.7, zorder=0)

    for idx_b, (barra, v, n_v) in enumerate(zip(barras, vals, counts.values)):
        em_foco = idx_b >= 4
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            v + 2.0,
            f"{fmt_pct(v)}\n(n={fmt_int(n_v)})",
            ha="center",
            va="bottom",
            fontsize=9.2,
            fontweight="bold" if em_foco else "normal",
            color=STATUS_CORES["non functional"] if em_foco else COR_TEXTO,
        )

    ax.annotate(
        f"Acima de 30 anos, taxa chega a {fmt_pct(vals[-1])}\n({fmt_num(vals[-1] / vals[0], 1)}x a taxa de bombas de 0 a 5 anos)\nMediana de idade: {fmt_int(med_func)} anos (funcionais) vs. {fmt_int(med_nf)} anos (inoperantes)",
        xy=(5, vals[-1]),
        xytext=(0.15, 58.0),
        fontsize=9.2,
        fontweight="bold",
        color=COR_TEXTO,
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#FFF7ED", edgecolor=STATUS_CORES["non functional"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=STATUS_CORES["non functional"], lw=1.3, connectionstyle="arc3,rad=-0.12"),
    )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.8)
    ax.set_ylim(0, 76)
    ax.set_ylabel("Taxa de pontos não funcionais (%)", fontsize=10.5)
    ax.set_xlabel("Faixa de idade do ponto d'água no momento da coleta (idade_no_registro)", fontsize=10)

    fig.suptitle(
        "Envelhecimento da rede: taxa de bombas inoperantes mais que dobra após 20 anos de uso",
        x=0.02,
        ha="left",
        fontsize=12.8,
        fontweight="bold",
        y=0.99,
    )
    ax.set_title(
        "Percentual de pontos não funcionais por faixa de idade, considerando apenas registros com ano de construção informado",
        loc="left",
        fontsize=9.8,
        color=COR_SUBTEXTO,
        pad=12,
    )
    adicionar_rodape(
        fig,
        f"Fonte: DrivenData/Taarifa (Pump it Up) | 2011 a 2013 | Somente ausente_construction_year = 0 (n = {fmt_int(len(val))}; 34,8% omitidos por ausência MAR)",
        y=-0.05,
    )
    fig.tight_layout(rect=[0, 0.01, 1, 0.94])
    salvar_fig(fig, "08_explan_02a_idade_vs_falha")


def gerar_explan_02b_classificador_metricas():
    """Explanatoria 2B (2a parte da pergunta de pesquisa): desempenho do Random Forest e gargalo na classe minoritaria."""
    df_met = pd.read_csv(METRICAS_PATH)
    df_imp = pd.read_csv(IMPORTANCIA_PATH)

    rf = df_met[(df_met["modelo"] == "Random Forest") & (df_met["classe"].isin(STATUS_ORDEM))].copy()
    rf["classe"] = pd.Categorical(rf["classe"], categories=STATUS_ORDEM, ordered=True)
    rf = rf.sort_values("classe")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.2, 5.5), gridspec_kw={"width_ratios": [1.05, 1.05]})

    # Painel esquerdo: Precisao vs Recall por classe (destacando o gargalo de 27,0% em needs repair)
    x = np.arange(len(STATUS_ORDEM))
    w = 0.34
    prec = rf["precisao"].values
    rec = rf["recall"].values

    cores_prec = [COR_CINZA, "#F5D08A", COR_CINZA]
    cores_rec = [STATUS_CORES["functional"], STATUS_CORES["non functional"], STATUS_CORES["functional"]]

    b1 = ax1.bar(x - w / 2, prec, width=w, color=cores_prec, label="Precisão (%)", zorder=3)
    b2 = ax1.bar(x + w / 2, rec, width=w, color=cores_rec, label="Recall / Cobertura (%)", zorder=3)
    ax1.grid(axis="y", color=COR_GRADE, linestyle="--", linewidth=0.7, zorder=0)

    for idx_b, (bar_p, bar_r, vp, vr) in enumerate(zip(b1, b2, prec, rec)):
        ax1.text(bar_p.get_x() + bar_p.get_width() / 2, vp + 1.8, fmt_pct(vp), ha="center", va="bottom", fontsize=9, color=COR_TEXTO)
        ax1.text(
            bar_r.get_x() + bar_r.get_width() / 2,
            vr + 1.8,
            fmt_pct(vr),
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color=STATUS_CORES["non functional"] if idx_b == 1 else COR_TEXTO,
        )

    ax1.annotate(
        "Classe minoritária (7,3%):\nprecisão 65,8%, recall 27,0%",
        xy=(1 + w / 2, rec[1] + 5.5),
        xytext=(1.12, 98.0),
        ha="center",
        fontsize=8.6,
        fontweight="bold",
        color=STATUS_CORES["non functional"],
        bbox=dict(boxstyle="round,pad=0.38", facecolor="#FFF7ED", edgecolor=STATUS_CORES["non functional"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=STATUS_CORES["non functional"], lw=1.2),
        zorder=6,
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels([STATUS_ROTULO_PT[c] for c in STATUS_ORDEM], fontsize=9.8, fontweight="bold")
    ax1.set_ylim(0, 128)
    ax1.set_ylabel("Desempenho no conjunto de teste (%)", fontsize=10)
    ax1.set_title("Random Forest por classe (acurácia global: 80,6%)", loc="left", fontsize=11, fontweight="bold", pad=10)
    ax1.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02), frameon=False, fontsize=9)

    # Painel direito: Top 10 variaveis mais importantes (inclui extraction_type_class)
    top10 = df_imp.head(10).iloc[::-1]
    destaque_vars = {"ward", "quantity", "extraction_type_class"}
    cores_imp = [STATUS_CORES["functional"] if c in destaque_vars else COR_CINZA for c in top10["coluna"]]
    y2 = np.arange(len(top10))

    barras2 = ax2.barh(y2, top10["importancia_pct"].values, height=0.64, color=cores_imp, zorder=3)
    ax2.grid(axis="x", color=COR_GRADE, linestyle="--", linewidth=0.7, zorder=0)
    for barra, col, val in zip(barras2, top10["coluna"], top10["importancia_pct"]):
        em_foco = col in destaque_vars
        ax2.text(
            val + 0.35,
            barra.get_y() + barra.get_height() / 2,
            fmt_pct(val),
            va="center",
            ha="left",
            fontsize=9.0,
            fontweight="bold" if em_foco else "normal",
            color=STATUS_CORES["functional"] if em_foco else COR_TEXTO,
        )

    ax2.set_yticks(y2)
    ax2.set_yticklabels([f"{c} ({g})" for c, g in zip(top10["coluna"], top10["glossario"])], fontsize=8.5)
    ax2.set_xlim(0, top10["importancia_pct"].max() + 3.8)
    ax2.set_xlabel("Importância agregada no Random Forest (%)", fontsize=10)
    ax2.set_title("Top 10 atributos mais relevantes no classificador", loc="left", fontsize=11, fontweight="bold", pad=10)

    fig.suptitle(
        "Classificador atinge 80,6% de acurácia, mas alerta para baixo recall em bombas que precisam de reparo",
        x=0.02,
        ha="left",
        fontsize=12.8,
        fontweight="bold",
        y=1.01,
    )
    adicionar_rodape(
        fig,
        "Fonte: DrivenData/Taarifa (Pump it Up) | RandomForestClassifier (200 árvores, hold-out 80/20 estratificado, teste n = 11.867, sem data leakage)",
        y=-0.05,
    )
    fig.tight_layout(rect=[0, 0.01, 1, 0.95])
    salvar_fig(fig, "08_explan_02b_classificador_metricas")


def main():
    configurar_estilo()
    df = pd.read_csv(CLEAN_PATH)
    print(f"Base limpa carregada: {len(df):,} linhas x {df.shape[1]} colunas")
    gerar_expl_01_distribuicao_status(df)
    gerar_expl_02_status_por_categoria(df)
    gerar_expl_03_contraste_regional_mapa(df)
    gerar_expl_04_heatmap_quantity_extraction(df)
    gerar_explan_01_tecnologia_com_agua(df)
    gerar_explan_02a_idade_vs_falha(df)
    gerar_explan_02b_classificador_metricas()
    print("Todas as 7 figuras finais foram geradas com sucesso.")


if __name__ == "__main__":
    main()
