import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload Dataset", layout="wide")

st.title("DataViz")
st.title("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="latin1")
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state["data"] = df
        st.session_state["filename"] = uploaded_file.name

        st.success("✅ Dataset uploaded successfully")
        st.subheader("🔍 Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"❌ {e}")

else:
    st.info("Please upload a dataset to continue.")
