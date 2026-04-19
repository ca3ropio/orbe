import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Orbe", layout="centered")

# Título con la estética de tu proyecto
st.markdown("<h1 style='text-align: center; color: #E0E0E0;'>✨ Orbe: Registro Estelar</h1>", unsafe_allow_html=True)

if 'cosmos_data' not in st.session_state:
    st.session_state.cosmos_data = []

def registrar_estrella(categoria, intensidad):
    nueva_estrella = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "categoria": categoria,
        "intensidad": intensidad
    }
    st.session_state.cosmos_data.append(nueva_estrella)
    st.balloons()
    st.success(f"Una estrella de tipo {categoria} ha nacido.")

# Panel de botones para iPhone
st.write("### Selecciona el origen de tu estrella")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌀\nFísico"):
        registrar_estrella("Físico", "Alta")
with col2:
    if st.button("💠\nIntelectual"):
        registrar_estrella("Intelectual", "Alta")
with col3:
    if st.button("🕸️\nRitual"):
        registrar_estrella("Ritual", "Alta")

st.divider()
st.write(f"🌌 Estrellas en tu orbe: {len(st.session_state.cosmos_data)}")
