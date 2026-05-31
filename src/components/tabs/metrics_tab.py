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
        followers = snapshot.get("followers_count", snapshot.get("follower_count", 0))
        posts_count = snapshot.get("posts_count", 0)

        daily_metrics = self.data.get("daily_metrics") or []
        df_daily = pd.DataFrame(daily_metrics)
        if not df_daily.empty and "date" in df_daily.columns:
            df_daily["date"] = pd.to_datetime(df_daily["date"], errors="coerce")
            df_daily = df_daily.dropna(subset=["date"]).sort_values("date")

        def _sum_col(df, cols):
            for c in cols:
                if c in df.columns:
                    return pd.to_numeric(df[c], errors="coerce").fillna(0).sum()
            return 0.0

        def _delta_pct(curr, prev):
            if prev in (None, 0):
                return None
            return ((curr - prev) / prev) * 100

        if not df_daily.empty:
            max_date = df_daily["date"].max()
            cur_start = max_date - pd.Timedelta(days=29)
            prev_start = cur_start - pd.Timedelta(days=30)
            prev_end = cur_start - pd.Timedelta(days=1)

            cur_df = df_daily[(df_daily["date"] >= cur_start) & (df_daily["date"] <= max_date)]
            prev_df = df_daily[(df_daily["date"] >= prev_start) & (df_daily["date"] <= prev_end)]
        else:
            cur_df = pd.DataFrame()
            prev_df = pd.DataFrame()

        reach_30d = _sum_col(cur_df, ["reach", "accounts_reached", "totalReach"])
        prev_reach_30d = _sum_col(prev_df, ["reach", "accounts_reached", "totalReach"])

        interactions_30d = _sum_col(cur_df, ["engagements", "interactions", "engaged", "totalEngagement"])
        prev_interactions_30d = _sum_col(prev_df, ["engagements", "interactions", "engaged", "totalEngagement"])

        d_reach = _delta_pct(reach_30d, prev_reach_30d)
        d_interactions = _delta_pct(interactions_30d, prev_interactions_30d)

        posts = self.data.get("posts") or []
        likes = sum(float(p.get("likes_count", p.get("likes", 0)) or 0) for p in posts)
        comments = sum(float(p.get("comments_count", p.get("comments", 0)) or 0) for p in posts)
        saves = sum(float(p.get("saves", p.get("saves_count", 0)) or 0) for p in posts)
        shares = sum(float(p.get("shares", p.get("shares_count", 0)) or 0) for p in posts)
        engagement_rate_calc = ((likes + comments + saves + shares) / reach_30d * 100) if reach_30d > 0 else None
        ratio_saved_likes = (saves / likes) if likes > 0 else None

        def _fmt_num(value):
            return f"{int(round(value)):,}" if value is not None else "No disponible"

        def _fmt_pct(value):
            return f"{float(value):.2f}%" if value is not None else "No disponible"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Seguidores", _fmt_num(followers))
        with col2:
            st.metric("Publicaciones", _fmt_num(posts_count))
        with col3:
            st.metric("Reach (30d)", _fmt_num(reach_30d), delta=_fmt_pct(d_reach) if d_reach is not None else None)
        with col4:
            st.metric("Interacciones (30d)", _fmt_num(interactions_30d), delta=_fmt_pct(d_interactions) if d_interactions is not None else None)

        extra1, extra2 = st.columns(2)
        with extra1:
            st.metric("Tasa de engagement (calc)", _fmt_pct(engagement_rate_calc))
            st.caption("Benchmark orientativo IG: 1-3%")
        with extra2:
            idx_valor = f"{ratio_saved_likes:.2f}" if ratio_saved_likes is not None else "No disponible"
            st.metric("Indice de valor (guardados/likes)", idx_valor)

        if not df_daily.empty and "engagement_rate" in df_daily.columns:
            fig = px.line(df_daily, x="date", y="engagement_rate", title="Tendencia de Engagement")
            st.plotly_chart(fig, use_container_width=True, key="metrics_engagement")

        if posts:
            best_post = sorted(
                posts,
                key=lambda p: (
                    float(p.get("saves", p.get("saves_count", 0)) or 0),
                    float(p.get("reach", 0) or 0),
                ),
                reverse=True,
            )[0]

            st.divider()
            st.subheader("🏆 Mejor post del período")
            c_img, c_txt = st.columns([1, 2])
            with c_img:
                img = best_post.get("thumbnail_url") or best_post.get("image_url")
                if img:
                    st.image(img, use_column_width=True)
            with c_txt:
                caption = (best_post.get("caption") or "Sin caption").strip()
                st.write(caption[:180] + ("..." if len(caption) > 180 else ""))
                st.write(
                    f"💾 {int(float(best_post.get('saves', best_post.get('saves_count', 0)) or 0)):,} guardados · "
                    f"📈 {int(float(best_post.get('reach', 0) or 0)):,} alcance"
                )
                permalink = best_post.get("permalink")
                if permalink:
                    st.markdown(f"[Ver publicación →]({permalink})")

