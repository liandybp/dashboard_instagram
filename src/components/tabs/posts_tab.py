"""Tab 4 - Posts."""

import streamlit as st

from src.components.idea_filters import count_substantive, filter_spam_comments
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

        sort_option = st.selectbox(
            "Ordenar por:",
            ["Guardados", "Alcance", "Likes", "Comentarios", "Ratio engagement"],
            index=0,
        )

        def _score(post):
            likes = float(post.get("likes_count", post.get("likes", 0)) or 0)
            comments = float(post.get("comments_count", post.get("comments", 0)) or 0)
            saves = float(post.get("saves", post.get("saves_count", 0)) or 0)
            reach = float(post.get("reach", 0) or 0)
            if sort_option == "Guardados":
                return saves
            if sort_option == "Alcance":
                return reach
            if sort_option == "Likes":
                return likes
            if sort_option == "Comentarios":
                return comments
            return ((likes + comments + saves) / reach) * 100 if reach > 0 else 0

        posts = sorted(posts, key=_score, reverse=True)

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

                permalink = (post.get("permalink") or "").lower()
                if "/reel/" in permalink:
                    st.caption("🎬 Reel")
                else:
                    st.caption("🖼 Post")

                likes = post.get("likes_count", 0)
                comments_count = post.get("comments_count", 0)
                st.write(f"👍 {likes} | 💬 {comments_count}")

                if st.button("Ver comentarios", key=f"comment_{post['id']}"):
                    with st.expander("Comentarios"):
                        post_comments = [c for c in self.data.get("comments", []) if c.get("post_id") == post.get("id")]
                        total_comments = len(post_comments)
                        substantive_comments = count_substantive(post_comments)
                        st.caption(f"{total_comments} total · {substantive_comments} sustantivos")
                        for comment in post_comments:
                            if filter_spam_comments(comment["text"]):
                                author = comment.get("author") or comment.get("username") or "usuario"
                                st.write(f"🗣️ **{author}**: {comment['text']}")
                            else:
                                st.markdown("💬 _Comentario filtrado_")

