import streamlit as st
import pandas as pd
import json
from io import BytesIO

st.set_page_config(page_title="Upload Dataset", layout="wide")

st.title("DataViz")
st.title("📂 Upload Dataset")


uploaded_file = st.file_uploader(
    "Upload CSV, Excel, or JSON file",
    type=["csv", "xlsx", "xls", "json"]
)

def load_csv_any_encoding(file):
    """Try reading CSV with multiple encodings"""
    encodings = ["utf-8", "utf-8-sig", "latin1", "ISO-8859-1"]

    for enc in encodings:
        try:
            file.seek(0)
            return pd.read_csv(file, encoding=enc)
        except Exception:
            continue

    # Last fallback (let pandas guess)
    file.seek(0)
    return pd.read_csv(file, encoding_errors="replace")


def load_json_any_format(file):
    """Load JSON supporting records, dict, or nested formats"""
    file.seek(0)
    try:
        data = json.load(file)
        return pd.json_normalize(data)
    except Exception:
        file.seek(0)
        return pd.read_json(file)


if uploaded_file is not None:
    try:
        file_name = uploaded_file.name.lower()

        # ---------------- CSV ----------------
        if file_name.endswith(".csv"):
            df = load_csv_any_encoding(uploaded_file)

        # ---------------- EXCEL ----------------
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        # ---------------- JSON ----------------
        elif file_name.endswith(".json"):
            df = load_json_any_format(uploaded_file)

        # Save to session
        st.session_state["data"] = df
        st.session_state["original_data"] = df.copy()

        st.success("✅ Dataset uploaded successfully")
        st.subheader("🔍 Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")

else:
    st.info("Please upload a CSV, Excel, or JSON file to continue.")

