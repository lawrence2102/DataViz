# 📊 DataViz App

**Live Demo:** https://dataviz-1.streamlit.app/

An interactive multi-page data analysis application built with **Streamlit**, **Pandas**, and **Plotly** — designed for exploratory data analysis (EDA), cleaning, and visualization without writing a single line of code.

---

## 🚀 Overview

This app provides a guided data analysis experience through four intuitive sections:

1. **Upload Dataset** — Upload CSV / Excel files  
2. **Explore Data** — Summary, column types, missing values, duplicates  
3. **Clean Data** — Button-driven cleaning actions (same UX as visualize)  
4. **Visualize Data** — Interactive Plotly visualizations with dynamic parameters

All actions are:
- Explicit and user-controlled
- Context-aware (only relevant inputs shown)
- Safe, reversible, and session-managed

---

## 📦 Features

### 🗂 Upload Page
- Accepts `.csv` (UTF-8/Latin-1/ISO encodings) and `.xlsx`
- Preview first rows after upload
- Stores data in session state for downstream pages

### 📋 Explore Page
- Dataset overview (rows, columns)
- Column type grouping by inferred dtypes
- Missing values summary & percentages
- Duplicate row detection
- Dynamic lists of columns by data type

### 🧹 Clean Page
Button-based cleaning actions:
- Remove duplicates
- Handle missing values (numeric & categorical) on selected columns
- Binary (Yes/No/Null) handling with multiple conversion options
- Delete rows with nulls (with condition options)
- Delete columns with nulls
- Drop columns manually
- Rename columns
- Reset to original dataset

Each action reveals only **relevant parameters** and executes only on click.

### 📈 Visualize Page
Interactive Plotly charts:
- Histogram
- Box plot
- Bar chart
- Count plot
- Scatter plot
- Line chart
- Correlation heatmap
- Area chart
- Violin plot
- Pair plot
- Sunburst
- Choropleth map

All parameter inputs (column selectors, multi-selects) appear dynamically based on plot type and dataset metadata.

---

## 🧪 Usage

1. **Upload** a dataset in CSV or Excel format.
2. Navigate to **Explore** to audit the dataset.
3. Go to **Clean** to fix issues such as missing values or duplicates.
4. Visit **Visualize** to generate interactive charts.

Your cleaned and visualized data helps you understand patterns without programming.

---

## 📁 Folder Structure

```plaintext
dataviz_app/
│
├── app.py                  # Upload page
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_Explore.py
│   ├── 2_Clean.py
│   └── 3_Visualize.py
