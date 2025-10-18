# app.py
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ranking Simples", layout="wide")
st.title("Ranking — Ampla, PPI e PCD")

# ========================
# Leitura direta do arquivo local (notas.xlsx no repo)
# ========================
df = pd.read_excel("notas.xlsx", dtype=str)

# Converte vírgulas e garante números
for col in ["Nota Preliminar", "Nota Objetiva", "Média Até Aqui"]:
    # trata NaN e vírgula decimal
    df[col] = (
        df[col]
        .fillna("")
        .astype(str)
        .str.replace(".", "", regex=False)      # remove separador de milhar "1.234,56"
        .str.replace(",", ".", regex=False)     # converte vírgula decimal
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Ordena por Média Até Aqui (desc) e cria classificação
df = df.sort_values("Média Até Aqui", ascending=False).reset_index(drop=True)
df["Classificação"] = df.index + 1

# Normaliza flags (aceita 'sim' e variações)
def _is_sim(x):
    return str(x).strip().lower() in {"sim", "s", "true", "1", "x", "yes", "y"}

# Guardamos flags normalizadas em colunas auxiliares (sem exibir)
df["_is_ppi"] = df["PPI"].apply(_is_sim) if "PPI" in df.columns else False
df["_is_pcd"] = df["PCD"].apply(_is_sim) if "PCD" in df.columns else False

# Colunas que serão exibidas na Ampla (sem PPI/PCD)
cols_show = ["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]
df_show = df[cols_show].copy()

# Formatação condicional (usa as flags do df original pelos índices)
def highlight(row):
    idx = row.name  # índice da linha em df_show coincide com df
    style = ""
    if df.loc[idx, "_is_ppi"]:
        style += "font-weight: bold;"
    if df.loc[idx, "_is_pcd"]:
        style += "color: red;"
    return [style] * len(row)

# ===== Exibição =====
st.write("### 🏁 Ranking Geral (Ampla)")
st.caption("**Legenda:** vermelho = PCD • preto em **negrito** = PPI")

st.table(
    df_show.style.apply(highlight, axis=1).format({
        "Nota Preliminar": "{:.2f}",
        "Nota Objetiva": "{:.2f}",
        "Média Até Aqui": "{:.2f}",
    })
)

# Subconjuntos (mantendo a mesma ordenação)
ppi = df[df["_is_ppi"]].copy()
pcd = df[df["_is_pcd"]].copy()

st.write("### 🟣 PPI")
if ppi.empty:
    st.info("Nenhum candidato marcado como PPI.")
else:
    st.dataframe(
        ppi[["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]]
        .style.format({
            "Nota Preliminar": "{:.2f}",
            "Nota Objetiva": "{:.2f}",
            "Média Até Aqui": "{:.2f}",
        }),
        use_container_width=True,
        height=(len(ppi) + 1) * 35
    )

st.write("### 🔴 PCD")
if pcd.empty:
    st.info("Nenhum candidato marcado como PCD.")
else:
    st.dataframe(
        pcd[["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]]
        .style.format({
            "Nota Preliminar": "{:.2f}",
            "Nota Objetiva": "{:.2f}",
            "Média Até Aqui": "{:.2f}",
        }),
        use_container_width=True,
        height=(len(pcd) + 1) * 35
    )

