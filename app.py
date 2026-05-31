#!/usr/bin/env python3

# Cargar variables de entorno antes que cualquier otra cosa
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "env", override=True)
load_dotenv(BASE_DIR / ".env", override=True)

import os
import sys

# Añadir el directorio raíz al path para permitir imports relativos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# Configuración de página — debe ser el primer comando de Streamlit
st.set_page_config(
    page_title="Instagram Dashboard",
    page_icon="📊",
    layout="wide"
)

from src.data.loader import load_account_data_from_zernio_with_fallback
from cache import init_db
from src.components.theme import apply_brand_theme
from src.components.tabs import (
    MetricsTab,
    HealthTab,
    AudienceTab,
    PostsTab,
    BestTimeTab,
    FrequencyTab,
    IdeasTab,
)


@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_account_data() -> dict:
    data = load_account_data_from_zernio_with_fallback()
    if isinstance(data, dict):
        return data
    # Fallback defensivo adicional (no debería ejecutarse normalmente).
    return {
        "account_snapshot": {},
        "account_health": {},
        "daily_metrics": [],
        "posts": [],
        "comments": [],
        "follower_history": [],
        "best_time_to_post": [],
        "posting_frequency": [],
        "content_decay": [],
        "demographics": {
            "instagram": {"age": [], "gender": [], "country": [], "city": []},
            "youtube": {"age": [], "gender": [], "country": []},
        },
    }


def _trigger_refresh() -> None:
    """Fuerza recarga de datos invalidando caché y relanzando la app."""
    load_account_data.clear()
    st.cache_data.clear()
    st.rerun()


def _toggle_theme_mode() -> None:
    """Alterna entre modo claro y oscuro."""
    current = st.session_state.get("theme_mode", "light")
    st.session_state["theme_mode"] = "dark" if current == "light" else "light"
    st.rerun()


def _last_sync_text(data: dict) -> str:
    checked_at = data.get("account_health", {}).get("checked_at")
    updated_at = data.get("account_snapshot", {}).get("updated_at")
    stamp = checked_at or updated_at
    if not stamp:
        return "Sin sincronización registrada"
    return f"Última sincronización: {str(stamp)[:16].replace('T', ' ')}"


def main() -> None:
    # Asegura tablas SQLite requeridas por pestañas que leen caché.
    init_db()

    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "light"

    theme_mode = st.session_state["theme_mode"]

    # Aplicar branding global (fuente + paleta).
    apply_brand_theme(theme_mode)

    # Cargar datos
    data = load_account_data()

    title_col, refresh_col, theme_col = st.columns([11.8, 0.3, 0.3], gap="small")
    with title_col:
        st.title("📊 Dashboard de Instagram")
    with refresh_col:
        if st.button("🔄", help="Refrescar datos", use_container_width=True):
            _trigger_refresh()
    with theme_col:
        theme_button_label = "🌙" if theme_mode == "light" else "☀️"
        if st.button(theme_button_label, help="Cambiar entre tema claro y oscuro", use_container_width=True):
            _toggle_theme_mode()

    st.caption(_last_sync_text(data))

    # Instanciar las pestañas (POO)
    tab_objects = [
        MetricsTab(data),
        HealthTab(data),
        AudienceTab(data),
        PostsTab(data),
        BestTimeTab(data),
        FrequencyTab(data),
        IdeasTab(data),
    ]

    # Crear las pestañas de Streamlit usando las etiquetas de cada clase
    st_tabs = st.tabs([t.label for t in tab_objects])

    # Renderizar cada pestaña dentro de su contenedor
    for tab_obj, tab_ui in zip(tab_objects, st_tabs):
        with tab_ui:
            tab_obj.render()


if __name__ == "__main__":
    main()
