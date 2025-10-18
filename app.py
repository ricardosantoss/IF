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
    df[col] = df[col].str.replace(",", ".").astype(float)

# Ordena
df = df.sort_values("Média Até Aqui", ascending=False).reset_index(drop=True)
df["Classificação"] = df.index + 1

# Formatação condicional (PPI em negrito, PCD em vermelho)
def highlight(row):
    style = ""
    if str(row["PPI"]).strip().lower() == "sim":
        style += "font-weight: bold;"
    if str(row["PCD"]).strip().lower() == "sim":
        style += "color: red;"
    return [style] * len(row)

# Exibição
st.write("### 🏁 Ranking Geral (Ampla com destaque para PPI e PCD)")
st.dataframe(
    df.style.apply(highlight, axis=1).format({
        "Nota Preliminar": "{:.2f}",
        "Nota Objetiva": "{:.2f}",
        "Média Até Aqui": "{:.2f}",
    }),
    use_container_width=True,
)

# Subconjuntos
ppi = df[df["PPI"].str.lower() == "sim"]
pcd = df[df["PCD"].str.lower() == "sim"]

st.write("### 🟣 PPI")
st.dataframe(ppi[["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]])

st.write("### 🔴 PCD")
st.dataframe(pcd[["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"]])
