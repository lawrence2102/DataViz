import streamlit as st
import pandas as pd

st.set_page_config(page_title="Clean Data", layout="wide")
st.title("🧹 Clean Dataset")

# ------------------ Data Check ------------------
if "data" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

# Store original dataset once
if "original_data" not in st.session_state:
    st.session_state["original_data"] = st.session_state["data"].copy()

df = st.session_state["data"]

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# ------------------ Cleaning Actions ------------------
CLEAN_ACTIONS = [
    "Remove Duplicates",
    "Handle Numeric Missing",
    "Handle Categorical Missing",
    "Handle Binary Columns",
    "Delete Rows with Nulls",
    "Delete Columns with Nulls",
    "Drop Columns",
    "Rename Column",
    "Reset Dataset"
]

st.subheader("📌 Select a Cleaning Action")

cols = st.columns(3)
for i, action in enumerate(CLEAN_ACTIONS):
    if cols[i % 3].button(action):
        st.session_state["clean_action"] = action

action = st.session_state.get("clean_action")

# ------------------ Parameter Section ------------------
if action:
    st.divider()
    st.subheader(f"⚙️ Parameters — {action}")

    # =================================================
    # 🔁 REMOVE DUPLICATES
    # =================================================
    if action == "Remove Duplicates":
        dup_count = df.duplicated().sum()
        st.write(f"Duplicate Rows Found: **{dup_count}**")

        if st.button("Apply"):
            st.session_state["data"] = df.drop_duplicates()
            st.success("Duplicate rows removed")

    # =================================================
    # 🩹 HANDLE NUMERIC MISSING (COLUMN-LEVEL)
    # =================================================
    elif action == "Handle Numeric Missing":
        num_null_cols = [c for c in num_cols if df[c].isnull().any()]

        if not num_null_cols:
            st.info("✅ No numeric columns contain null values.")
        else:
            selected_cols = st.multiselect(
                "Select Numeric Columns (with nulls only)",
                num_null_cols
            )

            strategy = st.selectbox(
                "Strategy",
                ["Fill with Mean", "Fill with Median", "Fill with Zero", "Drop Rows"]
            )

            ready = len(selected_cols) > 0

            if st.button("Apply", disabled=not ready):
                df_new = df.copy()

                for col in selected_cols:
                    if strategy == "Fill with Mean":
                        df_new[col] = df_new[col].fillna(df_new[col].mean())
                    elif strategy == "Fill with Median":
                        df_new[col] = df_new[col].fillna(df_new[col].median())
                    elif strategy == "Fill with Zero":
                        df_new[col] = df_new[col].fillna(0)

                if strategy == "Drop Rows":
                    df_new = df_new.dropna(subset=selected_cols)

                st.session_state["data"] = df_new
                st.success("Numeric missing values handled for selected columns only")

    # =================================================
    # 🩹 HANDLE CATEGORICAL MISSING (COLUMN-LEVEL)
    # =================================================
    elif action == "Handle Categorical Missing":
        cat_null_cols = [c for c in cat_cols if df[c].isnull().any()]

        if not cat_null_cols:
            st.info("✅ No categorical columns contain null values.")
        else:
            selected_cols = st.multiselect(
                "Select Categorical Columns (with nulls only)",
                cat_null_cols
            )

            strategy = st.selectbox(
                "Strategy",
                ["Fill with Mode", "Fill with 'Unknown'", "Drop Rows"]
            )

            ready = len(selected_cols) > 0

            if st.button("Apply", disabled=not ready):
                df_new = df.copy()

                for col in selected_cols:
                    if strategy == "Fill with Mode":
                        if not df_new[col].mode().empty:
                            df_new[col] = df_new[col].fillna(df_new[col].mode()[0])
                    elif strategy == "Fill with 'Unknown'":
                        df_new[col] = df_new[col].fillna("Unknown")

                if strategy == "Drop Rows":
                    df_new = df_new.dropna(subset=selected_cols)

                st.session_state["data"] = df_new
                st.success("Categorical missing values handled for selected columns only")

    # =================================================
    # 🔘 HANDLE BINARY (YES / NO / NULL)
    # =================================================
    elif action == "Handle Binary Columns":
        cat_null_cols = [c for c in cat_cols if df[c].isnull().any()]

        if not cat_null_cols:
            st.info("✅ No binary-like columns contain null values.")
        else:
            selected_cols = st.multiselect(
                "Select Binary Columns",
                cat_null_cols
            )

            transform = st.selectbox(
                "Transformation",
                [
                    "Fill Null with 'No'",
                    "Fill Null with 'Yes'",
                    "Convert to Boolean (True/False)",
                    "Convert to Numeric (1/0)"
                ]
            )

            ready = len(selected_cols) > 0

            if st.button("Apply", disabled=not ready):
                df_new = df.copy()

                for col in selected_cols:
                    normalized = (
                        df_new[col]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .replace({"nan": None, "null": None})
                    )

                    if transform == "Fill Null with 'No'":
                        df_new[col] = normalized.fillna("No")

                    elif transform == "Fill Null with 'Yes'":
                        df_new[col] = normalized.fillna("Yes")

                    elif transform == "Convert to Boolean (True/False)":
                        df_new[col] = normalized.map({"yes": True, "no": False})

                    elif transform == "Convert to Numeric (1/0)":
                        df_new[col] = normalized.map({"yes": 1, "no": 0})

                st.session_state["data"] = df_new
                st.success("Binary columns handled successfully")

    # =================================================
    # ❌ DELETE ROWS WITH NULLS (FILTERED DROPDOWN)
    # =================================================
    elif action == "Delete Rows with Nulls":
        null_cols = df.columns[df.isnull().any()].tolist()

        if not null_cols:
            st.info("✅ No columns contain null values. Nothing to delete.")
        else:
            selected_cols = st.multiselect(
                "Select Columns (only columns with nulls shown)",
                null_cols
            )

            condition = st.radio(
                "Deletion Condition",
                ["If ANY selected column is null", "If ALL selected columns are null"]
            )

            ready = len(selected_cols) > 0

            if st.button("Apply", disabled=not ready):
                if condition == "If ANY selected column is null":
                    df_new = df.dropna(subset=selected_cols, how="any")
                else:
                    df_new = df.dropna(subset=selected_cols, how="all")

                st.session_state["data"] = df_new
                st.success("Rows with null values deleted successfully")

    # =================================================
    # ❌ DELETE COLUMNS WITH NULLS
    # =================================================
    elif action == "Delete Columns with Nulls":
        null_cols = df.columns[df.isnull().any()].tolist()

        if not null_cols:
            st.info("✅ No columns contain null values.")
        else:
            selected_cols = st.multiselect(
                "Select Columns (only columns with nulls shown)",
                null_cols
            )

            ready = len(selected_cols) > 0

            if st.button("Apply", disabled=not ready):
                st.session_state["data"] = df.drop(columns=selected_cols)
                st.success("Selected columns with nulls dropped")

    # =================================================
    # 🗑️ DROP COLUMNS (MANUAL)
    # =================================================
    elif action == "Drop Columns":
        drop_cols = st.multiselect("Select Columns to Drop", df.columns)
        ready = len(drop_cols) > 0

        if st.button("Apply", disabled=not ready):
            st.session_state["data"] = df.drop(columns=drop_cols)
            st.success("Selected columns dropped")

    # =================================================
    # ✏️ RENAME COLUMN
    # =================================================
    elif action == "Rename Column":
        col = st.selectbox("Select Column", df.columns)
        new_name = st.text_input("New Column Name")
        ready = bool(new_name)

        if st.button("Apply", disabled=not ready):
            st.session_state["data"] = df.rename(columns={col: new_name})
            st.success("Column renamed")

    # =================================================
    # 🔄 RESET DATASET
    # =================================================
    elif action == "Reset Dataset":
        if st.button("Reset to Original Dataset"):
            st.session_state["data"] = st.session_state["original_data"].copy()
            st.success("Dataset reset to original state")

# ------------------ PREVIEW ------------------
st.divider()
st.subheader("🔍 Current Dataset Preview")
st.dataframe(st.session_state["data"].head(10), use_container_width=True)
