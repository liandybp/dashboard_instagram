"""Tab 5 - Mejor Horario para Publicar."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.components.tabs.base_tab import BaseTab


class BestTimeTab(BaseTab):
    """Pestaña de mejor horario: heatmap de engagement por día y hora."""

    @property
    def label(self) -> str:
        return "⏰ Mejor Horario"

    def render(self) -> None:
        st.subheader("⏰ Mejor Horario para Publicar")

        best_time_data = self.data.get("best_time_to_post", [])
        if not best_time_data:
            st.info("No hay datos de mejor horario disponibles")
            return

        df = pd.DataFrame(best_time_data)
        heatmap_data = df.pivot_table(
            values="value",
            index="day_of_week",
            columns="hour",
            aggfunc="mean"
        )

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale="Blues",
            text=heatmap_data.values,
            texttemplate="%{text:.0f}"
        ))
        fig.update_layout(
            title="Mejor Horario por Día de la Semana",
            xaxis_title="Hora del Día",
            yaxis_title="Día de la Semana"
        )
        st.plotly_chart(fig, use_container_width=True, key="best_time_heatmap")

