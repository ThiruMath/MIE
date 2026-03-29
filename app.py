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

# -- Google Fonts + Premium CSS --
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* ── Global ── */
    *, *::before, *::after { box-sizing: border-box; }

    .stApp {
        background: #0D0D12;
        color: #CBD5E1;
        font-family: 'Inter', sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111118 0%, #0D0D12 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #94A3B8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 1rem;
    }

    /* ── Typography ── */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 0;
    }
    .hero-subtitle {
        color: #64748B;
        font-size: 1rem;
        margin-top: 0.25rem;
        margin-bottom: 1.5rem;
    }
    h2, h3 {
        color: #E2E8F0 !important;
        font-weight: 600;
    }

    /* ── Glassmorphism Metric Cards ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
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
        font-size: 0.85rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab-list"] button {
        color: #64748B;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.25s ease;
        border-bottom: none !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #F8FAFC;
        background: rgba(56, 189, 248, 0.12);
        border-bottom: none !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.1);
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }

    /* ── Inputs & Forms ── */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #1A1A24 !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        transition: border-color 0.2s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15) !important;
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
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;
    }
    .stFormSubmitButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 25px rgba(56, 189, 248, 0.45) !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
    }

    /* ── Dividers ── */
    hr {
        border-color: rgba(255,255,255,0.06) !important;
    }

    /* ── Error / Success / Info Boxes ── */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ── Section headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .section-header .icon {
        font-size: 1.5rem;
    }
    .section-header .label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E2E8F0;
    }
    .section-desc {
        color: #64748B;
        font-size: 0.875rem;
        margin-bottom: 1rem;
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
st.sidebar.markdown("## 🧠 MIE")
st.sidebar.markdown("---")
st.sidebar.markdown("## Filters")

if df.empty:
    st.error("⚠️ Data not found! Please run `python synthetic_data_generator.py` first.")
    st.stop()

students = ["All Students"] + sorted(df['student_id'].unique().tolist())
selected_student = st.sidebar.selectbox("Student", students)

error_types = ["All Types"] + sorted([e for e in df['error_type'].unique().tolist() if e != 'None'])
selected_error = st.sidebar.selectbox("Error Category", error_types)

# Apply filters
filtered_df = df.copy()
if selected_student != "All Students":
    filtered_df = filtered_df[filtered_df['student_id'] == selected_student]
if selected_error != "All Types":
    filtered_df = filtered_df[filtered_df['error_type'] == selected_error]

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<p style="color:#475569; font-size:0.75rem;">Powered by Google Gemini &middot; PedCoT v1</p>',
    unsafe_allow_html=True
)

