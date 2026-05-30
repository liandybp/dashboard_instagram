import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re
from zoneinfo import ZoneInfo
import os

# Load environment variables with override
from dotenv import load_dotenv
load_dotenv(override=True)

# Import our custom modules
import refresh
from idea_filters import is_substantive_comment

# Define ID stripping patterns
_ID_PATTERN_LONG = re.compile(r"\b(post|comment|message)[\s_-]?id[:\s]*\d+\b", re.IGNORECASE)
_ID_PATTERN_LABELED = re.compile(r"\b(post|comment|message)\s+\d{10,}\b", re.IGNORECASE)
_ID_PATTERN_BARE = re.compile(r"\b\d{12,}\b")

def strip_ids(text):
    """Strip numeric IDs that might have been added by Claude"""
    if not isinstance(text, str):
        return text
    text = _ID_PATTERN_LONG.sub("", text)
    text = _ID_PATTERN_LABELED.sub("", text)
    text = _ID_PATTERN_BARE.sub("", text)
    return text.strip()

# Function to get health indicator color
def get_health_color(status):
    if status == "healthy":
        return "🟢"
    elif status == "warning":
        return "🟡"
    else:
        return "🔴"

# Function to load data (mocked for now, will be replaced with actual data loading)
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_account_data():
    """Load account data - this would connect to database in real implementation"""
    # Mock data for demonstration purposes
    return {
        "account_snapshot": {
            "username": "test_user",
            "profile_image": "https://via.placeholder.com/100",
            "follower_count": 12500,
            "account_health": {"status": "healthy"}
        },
        "account_insights_30d": {
            "reach": 45000,
            "views": 22000,
            "engaged": 3800,
            "interactions": 1200,
            "likes": 950,
            "comments": 180,
            "saves": 75,
            "shares": 45
        },
        "daily_metrics": {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "reach": [1000, 1200, 950, 1100, 1300],
            "views": [500, 600, 480, 550, 700],
            "engaged": [200, 250, 180, 220, 300],
            "interactions": [50, 60, 45, 55, 70]
        },
        "follower_history": {
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "followers": [12000, 12100, 12050, 12200, 12300]
        },
        "audience_ig": {
            "age": [25, 35, 45, 55],
            "count": [3000, 4500, 2800, 1200]
        },
        "audience_yt": {
            "age": [25, 35, 45, 55],
            "count": [3000, 4500, 2800, 1200]
        },
        "posts": [
            {"id": 1, "image_url": "https://via.placeholder.com/300", "title": "Post 1"},
            {"id": 2, "image_url": "https://via.placeholder.com/300", "title": "Post 2"},
            {"id": 3, "image_url": "https://via.placeholder.com/300", "title": "Post 3"},
            {"id": 4, "image_url": "https://via.placeholder.com/300", "title": "Post 4"},
            {"id": 5, "image_url": "https://via.placeholder.com/300", "title": "Post 5"},
            {"id": 6, "image_url": "https://via.placeholder.com/300", "title": "Post 6"}
        ],
        "comments": [
            {"id": 1, "text": "¡Excelente contenido!", "author": "user1", "timestamp": "2023-01-01"},
            {"id": 2, "text": "Me encanta este post", "author": "user2", "timestamp": "2023-01-01"},
            {"id": 3, "text": "te amo eres mi ídola", "author": "user3", "timestamp": "2023-01-01"}
        ],
        "best_time": {
            "hour": [9, 10, 11, 12, 13, 14],
            "day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "value": [85, 75, 90, 65, 80, 95]
        },
        "content_decay": {
            "days": [1, 7, 14, 21, 30],
            "engagement": [100, 75, 60, 45, 30]
        }
    }

# Load data
data = load_account_data()

# Header section
st.set_page_config(page_title="Dashboard Instagram", layout="wide")
st.title("📊 Dashboard Instagram")

# Get account snapshot data
account_snapshot = data["account_snapshot"]
health_icon = get_health_color(account_snapshot["account_health"]["status"])

# Create header row with profile info and refresh button
col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
with col1:
    st.image(account_snapshot["profile_image"], width=80)
with col2:
    st.subheader(f"@{account_snapshot['username']}")
    st.metric("Seguidores", account_snapshot["follower_count"])
    st.markdown(f"Estado: {health_icon} {account_snapshot['account_health']['status']}")
with col3:
    # Last updated info
    st.write("Última actualización: 2023-01-05 14:30")
with col4:
    if st.button("🔄 Refrescar datos"):
        refresh.main()

# Global platform selector
platform = st.radio("Plataforma:", ["Instagram", "YouTube", "Ambas"], horizontal=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Resumen", 
    "Tendencia", 
    "Audiencia", 
    "Posts", 
    "Cuándo publicar", 
    "Frecuencia", 
    "Ideas"
])

# Tab 1 - Resumen
with tab1:
    st.subheader("📈 KPIs del Último Mes")
    
    insights = data["account_insights_30d"]
    
    # Create metrics grid
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Reach", insights["reach"])
    with col2:
        st.metric("Views", insights["views"])
    with col3:
        st.metric("Engaged", insights["engaged"])
    with col4:
        st.metric("Interacciones", insights["interactions"])
    with col5:
        st.metric("Likes", insights["likes"])
    
    # Additional metrics
    col6, col7, col8 = st.columns(3)
    with col6:
        st.metric("Comentarios", insights["comments"])
    with col7:
        st.metric("Saves", insights["saves"])
    with col8:
        st.metric("Shares", insights["shares"])

