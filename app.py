import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Page config with modern dark theme
st.set_page_config(
    page_title="AI Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini API client
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"❌ API Configuration Error: {e}")
    model = None

# Custom CSS for modern dark theme with user-friendly colors
st.markdown("""
<style>
    * {
        color-scheme: dark;
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Main container */
    .stMainBlockContainer {
        padding: 20px;
    }
    
    /* Headers with vibrant gradients */
    h1 {
        background: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 2.5em !important;
    }
    
    h2, h3 {
        background: linear-gradient(90deg, #10b981, #06b6d4, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 2px solid #06b6d4;
    }
    
    .stSidebar [data-testid="stSidebarNav"] {
        background: transparent;
    }
    
    /* Radio buttons and selection */
    [data-testid="stRadio"] {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #06b6d4;
    }
    
    /* Metrics with beautiful colors */
    .stMetric {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #06b6d4;
        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.2);
    }
    
    .stMetric label {
        color: #93c5fd !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 24px !important;
    }
    
    /* Buttons with gradient */
    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #0891b2);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0891b2, #0d9488);
        box-shadow: 0px 12px 30px rgba(6, 182, 212, 0.6);
        transform: translateY(-2px);
    }
    
    /* Selectbox and input fields */
    .stSelectbox, .stMultiSelect, .stFileUploader {
        background-color: #1e293b !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: #1e293b !important;
        border: 2px solid #06b6d4 !important;
        border-radius: 8px !important;
    }
    
    .stMultiSelect [data-baseweb="select"] {
        background: #1e293b !important;
        border: 2px solid #10b981 !important;
        border-radius: 8px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f172a;
        border-bottom: 2px solid #06b6d4;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 8px 8px 0 0;
        color: #cbd5e1;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #06b6d4, #0891b2);
        color: #ffffff;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 15px;
        color: #d1fae5;
    }
    
    /* Warning message */
    .stWarning {
        background: linear-gradient(135deg, #78350f 0%, #b45309 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 15px;
        color: #fef3c7;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, #7f1d1d 0%, #b91c1c 100%);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 15px;
        color: #fee2e2;
    }
    
    /* Info message */
    .stInfo {
        background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%);
        border-left: 4px solid #06b6d4;
        border-radius: 8px;
        padding: 15px;
        color: #cffafe;
    }
    
    /* Divider */
    .stDivider {
        border-color: #06b6d4;
        opacity: 0.6;
    }
    
    /* Captions */
    .stCaption {
        color: #06b6d4 !important;
        font-weight: 500;
    }
    
    /* Text styling */
    p {
        color: #e2e8f0 !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #06b6d4, #3b82f6);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0891b2, #2563eb);
    }
    
    /* Expander */
    .stExpander {
        background-color: #1e293b;
        border: 1px solid #06b6d4;
        border-radius: 8px;
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: #0f172a;
    }
    
    .stDataFrame thead {
        background-color: #1e293b;
    }
    
    .stDataFrame tbody tr {
        border-bottom: 1px solid #334155;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Dashboard")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["📤 Upload Data", "📈 Dashboard", "🤖 AI Insights"],
    help="Select a section to navigate"
)

# Main title
st.title("📊 AI Business Dashboard")
st.caption("✨ Transform your data into powerful business insights using AI")

# Upload section
if menu == "📤 Upload Data":
    st.subheader("📤 Upload Your Data")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        file = st.file_uploader(
            "📁 Upload your CSV file",
            type=["csv"],
            help="Select a CSV file to analyze"
        )
    
    if file:
        try:
            df = pd.read_csv(file)
            df.to_csv("data.csv", index=False)
            st.success("✅ File uploaded successfully!")
            st.info(f"📊 Dataset: {len(df)} rows × {len(df.columns)} columns")
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error uploading file: {e}")
else:
    file = None

# Load data
try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    df = None
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    df = None

# Dashboard
if menu == "📈 Dashboard" and df is not None:
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    df_filtered = df.copy()

    cat_cols = df.select_dtypes(include='object').columns
    
    for col in cat_cols:
        options = df[col].unique()
        selected = st.sidebar.multiselect(f"Filter {col}", options)
        
        if selected:
            df_filtered = df_filtered[df_filtered[col].isin(selected)]

    st.subheader("📊 Key Metrics")

    num_cols = df_filtered.select_dtypes(include='number').columns

    if len(num_cols) > 0:
        selected_kpi = st.selectbox("📈 Select KPI Column", num_cols)

        total = df_filtered[selected_kpi].sum()
        avg = df_filtered[selected_kpi].mean()
        max_val = df_filtered[selected_kpi].max()
        min_val = df_filtered[selected_kpi].min()

        col1, col2, col3, col4 = st.columns(4, gap="large")

        with col1:
            st.metric("💰 Total", f"{total:,.2f}")
        with col2:
            st.metric("📈 Average", f"{avg:,.2f}")
        with col3:
            st.metric("⬆️ Maximum", f"{max_val:,.2f}")
        with col4:
            st.metric("⬇️ Minimum", f"{min_val:,.2f}")

    st.divider()

    # Charts
    st.subheader("📈 Visual Analysis")

    chart_type = st.selectbox(
        "📊 Choose Chart Type",
        ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Area Chart"]
    )

    if chart_type == "Bar Chart" and len(cat_cols) > 0 and len(num_cols) > 0:
        x_col = st.selectbox("X-axis", cat_cols, key="bar_x")
        y_col = st.selectbox("Y-axis", num_cols, key="bar_y")

        fig = px.bar(
            df_filtered, 
            x=x_col, 
            y=y_col,
            color_discrete_sequence=['#06b6d4'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart" and len(num_cols) > 0:
        y_col = st.selectbox("Y-axis", num_cols, key="line_y")

        fig = px.line(
            df_filtered, 
            y=y_col,
            color_discrete_sequence=['#10b981'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie Chart" and len(cat_cols) > 0 and len(num_cols) > 0:
        names = st.selectbox("Category", cat_cols, key="pie_names")
        values = st.selectbox("Values", num_cols, key="pie_values")

        fig = px.pie(
            df_filtered,
            names=names,
            values=values,
            color_discrete_sequence=['#06b6d4', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#ec4899', '#3b82f6'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot" and len(num_cols) > 1:
        x_col = st.selectbox("X-axis", num_cols, key="scatter_x")
        y_col = st.selectbox("Y-axis", num_cols, key="scatter_y")

        fig = px.scatter(
            df_filtered,
            x=x_col,
            y=y_col,
            color_discrete_sequence=['#8b5cf6'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12),
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Area Chart" and len(num_cols) > 0:
        y_col = st.selectbox("Y-axis", num_cols, key="area_y")

        fig = px.area(
            df_filtered,
            y=y_col,
            color_discrete_sequence=['#f59e0b'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top performers
    st.subheader("🏆 Top Performers")

    if len(cat_cols) > 0 and len(num_cols) > 0:
        cat = cat_cols[0]
        num = num_cols[0]

        top_data = df_filtered.groupby(cat)[num].sum().sort_values(ascending=False).head(5)

        fig = px.bar(
            x=top_data.index,
            y=top_data.values,
            labels={"x": cat, "y": num},
            color_discrete_sequence=['#10b981'],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='#e2e8f0', size=12),
            xaxis_title=cat,
            yaxis_title=num,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

# AI Insights (Gemini)
if menu == "🤖 AI Insights" and df is not None:
    st.subheader("🤖 AI Insights Engine")
    st.info("💡 Get intelligent AI-powered analysis of your data using Google Gemini")

    if model is None:
        st.error("❌ Gemini API is not configured. Please add GEMINI_API_KEY to your Streamlit secrets.")
        st.write("**How to fix:**")
        st.write("1. Create a free API key at: https://makersuite.google.com/app/apikey")
        st.write("2. Add it to your Streamlit secrets (if using Streamlit Cloud):")
        st.code("GEMINI_API_KEY = 'your-api-key-here'")
        st.write("3. Or add it to `.streamlit/secrets.toml` (local development):")
        st.code("[GEMINI_API_KEY]\nGEMINI_API_KEY = 'your-api-key-here'")
    else:
        if st.button("🚀 Generate Insights", use_container_width=True):
            with st.spinner("🔍 Analyzing your data..."):
                try:
                    data_summary = df.describe().to_string()
                    
                    prompt = f"""You are a professional business analyst with expertise in data analysis and strategic insights.

Analyze this dataset and provide comprehensive business intelligence:

DATASET STATISTICS:
{data_summary}

DATASET INFORMATION:
- Total Records: {len(df):,}
- Total Columns: {len(df.columns)}
- Data Columns: {', '.join(df.columns)}
- Data Types: {dict(df.dtypes)}

Please provide a detailed analysis with these sections:

1. **📊 Executive Summary**
   - What does this data represent?
   - Overall health and status of the data

2. **📈 Key Trends & Patterns**
   - Identify main trends and patterns
   - Growth or decline indicators
   - Seasonal patterns (if applicable)

3. **💡 Business Insights**
   - Most important findings
   - What the metrics tell about business performance
   - Correlations and relationships

4. **⚠️ Risks & Concerns**
   - Potential risks or red flags
   - Areas of concern
   - Issues that need attention

5. **🎯 Opportunities**
   - Growth opportunities
   - Areas for improvement
   - Untapped potential

6. **💼 Recommendations**
   - Top 3-5 actionable recommendations
   - Priority order
   - Expected impact

Please format with clear headings and bullet points for easy reading."""

                    response = model.generate_content(prompt)
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Display the response in a nice format
                    st.markdown("""
                    <style>
                    .analysis-container {
                        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid #06b6d4;
                        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.2);
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error generating insights: {str(e)}")
                    st.info("**Troubleshooting:**")
                    st.write("- Verify your API key is correct")
                    st.write("- Check if your quota is exceeded")
                    st.write("- Try with a smaller dataset")
                    st.write("- Visit: https://makersuite.google.com/app/apikey to verify your key")

# If no data
if df is None:
    st.warning("⚠️ No data loaded. Please upload a dataset to get started.")
    st.info("📝 Navigate to '📤 Upload Data' section to upload your CSV file.")
