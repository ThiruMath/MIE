import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mie_engine import diagnose_mistake

# ── Page Configuration ──
st.set_page_config(
    page_title="MIE · Mistake Intelligence Engine | ThiruMath",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS + Google Fonts ──
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    /* ── Reset & Global ── */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: #0A0A0F;
        color: #CBD5E1;
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F0F17 0%, #0A0A0F 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #64748B;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin-top: 1.5rem;
    }

    /* ── Hero Section ── */
    .hero-badge {
        display: inline-block;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.2);
        color: #38BDF8;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 40%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.15;
        margin-bottom: 0.25rem;
        letter-spacing: -1.5px;
    }
    .hero-subtitle {
        color: #64748B;
        font-size: 1.05rem;
        margin-top: 0;
        margin-bottom: 0.75rem;
        line-height: 1.6;
    }

    /* ── Tech Stack Badges ── */
    .tech-stack {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .tech-chip {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: #94A3B8;
        padding: 0.25rem 0.7rem;
        border-radius: 8px;
        font-size: 0.72rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── Typography ── */
    h2, h3 { color: #E2E8F0 !important; font-weight: 600; }

    /* ── Glassmorphism Metric Cards ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(56, 189, 248, 0.08);
    }
    [data-testid="stMetricValue"] {
        color: #38BDF8;
        font-weight: 700;
        font-size: 2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8;
        font-weight: 500;
        font-size: 0.8rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255,255,255,0.02);
        border-radius: 14px;
        padding: 5px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .stTabs [data-baseweb="tab-list"] button {
        color: #475569;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.25s ease;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #F1F5F9;
        background: rgba(56, 189, 248, 0.1);
        border-bottom: none !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.08);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ── Inputs & Forms ── */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        background-color: #12121A !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.12) !important;
    }
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: #94A3B8 !important;
        font-weight: 500;
    }

    /* ── Form Submit Button ── */
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.25) !important;
    }
    .stFormSubmitButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 25px rgba(56, 189, 248, 0.4) !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* ── Dividers ── */
    hr { border-color: rgba(255,255,255,0.05) !important; }

    /* ── Alerts ── */
    .stAlert { border-radius: 12px !important; }

    /* ── Section Components ── */
    .section-header {
        display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;
    }
    .section-header .icon { font-size: 1.4rem; }
    .section-header .label { font-size: 1.05rem; font-weight: 600; color: #E2E8F0; }
    .section-desc {
        color: #64748B; font-size: 0.85rem; margin-bottom: 1rem; line-height: 1.5;
    }

    /* ── Glass Card ── */
    .glass-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1rem;
    }
    .glass-card h4 {
        color: #E2E8F0; margin: 0 0 0.5rem; font-weight: 600; font-size: 1rem;
    }
    .glass-card p {
        color: #94A3B8; margin: 0; font-size: 0.9rem; line-height: 1.6;
    }

    /* ── Profile Page ── */
    .profile-name {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(135deg, #38BDF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .profile-role {
        color: #94A3B8; font-size: 1.1rem; font-weight: 400; margin-top: 0.1rem;
    }
    .profile-bio {
        color: #CBD5E1; font-size: 0.95rem; line-height: 1.7; max-width: 700px;
    }
    .skill-tag {
        display: inline-block;
        background: rgba(129,140,248,0.1);
        border: 1px solid rgba(129,140,248,0.2);
        color: #A5B4FC;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    .contact-link {
        display: inline-flex; align-items: center; gap: 0.4rem;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: #38BDF8;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 500;
        text-decoration: none;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    .contact-link:hover {
        background: rgba(56,189,248,0.1);
        border-color: rgba(56,189,248,0.3);
        transform: translateY(-1px);
    }

    /* ── Methodology Card ── */
    .method-step {
        display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1.25rem;
    }
    .method-num {
        background: linear-gradient(135deg, #38BDF8, #818CF8);
        color: white; font-weight: 700; font-size: 0.85rem;
        min-width: 32px; height: 32px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
    }
    .method-text h5 {
        color: #E2E8F0; margin: 0 0 0.2rem; font-size: 0.95rem; font-weight: 600;
    }
    .method-text p {
        color: #94A3B8; margin: 0; font-size: 0.82rem; line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ──
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_logs.csv")
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()

# ── Sidebar ──
st.sidebar.markdown(
    '<p style="color:#38BDF8; font-weight:800; font-size:1.3rem; letter-spacing:-0.5px; margin-bottom:0;">🧠 MIE</p>'
    '<p style="color:#475569; font-size:0.7rem; letter-spacing:1px; text-transform:uppercase;">Mistake Intelligence Engine</p>',
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.markdown("## Filters")

if df.empty:
    st.error("⚠️ Data not found! Run `python synthetic_data_generator.py` first.")
    st.stop()

students = ["All Students"] + sorted(df['student_id'].unique().tolist())
selected_student = st.sidebar.selectbox("Student", students)

error_types = ["All Types"] + sorted([e for e in df['error_type'].dropna().unique().tolist() if e != 'None'])
selected_error = st.sidebar.selectbox("Error Category", error_types)

filtered_df = df.copy()
if selected_student != "All Students":
    filtered_df = filtered_df[filtered_df['student_id'] == selected_student]
if selected_error != "All Types":
    filtered_df = filtered_df[filtered_df['error_type'] == selected_error]

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<p style="color:#334155; font-size:0.7rem; text-align:center;">'
    'Built by ThiruMath &middot; Powered by Gemini</p>',
    unsafe_allow_html=True
)

# ── Hero Header ──
st.markdown('<span class="hero-badge">📐 EdTech AI Portfolio Project</span>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">Mistake Intelligence Engine</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">'
    'An AI-powered diagnostic system that analyzes <em>how</em> students think — not just <em>what</em> they answer. '
    'Built using Pedagogical Chain-of-Thought (PedCoT) methodology and Google Gemini.'
    '</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="tech-stack">'
    '<span class="tech-chip">Python</span>'
    '<span class="tech-chip">Streamlit</span>'
    '<span class="tech-chip">Gemini 2.0 Flash</span>'
    '<span class="tech-chip">Plotly</span>'
    '<span class="tech-chip">Pandas</span>'
    '<span class="tech-chip">PedCoT</span>'
    '<span class="tech-chip">Repair Theory</span>'
    '</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Dashboard",
    "🔬  Live Diagnosis",
    "📋  Methodology",
    "📝  Data Logs",
    "👤  About Me"
])

# ======================================================
# TAB 1: Diagnostic Dashboard
# ======================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)

    total_attempts = len(filtered_df)
    incorrect_attempts = len(filtered_df[~filtered_df['is_correct']])
    error_rate = (incorrect_attempts / total_attempts * 100) if total_attempts > 0 else 0
    conceptual_errors = len(filtered_df[filtered_df['error_type'] == 'Conceptual'])

    col1.metric("Total Attempts", f"{total_attempts:,}")
    col2.metric("Buggy Steps Found", f"{incorrect_attempts:,}")
    col3.metric("Class Error Rate", f"{error_rate:.1f}%")
    col4.metric("Conceptual Gaps", f"{conceptual_errors:,}")

    st.markdown("")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            '<div class="section-header"><span class="icon">🗺️</span><span class="label">Mastery Heatmap</span></div>'
            '<p class="section-desc">Cross-referencing each student against mathematical concepts. '
            'Green cells indicate mastery; red cells reveal knowledge blind spots that need targeted intervention.</p>',
            unsafe_allow_html=True
        )
        heatmap_data = df.groupby(['student_id', 'concept_tag'])['is_correct'].mean().reset_index()
        heatmap_data['accuracy'] = heatmap_data['is_correct'] * 100
        pivot_data = heatmap_data.pivot(index='student_id', columns='concept_tag', values='accuracy')

        fig_heat = px.imshow(
            pivot_data,
            color_continuous_scale=[[0, "#EF4444"], [0.5, "#FBBF24"], [1, "#22C55E"]],
            aspect="auto",
            labels=dict(x="Concept", y="Student", color="Accuracy %")
        )
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8", size=11),
            margin=dict(t=10, l=0, r=0, b=0),
            coloraxis_colorbar=dict(tickfont=dict(color="#94A3B8"), title=dict(font=dict(color="#94A3B8"))),
            xaxis=dict(tickfont=dict(color="#CBD5E1")),
            yaxis=dict(tickfont=dict(color="#CBD5E1", size=9)),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with chart_col2:
        st.markdown(
            '<div class="section-header"><span class="icon">🎯</span><span class="label">Cognitive Risk Radar</span></div>'
            '<p class="section-desc">Visualizing the distribution of error types — a skewed radar reveals systematic '
            'thinking patterns that require pedagogical intervention, not just more practice.</p>',
            unsafe_allow_html=True
        )
        if selected_student != "All Students":
            radar_subset = filtered_df[filtered_df['error_type'] != 'None']
        else:
            radar_subset = df[df['error_type'] != 'None']

        error_counts = radar_subset['error_type'].value_counts().reset_index()
        error_counts.columns = ['error_type', 'count']

        categories = ['Factual', 'Procedural', 'Conceptual']
        radar_values = []
        for cat in categories:
            val = error_counts[error_counts['error_type'] == cat]['count'].values
            radar_values.append(int(val[0]) if len(val) > 0 else 0)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values + [radar_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=selected_student if selected_student != "All Students" else "Class Avg",
            line=dict(color='#818CF8', width=2),
            fillcolor='rgba(129, 140, 248, 0.15)',
            marker=dict(size=8, color='#C084FC')
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, color="#475569", showline=False,
                                gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10)),
                angularaxis=dict(color="#CBD5E1", gridcolor="rgba(255,255,255,0.05)",
                                 tickfont=dict(size=13, color="#E2E8F0")),
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color="#94A3B8",
            margin=dict(t=40, l=60, r=60, b=40),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Error Breakdown ──
    st.markdown(
        '<div class="section-header"><span class="icon">📊</span><span class="label">Error Distribution by Concept</span></div>'
        '<p class="section-desc">Understanding which mathematical concepts trigger which types of cognitive errors — '
        'critical data for curriculum designers and adaptive learning systems.</p>',
        unsafe_allow_html=True
    )
    errors_only = filtered_df[filtered_df['error_type'] != 'None']
    if not errors_only.empty:
        bar_data = errors_only.groupby(['concept_tag', 'error_type']).size().reset_index(name='count')
        color_map = {'Factual': '#F87171', 'Procedural': '#FBBF24', 'Conceptual': '#818CF8'}
        fig_bar = px.bar(
            bar_data, x='concept_tag', y='count', color='error_type',
            barmode='group', color_discrete_map=color_map,
            labels={'concept_tag': 'Concept', 'count': 'Errors', 'error_type': 'Type'}
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8", size=12),
            margin=dict(t=10, l=0, r=0, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        font=dict(color="#CBD5E1")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.03)", tickfont=dict(color="#CBD5E1")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#94A3B8")),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No errors found for the current filter selection.")

# ======================================================
# TAB 2: Live Diagnosis
# ======================================================
with tab2:
    st.markdown(
        '<div class="section-header"><span class="icon">🔬</span><span class="label">PedCoT Live Playground</span></div>'
        '<p class="section-desc">Watch the Gemini-powered diagnostic engine work in real-time. '
        'Enter any math problem and a student\'s incorrect reasoning to see the AI classify the cognitive error.</p>',
        unsafe_allow_html=True
    )

    # ── Preset Examples ──
    st.markdown(
        '<p style="color:#64748B; font-size:0.8rem; font-weight:500; margin-bottom:0.5rem;">💡 TRY A PRESET EXAMPLE</p>',
        unsafe_allow_html=True
    )
    presets = {
        "Whole Number Bias (Conceptual)": {
            "q": "Which is larger: 0.8 or 0.355?",
            "a": "0.8",
            "attempt": "0.355 because 355 is a bigger number than 8."
        },
        "Sign Error (Procedural)": {
            "q": "Solve for x: 2x - 5 = 11",
            "a": "x = 8",
            "attempt": "2x - 5 = 11 → 2x = 11 - 5 = 6 → x = 3"
        },
        "BODMAS Misunderstanding (Conceptual)": {
            "q": "Evaluate: 4 + 3 × 2",
            "a": "10",
            "attempt": "4 + 3 = 7, then 7 × 2 = 14"
        },
        "Wrong Recall (Factual)": {
            "q": "What is 3 squared?",
            "a": "9",
            "attempt": "3 squared = 3 × 2 = 6"
        }
    }

    selected_preset = st.selectbox("Choose a demo scenario:", ["Custom Input"] + list(presets.keys()))

    if selected_preset != "Custom Input":
        preset = presets[selected_preset]
        default_q, default_a, default_attempt = preset["q"], preset["a"], preset["attempt"]
    else:
        default_q, default_a, default_attempt = "", "", ""

    with st.form("live_diagnosis_form"):
        col_q, col_a = st.columns(2)
        with col_q:
            test_question = st.text_input("Math Question", value=default_q)
        with col_a:
            test_correct = st.text_input("Correct Answer", value=default_a)

        test_attempt = st.text_area(
            "Student's Incorrect Attempt (show their reasoning)",
            value=default_attempt, height=100
        )
        submitted = st.form_submit_button("🧠  Run MIE Diagnosis")

    if submitted:
        if not test_question or not test_correct or not test_attempt:
            st.warning("Please fill in all fields before running a diagnosis.")
        else:
            with st.spinner("Analyzing student cognition via PedCoT..."):
                result = diagnose_mistake(test_question, test_correct, test_attempt)

            if "error" in result and result.get("error_category") == "API Error":
                st.error(f"**API Error:** {result['error']}")
                st.caption(result.get('pedagogical_advice', ''))
            else:
                st.markdown("---")
                r1, r2 = st.columns([1, 2])
                with r1:
                    cat = result.get('error_category', 'Unknown')
                    cat_colors = {'Factual': '#F87171', 'Procedural': '#FBBF24',
                                  'Conceptual': '#818CF8', 'None': '#22C55E'}
                    color = cat_colors.get(cat, '#94A3B8')
                    st.markdown(
                        f'<div style="background:rgba(255,255,255,0.03); border:1px solid {color}40; '
                        f'border-radius:16px; padding:1.75rem; text-align:center;">'
                        f'<p style="color:#64748B; font-size:0.7rem; letter-spacing:1.5px; margin:0;">ERROR CATEGORY</p>'
                        f'<p style="color:{color}; font-size:2rem; font-weight:800; margin:0.3rem 0; letter-spacing:-0.5px;">{cat}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                with r2:
                    st.markdown(
                        f'<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); '
                        f'border-radius:16px; padding:1.75rem;">'
                        f'<p style="color:#64748B; font-size:0.7rem; letter-spacing:1.5px; margin:0 0 0.5rem;">DIAGNOSIS</p>'
                        f'<p style="color:#E2E8F0; font-size:1rem; line-height:1.6; margin:0;">{result.get("diagnosis", "N/A")}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                st.markdown("")
                st.info(f"💡 **Pedagogical Hint for the Student:** {result.get('pedagogical_advice', 'N/A')}")

# ======================================================
# TAB 3: Methodology
# ======================================================
with tab3:
    st.markdown(
        '<div class="section-header"><span class="icon">📋</span><span class="label">How MIE Works</span></div>'
        '<p class="section-desc">The Mistake Intelligence Engine is grounded in established learning science research. '
        'Here is the methodology behind the diagnostic pipeline.</p>',
        unsafe_allow_html=True
    )

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("""
        <div class="glass-card">
            <h4>🔬 Pedagogical Chain-of-Thought (PedCoT)</h4>
            <p>Traditional error-checking simply marks answers right or wrong. PedCoT goes deeper — it forces the AI
            to reconstruct the student's <em>reasoning process</em> step by step, identify the exact moment of
            divergence, and classify the <em>type</em> of cognitive breakdown.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
            <h4>🧩 Repair Theory (Brown & VanLehn, 1980)</h4>
            <p>Students don't make random mistakes — they apply <em>buggy procedures</em>: systematic, predictable
            variations of the correct algorithm. MIE identifies these "cognitive bugs" so teachers can address the
            root cause, not just the symptom.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown("""
        <div class="glass-card">
            <h4>📊 Three-Tier Error Taxonomy</h4>
            <div style="margin-top:0.75rem;">
                <div class="method-step">
                    <div class="method-num" style="background:#F87171;">F</div>
                    <div class="method-text">
                        <h5 style="color:#F87171;">Factual Errors</h5>
                        <p>Wrong facts recalled from memory. Example: "7 × 8 = 54" instead of 56.</p>
                    </div>
                </div>
                <div class="method-step">
                    <div class="method-num" style="background:#FBBF24;">P</div>
                    <div class="method-text">
                        <h5 style="color:#FBBF24;">Procedural Errors</h5>
                        <p>Correct concept, wrong execution. Example: Subtracting instead of adding when isolating x.</p>
                    </div>
                </div>
                <div class="method-step">
                    <div class="method-num" style="background:#818CF8;">C</div>
                    <div class="method-text">
                        <h5 style="color:#818CF8;">Conceptual Errors</h5>
                        <p>Fundamental misunderstanding. Example: Treating 0.355 as larger than 0.8 (whole number bias).</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        '<div class="section-header"><span class="icon">⚙️</span><span class="label">Architecture Pipeline</span></div>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="glass-card">
        <div class="method-step">
            <div class="method-num">1</div>
            <div class="method-text">
                <h5>Data Ingestion</h5>
                <p>Student interaction logs (attempts, timestamps, hint requests) are ingested from CSV or a live database.</p>
            </div>
        </div>
        <div class="method-step">
            <div class="method-num">2</div>
            <div class="method-text">
                <h5>PedCoT Prompt Engineering</h5>
                <p>A structured prompt forces Gemini to follow the pedagogical reasoning chain before classifying the error.</p>
            </div>
        </div>
        <div class="method-step">
            <div class="method-num">3</div>
            <div class="method-text">
                <h5>AI Diagnosis (Gemini 2.0 Flash)</h5>
                <p>Google's Gemini model provides the cognitive diagnosis in structured JSON, enabling programmatic downstream use.</p>
            </div>
        </div>
        <div class="method-step">
            <div class="method-num">4</div>
            <div class="method-text">
                <h5>Visualization & Action</h5>
                <p>Results are aggregated into the Mastery Heatmap and Risk Radar, turning raw AI outputs into teacher-facing insights.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# TAB 4: Data Logs
# ======================================================
with tab4:
    st.markdown(
        '<div class="section-header"><span class="icon">📝</span><span class="label">Student Interaction Logs</span></div>'
        '<p class="section-desc">Raw dataset of all simulated student attempts. Use the sidebar filters to narrow results.</p>',
        unsafe_allow_html=True
    )
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "is_correct": st.column_config.CheckboxColumn("Correct?"),
            "time_to_first_response_ms": st.column_config.NumberColumn("Response Time (ms)", format="%d"),
            "hint_requests": st.column_config.NumberColumn("Hints"),
        }
    )

# ======================================================
# TAB 5: About Me / Profile
# ======================================================
with tab5:
    prof_col1, prof_col2 = st.columns([2, 1])

    with prof_col1:
        st.markdown('<p class="profile-name">ThiruMath</p>', unsafe_allow_html=True)
        st.markdown('<p class="profile-role">EdTech AI Developer &middot; Learning Engineer &middot; Data Scientist</p>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown(
            '<p class="profile-bio">'
            'I build AI-powered education tools that go beyond right-or-wrong grading. '
            'My work focuses on understanding <em>how</em> students think — using cognitive science, '
            'pedagogical AI, and modern data visualization to turn raw learning data into actionable insights. '
            'The Mistake Intelligence Engine is a demonstration of how Large Language Models can be combined with '
            'established learning theories like Repair Theory to create genuinely useful diagnostic tools for teachers.'
            '</p>',
            unsafe_allow_html=True
        )

        st.markdown("")

        # ── Contact Links ──
        st.markdown(
            '<a class="contact-link" href="https://github.com/ThiruMath" target="_blank">🔗 GitHub</a>'
            '<a class="contact-link" href="https://linkedin.com/in/YOUR-LINKEDIN" target="_blank">💼 LinkedIn</a>'
            '<a class="contact-link" href="mailto:your.email@example.com">📧 Email</a>',
            unsafe_allow_html=True
        )

    with prof_col2:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:2rem;">
            <p style="font-size:3.5rem; margin:0;">🧠</p>
            <p style="color:#38BDF8; font-weight:700; font-size:1rem; margin:0.5rem 0 0.2rem;">MIE v1.0</p>
            <p style="color:#475569; font-size:0.75rem;">Portfolio Project</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Skills ──
    st.markdown(
        '<div class="section-header"><span class="icon">🛠️</span><span class="label">Technical Skills</span></div>',
        unsafe_allow_html=True
    )
    skills = [
        "Python", "Streamlit", "Pandas", "Plotly", "Google Gemini API",
        "Prompt Engineering", "LLM Integration", "Data Visualization",
        "EdTech", "Pedagogical AI", "Machine Learning", "Cognitive Science",
        "Git & GitHub", "REST APIs", "SQL"
    ]
    st.markdown(
        '<div style="margin-bottom:1.5rem;">' +
        ''.join([f'<span class="skill-tag">{s}</span>' for s in skills]) +
        '</div>',
        unsafe_allow_html=True
    )

    # ── What Makes This Project Special ──
    st.markdown(
        '<div class="section-header"><span class="icon">⭐</span><span class="label">Why This Project Matters</span></div>',
        unsafe_allow_html=True
    )

    why_col1, why_col2, why_col3 = st.columns(3)

    with why_col1:
        st.markdown("""
        <div class="glass-card">
            <h4>🎓 Subject Matter Expertise</h4>
            <p>This isn't a generic dashboard. It demonstrates deep understanding of <strong>Repair Theory</strong>
            and error taxonomy — the "why" behind every student mistake.</p>
        </div>
        """, unsafe_allow_html=True)

    with why_col2:
        st.markdown("""
        <div class="glass-card">
            <h4>🤖 AI Orchestration</h4>
            <p>The PedCoT prompt methodology shows I can <strong>architect AI systems</strong> —
            not just call APIs, but design structured reasoning chains for domain-specific tasks.</p>
        </div>
        """, unsafe_allow_html=True)

    with why_col3:
        st.markdown("""
        <div class="glass-card">
            <h4>📊 Actionable Insights</h4>
            <p>The Mastery Heatmap and Risk Radar prove I can turn raw ML outputs into
            <strong>teacher-facing, decision-driving visualizations</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
