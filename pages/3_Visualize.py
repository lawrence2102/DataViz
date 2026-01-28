import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Visualize Data", layout="wide")
st.title("📊 Visualize Dataset")

# ------------------ Data Check ------------------
if "data" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["data"]

# ------------------ Column Groups ------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
datetime_cols = df.select_dtypes(include="datetime").columns.tolist()

# ------------------ Plot Buttons ------------------
PLOTS = [
    "Histogram", "Box Plot", "Bar Chart", "Count Plot",
    "Scatter Plot", "Line Chart", "Correlation Heatmap",
    "Area Chart", "Violin Plot", "Pair Plot",
    "Sunburst", "Choropleth Map"
]

st.subheader("📌 Select a Plot")

cols = st.columns(4)
for i, plot in enumerate(PLOTS):
    if cols[i % 4].button(plot):
        st.session_state["selected_plot"] = plot

plot_type = st.session_state.get("selected_plot")

# ------------------ Parameter Section ------------------
if plot_type:
    st.divider()
    st.subheader(f"⚙️ Parameters — {plot_type}")

    params = {}
    ready = True

    # ---------- HISTOGRAM ----------
    if plot_type == "Histogram":
        params["x"] = st.multiselect("Numeric Columns", numeric_cols)
        params["bins"] = st.slider("Bins", 5, 100, 30)
        ready = len(params["x"]) > 0

    # ---------- BOX ----------
    elif plot_type == "Box Plot":
        params["y"] = st.multiselect("Numeric Columns", numeric_cols)
        params["x"] = st.selectbox("Category (Optional)", [None] + categorical_cols)
        ready = len(params["y"]) > 0

    # ---------- BAR ----------
    elif plot_type == "Bar Chart":
        params["x"] = st.selectbox("Category", categorical_cols)
        params["y"] = st.multiselect("Numeric Metrics", numeric_cols)
        ready = len(params["y"]) > 0

    # ---------- COUNT ----------
    elif plot_type == "Count Plot":
        params["x"] = st.selectbox("Category Column", categorical_cols)

    # ---------- SCATTER ----------
    elif plot_type == "Scatter Plot":
        params["x"] = st.selectbox("X Axis", numeric_cols)
        params["y"] = st.multiselect("Y Axis (Multi)", numeric_cols)
        params["color"] = st.selectbox("Color (Optional)", [None] + categorical_cols)
        ready = len(params["y"]) > 0

    # ---------- LINE ----------
    elif plot_type == "Line Chart":
        if not datetime_cols:
            st.warning("No datetime column available.")
            ready = False
        else:
            params["x"] = st.selectbox("Datetime Column", datetime_cols)
            params["y"] = st.multiselect("Y Axis (Multi)", numeric_cols)
            ready = len(params["y"]) > 0

    # ---------- HEATMAP ----------
    elif plot_type == "Correlation Heatmap":
        params["cols"] = st.multiselect("Numeric Columns", numeric_cols)
        ready = len(params["cols"]) >= 2

    # ---------- AREA ----------
    elif plot_type == "Area Chart":
        params["x"] = st.selectbox("X Axis", datetime_cols + categorical_cols)
        params["y"] = st.multiselect("Numeric Columns", numeric_cols)
        ready = len(params["y"]) > 0

    # ---------- VIOLIN ----------
    elif plot_type == "Violin Plot":
        params["y"] = st.multiselect("Numeric Columns", numeric_cols)
        params["x"] = st.selectbox("Category (Optional)", [None] + categorical_cols)
        ready = len(params["y"]) > 0

    # ---------- PAIR ----------
    elif plot_type == "Pair Plot":
        params["cols"] = st.multiselect("Numeric Columns", numeric_cols)
        ready = len(params["cols"]) >= 2

    # ---------- SUNBURST ----------
    elif plot_type == "Sunburst":
        params["path"] = st.multiselect("Hierarchy Columns", categorical_cols)
        params["values"] = st.selectbox("Numeric Value", numeric_cols)
        ready = len(params["path"]) > 0

    # ---------- MAP ----------
    elif plot_type == "Choropleth Map":
        params["location"] = st.selectbox("Location Column", categorical_cols)
        params["value"] = st.selectbox("Numeric Value", numeric_cols)

    # ------------------ Generate Plot ------------------
    st.divider()
    if st.button("📈 Generate Plot", disabled=not ready):

        if plot_type == "Histogram":
            fig = px.histogram(df, x=params["x"], nbins=params["bins"])

        elif plot_type == "Box Plot":
            fig = px.box(df, y=params["y"], x=params["x"])

        elif plot_type == "Bar Chart":
            fig = px.bar(df, x=params["x"], y=params["y"])

        elif plot_type == "Count Plot":
            fig = px.histogram(df, x=params["x"])

        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=params["x"], y=params["y"], color=params["color"])

        elif plot_type == "Line Chart":
            fig = px.line(df, x=params["x"], y=params["y"])

        elif plot_type == "Correlation Heatmap":
            fig = px.imshow(df[params["cols"]].corr(), text_auto=True)

        elif plot_type == "Area Chart":
            fig = px.area(df, x=params["x"], y=params["y"])

        elif plot_type == "Violin Plot":
            fig = px.violin(df, y=params["y"], x=params["x"], box=True)

        elif plot_type == "Pair Plot":
            fig = px.scatter_matrix(df[params["cols"]])

        elif plot_type == "Sunburst":
            fig = px.sunburst(df, path=params["path"], values=params["values"])

        elif plot_type == "Choropleth Map":
            fig = px.choropleth(
                df,
                locations=params["location"],
                color=params["value"],
                locationmode="country names"
            )

        st.plotly_chart(fig, use_container_width=True)
