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

        audience_data = [
            {"age": "18-24", "count": 1500},
            {"age": "25-34", "count": 2500},
            {"age": "35-44", "count": 2000},
            {"age": "45-54", "count": 1200},
            {"age": "55+",   "count": 800},
        ]
        df_audience = pd.DataFrame(audience_data)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Edad")
            fig = px.bar(df_audience, x="age", y="count", title="Distribución por Edad")
            st.plotly_chart(fig, key="aud_age_ig", use_container_width=True)

        with col2:
            st.subheader("Género")
            df = pd.DataFrame({"gender": ["Hombre", "Mujer"], "count": [5000, 7500]})
            fig = px.bar(df, x="gender", y="count", title="Distribución por Género")
            st.plotly_chart(fig, key="aud_gender_ig", use_container_width=True)

        with col3:
            st.subheader("País")
            df = pd.DataFrame({"country": ["EE.UU.", "México", "España"], "count": [4000, 3500, 2500]})
            fig = px.bar(df, x="country", y="count", title="Distribución por País")
            st.plotly_chart(fig, key="aud_country_ig", use_container_width=True)

        with col4:
            st.subheader("Ciudad")
            df = pd.DataFrame({"city": ["Madrid", "Barcelona", "México DF"], "count": [2000, 1500, 1000]})
            fig = px.bar(df, x="city", y="count", title="Distribución por Ciudad")
            st.plotly_chart(fig, key="aud_city_ig", use_container_width=True)

    def _render_youtube(self) -> None:
        st.subheader("YouTube")

        audience_yt = [
            {"age": "18-24", "count": 1200},
            {"age": "25-34", "count": 2000},
            {"age": "35-44", "count": 1800},
            {"age": "45-54", "count": 1000},
            {"age": "55+",   "count": 600},
        ]
        df_audience_yt = pd.DataFrame(audience_yt)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Edad")
            fig = px.bar(df_audience_yt, x="age", y="count", title="Distribución por Edad")
            st.plotly_chart(fig, key="aud_age_yt", use_container_width=True)

        with col2:
            st.subheader("Género")
            df = pd.DataFrame({"gender": ["Hombre", "Mujer"], "count": [4500, 6000]})
            fig = px.bar(df, x="gender", y="count", title="Distribución por Género")
            st.plotly_chart(fig, key="aud_gender_yt", use_container_width=True)

        with col3:
            st.subheader("País")
            df = pd.DataFrame({"country": ["EE.UU.", "México", "España"], "count": [3500, 3000, 2000]})
            fig = px.bar(df, x="country", y="count", title="Distribución por País")
            st.plotly_chart(fig, key="aud_country_yt", use_container_width=True)

