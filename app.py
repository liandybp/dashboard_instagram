import streamlit as st

# Header (siempre visible)
st.title("Dashboard Instagram")

# Selector de plataforma
platform = st.radio("Seleccionar plataforma", ("Instagram", "YouTube", "Ambas"))

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Resumen",
    "Tendencia",
    "Audiencia",
    "Posts",
    "Cuándo publicar",
    "Frecuencia",
    "Ideas"
])

with tab1:
    st.write("Tab 1: en construcción")

with tab2:
    st.write("Tab 2: en construcción")

with tab3:
    st.write("Tab 3: en construcción")

with tab4:
    st.write("Tab 4: en construcción")

with tab5:
    st.write("Tab 5: en construcción")

with tab6:
    st.write("Tab 6: en construcción")

with tab7:
    st.write("Tab 7: en construcción")