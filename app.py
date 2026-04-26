import streamlit as st
import pandas as pd
import plotly.express as px # pyright: ignore[reportMissingImports]
from groq import Groq

# Page config

st.set_page_config(page_title="AI Business Dashboard", page_icon="📊", layout="wide")

# Initialize Groq client

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Custom CSS

st.markdown("""

<style>
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    text-align: center;
}
</style>

""", unsafe_allow_html=True)

# Sidebar

st.sidebar.title("📊 Dashboard")
menu = st.sidebar.radio("Navigation", ["Upload Data", "Dashboard", "AI Insights"])

st.title("📊 AI Business Dashboard")
st.caption("Turn your data into actionable insights using AI")

# Upload section

if menu == "Upload Data":
    file = st.file_uploader("Upload your CSV file", type=["csv"])


if file:
    df = pd.read_csv(file)
    df.to_csv("data.csv", index=False)
    st.success("File uploaded successfully!")


# Load data

try:
    df = pd.read_csv("data.csv")
except:
    df = None

# Dashboard

if menu == "Dashboard" and df is not None:

# Sidebar filters
    st.sidebar.header("🔍 Filters")
    df_filtered = df.copy()

    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        options = df[col].unique()
        selected = st.sidebar.multiselect(f"{col}", options)

    if selected:
        df_filtered = df_filtered[df_filtered[col].isin(selected)]

st.subheader("📊 Key Metrics")

num_cols = df_filtered.select_dtypes(include='number').columns

if len(num_cols) > 0:
    selected_kpi = st.selectbox("Select KPI Column", num_cols)

    total = df_filtered[selected_kpi].sum()
    avg = df_filtered[selected_kpi].mean()
    max_val = df_filtered[selected_kpi].max()
    min_val = df_filtered[selected_kpi].min()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", f"{total:.2f}")
    col2.metric("Average", f"{avg:.2f}")
    col3.metric("Max", f"{max_val:.2f}")
    col4.metric("Min", f"{min_val:.2f}")

st.divider()

# Charts
st.subheader("📈 Visual Analysis")

chart_type = st.selectbox("Choose Chart Type", ["Bar", "Line", "Pie"])

if chart_type == "Bar" and len(cat_cols) > 0:
    x_col = st.selectbox("X-axis", cat_cols)
    y_col = st.selectbox("Y-axis", num_cols)

    fig = px.bar(df_filtered, x=x_col, y=y_col)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line":
    y_col = st.selectbox("Y-axis", num_cols)

    fig = px.line(df_filtered, y=y_col)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie" and len(cat_cols) > 0:
    names = st.selectbox("Category", cat_cols)
    values = st.selectbox("Values", num_cols)

    fig = px.pie(df_filtered, names=names, values=values)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Top performers
st.subheader("🏆 Top Performers")

if len(cat_cols) > 0 and len(num_cols) > 0:
    cat = cat_cols[0]
    num = num_cols[0]

    top_data = df_filtered.groupby(cat)[num].sum().sort_values(ascending=False).head(5)

    fig = px.bar(top_data, x=top_data.index, y=top_data.values)
    st.plotly_chart(fig, use_container_width=True)


# AI Insights (Groq)

if menu == "AI Insights" and df is not None:

    st.subheader("🤖 AI Insights Engine")

if st.button("Generate Insights"):
    with st.spinner("Analyzing data..."):

        prompt = f"""
        You are a business analyst.

        Analyze this dataset summary:
        {df.describe()}

        Provide:
        - Key trends
        - Risks
        - Opportunities
        - Recommendations
        """

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("Analysis Complete!")
        st.write(response.choices[0].message.content)


# If no data

if df is None:
    st.warning("Please upload a dataset to get started.")
