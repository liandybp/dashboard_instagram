"""Tab 2 - Salud de Cuenta."""

import json
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from cache import read_account_health_dict, read_follower_history_list
from src.components.tabs.base_tab import BaseTab


class HealthTab(BaseTab):
    """Pestaña de salud de cuenta: token, permisos, seguidores."""

    @property
    def label(self) -> str:
        return "🔍 Health"

    def render(self) -> None:
        st.subheader("🩺 Salud de Cuenta")

        def _parse_json_list(value):
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                try:
                    parsed = json.loads(value or "[]")
                    return parsed if isinstance(parsed, list) else []
                except Exception:
                    return []
            return []

        account_id = self.data.get("account_snapshot", {}).get("id")
        platform = "instagram"
        health = None

        try:
            health = read_account_health_dict(account_id, platform)
        except Exception as e:
            st.warning(f"No se pudo leer salud de cuenta desde caché: {e}")

        # Fallback: usar payload cargado desde API en esta misma ejecución.
        if not health:
            health = self.data.get("account_health")

        if not health:
            st.info("Sin datos de salud. Haz clic en 'Refrescar datos' para verificar.")
            return

        token_valid = bool(health.get("token_valid", health.get("tokenValid", True)))
        is_active = bool(health.get("is_active", health.get("isActive", True)))
        is_verified = bool(health.get("is_verified", health.get("isVerified", False)))
        is_restricted = bool(health.get("is_restricted", health.get("isRestricted", False)))
        scopes_ok = bool(health.get("scopes_ok", health.get("scopesOk", True)))

        # --- Bloque 1: Indicadores booleanos ---
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            icon = "🟢" if token_valid else "🔴"
            st.metric("Token OAuth", f"{icon} {'Válido' if token_valid else 'Expirado'}")
        with col2:
            icon = "🟢" if is_active else "🔴"
            st.metric("Cuenta activa", f"{icon} {'Sí' if is_active else 'No'}")
        with col3:
            icon = "✅" if is_verified else "—"
            st.metric("Verificada", f"{icon} {'Sí' if is_verified else 'No'}")
        with col4:
            icon = "⚠️" if is_restricted else "🟢"
            label = "Restringida" if is_restricted else "Sin restricciones"
            st.metric("Restricciones", f"{icon} {label}")

        # --- Bloque 2: Permisos ---
        st.divider()
        st.subheader("Permisos de la integración")

        if scopes_ok:
            st.success("✅ Todos los permisos necesarios están activos.")
        else:
            missing = _parse_json_list(health.get("missing_scopes", health.get("missingScopes", [])))
            st.error(f"❌ Faltan {len(missing)} permiso(s): {', '.join(missing)}")
            st.caption("Reconecta tu cuenta en zernio.com para restaurar los permisos.")

        # --- Bloque 3: Problemas y recomendaciones ---
        issues = _parse_json_list(health.get("issues", []))
        recommendations = _parse_json_list(health.get("recommendations", []))

        if issues:
            st.divider()
            st.subheader("⚠️ Problemas detectados")
            for issue in issues:
                st.warning(issue)

        if recommendations:
            st.subheader("💡 Recomendaciones")
            for rec in recommendations:
                st.info(rec)

        if not issues and not recommendations:
            st.divider()
            st.success("Todo en orden. No hay problemas ni recomendaciones pendientes.")

        # --- Bloque 4: Dinámica de seguidores ---
        st.divider()
        st.subheader("Dinámica de seguidores (últimos 90 días)")

        try:
            follower_data = read_follower_history_list(platform, days=90)
        except Exception as e:
            st.warning(f"No se pudo leer historial de seguidores: {e}")
            follower_data = []

        if not follower_data:
            follower_data = self.data.get("follower_history", [])

        if not follower_data:
            st.info("Sin historial de seguidores. Refresca para cargar datos.")
            return

        df = pd.DataFrame(follower_data)

        fig_total = px.line(
            df, x="date", y="followers",
            title="Total de seguidores por día",
            labels={"date": "Fecha", "followers": "Seguidores"},
            color_discrete_sequence=["#E1306C"]
        )
        fig_total.update_layout(hovermode="x unified")
        st.plotly_chart(fig_total, use_container_width=True, key="health_followers_total")

        if "followers_gained" in df.columns and df["followers_gained"].sum() > 0:
            fig_delta = go.Figure()
            fig_delta.add_trace(go.Bar(
                x=df["date"], y=df["followers_gained"],
                name="Ganados", marker_color="#4CAF50"
            ))
            fig_delta.add_trace(go.Bar(
                x=df["date"], y=[-v for v in df["followers_lost"]],
                name="Perdidos", marker_color="#F44336"
            ))
            fig_delta.update_layout(
                title="Seguidores ganados y perdidos por día",
                barmode="relative",
                hovermode="x unified",
                yaxis_title="Seguidores",
                xaxis_title="Fecha"
            )
            st.plotly_chart(fig_delta, use_container_width=True, key="health_followers_delta")
            st.caption(
                "ℹ️ Meta eliminó el historial de ganados/perdidos de su API nativa. "
                "Zernio reconstruye esta métrica mediante capturas diarias."
            )
        else:
            st.caption("Los datos de seguidores ganados/perdidos estarán disponibles "
                       "tras varios días de capturas consecutivas.")

        checked_at = str(health.get("checked_at", datetime.now().isoformat()))
        st.caption(f"Última verificación: {checked_at[:16].replace('T', ' ')} UTC")

