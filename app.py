import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq

# Page config with modern dark theme
st.set_page_config(
    page_title="AI Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme toggle in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Initialize Groq API client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model_ready = True
except Exception as e:
    st.error(f"❌ API Configuration Error: {e}")
    model_ready = False

# Define color schemes
THEMES = {
    "dark": {
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        "sidebar_bg": "linear-gradient(180deg, #1e293b 0%, #0f172a 100%)",
        "accent": "#06b6d4",
        "accent_secondary": "#3b82f6",
        "accent_tertiary": "#8b5cf6",
        "text_primary": "#ffffff",
        "text_secondary": "#e2e8f0",
        "text_tertiary": "#cbd5e1",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#06b6d4",
        "metric_bg": "#1e3a8a",
        "button_bg": "#06b6d4",
        "button_hover": "#0891b2",
        "container_bg": "#1e293b",
        "scrollbar_primary": "#06b6d4",
        "scrollbar_hover": "#2563eb"
    },
    "light": {
        "bg_gradient": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        "sidebar_bg": "linear-gradient(180deg, #e2e8f0 0%, #f1f5f9 100%)",
        "accent": "#0891b2",
        "accent_secondary": "#2563eb",
        "accent_tertiary": "#7c3aed",
        "text_primary": "#0f172a",
        "text_secondary": "#334155",
        "text_tertiary": "#475569",
        "success": "#059669",
        "warning": "#d97706",
        "error": "#dc2626",
        "info": "#0891b2",
        "metric_bg": "#dbeafe",
        "button_bg": "#0891b2",
        "button_hover": "#0369a1",
        "container_bg": "#f1f5f9",
        "scrollbar_primary": "#0891b2",
        "scrollbar_hover": "#2563eb"
    }
}

theme = THEMES[st.session_state.theme]

# Custom CSS with dynamic theme
css_content = f"""
<style>
    * {{
        color-scheme: {'dark' if st.session_state.theme == 'dark' else 'light'};
    }}
    
    body {{
        background: {theme['bg_gradient']};
        color: {theme['text_primary']};
    }}
    
    .stApp {{
        background: {theme['bg_gradient']};
    }}
    
    /* Main container */
    .stMainBlockContainer {{
        padding: 20px;
    }}
    
    /* Headers with vibrant gradients */
    h1 {{
        background: linear-gradient(90deg, {theme['accent']}, {theme['accent_secondary']}, {theme['accent_tertiary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 2.5em !important;
    }}
    
    h2, h3 {{
        background: linear-gradient(90deg, {theme['success']}, {theme['accent']}, {theme['accent_secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }}
    
    /* Sidebar styling */
    .stSidebar {{
        background: {theme['sidebar_bg']};
        border-right: 2px solid {theme['accent']};
    }}
    
    .stSidebar [data-testid="stSidebarNav"] {{
        background: transparent;
    }}
    
    /* Radio buttons and selection */
    [data-testid="stRadio"] {{
        background-color: {theme['container_bg']};
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid {theme['accent']};
    }}
    
    /* Metrics with beautiful colors */
    .stMetric {{
        background: {theme['metric_bg']};
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid {theme['accent']};
        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.2);
    }}
    
    .stMetric label {{
        color: {theme['text_primary']} !important;
        font-weight: 700 !important;
    }}
    
    .stMetric [data-testid="stMetricValue"] {{
        color: {theme['accent']} !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }}
    
    /* Buttons with gradient */
    .stButton > button {{
        background: linear-gradient(90deg, {theme['button_bg']}, {theme['button_hover']});
        color: {theme['text_primary']} !important;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(90deg, {theme['button_hover']}, {theme['accent_secondary']});
        box-shadow: 0px 12px 30px rgba(6, 182, 212, 0.6);
        transform: translateY(-2px);
    }}
    
    /* Selectbox and input fields */
    .stSelectbox, .stMultiSelect, .stFileUploader {{
        background-color: {theme['container_bg']} !important;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        background: {theme['container_bg']} !important;
        border: 2px solid {theme['accent']} !important;
        border-radius: 8px !important;
        color: {theme['text_primary']} !important;
    }}
    
    .stMultiSelect [data-baseweb="select"] {{
        background: {theme['container_bg']} !important;
        border: 2px solid {theme['success']} !important;
        border-radius: 8px !important;
        color: {theme['text_primary']} !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {theme['container_bg']};
        border-bottom: 2px solid {theme['accent']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {theme['container_bg']};
        border-radius: 8px 8px 0 0;
        color: {theme['text_tertiary']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {theme['accent']}, {theme['button_hover']});
        color: {theme['text_primary']};
    }}
    
    /* Success message */
    .stSuccess {{
        background: {'linear-gradient(135deg, #064e3b 0%, #047857 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)'};
        border-left: 4px solid {theme['success']};
        border-radius: 8px;
        padding: 15px;
        color: {theme['text_primary']} !important;
    }}
    
    /* Warning message */
    .stWarning {{
        background: {'linear-gradient(135deg, #78350f 0%, #b45309 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)'};
        border-left: 4px solid {theme['warning']};
        border-radius: 8px;
        padding: 15px;
        color: {theme['text_primary']} !important;
    }}
    
    /* Error message */
    .stError {{
        background: {'linear-gradient(135deg, #7f1d1d 0%, #b91c1c 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)'};
        border-left: 4px solid {theme['error']};
        border-radius: 8px;
        padding: 15px;
        color: {theme['text_primary']} !important;
    }}
    
    /* Info message */
    .stInfo {{
        background: {'linear-gradient(135deg, #0c4a6e 0%, #0369a1 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #cffafe 0%, #a5f3fc 100%)'};
        border-left: 4px solid {theme['info']};
        border-radius: 8px;
        padding: 15px;
        color: {theme['text_primary']} !important;
    }}
    
    /* Divider */
    .stDivider {{
        border-color: {theme['accent']};
        opacity: 0.6;
    }}
    
    /* Captions */
    .stCaption {{
        color: {theme['accent']} !important;
        font-weight: 500;
    }}
    
    /* Text styling */
    p {{
        color: {theme['text_secondary']} !important;
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 12px;
        height: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {theme['container_bg']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {theme['scrollbar_primary']};
        border-radius: 6px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {theme['scrollbar_hover']};
    }}
    
    /* Expander */
    .stExpander {{
        background-color: {theme['container_bg']};
        border: 1px solid {theme['accent']};
        border-radius: 8px;
    }}
    
    /* DataFrames */
    .stDataFrame {{
        background-color: {theme['container_bg']};
    }}
    
    .stDataFrame thead {{
        background-color: {theme['accent']} !important;
        color: {theme['text_primary']} !important;
    }}
    
    .stDataFrame tbody tr {{
        border-bottom: 1px solid {theme['accent']};
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: {theme['metric_bg']};
    }}
    
    .stDataFrame {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Analysis container */
    .analysis-container {{
        background: {theme['container_bg']};
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid {theme['accent']};
        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.2);
        color: {theme['text_primary']};
    }}
    
    .analysis-container h3 {{
        color: {theme['accent']} !important;
    }}
    
    .analysis-container p {{
        color: {theme['text_secondary']} !important;
    }}
    
    .analysis-container ul {{
        color: {theme['text_secondary']} !important;
    }}
    
    .analysis-container li {{
        color: {theme['text_secondary']} !important;
    }}
</style>
"""

st.markdown(css_content, unsafe_allow_html=True)

# Sidebar with theme toggle
col1, col2 = st.sidebar.columns([0.8, 0.2])
with col1:
    st.sidebar.title("📊 Dashboard")
with col2:
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    if st.sidebar.button(theme_icon, help="Toggle Light/Dark Mode", key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

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

    plot_template = "plotly_dark" if st.session_state.theme == "dark" else "plotly"

    if chart_type == "Bar Chart" and len(cat_cols) > 0 and len(num_cols) > 0:
        x_col = st.selectbox("X-axis", cat_cols, key="bar_x")
        y_col = st.selectbox("Y-axis", num_cols, key="bar_y")

        fig = px.bar(
            df_filtered, 
            x=x_col, 
            y=y_col,
            color_discrete_sequence=[theme['accent']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Line Chart" and len(num_cols) > 0:
        y_col = st.selectbox("Y-axis", num_cols, key="line_y")

        fig = px.line(
            df_filtered, 
            y=y_col,
            color_discrete_sequence=[theme['success']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12),
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
            color_discrete_sequence=[theme['accent'], theme['success'], theme['accent_tertiary'], theme['warning'], theme['error'], theme['accent_secondary'], theme['info']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12)
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot" and len(num_cols) > 1:
        x_col = st.selectbox("X-axis", num_cols, key="scatter_x")
        y_col = st.selectbox("Y-axis", num_cols, key="scatter_y")

        fig = px.scatter(
            df_filtered,
            x=x_col,
            y=y_col,
            color_discrete_sequence=[theme['accent_tertiary']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12),
            hovermode='closest'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Area Chart" and len(num_cols) > 0:
        y_col = st.selectbox("Y-axis", num_cols, key="area_y")

        fig = px.area(
            df_filtered,
            y=y_col,
            color_discrete_sequence=[theme['warning']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12),
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
            color_discrete_sequence=[theme['success']],
            template=plot_template
        )
        fig.update_layout(
            plot_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            paper_bgcolor=theme['container_bg'] if st.session_state.theme == "dark" else "#ffffff",
            font=dict(color=theme['text_primary'], size=12),
            xaxis_title=cat,
            yaxis_title=num,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

# AI Insights (Groq)
if menu == "🤖 AI Insights" and df is not None:
    st.subheader("🤖 AI Insights Engine - Powered by Groq ⚡")
    st.info("💡 Lightning-fast AI analysis using Groq's latest Llama models")

    if not model_ready:
        st.error("❌ Groq API is not configured. Please add GROQ_API_KEY to your Streamlit secrets.")
        st.write("**How to fix (3 easy steps):**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🌐 Streamlit Cloud")
            st.write("1. Go to **Manage app** (bottom right)")
            st.write("2. Click **Secrets**")
            st.write("3. Add this:")
            st.code("GROQ_API_KEY = 'your-key-here'")
        
        with col2:
            st.subheader("💻 Local Development")
            st.write("1. Create `.streamlit/secrets.toml`")
            st.write("2. Add this:")
            st.code("GROQ_API_KEY = 'your-key-here'")
            st.write("3. Run: `streamlit run app.py`")
        
        st.write("**Get Free API Key (25 req/min):**")
        st.write("👉 https://console.groq.com")
    else:
        if st.button("🚀 Generate AI Insights", use_container_width=True):
            with st.spinner("⚡ Groq is analyzing your data (lightning fast)..."):
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

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2048
                    )
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Display the response in a nice format
                    st.markdown(f"""
                    <style>
                    .analysis-container {{
                        background: {theme['container_bg']};
                        padding: 20px;
                        border-radius: 12px;
                        border-left: 4px solid {theme['accent']};
                        box-shadow: 0px 8px 20px rgba(6, 182, 212, 0.2);
                        color: {theme['text_primary']};
                    }}
                    .analysis-container h3 {{
                        color: {theme['accent']} !important;
                        margin-top: 15px;
                        margin-bottom: 10px;
                    }}
                    .analysis-container p {{
                        color: {theme['text_secondary']} !important;
                        line-height: 1.6;
                    }}
                    .analysis-container ul, .analysis-container ol {{
                        color: {theme['text_secondary']} !important;
                    }}
                    .analysis-container li {{
                        color: {theme['text_secondary']} !important;
                        margin-bottom: 8px;
                        line-height: 1.5;
                    }}
                    .analysis-container strong {{
                        color: {theme['accent']} !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
                    st.markdown(response.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("**Troubleshooting:**")
                    st.write("- ✓ API key is correct?")
                    st.write("- ✓ Rate limit (25 req/min) exceeded?")
                    st.write("- ✓ Internet connection stable?")
                    st.write("- ✓ Try with smaller dataset?")

# If no data
if df is None:
    st.warning("⚠️ No data loaded. Please upload a dataset to get started.")
    st.info("📝 Navigate to '📤 Upload Data' section to upload your CSV file.")
