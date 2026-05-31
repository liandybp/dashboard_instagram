"""Tab 4 - Posts."""

import streamlit as st

from src.components.idea_filters import filter_spam_comments
from src.components.tabs.base_tab import BaseTab


class PostsTab(BaseTab):
    """Pestaña de posts: grid de publicaciones con métricas y comentarios."""

    @property
    def label(self) -> str:
        return "📸 Posts"

    def render(self) -> None:
        st.subheader("📸 Posts")

        posts = self.data.get("posts", [])
        if not posts:
            st.info("No hay posts disponibles")
            return

        cols = st.columns(3)
        for i, post in enumerate(posts):
            with cols[i % 3]:
                image_url = post.get("thumbnail_url", "")
                if image_url:
                    st.image(image_url, use_column_width=True)
                else:
                    st.image("https://placehold.co/300x300?text=No+Image", use_column_width=True)

                caption = post.get("caption", "Sin título")
                st.write(f"**{caption}**")

                likes = post.get("likes_count", 0)
                comments_count = post.get("comments_count", 0)
                st.write(f"👍 {likes} | 💬 {comments_count}")

                if st.button("Ver comentarios", key=f"comment_{post['id']}"):
                    with st.expander("Comentarios"):
                        for comment in self.data.get("comments", []):
                            if filter_spam_comments(comment["text"]):
                                st.write(f"🗣️ **{comment['author']}**: {comment['text']}")
                            else:
                                st.markdown("💬 _Comentario filtrado_")

