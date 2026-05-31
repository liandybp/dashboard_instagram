"""Tab 7 - Sistema de Ideas."""

import asyncio

import streamlit as st

from src.components.idea_filters import count_substantive
from src.components.tabs.base_tab import BaseTab


class IdeasTab(BaseTab):
    """Pestaña de ideas: generación y gestión de ideas de contenido con IA."""

    @property
    def label(self) -> str:
        return "💡 Ideas"

    def render(self) -> None:
        st.subheader("💡 Sistema de Ideas")

        comments = self.data.get("comments", [])
        dms = self.data.get("dms", [])
        demographics = self.data.get("demographics", {}).get("instagram", {})

        age = demographics.get("age", [])
        gender = demographics.get("gender", [])
        dominant_age = max(age, key=lambda x: x.get("pct", 0))["label"] if age else "N/D"
        dominant_gender = max(gender, key=lambda x: x.get("pct", 0))["label"] if gender else "N/D"

        with st.expander("📊 Contexto disponible"):
            st.markdown(f"- Comentarios: **{len(comments)}** total · **{count_substantive(comments)}** sustantivos")
            st.markdown(f"- DMs: **{len(dms)}** total · **{count_substantive(dms)}** sustantivos")
            st.markdown(f"- Demografía dominante: **{dominant_age}** · **{dominant_gender}**")
            estimated_tokens = (len(comments) * 30) + (len(dms) * 40) + 16000
            estimated_cost = (estimated_tokens * 0.000003) + (16000 * 0.000015)
            st.caption(f"Costo estimado de generación: ~${estimated_cost:.2f}")

        platform = st.radio("Plataforma:", ["Instagram", "YouTube"], horizontal=True)

        if st.button("Generar ideas"):
            with st.spinner(f"Generando ideas para {platform.lower()}..."):
                try:
                    if platform == "Instagram":
                        from src.components.ideas import generate_all_ideas_ig
                        ideas_list = asyncio.run(generate_all_ideas_ig())
                    else:
                        from src.components.ideas import generate_all_ideas_yt
                        ideas_list = generate_all_ideas_yt()

                    st.session_state["generated_ideas"] = ideas_list
                    if ideas_list:
                        st.success(f"Ideas generadas con exito: {len(ideas_list)}")
                    else:
                        st.warning("No se generaron ideas en esta ejecucion. Intenta refrescar y volver a generar.")
                except Exception as e:
                    st.error(f"Error al generar ideas: {str(e)}")

        if "generated_ideas" not in st.session_state:
            st.info("Haz clic en 'Generar ideas' para comenzar.")
            return

        ideas_data = st.session_state["generated_ideas"]
        if not ideas_data:
            st.info("Aun no hay ideas para mostrar. Pulsa generar de nuevo.")
            return

        # Agrupar por bucket
        ideas_by_bucket: dict = {}
        for idea in ideas_data:
            bucket = idea.get("bucket", "comments")
            ideas_by_bucket.setdefault(bucket, []).append(idea)

        for bucket in ["comments", "dms", "top_content"]:
            if bucket not in ideas_by_bucket:
                continue
            with st.expander(f"De {bucket} — {len(ideas_by_bucket[bucket])} ideas"):
                for idea in ideas_by_bucket[bucket]:
                    st.markdown(f"**{idea['angle']}**")
                    st.markdown("> " + "\n> ".join(idea["evidence_quotes"]))
                    st.markdown(f"**Por qué es buena idea:** {idea['why_good_idea']}")
                    st.markdown(f"**Ángulo sugerido:** {idea['suggested_angle']}")

                    basis_post_ids = idea.get("basis_post_ids", [])
                    if basis_post_ids:
                        posts_by_id = {str(p.get("id")): p for p in self.data.get("posts", [])}
                        linked = False
                        for pid in basis_post_ids:
                            post = posts_by_id.get(str(pid))
                            if post and post.get("permalink"):
                                st.markdown(f"[Ver post original →]({post['permalink']})")
                                linked = True
                                break
                        if not linked:
                            st.caption("No se encontró permalink para basis_post_ids en cache.")

                    if st.button("✕ Descartar", key=f"discard_{idea['id']}"):
                        with st.expander("Descartar idea"):
                            reason_quick = st.radio(
                                "Razón rápida:",
                                ["Tema cubierto", "No me interesa", "Muy básica",
                                 "No es mi estilo", "Otro"],
                                key=f"reason_quick_{idea['id']}"
                            )
                            reason_text = st.text_area(
                                "Descripción detallada:", key=f"reason_text_{idea['id']}"
                            )
                            if st.button("Confirmar descarte", key=f"confirm_discard_{idea['id']}"):
                                from src.components.ideas import discard_idea
                                discard_idea(idea["id"], reason_quick, reason_text)
                                st.success(f"Idea descartada: {idea['angle']}")

