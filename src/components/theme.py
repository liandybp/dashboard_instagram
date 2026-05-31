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


def apply_plotly_theme() -> None:
    """Apply a global Plotly theme aligned with brand colors."""
    pio.templates["greter"] = {
        "layout": {
            "paper_bgcolor": CREAM,
            "plot_bgcolor": CREAM,
            "font": {"family": "Jost, sans-serif", "color": CHARCOAL, "size": 14},
            "title": {"font": {"family": "Playfair Display, serif", "size": 24, "color": GARNET_DEEP}},
            "colorway": [GARNET, GOLD, GARNET_DEEP, BLUSH_MID, GOLD_LIGHT, WARM_GRAY],
            "xaxis": {"gridcolor": BLUSH_MID, "zerolinecolor": BLUSH_MID},
            "yaxis": {"gridcolor": BLUSH_MID, "zerolinecolor": BLUSH_MID},
        }
    }
    pio.templates.default = "greter"


def apply_streamlit_theme() -> None:
    """Inject global CSS to enforce brand typography and accents."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&display=swap');

        :root {
            --greter-garnet: #6B1E3A;
            --greter-garnet-deep: #4A1228;
            --greter-gold: #C9A96E;
            --greter-gold-light: #E2C99A;
            --greter-cream: #FAF6EF;
            --greter-blush: #F0DDD6;
            --greter-blush-mid: #E8C9BE;
            --greter-charcoal: #2C1A20;
            --greter-warm-gray: #8A7A7F;
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stApp"],
        [data-testid="stHeader"], [data-testid="stToolbar"], .main, .block-container {
            font-family: 'Jost', sans-serif;
            color: var(--greter-charcoal);
            background-color: var(--greter-cream);
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif !important;
            color: var(--greter-garnet-deep);
            letter-spacing: 0.01em;
        }

        p, li, label, span, div {
            font-family: 'Jost', sans-serif;
        }

        [data-testid="stMarkdownContainer"] p {
            line-height: 1.75;
        }

        [data-testid="stMetric"] {
            background: var(--greter-blush);
            border: 1px solid var(--greter-blush-mid);
            border-radius: 12px;
            padding: 10px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--greter-warm-gray);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
        }

        [data-testid="stMetricValue"] {
            color: var(--greter-garnet-deep);
            font-family: 'Playfair Display', serif;
        }

        .stButton > button {
            background-color: var(--greter-garnet);
            color: var(--greter-cream);
            border: 1px solid var(--greter-garnet-deep);
            border-radius: 10px;
            font-family: 'Jost', sans-serif;
            font-weight: 500;
        }

        .stButton > button:hover {
            border-color: var(--greter-gold);
            color: var(--greter-gold-light);
        }

        button[data-baseweb="tab"] {
            font-family: 'Jost', sans-serif;
            font-weight: 500;
            color: var(--greter-warm-gray);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--greter-garnet);
            border-bottom-color: var(--greter-gold) !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--greter-blush);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_brand_theme() -> None:
    """Apply full app theme (Streamlit + Plotly)."""
    apply_plotly_theme()
    apply_streamlit_theme()


