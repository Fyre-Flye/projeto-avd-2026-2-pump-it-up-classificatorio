"""Camada de dados, cache e pipelines do classificador para o dashboard Streamlit.

# [IA] Gemini – carga de dados tratados com @st.cache_data, utilitarios pt-BR e pipelines anti-data-leakage com @st.cache_resource
"""

from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.tree import DecisionTreeClassifier


# Caminhos relativos a raiz do repositorio (compativel local e Streamlit Community Cloud)
def obter_raiz_projeto():
    """Sobe diretorios ate localizar requirements.txt na raiz do repositorio."""
    atual = Path(__file__).resolve()
    for pai in [atual.parent] + list(atual.parents):
        if (pai / "requirements.txt").exists():
            return pai
    return Path.cwd()


ROOT = obter_raiz_projeto()
CLEAN_PATH = ROOT / "data" / "parte_especifica" / "clean" / "pump_it_up_clean.csv"
OUT_DIR = ROOT / "out" / "parte_especifica"
METRICAS_PATH = OUT_DIR / "06_metricas_classificadores.csv"
IMPORTANCIA_PATH = OUT_DIR / "06_importancia_features.csv"

COL_ALVO = "status_group"
RANDOM_STATE = 42

# Paleta fixa Okabe-Ito (acessivel a daltonismo, padrao 06_GUIDELINES)
STATUS_ORDEM = ["functional", "functional needs repair", "non functional"]
STATUS_ROTULO = {
    "functional": "Funcional",
    "functional needs repair": "Precisa de reparo",
    "non functional": "Nao funcional",
}
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
COR_CINZA_ESCURO = "#6B7280"
COR_TEXTO = "#111827"
COR_AZUL = "#0072B2"
COR_LARANJA_ALERTA = "#D55E00"
COR_AMARELO = "#E69F00"

COLS_IMPUTAR = ["population", "construction_year", "gps_height", "longitude", "latitude"]

COLS_NUM = [
    "amount_tsh", "gps_height", "longitude", "latitude",
    "population", "construction_year", "ano_registro", "idade_no_registro",
    "ausente_population", "ausente_construction_year", "ausente_gps_height", "ausente_coords",
]

COLS_CAT_BAIXA = [
    "quantity", "extraction_type_class", "waterpoint_type_group", "payment_type",
    "quality_group", "source_class", "management_group", "scheme_management",
    "basin", "region", "public_meeting", "permit",
]

COLS_CAT_ALTA = ["lga", "ward", "funder", "installer"]

FAIXAS_IDADE_BINS = [-1, 5, 10, 15, 20, 30, 100]
FAIXAS_IDADE_LABELS = [
    "0 a 5 anos",
    "6 a 10 anos",
    "11 a 15 anos",
    "16 a 20 anos",
    "21 a 30 anos",
    "Mais de 30 anos",
]

GLOSSARIO_COLUNAS = {
    "id": "Identificador único do ponto d'água",
    "date_recorded": "Data em que o registro foi coletado",
    "ano_registro": "Ano extraído de date_recorded (recorte 2011 a 2013)",
    "amount_tsh": "Total static head: carga hidráulica/água disponível no ponto",
    "gps_height": "Altitude do ponto d'água (imputada em cascata; litoral >= 0)",
    "longitude": "Longitude geográfica (coordenada GPS)",
    "latitude": "Latitude geográfica (coordenada GPS)",
    "population": "População estimada ao redor do ponto d'água",
    "construction_year": "Ano de construção do ponto d'água",
    "idade_no_registro": "Idade do ponto na coleta (ano_registro menos construction_year)",
    "ausente_population": "Flag binária: 1 se population original era 0 (MAR)",
    "ausente_construction_year": "Flag binária: 1 se construction_year original era 0 (MAR)",
    "ausente_gps_height": "Flag binária: 1 se gps_height original era 0 (MAR)",
    "ausente_coords": "Flag binária: 1 se coordenadas originais estavam zeradas",
    "quantity": "Disponibilidade de água (enough, insufficient, dry, seasonal, unknown)",
    "extraction_type_class": "Classe geral da tecnologia de extração",
    "waterpoint_type_group": "Grupo geral do tipo de ponto d'água",
    "payment_type": "Forma de pagamento pela água",
    "quality_group": "Qualidade da água (nível agrupado)",
    "source_class": "Classe da fonte de água (groundwater, surface, unknown)",
    "management_group": "Modelo de gestão do ponto d'água (agrupado)",
    "scheme_management": "Entidade operadora do esquema de água",
    "basin": "Bacia hidrográfica",
    "region": "Região administrativa da Tanzânia (21 regiões)",
    "lga": "Autoridade local / município (alta cardinalidade)",
    "ward": "Subdistrito / ward (alta cardinalidade)",
    "funder": "Financiador da construção (padronizado em minúsculas)",
    "installer": "Instalador da bomba (padronizado em minúsculas)",
    "public_meeting": "Indica se houve reunião pública (true, false, desconhecido)",
    "permit": "Indica se o ponto possui licença/permissão",
    "status_group": "Variável-alvo: situação operacional do ponto d'água",
}

