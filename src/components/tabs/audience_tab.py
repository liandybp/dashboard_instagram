"""Tab 3 - Audiencia."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.components.tabs.base_tab import BaseTab


class AudienceTab(BaseTab):
    """Pestaña de audiencia: distribución demográfica de Instagram y YouTube."""

    @property
    def label(self) -> str:
        return "👥 Audiencia"

    def render(self) -> None:
        st.subheader("👥 Audiencia")

        tab_ig, tab_yt = st.tabs(["Instagram", "YouTube"])

        with tab_ig:
            self._render_instagram()

        with tab_yt:
            self._render_youtube()

    def _render_instagram(self) -> None:
        st.subheader("Instagram")

        demographics = self.data.get("demographics", {}).get("instagram", {})

        def _fallback_age():
            return [
                {"label": "18-24", "count": 1500, "pct": 18.0},
                {"label": "25-34", "count": 2500, "pct": 30.0},
                {"label": "35-44", "count": 2000, "pct": 24.0},
                {"label": "45-54", "count": 1200, "pct": 15.0},
                {"label": "55+", "count": 800, "pct": 13.0},
            ]

        def _fallback_gender():
            return [
                {"label": "Mujer", "count": 7500, "pct": 60.0},
                {"label": "Hombre", "count": 5000, "pct": 40.0},
            ]

        def _fallback_country():
            return [
                {"label": "España", "count": 4000, "pct": 40.0},
                {"label": "México", "count": 3500, "pct": 35.0},
                {"label": "EE.UU.", "count": 2500, "pct": 25.0},
            ]

        def _fallback_city():
            return [
                {"label": "Madrid", "count": 2000, "pct": 40.0},
                {"label": "Barcelona", "count": 1500, "pct": 30.0},
                {"label": "Ciudad de Mexico", "count": 1500, "pct": 30.0},
            ]

        age = demographics.get("age") or _fallback_age()
        gender = demographics.get("gender") or _fallback_gender()
        country = demographics.get("country") or _fallback_country()
        city = demographics.get("city") or _fallback_city()

        df_age = pd.DataFrame(age)
        df_gender = pd.DataFrame(gender)
        df_country = pd.DataFrame(country)
        df_city = pd.DataFrame(city)

        if not df_age.empty:
            dominant_age = df_age.sort_values("pct", ascending=False).iloc[0]
            st.metric("Rango de edad dominante", f"{dominant_age['label']} años", f"{dominant_age['pct']:.1f}%")

        if not df_gender.empty and len(df_gender) >= 2:
            sorted_gender = df_gender.sort_values("pct", ascending=False)
            g1, g2 = sorted_gender.iloc[0], sorted_gender.iloc[1]
            st.caption(f"Tu audiencia es {g1['pct']:.1f}% {g1['label']} / {g2['pct']:.1f}% {g2['label']}")
            if g1["pct"] >= 80:
                st.info("La audiencia está muy desbalanceada por género (>80/20). Revisa si tu mensaje está hipersegmentado.")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Edad")
            fig = px.bar(df_age, x="label", y="count", title="Distribución por Edad")
            st.plotly_chart(fig, key="aud_age_ig", use_container_width=True)

        with col2:
            st.subheader("Género")
            fig = px.bar(df_gender, x="label", y="count", title="Distribución por Género")
            st.plotly_chart(fig, key="aud_gender_ig", use_container_width=True)

        with col3:
            st.subheader("País")
            fig = px.bar(df_country, x="label", y="count", title="Distribución por País")
            st.plotly_chart(fig, key="aud_country_ig", use_container_width=True)

            if not df_country.empty:
                top3_pct = df_country.sort_values("pct", ascending=False).head(3)["pct"].sum()
                st.caption(f"Top 3 países = {top3_pct:.1f}% de tu audiencia")
                st.dataframe(
                    df_country.sort_values("pct", ascending=False)[["label", "pct"]].rename(
                        columns={"label": "País", "pct": "% audiencia"}
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
                top_country_pct = float(df_country.sort_values("pct", ascending=False).iloc[0]["pct"])
                if top_country_pct > 60:
                    st.info("Audiencia concentrada: tu país #1 supera el 60%. Buen escenario para un nicho local.")
                elif top_country_pct < 30:
                    st.info("Audiencia dispersa: tu país #1 está por debajo del 30%. Considera mensajes más globales.")
                else:
                    st.info("Audiencia balanceada: tienes una mezcla sana entre foco local e internacional.")

        with col4:
            st.subheader("Ciudad")
            fig = px.bar(df_city, x="label", y="count", title="Distribución por Ciudad")
            st.plotly_chart(fig, key="aud_city_ig", use_container_width=True)

    def _render_youtube(self) -> None:
        st.subheader("YouTube")

        demographics = self.data.get("demographics", {}).get("youtube", {})
        age = demographics.get("age") or [
            {"label": "18-24", "count": 1200, "pct": 18.0},
            {"label": "25-34", "count": 2000, "pct": 31.0},
            {"label": "35-44", "count": 1800, "pct": 28.0},
            {"label": "45-54", "count": 1000, "pct": 15.0},
            {"label": "55+", "count": 600, "pct": 8.0},
        ]
        gender = demographics.get("gender") or [
            {"label": "Mujer", "count": 6000, "pct": 57.0},
            {"label": "Hombre", "count": 4500, "pct": 43.0},
        ]
        country = demographics.get("country") or [
            {"label": "EE.UU.", "count": 3500, "pct": 41.0},
            {"label": "México", "count": 3000, "pct": 35.0},
            {"label": "España", "count": 2000, "pct": 24.0},
        ]

        df_audience_yt = pd.DataFrame(age)
        df_gender_yt = pd.DataFrame(gender)
        df_country_yt = pd.DataFrame(country)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Edad")
            fig = px.bar(df_audience_yt, x="label", y="count", title="Distribución por Edad")
            st.plotly_chart(fig, key="aud_age_yt", use_container_width=True)

        with col2:
            st.subheader("Género")
            fig = px.bar(df_gender_yt, x="label", y="count", title="Distribución por Género")
            st.plotly_chart(fig, key="aud_gender_yt", use_container_width=True)

        with col3:
            st.subheader("País")
            fig = px.bar(df_country_yt, x="label", y="count", title="Distribución por País")
            st.plotly_chart(fig, key="aud_country_yt", use_container_width=True)

