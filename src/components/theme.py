"""Brand theme helpers for Streamlit and Plotly."""

import plotly.io as pio
import streamlit as st

# Brand palette from docs/manual-identidad-gretercomunica.md
GARNET = "#6B1E3A"
GARNET_DEEP = "#4A1228"
GOLD = "#C9A96E"
GOLD_LIGHT = "#E2C99A"
CREAM = "#FAF6EF"
BLUSH = "#F0DDD6"
BLUSH_MID = "#E8C9BE"
CHARCOAL = "#2C1A20"
WARM_GRAY = "#8A7A7F"

LIGHT_THEME = {
    "name": "light",
    "background": CREAM,
    "surface": BLUSH,
    "surface_alt": BLUSH_MID,
    "text": CHARCOAL,
    "muted": WARM_GRAY,
    "title": GARNET_DEEP,
    "accent": GARNET,
    "accent_soft": GOLD_LIGHT,
    "border": BLUSH_MID,
    "button_bg": GARNET,
    "button_text": CREAM,
    "button_border": GARNET_DEEP,
    "button_hover_bg": GARNET_DEEP,
    "button_hover_text": GOLD_LIGHT,
    "status_bg": CREAM,
    "status_text": CHARCOAL,
    "color_scheme": "light",
}

DARK_THEME = {
    "name": "dark",
    "background": "#140A11",
    "surface": "#26131D",
    "surface_alt": "#341723",
    "text": CREAM,
    "muted": "#C7B7BA",
    "title": GOLD_LIGHT,
    "accent": GOLD,
    "accent_soft": "#F0DDD6",
    "border": "#5E3040",
    "button_bg": GOLD,
    "button_text": GARNET_DEEP,
    "button_border": GOLD_LIGHT,
    "button_hover_bg": GOLD_LIGHT,
    "button_hover_text": GARNET_DEEP,
    "status_bg": "#2A1721",
    "status_text": CREAM,
    "color_scheme": "dark",
}


def _get_theme_tokens(mode: str) -> dict:
    return DARK_THEME if mode == "dark" else LIGHT_THEME


def apply_plotly_theme(mode: str = "light") -> None:
    """Apply a global Plotly theme aligned with brand colors."""
    tokens = _get_theme_tokens(mode)
    template_name = f"greter_{tokens['name']}"

    pio.templates[template_name] = {
        "layout": {
            "paper_bgcolor": tokens["background"],
            "plot_bgcolor": tokens["background"],
            "font": {"family": "Jost, sans-serif", "color": tokens["text"], "size": 14},
            "title": {"font": {"family": "Playfair Display, serif", "size": 24, "color": tokens["title"]}},
            "colorway": [tokens["accent"], GOLD, GARNET_DEEP, BLUSH_MID, GOLD_LIGHT, WARM_GRAY],
            "xaxis": {"gridcolor": tokens["border"], "zerolinecolor": tokens["border"]},
            "yaxis": {"gridcolor": tokens["border"], "zerolinecolor": tokens["border"]},
        }
    }
    pio.templates.default = template_name


