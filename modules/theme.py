import streamlit as st


def ensure_theme_state(default_light_mode: bool = False) -> None:
    if "light_mode" not in st.session_state:
        st.session_state.light_mode = default_light_mode


def get_theme_tokens(is_light_mode: bool) -> dict[str, str]:
    if is_light_mode:
        return {
            "background": "#f8fafc",
            "surface": "#ffffff",
            "surface_alt": "#f1f5f9",
            "text": "#0f172a",
            "muted": "#334155",
            "border": "rgba(15, 23, 42, 0.14)",
            "shadow": "0 18px 40px rgba(15, 23, 42, 0.10)",
            "plotly_template": "plotly_white",
            "grid": "#e5e7eb",
        }

    return {
        "background": "#020617",
        "surface": "rgba(15, 23, 42, 0.92)",
        "surface_alt": "rgba(30, 41, 59, 0.90)",
        "text": "#f8fafc",
        "muted": "#cbd5e1",
        "border": "rgba(148, 163, 184, 0.14)",
        "shadow": "0 28px 70px rgba(0, 0, 0, 0.45)",
        "plotly_template": "plotly_dark",
        "grid": "rgba(148, 163, 184, 0.18)",
    }


def apply_theme(is_light_mode: bool, extra_css: str = "") -> dict[str, str]:
    tokens = get_theme_tokens(is_light_mode)
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: {tokens['background']};
                color: {tokens['text']};
            }}
            h1, h2, h3, h4, h5, h6,
            p, li, label, span, div,
            .stMarkdown,
            .stMarkdown p,
            .stMarkdown li,
            .stCaption,
            .stSubheader,
            .stHeader,
            .stMetricLabel,
            .stMetricValue {{
                color: {tokens['text']};
            }}
            .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
            }}
            .stSidebar {{
                background: {tokens['background']};
            }}
            .stSidebar [data-testid="stSidebarContent"] {{
                padding-top: 1rem;
            }}
            .stSidebar label,
            .stSidebar p,
            .stSidebar div,
            .stSidebar span,
            .stSidebar input,
            .stSidebar textarea,
            .stSelectbox label,
            .stMultiSelect label,
            .stSlider label,
            .stRadio label,
            .stCheckbox label,
            .stDateInput label,
            .stTextInput label,
            .stNumberInput label {{
                color: {tokens['text']};
            }}
            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] input,
            div[data-baseweb="select"] span,
            div[data-baseweb="select"] svg {{
                color: {tokens['text']};
                fill: {tokens['text']};
            }}
            div[data-baseweb="select"] [role="button"],
            div[data-baseweb="select"] [aria-haspopup="listbox"] {{
                color: {tokens['text']};
            }}
            div[data-baseweb="select"] > div {{
                background-color: {tokens['surface']};
                border-color: {tokens['border']};
            }}
            div[data-baseweb="popover"] {{
                color: {tokens['text']};
            }}
            .stInfo,
            .stAlert p,
            .stAlert div {{
                color: {tokens['text']};
            }}
            .stDataFrame, .stDataFrame * {{
                color: {tokens['text']};
            }}
            .stButton > button {{
                border-radius: 999px;
                border: 1px solid {tokens['border']};
                background: {tokens['text']};
                color: {tokens['background']};
                padding: 0.7rem 1.2rem;
                font-weight: 700;
                transition: transform 0.15s ease, opacity 0.15s ease;
            }}
            .stButton > button:hover {{
                transform: translateY(-1px);
                opacity: 0.92;
            }}
{extra_css}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return tokens