ROTULOS_VARS_CAT = {
    "quantity": "Disponibilidade de água (quantity)",
    "extraction_type_class": "Tecnologia de extração (extraction_type_class)",
    "waterpoint_type_group": "Tipo de ponto d'água (waterpoint_type_group)",
    "payment_type": "Forma de pagamento (payment_type)",
    "quality_group": "Qualidade da água (quality_group)",
    "source_class": "Fonte da água (source_class)",
    "management_group": "Grupo de gestão (management_group)",
    "scheme_management": "Operador do esquema (scheme_management)",
    "basin": "Bacia hidrográfica (basin)",
    "region": "Região geográfica (region)",
    "public_meeting": "Reunião pública (public_meeting)",
    "permit": "Possui licença (permit)",
}


def fmt_int(valor):
    """Formata numero inteiro no padrao pt-BR (separador de milhar com ponto)."""
    return f"{int(round(valor)):,}".replace(",", ".")


def fmt_pct(valor, casas=1):
    """Formata percentual (ja em escala 0 a 100) no padrao pt-BR."""
    return f"{valor:.{casas}f}%".replace(".", ",")


def fmt_num(valor, casas=1):
    """Formata numero decimal no padrao pt-BR."""
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


@st.cache_data(show_spinner="Carregando base tratada do Pump it Up...")
def carregar_dados():
    """Carrega exclusivamente o dataset tratado gerado ao final da EDA."""
    df = pd.read_csv(CLEAN_PATH)
    df["faixa_idade"] = pd.cut(
        df["idade_no_registro"],
        bins=FAIXAS_IDADE_BINS,
        labels=FAIXAS_IDADE_LABELS,
    ).astype(str)
    return df


@st.cache_data(show_spinner=False)
def carregar_tabelas_classificador():
    """Carrega os CSVs de metricas e importancia de features exportados pelo classificador."""
    df_metricas = pd.read_csv(METRICAS_PATH) if METRICAS_PATH.exists() else pd.DataFrame()
    df_imp = pd.read_csv(IMPORTANCIA_PATH) if IMPORTANCIA_PATH.exists() else pd.DataFrame()
    return df_metricas, df_imp


class ImputadorCascata(BaseEstimator, TransformerMixin):
    """Aprende medianas por lga -> region -> basin -> global SOMENTE no treino e deriva idade_no_registro."""

    def __init__(self, colunas=COLS_IMPUTAR, grupos=("lga", "region", "basin")):
        self.colunas = colunas
        self.grupos = grupos

    def fit(self, X, y=None):
        self.medianas_ = {}
        self.mediana_global_ = {}
        for col in self.colunas:
            self.medianas_[col] = {g: X.groupby(g)[col].median().to_dict() for g in self.grupos}
            self.mediana_global_[col] = float(X[col].median())
        return self

    def transform(self, X):
        X_out = X.copy()
        for col in self.colunas:
            serie = X_out[col].copy()
            for g in self.grupos:
                mapa = self.medianas_[col][g]
                serie = serie.fillna(X_out[g].map(mapa))
            X_out[col] = serie.fillna(self.mediana_global_[col])
        X_out["gps_height"] = X_out["gps_height"].clip(lower=0)
        X_out["idade_no_registro"] = (X_out["ano_registro"] - X_out["construction_year"]).clip(lower=0)
        return X_out