# Tab 2 - Tendencia
with tab2:
    st.subheader("📈 Tendencia de Métricas")
    
    # Metrics selector
    metrics = ["reach", "views", "engaged", "interactions"]
    selected_metrics = st.multiselect("Seleccionar métricas:", metrics, default=metrics)
    
    # Plot line chart
    df_daily = pd.DataFrame(data["daily_metrics"])
    
    fig = go.Figure()
    
    for metric in selected_metrics:
        fig.add_trace(go.Scatter(
            x=df_daily['date'],
            y=df_daily[metric],
            mode='lines+markers',
            name=metric.capitalize(),
            line=dict(width=2)
        ))
    
    # Add follower history
    df_followers = pd.DataFrame(data["follower_history"])
    fig.add_trace(go.Scatter(
        x=df_followers['date'],
        y=df_followers['followers'],
        mode='lines+markers',
        name='Seguidores',
        line=dict(width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Tendencia de Métricas",
        xaxis_title="Fecha",
        yaxis_title="Valor",
        yaxis2=dict(title="Seguidores", overlaying='y', side='right')
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Tab 3 - Audiencia
with tab3:
    st.subheader("👥 Audiencia")
    
    # Create tabs for IG and YT
    tab_ig, tab_yt = st.tabs(["Instagram", "YouTube"])
    
    with tab_ig:
        st.subheader("Instagram")
        
        audience_data = data["audience_ig"]
        df_audience = pd.DataFrame(audience_data)
        
        # Create 4 bar charts
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Edad")
            fig_age = px.bar(df_audience, x='age', y='count', title="Distribución por Edad")
            st.plotly_chart(fig_age, use_container_width=True)
            
        with col2:
            st.subheader("Género") 
            # Mock gender data
            gender_data = {"gender": ["Hombre", "Mujer"], "count": [5000, 7500]}
            df_gender = pd.DataFrame(gender_data)
            fig_gender = px.bar(df_gender, x='gender', y='count', title="Distribución por Género")
            st.plotly_chart(fig_gender, use_container_width=True)
            
        with col3:
            st.subheader("País")
            # Mock country data
            country_data = {"country": ["EE.UU.", "México", "España"], "count": [4000, 3500, 2500]}
            df_country = pd.DataFrame(country_data)
            fig_country = px.bar(df_country, x='country', y='count', title="Distribución por País")
            st.plotly_chart(fig_country, use_container_width=True)
            
        with col4:
            st.subheader("Ciudad")
            # Mock city data
            city_data = {"city": ["Madrid", "Barcelona", "México DF"], "count": [2000, 1500, 1000]}
            df_city = pd.DataFrame(city_data)
            fig_city = px.bar(df_city, x='city', y='count', title="Distribución por Ciudad")
            st.plotly_chart(fig_city, use_container_width=True)
    
    with tab_yt:
        st.subheader("YouTube")
        
        audience_yt = data["audience_yt"]
        df_audience_yt = pd.DataFrame(audience_yt)
        
        # Create 3 bar charts (no city for YouTube)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Edad")
            fig_age = px.bar(df_audience_yt, x='age', y='count', title="Distribución por Edad")
            st.plotly_chart(fig_age, use_container_width=True)
            
        with col2:
            st.subheader("Género") 
            # Mock gender data
            gender_data = {"gender": ["Hombre", "Mujer"], "count": [4500, 6000]}
            df_gender = pd.DataFrame(gender_data)
            fig_gender = px.bar(df_gender, x='gender', y='count', title="Distribución por Género")
            st.plotly_chart(fig_gender, use_container_width=True)
            
        with col3:
            st.subheader("País")
            # Mock country data
            country_data = {"country": ["EE.UU.", "México", "España"], "count": [3500, 3000, 2000]}
            df_country = pd.DataFrame(country_data)
            fig_country = px.bar(df_country, x='country', y='count', title="Distribución por País")
            st.plotly_chart(fig_country, use_container_width=True)

# Tab 4 - Posts
with tab4:
    st.subheader("📸 Posts")
    
    # Create 3-column grid for posts
    cols = st.columns(3)
    
    for i, post in enumerate(data["posts"]):
        with cols[i % 3]:
            st.image(post["image_url"], use_column_width=True)
            st.write(f"**{post['title']}**")
            
            # Show comments button
            if st.button("Ver comentarios", key=f"comment_{post['id']}"):
                with st.expander("Comentarios"):
                    for comment in data["comments"]:
                        # Filter out non-substantive comments
                        if is_substantive_comment(comment["text"]):
                            st.write(f"🗣️ **{comment['author']}**: {strip_ids(comment['text'])}")
                        else:
                            # Show filtered comment as a note
                            st.markdown(f"💬 _Comentario filtrado_")

# Tab 5 - Cuándo publicar
with tab5:
    st.subheader("⏰ Mejor Horario para Publicar")
    
    best_time_data = data["best_time"]
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

# Tab 6 - Frecuencia
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
        content_decay_data = data["content_decay"]
        df_decay = pd.DataFrame(content_decay_data)
        fig_decay = px.bar(df_decay, x='days', y='engagement', title="Engagement por Días desde Publicación")
        st.plotly_chart(fig_decay, use_container_width=True)

# Tab 7 - Ideas
with tab7:
    st.subheader("💡 Sistema de Ideas")
    st.write("Sistema de ideas — Fase 8")
