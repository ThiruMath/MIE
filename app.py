import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mie_engine import diagnose_mistake

# -- Page Configuration --
st.set_page_config(
    page_title="Mistake Intelligence Engine (MIE)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -- Custom CSS for Dark Mode Aesthetics --
st.markdown("""
<style>
    /* Sleek gradient background for main content area */
    .stApp {
        background: linear-gradient(135deg, #1A1A1D 0%, #151515 100%);
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Elegant metric cards */
    [data-testid="stMetricValue"] {
        color: #4CAF50;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #A0AEC0;
        font-weight: 500;
    }
    
    /* Modern title typography */
    h1 {
        background: -webkit-linear-gradient(45deg, #0DE0FC, #0353A4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #E2E8F0;
        font-weight: 600;
    }
    
    /* Soft glowing effect on tabs */
    .stTabs [data-baseweb="tab-list"] button {
        color: #A0AEC0;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #0DE0FC;
        border-bottom: 2px solid #0DE0FC;
        text-shadow: 0 0 10px rgba(13, 224, 252, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# -- Load Data --
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("student_logs.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# -- Sidebar Controls --
st.sidebar.image("https://img.icons8.com/clouds/200/000000/brain.png", width=150)
st.sidebar.markdown("## Control Panel")

if df.empty:
    st.error("⚠️ Data not found! Please run `python synthetic_data_generator.py` locally.")
    st.stop()

students = ["All"] + list(df['student_id'].unique())
selected_student = st.sidebar.selectbox("Filter by Student:", students)

error_types = ["All"] + list(df['error_type'].unique())
selected_error = st.sidebar.selectbox("Filter by Error Type:", error_types)

# Apply filters
filtered_df = df.copy()
if selected_student != "All":
    filtered_df = filtered_df[filtered_df['student_id'] == selected_student]
if selected_error != "All":
    filtered_df = filtered_df[filtered_df['error_type'] == selected_error]

# -- Top Navigation --
st.title("🧠 Mistake Intelligence Engine (MIE)")
st.markdown("Diagnosing *how* students think, not just *what* they answer.")

tab1, tab2, tab3 = st.tabs(["📊 Diagnostic Dashboard", "📝 Raw Data Logs", "🤖 Live Tutor Diagnosis"])

# ==========================================
# TAB 1: Diagnostic Dashboard
# ==========================================
with tab1:
    st.markdown("### Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_attempts = len(filtered_df)
    incorrect_attempts = len(filtered_df[filtered_df['is_correct'] == False])
    error_rate = (incorrect_attempts / total_attempts * 100) if total_attempts > 0 else 0
    conceptual_errors = len(filtered_df[filtered_df['error_type'] == 'Conceptual'])
    
    col1.metric("Total Attempts Processed", total_attempts)
    col2.metric("Identified 'Buggy' Steps", incorrect_attempts)
    col3.metric("Class Error Rate", f"{error_rate:.1f}%")
    col4.metric("Conceptual Blocks", conceptual_errors)
    
    st.divider()

    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("### Mastery Heatmap")
        st.markdown("Visualizing student comprehension across different mathematical concepts.")
        
        # Aggregate data for heatmap
        heatmap_data = df.groupby(['student_id', 'concept_tag'])['is_correct'].mean().reset_index()
        heatmap_data['accuracy'] = heatmap_data['is_correct'] * 100
        
        # Pivot the data
        pivot_data = heatmap_data.pivot(index='student_id', columns='concept_tag', values='accuracy')
        
        fig_heat = px.imshow(
            pivot_data,
            color_continuous_scale="RdYlGn",
            aspect="auto",
            labels=dict(color="Accuracy %")
        )
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="#E2E8F0",
            margin=dict(t=20, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with chart_col2:
        st.markdown("### Cognitive Risk Radar")
        st.markdown("Identifies patterns in *what kind* of mistakes a student consistently makes.")
        
        # Aggregate error types
        if selected_student != "All":
            radar_subset = filtered_df[filtered_df['error_type'] != 'None']
        else:
            # If "All", show class average
            radar_subset = df[df['error_type'] != 'None']
            
        error_counts = radar_subset['error_type'].value_counts().reset_index()
        error_counts.columns = ['error_type', 'count']
        
        # Ensure Factual, Procedural, Conceptual are present
        categories = ['Factual', 'Procedural', 'Conceptual']
        radar_values = []
        for cat in categories:
            val = error_counts[error_counts['error_type'] == cat]['count'].values
            radar_values.append(val[0] if len(val) > 0 else 0)
            
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=categories,
            fill='toself',
            name=selected_student if selected_student != "All" else "Class Average",
            line_color='#0DE0FC',
            fillcolor='rgba(13, 224, 252, 0.4)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, color="#A0AEC0", showline=False, gridcolor="#333"),
                angularaxis=dict(color="#E2E8F0", gridcolor="#333")
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="#E2E8F0",
            margin=dict(t=30, l=30, r=30, b=30)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ==========================================
# TAB 2: Raw Data Logs
# ==========================================
with tab2:
    st.markdown("### Synthetic Student Logs")
    st.markdown("Filter applied via sidebar.")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "is_correct": st.column_config.CheckboxColumn("Correct?"),
            "time_to_first_response_ms": st.column_config.NumberColumn("Wait Time (ms)", format="%d"),
        }
    )

# ==========================================
# TAB 3: Live Tutor Diagnosis
# ==========================================
with tab3:
    st.markdown("### PedCoT Live Playground")
    st.markdown("Test the underlying Google Gemini AI logic! Submit a math problem and a 'buggy' student attempt, and watch the engine diagnose the *type* of error it is.")
    
    with st.form("live_diagnosis_form"):
        col_q, col_a = st.columns(2)
        with col_q:
            test_question = st.text_input("Math Question", value="Which is larger: 0.8 or 0.355?")
        with col_a:
            test_correct = st.text_input("Correct Answer", value="0.8")
            
        test_attempt = st.text_area("Student's Incorrect Attempt (Show their reasoning!)", value="0.355 because 355 is a bigger number than 8.")
        
        submitted = st.form_submit_button("🧠 Run MIE Diagnosis")
        
        if submitted:
            with st.spinner("Analyzing student cognition..."):
                result = diagnose_mistake(test_question, test_correct, test_attempt)
                
                if "error" in result and result["error_category"] == "API Error":
                    st.error(f"{result['error']}\n\n{result.get('pedagogical_advice', '')}")
                else:
                    st.success("Diagnosis Complete!")
                    st.markdown(f"**Error Category:** `{result.get('error_category', 'Unknown')}`")
                    st.markdown(f"**Diagnosis:** {result.get('diagnosis', 'N/A')}")
                    st.info(f"💡 **Tutor Action:** {result.get('pedagogical_advice', 'N/A')}")
