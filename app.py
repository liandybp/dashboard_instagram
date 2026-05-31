#!/usr/bin/env python3

# Load environment variables with override
from dotenv import load_dotenv
load_dotenv(override=True)

# Set page config as the FIRST command in the script
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os
import sys

# Add the current directory to Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from src.data.loader import load_account_data_from_zernio_with_fallback
from src.components.idea_filters import filter_spam_comments

# Load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

# Set page config
st.set_page_config(
    page_title="Instagram Dashboard",
    page_icon="📊",
    layout="wide"
)

# Function to load account data (this would normally come from a database or API)
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_account_data():
    return load_account_data_from_zernio_with_fallback()

# Load the data
data = load_account_data()

# Main title
st.title("📊 Dashboard de Instagram")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Métricas", 
    "🔍 Health", 
    "👥 Audiencia", 
    "📸 Posts", 
    "⏰ Mejor Horario", 
    "📊 Frecuencia", 
    "💡 Ideas"
])

# Tab 1 - Metrics
with tab1:
    st.subheader("📈 Métricas Generales")
    
    # Get account snapshot data
    account_snapshot = data["account_snapshot"]
    if account_snapshot:
        snapshot = account_snapshot
        
        # Create 4-column layout for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Seguidores", f"{snapshot.get('followers_count', 0):,}")
            
        with col2:
            st.metric("Publicaciones", f"{snapshot.get('posts_count', 0):,}")
            
        with col3:
            st.metric("Engagement Rate", f"{snapshot.get('engagement_rate', 0):.2f}%")
            
        with col4:
            st.metric("Reach", f"{snapshot.get('reach', 0):,}")
        
        # Show engagement trend
        daily_metrics = data["daily_metrics"]
        if daily_metrics:
            df_daily = pd.DataFrame(daily_metrics)
            df_daily['date'] = pd.to_datetime(df_daily['date'])
            
            fig = px.line(df_daily, x='date', y='engagement_rate', title="Tendencia de Engagement")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de métricas disponibles")

# Tab 2 - Health
    with tab2:
        st.subheader("🔍 Health de la Cuenta")
        
        # Get account health data
        account_health = data["account_health"]
        if account_health:
            health = account_health
            
            # Create 3-column layout for health metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Estado", f"{health.get('status', 'unknown')}")
                
            with col2:
                st.metric("ID Cuenta", f"{health.get('id', '')}")
                
            with col3:
                st.metric("Plataforma", f"{health.get('platform', '')}")
            
            # Show health details
            st.subheader("Detalles de Salud")
            for key, value in health.items():
                if key not in ['id', 'platform', 'status']:
                    st.write(f"**{key}**: {value}")
        else:
            st.info("No hay datos de salud disponibles")

