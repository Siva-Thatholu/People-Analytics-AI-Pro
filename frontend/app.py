import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI People Analytics", layout="wide", page_icon="📊")

# --- UI Styling ---
# ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E1E1E; border-radius: 10px; padding: 20px; 

        box-shadow: 2px 2px 10px rgba(0,0,0,0.5); text-align: center;
    }
    .metric-value { font-size: 32px; font-weight: bold; color: #4CAF50; }
    .metric-label { font-size: 16px; color: #AAAAAA; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3125/3125713.png", width=60)
    st.title("Admin Pipeline")
    st.markdown("Data Warehouse Controls")
    
    record_count = st.selectbox("Dataset Size (Stress Test)", [1000, 10000, 50000, 100000])
    if st.button("🔄 Generate Big Data Pipeline", type="primary"):
        with st.spinner(f"Ingesting {record_count} records via backend..."):
            try:
                res = requests.post(f"{API_URL}/api/generate?num_records={record_count}", timeout=30)
                st.success("Data Pipeline Execution Complete!")
                st.rerun()
            except Exception as e:
                st.error("FastAPI backend is not responding.")

    st.markdown("---")
    st.markdown("**Role**: Data Analyst")
    st.markdown("**Tech Stack**: Python, FastAPI, Gemini API, SQLite, Streamlit")

# --- Fetch Aggregated Data (Production Safe) ---
@st.cache_data(ttl=60)
def fetch_analytics():
    try:
        res = requests.get(f"{API_URL}/api/analytics/aggregates")
        return res.json()
    except:
        return None

data = fetch_analytics()

if not data or data.get("total_employees") == 0:
    st.title("🧠 AI-Driven People Analytics Platform")
    st.info("Warehouse is empty. Use the Sidebar to trigger the ELT pipeline and generate up to 100,000 synthetic records.")
else:
    # --- Tabs Layout ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "💰 Business Impact & ROI", "🔬 Live NLP Engine", "🏗️ Project Architecture"])
    
    with tab1:
        st.title("Executive Flight Risk Dashboard")
        
        # High Level Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f'<div class="metric-card"><div class="metric-label">Total Headcount Analyzed</div><div class="metric-value">{data["total_employees"]:,}</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="metric-card"><div class="metric-label">High Flight Risk</div><div class="metric-value" style="color:#F44336;">{data["high_risk_count"]:,}</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="metric-card"><div class="metric-label">Avg Sentiment (0-1)</div><div class="metric-value" style="color:#2196F3;">{data["average_sentiment"]}</div></div>', unsafe_allow_html=True)
        risk_pct = round((data["high_risk_count"] / data["total_employees"]) * 100, 1)
        col4.markdown(f'<div class="metric-card"><div class="metric-label">Critical Attrition %</div><div class="metric-value" style="color:#FF9800;">{risk_pct}%</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts
        c1, c2 = st.columns(2)
        with c1:
            dept_df = pd.DataFrame(data["department_stats"])
            fig_dept = px.bar(dept_df, x="department", y="count", color="risk",
                              color_discrete_map={"High": "#F44336", "Medium": "#FF9800", "Low": "#4CAF50"},
                              title="Flight Risk Distribution by Department", barmode="group")
            fig_dept.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_dept, use_container_width=True)
            
        with c2:
            theme_df = pd.DataFrame(data["theme_stats"])
            fig_theme = px.pie(theme_df, names="theme", values="count", hole=0.4,
                               title="Primary Drivers of Turnover (Extracted from Surveys)")
            fig_theme.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_theme, use_container_width=True)

        st.subheader("Raw Data Sample (Top 1000 Rows)")
        sample_res = requests.get(f"{API_URL}/api/employees/sample?limit=1000")
        if sample_res.status_code == 200:
            st.dataframe(pd.DataFrame(sample_res.json()).drop(columns=["id"]), height=300)
            
    with tab2:
        st.title("Cost of Turnover (ROI Calculator)")
        st.markdown("""
        Replacing an employee generally costs **50% to 200%** of their annual salary. 
        By utilizing NLP to identify high-risk employees before they quit, we can intervene and save millions.
        """)
        avg_salary = st.slider("Estimated Average Salary ($)", 50000, 150000, 85000)
        replacement_cost_pct = st.slider("Replacement Cost as % of Salary", 50, 200, 75) / 100.0
        
        cost_per_employee = avg_salary * replacement_cost_pct
        total_risk_exposure = data["high_risk_count"] * cost_per_employee
        
        st.error(f"### 🚨 Total Financial Risk Exposure: ${total_risk_exposure:,.2f}")
        st.success(f"**Actionable Insight:** If HR interventions can retain even 10% of these high-risk employees, the company saves **${(total_risk_exposure * 0.10):,.2f}** this quarter.")

    with tab3:
        st.title("Live NLP Engine")
        st.markdown("Test the LLM pipeline directly. Input sample exit interview or survey feedback below.")
        
        user_input = st.text_area("Employee Feedback:", "I feel completely overwhelmed. The hours are insane and my manager doesn't listen to my concerns about project timelines.")
        
        if st.button("Analyze with Gemini API"):
            with st.spinner("Calling Google Gemini..."):
                try:
                    res = requests.post(f"{API_URL}/api/analyze-live", json={"feedback": user_input})
                    result = res.json()
                    st.metric("Sentiment Score (0=Negative, 1=Positive)", result["sentiment_score"])
                    st.info(f"**Extracted Theme:** {result['key_theme'].title()}")
                except Exception as e:
                    st.error("Failed to connect to API.")
                    
    with tab4:
        st.title("Project Architecture & Flow")
        st.markdown("""
        ### 1. Data Generation (Big Data Simulation)
        The `Faker` library generates 10,000 to 100,000+ synthetic employee records. To prevent LLM rate-limiting during massive bulk inserts, the backend simulates the statistical distribution of LLM outputs.
        
        ### 2. FastAPI Backend (Data Warehouse)
        Acts as the core engine. It utilizes **SQLAlchemy** to perform bulk inserts into a local **SQLite** database, capable of handling large datasets efficiently.
        
        ### 3. Aggregate Endpoints (Optimization)
        Instead of crashing the browser by sending 100,000 rows via API, the FastAPI backend uses SQL `GROUP BY` and `COUNT` functions to send only lightweight aggregated statistics to the frontend.
        
        ### 4. LLM Integration (Gemini)
        Integrates `google-generativeai` to perform real-time sentiment scoring and thematic categorization on unstructured text data.
        
        ### 5. Streamlit Frontend
        Consumes the REST APIs, caches the data for performance (`@st.cache_data`), and visualizes the results interactively using **Plotly**.
        """)
