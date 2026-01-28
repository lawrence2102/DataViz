import streamlit as st
import pandas as pd

st.set_page_config(page_title="Explore Data", layout="wide")
st.title("🔎 Explore Dataset")

if "data" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["data"]

# ---------- Dataset Overview ----------
st.subheader("📊 Dataset Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Rows", df.shape[0])
c2.metric("Columns", df.shape[1])
c3.metric("Missing Values", df.isnull().sum().sum())

st.divider()

# ---------- Duplicate Rows Indicator ----------
st.subheader("🔁 Duplicate Rows")

total_rows = df.shape[0]
duplicate_rows = df.duplicated().sum()

duplicate_percentage = (
    (duplicate_rows / total_rows) * 100
    if total_rows > 0 else 0
)

c1, c2 = st.columns(2)
c1.metric("Duplicate Rows", duplicate_rows)
c2.metric("Duplicate Percentage", f"{duplicate_percentage:.2f}%")

st.divider()

# ---------- Column Types ----------
st.subheader("🧬 Column Types")

col_types = df.dtypes.reset_index()
col_types.columns = ["Column Name", "Data Type"]
col_types["Data Type"] = col_types["Data Type"].astype(str)

st.dataframe(col_types, use_container_width=True)

st.divider()

# ---------- Columns Grouped by Data Type ----------
st.subheader("🧬 Columns Grouped by Data Type")

dtype_groups = {}

for column, dtype in df.dtypes.items():
    dtype_name = str(dtype)
    if dtype_name not in dtype_groups:
        dtype_groups[dtype_name] = []
    dtype_groups[dtype_name].append(column)

# Display grouped columns
for dtype, columns in dtype_groups.items():
    with st.expander(f"{dtype} ({len(columns)})"):
        for col in columns:
            st.write(f"• {col}")

st.divider()

# ---------- Descriptive Statistics ----------
st.subheader("📈 Descriptive Statistics (Numeric Columns)")
st.dataframe(df.describe(), use_container_width=True)

st.divider()

# ---------- Missing Values ----------
st.subheader("🧩 Missing Values Summary")

missing_df = df.isnull().sum().reset_index()
missing_df.columns = ["Column", "Missing Count"]
missing_df = missing_df[missing_df["Missing Count"] > 0]

if missing_df.empty:
    st.success("No missing values found 🎉")
else:
    st.dataframe(missing_df, use_container_width=True)