# Tab 3 - Audience
with tab3:
    st.subheader("👥 Audiencia")
    
    # Create tabs for IG and YT
    tab_ig, tab_yt = st.tabs(["Instagram", "YouTube"])
    
    with tab_ig:
        st.subheader("Instagram")
        
        # Mock audience data since we don't have real demographic data from Zernio yet
        audience_data = [
            {"age": "18-24", "count": 1500},
            {"age": "25-34", "count": 2500},
            {"age": "35-44", "count": 2000},
            {"age": "45-54", "count": 1200},
            {"age": "55+", "count": 800}
        ]
        
        df_audience = pd.DataFrame(audience_data)
        
        # Create 4 bar charts
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Edad")
            fig_age_ig = px.bar(df_audience, x='age', y='count', title="Distribución por Edad")
            st.plotly_chart(fig_age_ig, key="fig_age_ig", use_container_width=True)
            
        with col2:
            st.subheader("Género") 
            # Mock gender data
            gender_data = {"gender": ["Hombre", "Mujer"], "count": [5000, 7500]}
            df_gender = pd.DataFrame(gender_data)
            fig_gender_ig = px.bar(df_gender, x='gender', y='count', title="Distribución por Género")
            st.plotly_chart(fig_gender_ig, key="fig_gender_ig", use_container_width=True)
            
        with col3:
            st.subheader("País")
            # Mock country data
            country_data = {"country": ["EE.UU.", "México", "España"], "count": [4000, 3500, 2500]}
            df_country = pd.DataFrame(country_data)
            fig_country_ig = px.bar(df_country, x='country', y='count', title="Distribución por País")
            st.plotly_chart(fig_country_ig, key="fig_country_ig", use_container_width=True)
            
        with col4:
            st.subheader("Ciudad")
            # Mock city data
            city_data = {"city": ["Madrid", "Barcelona", "México DF"], "count": [2000, 1500, 1000]}
            df_city = pd.DataFrame(city_data)
            fig_city_ig = px.bar(df_city, x='city', y='count', title="Distribución por Ciudad")
            st.plotly_chart(fig_city_ig, key="fig_city_ig", use_container_width=True)
    
    with tab_yt:
        st.subheader("YouTube")
        
        # Mock audience data for YouTube
        audience_yt = [
            {"age": "18-24", "count": 1200},
            {"age": "25-34", "count": 2000},
            {"age": "35-44", "count": 1800},
            {"age": "45-54", "count": 1000},
            {"age": "55+", "count": 600}
        ]
        
        df_audience_yt = pd.DataFrame(audience_yt)
        
        # Create 3 bar charts (no city for YouTube)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Edad")
            fig_age_yt = px.bar(df_audience_yt, x='age', y='count', title="Distribución por Edad")
            st.plotly_chart(fig_age_yt, key="fig_age_yt", use_container_width=True)
            
        with col2:
            st.subheader("Género") 
            # Mock gender data
            gender_data = {"gender": ["Hombre", "Mujer"], "count": [4500, 6000]}
            df_gender = pd.DataFrame(gender_data)
            fig_gender_yt = px.bar(df_gender, x='gender', y='count', title="Distribución por Género")
            st.plotly_chart(fig_gender_yt, key="fig_gender_yt", use_container_width=True)
            
        with col3:
            st.subheader("País")
            # Mock country data
            country_data = {"country": ["EE.UU.", "México", "España"], "count": [3500, 3000, 2000]}
            df_country = pd.DataFrame(country_data)
            fig_country_yt = px.bar(df_country, x='country', y='count', title="Distribución por País")
            st.plotly_chart(fig_country_yt, key="fig_country_yt", use_container_width=True)

# Tab 4 - Posts
with tab4:
    st.subheader("📸 Posts")
    
    # Create 3-column grid for posts
    cols = st.columns(3)
    
    posts = data["posts"]
    if posts:
        for i, post in enumerate(posts):
            with cols[i % 3]:
                # Use thumbnail_url instead of image_url (as we fixed in populate_db.py)
                image_url = post.get("thumbnail_url", "")
                if image_url:
                    st.image(image_url, use_column_width=True)
                else:
                    st.image("https://placehold.co/300x300?text=No+Image", use_column_width=True)
                
                caption = post.get("caption", "Sin título")
                st.write(f"**{caption}**")
                
                # Show engagement metrics
                likes = post.get("likes_count", 0)
                comments = post.get("comments_count", 0)
                st.write(f"👍 {likes} | 💬 {comments}")
                
                # Show comments button
                if st.button("Ver comentarios", key=f"comment_{post['id']}"):
                    with st.expander("Comentarios"):
                        for comment in data["comments"]:
                            # Filter out non-substantive comments
                            if filter_spam_comments(comment["text"]):
                                st.write(f"🗣️ **{comment['author']}**: {comment['text']}")
                            else:
                                # Show filtered comment as a note
                                st.markdown("💬 _Comentario filtrado_")
    else:
        st.info("No hay posts disponibles")

