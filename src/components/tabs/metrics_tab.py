"""Tab 1 - Métricas Generales."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.components.tabs.base_tab import BaseTab


class MetricsTab(BaseTab):
    """Pestaña de métricas generales: KPIs y tendencia de engagement."""

    @property
    def label(self) -> str:
        return "📈 Métricas"

    def render(self) -> None:
        st.subheader("📈 Métricas Generales")

        account_snapshot = self.data.get("account_snapshot")
        if not account_snapshot:
            st.info("No hay datos de métricas disponibles")
            return

        snapshot = account_snapshot
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Seguidores", f"{snapshot.get('followers_count', 0):,}")
        with col2:
            st.metric("Publicaciones", f"{snapshot.get('posts_count', 0):,}")
        with col3:
            st.metric("Engagement Rate", f"{snapshot.get('engagement_rate', 0):.2f}%")
        with col4:
            st.metric("Reach", f"{snapshot.get('reach', 0):,}")

        daily_metrics = self.data.get("daily_metrics")
        if daily_metrics:
            df_daily = pd.DataFrame(daily_metrics)
            df_daily["date"] = pd.to_datetime(df_daily["date"])
            fig = px.line(df_daily, x="date", y="engagement_rate", title="Tendencia de Engagement")
            st.plotly_chart(fig, use_container_width=True, key="metrics_engagement")

