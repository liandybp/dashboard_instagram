#!/usr/bin/env python3
"""
Dashboard Instagram - Archivo principal (versión corregida)
"""

# Load environment variables with override
from dotenv import load_dotenv
load_dotenv(override=True)

# Set page config as the FIRST command in the script
import streamlit as st
st.set_page_config(page_title="Dashboard Instagram", layout="wide")

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re
from zoneinfo import ZoneInfo
import os

# Import our custom modules
import refresh
from idea_filters import is_substantive_comment
import ideas

# Define ID stripping patterns
_ID_PATTERN_LONG = re.compile(r"\b(post|comment|message)[\s_-]?id[:\s]*\d+\b", re.IGNORECASE)
_ID_PATTERN_LABELED = re.compile(r"\b(post|comment|message)\s+\d{10,}\b", re.IGNORECASE)
_ID_PATTERN_BARE = re.compile(r"\b\d{12,}\b")

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
            "followers": [12000, 12100, 12200, 12300, 12400]
        },
        "audience_demographics": {
            "age_groups": ["18-24", "25-34", "35-44", "45-54", "55+"],
            "percentages": [35, 25, 20, 15, 5]
        },
        "top_posts": [
            {"id": "post1", "title": "Post 1", "engagement": 1200},
            {"id": "post2", "title": "Post 2", "engagement": 950},
            {"id": "post3", "title": "Post 3", "engagement": 800}
        ],
        "engagement_trends": {
            "days": [1, 7, 14, 21, 30],
            "engagement": [100, 75, 60, 45, 30]
        }
    }

# Header section
st.title("📊 Dashboard Instagram")

# Load data
data = load_account_data()

# Get account snapshot data
account_snapshot = data["account_snapshot"]
health_icon = "🟢" if account_snapshot["account_health"]["status"] == "healthy" else "🔴"

# Create header row with profile info and refresh button
col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
with col1:
    st.image(account_snapshot["profile_image"], width=80)
with col2:
    st.subheader(f"@{account_snapshot['username']}")
    st.metric("Seguidores", account_snapshot["follower_count"])
    st.markdown(f"Estado: {health_icon} {account_snapshot['account_health']['status']}")
with col3:
    if st.button("🔄 Refrescar datos"):
        # Aquí iría la lógica de refresco
        pass
with col4:
    st.empty()  # Espacio vacío para alineación

# Resto del dashboard...
st.write("Dashboard funcionando correctamente")