# Tab 5 - Best Time to Post
    with tab5:
        st.subheader("⏰ Mejor Horario para Publicar")
        
        # Get best time data (this was renamed in the loader)
        best_time_data = data.get("best_time_to_post", [])
        if best_time_data:
            df_best_time = pd.DataFrame(best_time_data)
            
            # Convert to heatmap format
            heatmap_data = df_best_time.pivot_table(
                values='value', 
                index='day_of_week', 
                columns='hour', 
                aggfunc='mean'
            )
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Blues',
                text=heatmap_data.values,
                texttemplate="%{text:.0f}"
            ))
            
            fig.update_layout(
                title="Mejor Horario por Día de la Semana",
                xaxis_title="Hora del Día",
                yaxis_title="Día de la Semana"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos de mejor horario disponibles")

# Tab 6 - Posting Frequency
    with tab6:
        st.subheader("📊 Frecuencia de Publicación")
        
        # Scatter plot: posts/week vs avg_engagement
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Posts por Semana vs Engagement Promedio")
            fig_scatter = px.scatter(
                x=[1, 2, 3, 4], 
                y=[85, 75, 90, 65],
                labels={'x': 'Posts por Semana', 'y': 'Engagement Promedio'},
                title="Relación entre Frecuencia y Engagement"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with col2:
            st.subheader("Decaimiento del Contenido")
            # content_decay is not available in current data structure
            st.info("No hay datos de decaimiento disponibles (no implementado)")

# Tab 7 - Ideas
with tab7:
    st.subheader("💡 Sistema de Ideas")
    
    # Platform selector for idea generation
    platform = st.radio("Plataforma:", ["Instagram", "YouTube"], horizontal=True)
    
    # Generate all ideas button
    if st.button(f"Generar todas las ideas de {platform}"):
        with st.spinner(f"Generando ideas para {platform.lower()}..."):
            try:
                if platform == "Instagram":
                    import asyncio
                    from src.components.ideas import generate_all_ideas_ig
                    ideas_list = asyncio.run(generate_all_ideas_ig())
                else:
                    from src.components.ideas import generate_all_ideas_yt
                    ideas_list = generate_all_ideas_yt()
                
                st.success("Ideas generadas con éxito!")
                # Store ideas in session state
                st.session_state['generated_ideas'] = ideas_list
            except Exception as e:
                st.error(f"Error al generar ideas: {str(e)}")
    
    # Display ideas by bucket if they exist
    if 'generated_ideas' in st.session_state:
        ideas_data = st.session_state['generated_ideas']
        
        # Categorize ideas by bucket
        ideas_by_bucket = {}
        for idea in ideas_data:
            bucket = idea.get('bucket', 'comments')
            if bucket not in ideas_by_bucket:
                ideas_by_bucket[bucket] = []
            ideas_by_bucket[bucket].append(idea)
        
        buckets = ["comments", "dms", "top_content"]
        for bucket in buckets:
            if bucket in ideas_by_bucket:
                with st.expander(f"De {bucket} — {len(ideas_by_bucket[bucket])} ideas"):
                    for idea in ideas_by_bucket[bucket]:
                        st.markdown(f"**{idea['angle']}**")
                        st.markdown("> " + "\n> ".join(idea['evidence_quotes']))
                        st.markdown(f"**Por qué es buena idea:** {idea['why_good_idea']}")
                        st.markdown(f"**Ángulo sugerido:** {idea['suggested_angle']}")
                        
                        # Discard button with modal
                        if st.button("✕ Descartar", key=f"discard_{idea['id']}"):
                            # Show discard modal
                            with st.expander("Descartar idea"):
                                reason_quick = st.radio(
                                    "Razón rápida:",
                                    ["Tema cubierto", "No me interesa", "Muy básica", "No es mi estilo", "Otro"]
                                )
                                reason_text = st.text_area("Descripción detallada:")
                                if st.button("Confirmar descarte"):
                                    from src.components.ideas import discard_idea
                                    discard_idea(idea['id'], reason_quick, reason_text)
                                    st.success(f"Idea descartada: {idea['angle']}")
    else:
        st.info("Haz clic en 'Generar todas las ideas' para comenzar.")