"""Tab 6 - Frecuencia de Publicación."""

import plotly.express as px
import streamlit as st

from src.components.tabs.base_tab import BaseTab


class FrequencyTab(BaseTab):
    """Pestaña de frecuencia de publicación: scatter posts/semana vs engagement."""

    @property
    def label(self) -> str:
        return "📊 Frecuencia"

    def render(self) -> None:
        st.subheader("📊 Frecuencia de Publicación")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Posts por Semana vs Engagement Promedio")
            fig = px.scatter(
                x=[1, 2, 3, 4],
                y=[85, 75, 90, 65],
                labels={"x": "Posts por Semana", "y": "Engagement Promedio"},
                title="Relación entre Frecuencia y Engagement"
            )
            st.plotly_chart(fig, use_container_width=True, key="frequency_scatter")

        with col2:
            st.subheader("Decaimiento del Contenido")
            st.info("No hay datos de decaimiento disponibles (no implementado)")

