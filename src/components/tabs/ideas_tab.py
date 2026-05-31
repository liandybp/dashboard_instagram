"""Tab 7 - Sistema de Ideas."""

import asyncio

import streamlit as st

from src.components.tabs.base_tab import BaseTab


class IdeasTab(BaseTab):
    """Pestaña de ideas: generación y gestión de ideas de contenido con IA."""

    @property
    def label(self) -> str:
        return "💡 Ideas"

    def render(self) -> None:
        st.subheader("💡 Sistema de Ideas")

        platform = st.radio("Plataforma:", ["Instagram", "YouTube"], horizontal=True)

        if st.button(f"Generar todas las ideas de {platform}"):
            with st.spinner(f"Generando ideas para {platform.lower()}..."):
                try:
                    if platform == "Instagram":
                        from src.components.ideas import generate_all_ideas_ig
                        ideas_list = asyncio.run(generate_all_ideas_ig())
                    else:
                        from src.components.ideas import generate_all_ideas_yt
                        ideas_list = generate_all_ideas_yt()

                    st.success("Ideas generadas con éxito!")
                    st.session_state["generated_ideas"] = ideas_list
                except Exception as e:
                    st.error(f"Error al generar ideas: {str(e)}")

        if "generated_ideas" not in st.session_state:
            st.info("Haz clic en 'Generar todas las ideas' para comenzar.")
            return

        ideas_data = st.session_state["generated_ideas"]

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

