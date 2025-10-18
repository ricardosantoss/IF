import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ranking Simples", layout="wide")
st.title("Ranking — Ampla, PPI e PCD")

# ========================
# Leitura direta do arquivo local
# (O GitHub serve o arquivo como estático)
# ========================
df = pd.read_excel("notas.xlsx", dtype=str)

# Padroniza nomes em maiúsculas
df["Nome"] = df["Nome"].str.upper()

# Converte vírgulas e garante números
for col in ["Nota Preliminar", "Nota Objetiva", "Média Até Aqui"]:
    df[col] = df[col].fillna("").astype(str).str.replace(",", ".").astype(float)

# Ordena
df = df.sort_values("Média Até Aqui", ascending=False).reset_index(drop=True)
df["Classificação"] = df.index + 1

# Mantém uma cópia original para o estilo
orig = df

# Cria DataFrame apenas com as colunas visíveis (sem PPI/PCD)
df_show = df[["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]].copy()

# Formatação condicional (PPI em negrito, PCD em vermelho)
def highlight_from_original(row):
    idx = row.name
    style = ""
    if "PPI" in orig.columns and str(orig.loc[idx, "PPI"]).strip().lower() == "sim":
        style += "font-weight: bold;"
    if "PCD" in orig.columns and str(orig.loc[idx, "PCD"]).strip().lower() == "sim":
        style += "color: red;"
    return [style] * len(row)

# Exibição — AMPLA (sem PPI/PCD nas colunas)
st.write("### 🏁 Ranking Geral (Ampla com destaque para PPI e PCD)")
st.caption("**Legenda:** vermelho = PCD • preto em **negrito** = PPI")

st.table(
    df_show.style.apply(highlight_from_original, axis=1).format({
        "Nota Preliminar": "{:.2f}",
        "Nota Objetiva": "{:.2f}",
        "Média Até Aqui": "{:.2f}",
    })
)

# Subconjuntos (mantidos)
ppi = df[df["PPI"].str.lower() == "sim"]
pcd = df[df["PCD"].str.lower() == "sim"]

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
