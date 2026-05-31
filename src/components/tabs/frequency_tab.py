"""Tab 6 - Frecuencia de Publicación."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

from src.components.tabs.base_tab import BaseTab


class FrequencyTab(BaseTab):
    """Pestaña de frecuencia de publicación: scatter posts/semana vs engagement."""

    @property
    def label(self) -> str:
        return "📊 Frecuencia"

    def render(self) -> None:
        st.subheader("📊 Frecuencia de Publicación")

        col1, col2 = st.columns(2)

        posting_frequency = self.data.get("posting_frequency", [])
        content_decay = self.data.get("content_decay", [])
        posts = self.data.get("posts", [])

        pf_df = pd.DataFrame(posting_frequency)
        if not pf_df.empty and {"posts_per_week", "avg_engagement_rate"}.issubset(pf_df.columns):
            x = pf_df["posts_per_week"].astype(float)
            y = pf_df["avg_engagement_rate"].astype(float)
            n = len(x)
            slope = 0.0
            intercept = float(y.mean()) if n > 0 else 0.0
            if n > 1:
                denom = (n * (x ** 2).sum()) - (x.sum() ** 2)
                if denom != 0:
                    slope = ((n * (x * y).sum()) - (x.sum() * y.sum())) / denom
                    intercept = (y.sum() - slope * x.sum()) / n
            pf_df["trend"] = slope * x + intercept
            best_row = pf_df.sort_values("avg_engagement_rate", ascending=False).iloc[0]
            optimal_min = max(1.0, float(best_row["posts_per_week"]) - 0.5)
            optimal_max = float(best_row["posts_per_week"]) + 0.5
        else:
            pf_df = pd.DataFrame({"posts_per_week": [1, 2, 3, 4], "avg_engagement_rate": [1.5, 2.2, 2.0, 1.3]})
            pf_df["trend"] = pf_df["avg_engagement_rate"]
            optimal_min, optimal_max = 2.5, 3.5

        with col1:
            st.subheader("Posts por Semana vs Engagement Promedio")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pf_df["posts_per_week"],
                y=pf_df["avg_engagement_rate"],
                mode="markers",
                name="Buckets observados",
            ))
            fig.add_trace(go.Scatter(
                x=pf_df["posts_per_week"],
                y=pf_df["trend"],
                mode="lines",
                name="Tendencia",
            ))
            fig.update_layout(
                title="Relación entre Frecuencia y Engagement",
                xaxis_title="Posts por Semana",
                yaxis_title="Engagement promedio",
            )
            st.plotly_chart(fig, use_container_width=True, key="frequency_scatter")
            st.caption(f"Zona óptima estimada: {optimal_min:.1f} - {optimal_max:.1f} posts/semana")

        with col2:
            st.subheader("Decaimiento del Contenido")
            decay_df = pd.DataFrame(content_decay)
            if not decay_df.empty and {"bucket", "avg_pct_of_final"}.issubset(decay_df.columns):
                fig_decay = px.line(decay_df, x="bucket", y="avg_pct_of_final", markers=True)
                st.plotly_chart(fig_decay, use_container_width=True, key="frequency_decay")
                if len(decay_df) >= 2:
                    seven_day_like = float(decay_df.iloc[min(1, len(decay_df)-1)]["avg_pct_of_final"])
                    st.caption(f"Tu contenido mantiene ~{seven_day_like:.1f}% del rendimiento inicial en el segundo tramo temporal.")
            else:
                st.info("No hay datos de decaimiento disponibles")

        st.divider()
        st.subheader("Cadencia real por semana")
        if posts:
            posts_df = pd.DataFrame(posts)
            ts_col = "timestamp" if "timestamp" in posts_df.columns else None
            if ts_col:
                posts_df[ts_col] = pd.to_datetime(posts_df[ts_col], errors="coerce")
                posts_df = posts_df.dropna(subset=[ts_col])
                if not posts_df.empty:
                    posts_df["week"] = posts_df[ts_col].dt.to_period("W").astype(str)
                    weekly = posts_df.groupby("week").size().reset_index(name="posts")
                    weekly["en_zona_optima"] = weekly["posts"].between(optimal_min, optimal_max)
                    colors = ["#4CAF50" if ok else "#C9A96E" for ok in weekly["en_zona_optima"]]
                    fig_weekly = go.Figure(go.Bar(x=weekly["week"], y=weekly["posts"], marker_color=colors))
                    fig_weekly.update_layout(xaxis_title="Semana", yaxis_title="Posts")
                    st.plotly_chart(fig_weekly, use_container_width=True, key="frequency_weekly")
                else:
                    st.info("No hay timestamps válidos en posts para calcular cadencia semanal.")
            else:
                st.info("No hay columna timestamp en posts para calcular cadencia semanal.")
        else:
            st.info("No hay posts para calcular cadencia semanal.")