# -- Hero --
st.markdown('<p class="hero-title">Mistake Intelligence Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Diagnosing <em>how</em> students think — not just <em>what</em> they answer.</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊  Dashboard", "📝  Data Logs", "🤖  Live Diagnosis"])

# ==========================================
# TAB 1: Diagnostic Dashboard
# ==========================================
with tab1:
    # ── KPI Row ──
    col1, col2, col3, col4 = st.columns(4)

    total_attempts = len(filtered_df)
    incorrect_attempts = len(filtered_df[~filtered_df['is_correct']])
    error_rate = (incorrect_attempts / total_attempts * 100) if total_attempts > 0 else 0
    conceptual_errors = len(filtered_df[filtered_df['error_type'] == 'Conceptual'])

    col1.metric("Total Attempts", f"{total_attempts:,}")
    col2.metric("Buggy Steps", f"{incorrect_attempts:,}")
    col3.metric("Error Rate", f"{error_rate:.1f}%")
    col4.metric("Conceptual Gaps", f"{conceptual_errors:,}")

    st.markdown("")  # spacer

    # ── Charts Row ──
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            '<div class="section-header"><span class="icon">🗺️</span><span class="label">Mastery Heatmap</span></div>'
            '<p class="section-desc">Student accuracy across mathematical concepts. Red = struggling, Green = mastery.</p>',
            unsafe_allow_html=True
        )

        heatmap_data = df.groupby(['student_id', 'concept_tag'])['is_correct'].mean().reset_index()
        heatmap_data['accuracy'] = heatmap_data['is_correct'] * 100
        pivot_data = heatmap_data.pivot(index='student_id', columns='concept_tag', values='accuracy')

        fig_heat = px.imshow(
            pivot_data,
            color_continuous_scale=[
                [0, "#EF4444"],      # red
                [0.5, "#FBBF24"],    # amber
                [1, "#22C55E"]       # green
            ],
            aspect="auto",
            labels=dict(x="Concept", y="Student", color="Accuracy %")
        )
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8", size=11),
            margin=dict(t=10, l=0, r=0, b=0),
            coloraxis_colorbar=dict(
                tickfont=dict(color="#94A3B8"),
                title=dict(font=dict(color="#94A3B8"))
            ),
            xaxis=dict(tickfont=dict(color="#CBD5E1")),
            yaxis=dict(tickfont=dict(color="#CBD5E1", size=9)),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with chart_col2:
        st.markdown(
            '<div class="section-header"><span class="icon">🎯</span><span class="label">Cognitive Risk Radar</span></div>'
            '<p class="section-desc">Distribution of error types — reveals which cognitive patterns need intervention.</p>',
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
            r=radar_values + [radar_values[0]],  # close the loop
            theta=categories + [categories[0]],
            fill='toself',
            name=selected_student if selected_student != "All Students" else "Class Avg",
            line=dict(color='#818CF8', width=2),
            fillcolor='rgba(129, 140, 248, 0.2)',
            marker=dict(size=8, color='#C084FC')
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True, color="#475569", showline=False,
                    gridcolor="rgba(255,255,255,0.06)", tickfont=dict(size=10),
                ),
                angularaxis=dict(
                    color="#CBD5E1", gridcolor="rgba(255,255,255,0.06)",
                    tickfont=dict(size=13, color="#E2E8F0"),
                )
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="#94A3B8",
            margin=dict(t=40, l=60, r=60, b=40),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── Error Breakdown Bar Chart ──
    st.markdown(
        '<div class="section-header"><span class="icon">📊</span><span class="label">Error Type Breakdown by Concept</span></div>'
        '<p class="section-desc">Grouped bar chart showing how error categories distribute across math topics.</p>',
        unsafe_allow_html=True
    )

    errors_only = filtered_df[filtered_df['error_type'] != 'None']
    if not errors_only.empty:
        bar_data = errors_only.groupby(['concept_tag', 'error_type']).size().reset_index(name='count')

        color_map = {
            'Factual': '#F87171',
            'Procedural': '#FBBF24',
            'Conceptual': '#818CF8',
        }

        fig_bar = px.bar(
            bar_data,
            x='concept_tag', y='count', color='error_type',
            barmode='group',
            color_discrete_map=color_map,
            labels={'concept_tag': 'Concept', 'count': 'Errors', 'error_type': 'Type'}
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#94A3B8", size=12),
            margin=dict(t=10, l=0, r=0, b=0),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="center", x=0.5, font=dict(color="#CBD5E1")
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#CBD5E1")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94A3B8")),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No errors found for the current filter selection.")

# ==========================================
# TAB 2: Raw Data Logs
# ==========================================
with tab2:
    st.markdown(
        '<div class="section-header"><span class="icon">📋</span><span class="label">Student Interaction Logs</span></div>'
        '<p class="section-desc">Filtered dataset of all student attempts. Use the sidebar to narrow results.</p>',
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

# ==========================================
# TAB 3: Live Tutor Diagnosis
# ==========================================
with tab3:
    st.markdown(
        '<div class="section-header"><span class="icon">🔬</span><span class="label">PedCoT Live Playground</span></div>'
        '<p class="section-desc">Test the Gemini-powered diagnostic engine. Enter a math problem and a student\'s incorrect reasoning below.</p>',
        unsafe_allow_html=True
    )

    with st.form("live_diagnosis_form"):
        col_q, col_a = st.columns(2)
        with col_q:
            test_question = st.text_input("Math Question", value="Which is larger: 0.8 or 0.355?")
        with col_a:
            test_correct = st.text_input("Correct Answer", value="0.8")

        test_attempt = st.text_area(
            "Student's Incorrect Attempt (show their reasoning)",
            value="0.355 because 355 is a bigger number than 8.",
            height=100
        )

        submitted = st.form_submit_button("🧠  Run MIE Diagnosis")

    if submitted:
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
                cat_colors = {
                    'Factual': '#F87171',
                    'Procedural': '#FBBF24',
                    'Conceptual': '#818CF8',
                    'None': '#22C55E',
                }
                color = cat_colors.get(cat, '#94A3B8')
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.04); border:1px solid {color}40; '
                    f'border-radius:16px; padding:1.5rem; text-align:center;">'
                    f'<p style="color:#94A3B8; font-size:0.8rem; margin:0;">ERROR CATEGORY</p>'
                    f'<p style="color:{color}; font-size:1.8rem; font-weight:700; margin:0.25rem 0;">{cat}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with r2:
                st.markdown(
                    f'<div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); '
                    f'border-radius:16px; padding:1.5rem;">'
                    f'<p style="color:#94A3B8; font-size:0.8rem; margin:0 0 0.5rem;">DIAGNOSIS</p>'
                    f'<p style="color:#E2E8F0; font-size:1rem; margin:0;">{result.get("diagnosis", "N/A")}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown("")
            st.info(f"💡 **Pedagogical Hint:** {result.get('pedagogical_advice', 'N/A')}")
