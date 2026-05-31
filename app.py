#!/usr/bin/env python3

# Cargar variables de entorno antes que cualquier otra cosa
from dotenv import load_dotenv
load_dotenv(override=True)

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
    }


def main() -> None:
    # Cargar datos
    data = load_account_data()

    st.title("📊 Dashboard de Instagram")

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
