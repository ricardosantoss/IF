import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ranking Simples", layout="wide")
st.title("Ranking — Ampla, PPI e PCD")

# ========================
# Leitura direta do arquivo local
# (O GitHub serve o arquivo como estático)
# ========================
df = pd.read_excel("notas.xlsx", dtype=str)

# Converte vírgulas e garante números
for col in ["Nota Preliminar", "Nota Objetiva", "Média Até Aqui"]:
    df[col] = df[col].fillna("").astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Ordena
df = df.sort_values("Média Até Aqui", ascending=False).reset_index(drop=True)
df["Classificação"] = df.index + 1

# >>> Apenas excluir as colunas PPI e PCD da exibição da AMPLA
cols_ampla = ["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]
df_ampla = df[cols_ampla].copy()

# Formatação condicional (mantida): PPI em negrito, PCD em vermelho
def highlight(row):
    idx = row.name  # mesmo índice de df
    style = ""
    if "PPI" in df.columns and str(df.loc[idx, "PPI"]).strip().lower() == "sim":
        style += "font-weight: bold;"
    if "PCD" in df.columns and str(df.loc[idx, "PCD"]).strip().lower() == "sim":
        style += "color: red;"
    return [style] * len(row)

# Exibição — AMPLA (sem colunas PPI/PCD)
st.write("### 🏁 Ranking Geral (Ampla)")
st.table(
    df_ampla.style.apply(highlight, axis=1).format({
        "Nota Preliminar": "{:.2f}",
        "Nota Objetiva": "{:.2f}",
        "Média Até Aqui": "{:.2f}",
    })
)

# Subconjuntos (já não exibiam PPI/PCD nas colunas)
ppi = df[df["PPI"].str.lower() == "sim"] if "PPI" in df.columns else df.iloc[0:0]
pcd = df[df["PCD"].str.lower() == "sim"] if "PCD" in df.columns else df.iloc[0:0]

st.write("### 🟣 PPI")
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
