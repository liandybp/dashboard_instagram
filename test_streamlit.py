#!/usr/bin/env python3
"""
Archivo de prueba para verificar el funcionamiento de Streamlit
"""
# Load environment variables with override
from dotenv import load_dotenv
load_dotenv(override=True)

# Set page config as the FIRST command in the script
import streamlit as st
st.set_page_config(page_title="Test Dashboard", layout="wide")

st.title("Test Dashboard")

# Test data loading
@st.cache_data(ttl=300)
def load_test_data():
    return {"test": "data"}

data = load_test_data()
st.write("Data loaded:", data)