def apply_streamlit_theme(mode: str = "light") -> None:
    """Inject global CSS to enforce brand typography and accents."""
    tokens = _get_theme_tokens(mode)
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

        :root {{
            --greter-garnet: #6B1E3A;
            --greter-garnet-deep: #4A1228;
            --greter-gold: #C9A96E;
            --greter-gold-light: #E2C99A;
            --greter-cream: #FAF6EF;
            --greter-blush: #F0DDD6;
            --greter-blush-mid: #E8C9BE;
            --greter-charcoal: #2C1A20;
            --greter-warm-gray: #8A7A7F;
            --greter-bg: {tokens['background']};
            --greter-surface: {tokens['surface']};
            --greter-surface-alt: {tokens['surface_alt']};
            --greter-text: {tokens['text']};
            --greter-muted: {tokens['muted']};
            --greter-title: {tokens['title']};
            --greter-border: {tokens['border']};
            --greter-accent: {tokens['accent']};
            --greter-button-bg: {tokens['button_bg']};
            --greter-button-text: {tokens['button_text']};
            --greter-button-border: {tokens['button_border']};
            --greter-button-hover-bg: {tokens['button_hover_bg']};
            --greter-button-hover-text: {tokens['button_hover_text']};
            --greter-status-bg: {tokens['status_bg']};
            --greter-status-text: {tokens['status_text']};
            --greter-color-scheme: {tokens['color_scheme']};
        }}

        html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stApp"],
        [data-testid="stHeader"], [data-testid="stToolbar"], .main, .block-container {{
            font-family: 'Jost', sans-serif;
            color: var(--greter-text) !important;
            background-color: var(--greter-bg) !important;
            color-scheme: var(--greter-color-scheme);
        }}

        .main *, .block-container *, [data-testid="stAppViewContainer"] *, [data-testid="stSidebar"] * {{
            color: var(--greter-text) !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Playfair Display', serif !important;
            color: var(--greter-title) !important;
            letter-spacing: 0.01em;
        }}

        p, li, label, span, a, small, strong, em, code, pre {{
            font-family: 'Jost', sans-serif;
            color: var(--greter-text) !important;
        }}

        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {{
            color: var(--greter-text) !important;
            line-height: 1.75;
        }}

        [data-testid="stMarkdownContainer"] * {{
            color: var(--greter-text) !important;
        }}

        [data-testid="stCaption"], .stCaption {{
            color: var(--greter-muted) !important;
        }}

        [data-testid="stText"], [data-testid="stWidgetLabel"], [data-testid="stRadio"],
        [data-testid="stSelectbox"], [data-testid="stMultiSelect"], [data-testid="stCheckbox"] {{
            color: var(--greter-text) !important;
        }}

        [data-testid="stAlert"] {{
            color: var(--greter-text) !important;
            border: 1px solid var(--greter-border) !important;
        }}

        [data-testid="stAlert"] * {{
            color: inherit !important;
        }}

        [data-testid="stDataFrame"] {{
            color: var(--greter-text) !important;
        }}

        input, textarea, select {{
            color: var(--greter-text) !important;
            background-color: var(--greter-surface) !important;
            border-color: var(--greter-border) !important;
        }}

        ::placeholder {{
            color: var(--greter-muted) !important;
            opacity: 0.85;
        }}

        [data-testid="stMetric"] {{
            background: var(--greter-surface);
            border: 1px solid var(--greter-border);
            border-radius: 12px;
            padding: 10px;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--greter-muted) !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--greter-title) !important;
            font-family: 'Playfair Display', serif;
        }}

        .stButton > button {{
            background-color: var(--greter-button-bg) !important;
            color: var(--greter-button-text) !important;
            border: 1px solid var(--greter-button-border) !important;
            border-radius: 8px;
            font-family: 'Jost', sans-serif;
            font-weight: 500;
            font-size: 0.82rem;
            line-height: 1;
            padding: 0.35rem 0.6rem;
            min-height: 2.1rem;
        }}

        .stButton > button *, .stButton > button p, .stButton > button span {{
            color: var(--greter-button-text) !important;
        }}

        .stButton > button:hover {{
            background-color: var(--greter-button-hover-bg) !important;
            border-color: var(--greter-gold) !important;
            color: var(--greter-button-hover-text) !important;
        }}

        .stButton > button:hover * {{
            color: var(--greter-button-hover-text) !important;
        }}

        [data-testid="stStatusWidget"],
        [data-testid="stStatusWidget"] > div,
        [data-testid="stStatusWidget"] > div > div,
        [data-testid="stStatusWidget"] [data-baseweb="notification"],
        [data-testid="stStatusWidget"] [role="status"],
        [data-testid="stStatusWidget"] [aria-live="polite"],
        [data-testid="stStatusWidget"] [class*="stStatus"],
        [data-testid="stStatusWidget"] [class*="status"] {{
            background-color: var(--greter-status-bg) !important;
            color: var(--greter-status-text) !important;
            border-color: var(--greter-border) !important;
        }}

        [data-testid="stStatusWidget"] *,
        [data-testid="stStatusWidget"] p,
        [data-testid="stStatusWidget"] span,
        [data-testid="stStatusWidget"] label,
        [data-testid="stStatusWidget"] small {{
            color: var(--greter-status-text) !important;
        }}

        [data-testid="stSpinner"], [data-testid="stSpinner"] * {{
            color: var(--greter-text) !important;
        }}

        [data-testid="stProgress"] > div > div > div {{
            background-color: var(--greter-surface-alt) !important;
        }}

        [data-testid="stProgress"] div[role="progressbar"] {{
            background-color: var(--greter-accent) !important;
        }}

        button[data-baseweb="tab"] {{
            font-family: 'Jost', sans-serif;
            font-weight: 500;
            color: var(--greter-muted) !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            color: var(--greter-garnet) !important;
            border-bottom-color: var(--greter-gold) !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: var(--greter-surface);
        }}

        [data-testid="stSidebar"] *, [data-testid="stSidebarNav"] * {{
            color: var(--greter-text) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_brand_theme(mode: str = "light") -> None:
    """Apply full app theme (Streamlit + Plotly)."""
    apply_plotly_theme(mode)
    apply_streamlit_theme(mode)


