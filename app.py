import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ranking Simples", layout="wide")
st.title("Ranking — Ampla, PPI e PCD")

# ========================
# Leitura do arquivo local (no repo do GitHub)
# ========================
df = pd.read_excel("notas.xlsx", dtype=str)

# Padroniza nomes em maiúsculas
if "Nome" in df.columns:
    df["Nome"] = df["Nome"].astype(str).str.upper()

# ---- Conversão numérica robusta (vírgula decimal, milhar, vazios) ----
def to_num_safe(s):
    if pd.isna(s):
        return pd.NA
    s = str(s).strip()
    if s == "" or s in {"-", "—"}:
        return pd.NA
    # remove separador de milhar e converte vírgula para ponto
    s = s.replace(".", "").replace(",", ".")
    return pd.to_numeric(s, errors="coerce")

for col in ["Nota Preliminar", "Nota Objetiva", "Média Até Aqui"]:
    if col in df.columns:
        df[col] = df[col].apply(to_num_safe)

# Ordena e cria classificação
df = df.sort_values("Média Até Aqui", ascending=False, na_position="last").reset_index(drop=True)
df["Classificação"] = df.index + 1

# Mantém uma cópia original para o estilo (lógica PPI/PCD)
orig = df

# AMPLA sem as colunas PPI/PCD
cols_ampla = [c for c in ["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"] if c in df.columns]
df_show = df[cols_ampla].copy()

# Formatação condicional: PPI em negrito, PCD em vermelho
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
    }, na_rep="")
)

# Subconjuntos (mantidos)
if "PPI" in df.columns:
    ppi = df[df["PPI"].astype(str).str.lower() == "sim"]
else:
    ppi = df.iloc[0:0]

if "PCD" in df.columns:
    pcd = df[df["PCD"].astype(str).str.lower() == "sim"]
else:
    pcd = df.iloc[0:0]

st.write("### 🟣 PPI")
if len(ppi) == 0:
    st.info("Nenhum candidato marcado como PPI.")
else:
    st.dataframe(
        ppi[[c for c in ["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"] if c in ppi.columns]]
            .style.format({
                "Nota Preliminar": "{:.2f}",
                "Nota Objetiva": "{:.2f}",
                "Média Até Aqui": "{:.2f}",
            }, na_rep=""),
        use_container_width=True,
        height=(len(ppi) + 1) * 35
    )

st.write("### 🔴 PCD")
if len(pcd) == 0:
    st.info("Nenhum candidato marcado como PCD.")
else:
    st.dataframe(
        pcd[[c for c in ["Classificação", "Nome", "Média Até Aqui", "Nota Preliminar", "Nota Objetiva"] if c in pcd.columns]]
            .style.format({
                "Nota Preliminar": "{:.2f}",
                "Nota Objetiva": "{:.2f}",
                "Média Até Aqui": "{:.2f}",
            }, na_rep=""),
        use_container_width=True,
        height=(len(pcd) + 1) * 35
    )