def criar_preprocessador():
    """Cria o ColumnTransformer (One-Hot em baixa cardinalidade e Target Encoding em alta cardinalidade)."""
    return ColumnTransformer(
        transformers=[
            ("num", "passthrough", COLS_NUM),
            ("cat_baixa", OneHotEncoder(handle_unknown="ignore", sparse_output=False), COLS_CAT_BAIXA),
            ("cat_alta", TargetEncoder(smooth="auto", random_state=RANDOM_STATE), COLS_CAT_ALTA),
        ],
        remainder="drop",
    )


def obter_nomes_features(preprocessador):
    """Retorna nomes legiveis de cada coluna apos o ColumnTransformer para auditar a Arvore."""
    nomes = list(COLS_NUM)
    ohe = preprocessador.named_transformers_["cat_baixa"]
    for col, cats in zip(COLS_CAT_BAIXA, ohe.categories_):
        for cat in cats:
            nomes.append(f"{col} == '{cat}'")
    status_curto = ["functional", "needs repair", "non functional"]
    for col in COLS_CAT_ALTA:
        for cls in status_curto:
            nomes.append(f"TE({col} -> {cls})")
    return nomes


def auditar_arvore(pipe_dt, linha_X):
    """Extrai a trilha real de decisoes (decision_path) percorrida pela Arvore de Decisao."""
    X_imp = pipe_dt.named_steps["imputacao"].transform(linha_X)
    X_enc = pipe_dt.named_steps["encoding"].transform(X_imp)
    arvore = pipe_dt.named_steps["modelo"].tree_
    nomes_feat = obter_nomes_features(pipe_dt.named_steps["encoding"])

    caminho = pipe_dt.named_steps["modelo"].decision_path(X_enc).indices
    regras = []
    for node_id in caminho[:-1]:
        feat_idx = arvore.feature[node_id]
        limiar = arvore.threshold[node_id]
        valor = float(X_enc[0, feat_idx])
        nome = nomes_feat[feat_idx]

        if " == '" in nome:
            cond = f"{nome}? {'NÃO' if valor <= limiar else 'SIM'}"
        elif nome.startswith("TE("):
            sinal = "<=" if valor <= limiar else ">"
            cond = f"{nome} = {valor * 100:.1f}% {sinal} {limiar * 100:.1f}%"
        else:
            sinal = "<=" if valor <= limiar else ">"
            cond = f"{nome} = {valor:,.1f} {sinal} {limiar:,.1f}"
        regras.append(cond)

    folha = caminho[-1]
    total_folha = int(arvore.n_node_samples[folha])
    return regras, len(regras), total_folha


