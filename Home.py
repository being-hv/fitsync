import streamlit as st


st.set_page_config(
    layout="wide",
    page_title="FitSync",
    page_icon="",
)


def apply_theme(is_light_mode: bool) -> None:
    if is_light_mode:
        background = "#f8fafc"
        surface = "rgba(255, 255, 255, 0.92)"
        surface_alt = "rgba(241, 245, 249, 0.95)"
        text = "#0f172a"
        muted = "#475569"
        border = "rgba(15, 23, 42, 0.10)"
        shadow = "0 24px 60px rgba(15, 23, 42, 0.08)"
        accent = "#0f172a"
        accent_soft = "rgba(15, 23, 42, 0.08)"
        hero_bg = "linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%)"
    else:
        background = "#020617"
        surface = "rgba(15, 23, 42, 0.92)"
        surface_alt = "rgba(30, 41, 59, 0.90)"
        text = "#f8fafc"
        muted = "#cbd5e1"
        border = "rgba(148, 163, 184, 0.14)"
        shadow = "0 28px 70px rgba(0, 0, 0, 0.45)"
        accent = "#e2e8f0"
        accent_soft = "rgba(226, 232, 240, 0.08)"
        hero_bg = "linear-gradient(135deg, #0f172a 0%, #020617 100%)"

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: {background};
                color: {text};
            }}
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}
            .hero-shell {{
                background: {hero_bg};
                border: 1px solid {border};
                border-radius: 28px;
                padding: 2.5rem 2rem;
                box-shadow: {shadow};
            }}
            .hero-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.45rem 0.9rem;
                border-radius: 999px;
                border: 1px solid {border};
                background: {accent_soft};
                color: {text};
                font-size: 0.92rem;
                letter-spacing: 0.02em;
            }}
            .hero-title {{
                font-size: clamp(2.4rem, 6vw, 4.8rem);
                line-height: 0.95;
                margin: 1rem 0 0.75rem 0;
                color: {text};
                font-weight: 800;
            }}
            .hero-subtitle {{
                color: {muted};
                font-size: 1.05rem;
                max-width: 760px;
                margin: 0 auto;
                line-height: 1.8;
            }}
            .section-label {{
                color: {muted};
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.18em;
                margin-bottom: 0.5rem;
            }}
            .feature-card {{
                background: {surface};
                border: 1px solid {border};
                border-radius: 22px;
                padding: 1.4rem;
                box-shadow: {shadow};
                height: 100%;
            }}
            .feature-title {{
                color: {text};
                font-size: 1.05rem;
                font-weight: 700;
                margin-bottom: 0.45rem;
            }}
            .feature-body {{
                color: {muted};
                line-height: 1.7;
                font-size: 0.98rem;
            }}
            .page-divider {{
                margin: 2rem 0;
                border-top: 1px solid {border};
            }}
            .metric-card {{
                background: {surface_alt};
                border: 1px solid {border};
                border-radius: 18px;
                padding: 1rem 1.1rem;
            }}
            .metric-label {{
                color: {muted};
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                margin-bottom: 0.35rem;
            }}
            .metric-value {{
                color: {text};
                font-size: 1.25rem;
                font-weight: 700;
            }}
            .stSidebar {{
                background: {background};
            }}
            .stSidebar [data-testid="stSidebarContent"] {{
                padding-top: 1rem;
            }}
            .stButton > button {{
                border-radius: 999px;
                border: 1px solid {border};
                background: {text};
                color: {background};
                padding: 0.7rem 1.2rem;
                font-weight: 700;
                transition: transform 0.15s ease, opacity 0.15s ease;
            }}
            .stButton > button:hover {{
                transform: translateY(-1px);
                opacity: 0.92;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


if "light_mode" not in st.session_state:
    st.session_state.light_mode = False


with st.sidebar:
    st.markdown("### Appearance")
    st.session_state.light_mode = st.toggle(
        "Light mode",
        value=st.session_state.light_mode,
        help="Switch between the black aesthetic and a clean light surface.",
    )
    st.caption("Toggle the interface style without leaving the page.")


apply_theme(st.session_state.light_mode)


mode_label = "Light Mode" if st.session_state.light_mode else "Dark Mode"
mode_icon = "☀️" if st.session_state.light_mode else "🌙"


st.markdown(
    f"""
    <div class="hero-shell" style="text-align:center;">
        <span class="hero-pill">{mode_icon} {mode_label} </span>
        <div class="hero-title">FitSync</div>
        <div class="hero-subtitle">
            A personal health analytics dashboard designed to help you track recovery,
            understand daily habits, and turn health data into clearer decisions.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)


st.markdown('<div class="section-label">What you will find</div>', unsafe_allow_html=True)
left_col, center_col, right_col = st.columns(3, gap="large")

with left_col:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">Main Page</div>
            <div class="feature-body">
                Overview of core metrics, navigation tips, and a quick introduction to the dashboard features.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with center_col:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">Dashboard</div>
            <div class="feature-body">
                KPI cards and interactive charts for recovery score, sleep, steps, heart rate, and calories.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">Trends</div>
            <div class="feature-body">
                Deeper insights with monthly recovery trends, summary statistics, and distributions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)


st.markdown('<div class="section-label">Core Metrics</div>', unsafe_allow_html=True)
metric_col1, metric_col2, metric_col3 = st.columns(3, gap="large")

with metric_col1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Recovery</div>
            <div class="metric-value">Recovery Score</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric_col2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Wellness</div>
            <div class="metric-value">Sleep, Steps, Calories</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric_col3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Navigation</div>
            <div class="metric-value">Sidebar Page Switcher</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)


st.info("Use the sidebar to switch between the pages and the appearance toggle to choose your preferred look.")

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        Built by Harshvardhanam <br>
        <b>FitSync</b> © 2026
    </div>
    """,
    unsafe_allow_html=True,
)
