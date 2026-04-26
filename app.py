import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# Page config with dark theme
st.set_page_config(
    page_title="AI Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini API client
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Custom CSS for dark theme with colorful UI
st.markdown("""
<style>
    * {
        color-scheme: dark;
    }
    
    body {
        background-color: #0a0e27;
        color: #e0e0e0;
    }
    
    .stApp {
        background-color: #0a0e27;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #60a5fa;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #a78bfa;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    
    .stSidebar {
        background-color: #111827;
        border-right: 2px solid #4f46e5;
    }
    
    .stSidebar [data-testid="stSidebarNav"] {
        background-color: #1f2937;
    }
    
    /* Colorful gradient background for headers */
    h1, h2, h3 {
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0px 4px 15px rgba(79, 70, 229, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #6d28d9, #a855f7);
        box-shadow: 0px 6px 20px rgba(168, 85, 247, 0.6);
    }
    
    .stSelectbox, .stMultiSelect, .stFileUploader, .stTextInput {
        background-color: #1f2937;
        border: 2px solid #4f46e5;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #111827;
        border-bottom: 2px solid #4f46e5;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4f46e5;
    }
    
    .stSuccess {
        background-color: #064e3b;
        border-left: 4px solid #10b981;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: #78350f;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #7f1d1d;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: #0c4a6e;
        border-left: 4px solid #0ea5e9;
        border-radius: 8px;
    }
    
    .stDivider {
        border-color: #4f46e5;
        opacity: 0.5;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111827;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4f46e5;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6d28d9;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Dashboard")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["📤 Upload Data", "📈 Dashboard", "🤖 AI Insights"])

# Main title
st.title("📊 AI Business Dashboard")
st.caption("✨ Turn your data into actionable insights using AI-powered analysis")

# Upload section
if menu == "📤 Upload Data":
    st.subheader("📤 Upload Your Data")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if file:
        df = pd.read_csv(file)
        df.to_csv("data.csv", index=False)
        st.success("✅ File uploaded successfully!")
        st.info(f"📊 Dataset has {len(df)} rows and {len(df.columns)} columns")
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

        with col1:
            st.metric("💰 Total", f"{total:.2f}", delta=None)
        with col2:
            st.metric("📈 Average", f"{avg:.2f}", delta=None)
        with col3:
            st.metric("⬆️ Max", f"{max_val:.2f}", delta=None)
        with col4:
            st.metric("⬇️ Min", f"{min_val:.2f}", delta=None)

    st.divider()

    # Charts
    st.subheader("📈 Visual Analysis")

    chart_type = st.selectbox("Choose Chart Type", ["Bar", "Line", "Pie", "Scatter"])

    if chart_type == "Bar" and len(cat_cols) > 0 and len(num_cols) > 0:
        x_col = st.selectbox("X-axis", cat_cols, key="bar_x")
        y_col = st.selectbox("Y-axis", num_cols, key="bar_y")

        fig = px.bar(df_filtered, x=x_col, y=y_col,
                    color_discrete_sequence=['#4f46e5'],
                    template="plotly_dark")
        fig.update_traces(marker_color='#a78bfa')
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line" and len(num_cols) > 0:
        y_col = st.selectbox("Y-axis", num_cols, key="line_y")

        fig = px.line(df_filtered, y=y_col,
                     color_discrete_sequence=['#60a5fa'],
                     template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pie" and len(cat_cols) > 0 and len(num_cols) > 0:
        names = st.selectbox("Category", cat_cols, key="pie_names")
        values = st.selectbox("Values", num_cols, key="pie_values")

        fig = px.pie(df_filtered, names=names, values=values,
                    color_discrete_sequence=['#4f46e5', '#7c3aed', '#a855f7', '#d946ef', '#f472b6', '#60a5fa', '#a78bfa'],
                    template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter" and len(num_cols) > 1:
        x_col = st.selectbox("X-axis", num_cols, key="scatter_x")
        y_col = st.selectbox("Y-axis", num_cols, key="scatter_y")

        fig = px.scatter(df_filtered, x=x_col, y=y_col,
                        color_discrete_sequence=['#f472b6'],
                        template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top performers
    st.subheader("🏆 Top Performers")

    if len(cat_cols) > 0 and len(num_cols) > 0:
        cat = cat_cols[0]
        num = num_cols[0]

        top_data = df_filtered.groupby(cat)[num].sum().sort_values(ascending=False).head(5)

        fig = px.bar(x=top_data.index, y=top_data.values,
                    labels={"x": cat, "y": num},
                    color_discrete_sequence=['#10b981'],
                    template="plotly_dark")
        fig.update_xaxes(title_text=cat)
        fig.update_yaxes(title_text=num)
        st.plotly_chart(fig, use_container_width=True)

# AI Insights (Gemini)
if menu == "🤖 AI Insights" and df is not None:
    st.subheader("🤖 AI Insights Engine")
    st.info("💡 Get intelligent analysis of your data using Google Gemini AI")

    if st.button("🚀 Generate Insights", use_container_width=True):
        with st.spinner("🔍 Analyzing data..."):
            try:
                data_summary = df.describe().to_string()
                
                prompt = f"""
You are a professional business analyst with expertise in data analysis and strategic insights.

Analyze this dataset summary and provide a comprehensive business analysis:

{data_summary}

Dataset Info:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}
- Columns: {', '.join(df.columns)}

Please provide:
1. **Key Trends**: Identify the main patterns and trends in the data
2. **Business Insights**: What do these metrics tell us about business performance?
3. **Risks**: Potential risks or concerns based on the data
4. **Opportunities**: Growth opportunities and areas for improvement
5. **Recommendations**: Specific, actionable recommendations for business improvement

Format your response with clear headings and bullet points for easy reading.
                """

                response = model.generate_content(prompt)
                
                st.success("✅ Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ Error generating insights: {e}")
                st.info("Please check your Gemini API key in the secrets.")

# If no data
if df is None:
    st.warning("⚠️ Please upload a dataset to get started.")
    st.info("📝 Go to the '📤 Upload Data' section to upload your CSV file.")