@st.cache_resource(show_spinner="Treinando Arvore de Decisao e Random Forest (sem data leakage)...")
def treinar_classificadores():
    """Reproduz fielmente o split estratificado e os 2 pipelines de src/parte_especifica/classificador.ipynb."""
    df = pd.read_csv(CLEAN_PATH)
    cols_ignorar = ["id", "date_recorded", COL_ALVO, "idade_no_registro"]
    X = df.drop(columns=cols_ignorar).copy()
    y = df[COL_ALVO].copy()

    # Reversao controlada antes do split para evitar vazamento de medianas (Aula 26)
    X.loc[X["ausente_population"] == 1, "population"] = np.nan
    X.loc[X["ausente_construction_year"] == 1, "construction_year"] = np.nan
    X.loc[X["ausente_gps_height"] == 1, "gps_height"] = np.nan
    X.loc[X["ausente_coords"] == 1, ["longitude", "latitude"]] = np.nan

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    pipe_dt = Pipeline([
        ("imputacao", ImputadorCascata()),
        ("encoding", criar_preprocessador()),
        ("modelo", DecisionTreeClassifier(max_depth=15, min_samples_leaf=5, random_state=RANDOM_STATE)),
    ])
    pipe_dt.fit(X_train, y_train)

    pipe_rf = Pipeline([
        ("imputacao", ImputadorCascata()),
        ("encoding", criar_preprocessador()),
        ("modelo", RandomForestClassifier(
            n_estimators=200,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )),
    ])
    pipe_rf.fit(X_train, y_train)

    pred_dt = pipe_dt.predict(X_test)
    pred_rf = pipe_rf.predict(X_test)

    cm_dt = confusion_matrix(y_test, pred_dt, labels=STATUS_ORDEM)
    cm_rf = confusion_matrix(y_test, pred_rf, labels=STATUS_ORDEM)

    # Perfil base mediano/modal para o simulador de bomba
    perfil_base = {}
    for col in X.columns:
        if col in COLS_NUM:
            perfil_base[col] = float(df[col].median())
        else:
            perfil_base[col] = str(df[col].mode().iloc[0])

    return {
        "pipe_dt": pipe_dt,
        "pipe_rf": pipe_rf,
        "X_test": X_test,
        "y_test": y_test,
        "cm_dt": cm_dt,
        "cm_rf": cm_rf,
        "acc_dt": accuracy_score(y_test, pred_dt) * 100.0,
        "acc_rf": accuracy_score(y_test, pred_rf) * 100.0,
        "perfil_base": perfil_base,
    }


def gerar_resumo_markdown(df_filtrado, df_total, filtros_ativos):
    """Gera relatorio resumido em Markdown do recorte filtrado para download no dashboard."""
    n_tot = len(df_total)
    n_f = len(df_filtrado)
    dist = df_filtrado[COL_ALVO].value_counts(normalize=True).reindex(STATUS_ORDEM).fillna(0) * 100
    validos_idade = df_filtrado[df_filtrado["ausente_construction_year"] == 0]
    med_idade = validos_idade["idade_no_registro"].median() if len(validos_idade) > 0 else np.nan

    linhas = [
        "# Resumo do Recorte: Pump it Up (Tanzânia)",
        "",
        f"Gerado pelo dashboard Streamlit em {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
        "Fonte: DrivenData / Taarifa (Ministério de Águas da Tanzânia), registros de 2011 a 2013.",
        "",
        "## Filtros aplicados",
    ]
    for chave, valor in filtros_ativos.items():
        linhas.append(f"- {chave}: {valor}")

    linhas.extend([
        "",
        "## Indicadores principais do recorte",
        f"- Total de pontos d'água no recorte: {fmt_int(n_f)} ({fmt_pct(n_f / n_tot * 100)} da base limpa de {fmt_int(n_tot)})",
        f"- Funcionais (functional): {fmt_pct(dist['functional'])}",
        f"- Precisam de reparo (functional needs repair): {fmt_pct(dist['functional needs repair'])}",
        f"- Não funcionais (non functional): {fmt_pct(dist['non functional'])}",
        f"- Idade mediana (registros sem imputação, n = {fmt_int(len(validos_idade))}): "
        + (f"{fmt_num(med_idade, 1)} anos" if pd.notna(med_idade) else "sem registros válidos"),
        "",
        "## Taxa de inoperância por tecnologia de extração (top categorias no recorte)",
    ])

    if n_f > 0:
        tab_ext = (
            pd.crosstab(df_filtrado["extraction_type_class"], df_filtrado[COL_ALVO], normalize="index")
            .reindex(columns=STATUS_ORDEM, fill_value=0)
            .mul(100)
        )
        tab_ext["n"] = df_filtrado["extraction_type_class"].value_counts()
        tab_ext = tab_ext.sort_values("non functional", ascending=False)
        for cat, row in tab_ext.iterrows():
            linhas.append(
                f"- {cat} (n = {fmt_int(row['n'])}): "
                f"{fmt_pct(row['non functional'])} não funcionais, "
                f"{fmt_pct(row['functional'])} funcionais"
            )

    return "\n".join(linhas) + "\n"
