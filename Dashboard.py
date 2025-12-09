# 📊 Enhanced MSME Dashboard (AI-Ready Version)
# Developed using Streamlit + Plotly + Pandas
# Author: Prince Arockyam (2025)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="MSME Business Dashboard", page_icon="📈", layout="wide")

st.title("📈 MSME Business Intelligence Dashboard")
st.markdown("#### *AI-powered insights for data-driven MSMEs*")

# ----------------------------
# Sidebar: File Upload & Settings
# ----------------------------
st.sidebar.header("⚙️ Dashboard Settings")
uploaded_file = st.sidebar.file_uploader("📤 Upload your sales dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df

    # ----------------------------
    # Data Overview
    # ----------------------------
    st.subheader("📋 Dataset Overview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    text_cols = df.select_dtypes(include=["object"]).columns.tolist()

    st.markdown("---")

    # ----------------------------
    # KPI Section
    # ----------------------------
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Records", len(df))
    if len(numeric_cols) >= 1:
        col2.metric(f"💰 Total {numeric_cols[0]}", f"{df[numeric_cols[0]].sum():,.2f}")
    if len(numeric_cols) >= 2:
        col3.metric(f"📈 Total {numeric_cols[1]}", f"{df[numeric_cols[1]].sum():,.2f}")

    st.markdown("---")

    # ----------------------------
    # Filters
    # ----------------------------
    st.sidebar.header("🔍 Filters")
    filter_col = st.sidebar.selectbox("Select column to filter (optional)", text_cols)
    unique_vals = df[filter_col].unique() if filter_col else []
    selected_val = st.sidebar.selectbox(f"Filter {filter_col} by:", unique_vals) if filter_col else None

    if selected_val:
        df = df[df[filter_col] == selected_val]
        st.success(f"✅ Filter applied: {filter_col} = {selected_val}")

    # ----------------------------
    # Chart Selection
    # ----------------------------
    st.subheader("📉 Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Area Chart", "Donut Chart", "Scatter Plot", "Gauge Chart"]
    )

    x_axis = st.selectbox("Select X-axis", df.columns, index=0)
    y_axis = st.selectbox("Select Y-axis", numeric_cols, index=0)

    fig = None
    if chart_type == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, markers=True, title=f"{y_axis} over {x_axis}")
    elif chart_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, title=f"{y_axis} by {x_axis}")
    elif chart_type == "Area Chart":
        fig = px.area(df, x=x_axis, y=y_axis, title=f"{y_axis} Trend (Area)")
    elif chart_type == "Donut Chart":
        fig = px.pie(df, names=x_axis, values=y_axis, hole=0.5, title="Category Distribution")
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, size=y_axis, title=f"{y_axis} vs {x_axis}")
    elif chart_type == "Gauge Chart":
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=df[y_axis].mean(),
            title={"text": f"Average {y_axis}"},
            gauge={"axis": {"range": [0, df[y_axis].max()]}}
        ))

    if fig:
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📂 Please upload your dataset using the sidebar to begin.")
