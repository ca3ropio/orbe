import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Estética Orbe
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 70px; height: 70px; font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar datos
if 'cosmos_df' not in st.session_state:
    st.session_state.cosmos_df = pd.DataFrame(columns=['x', 'y', 'categoria', 'tamaño', 'simbolo', 'color'])

def registrar_estrella(cat, color_hex, simb):
    n = len(st.session_state.cosmos_df)
    # Espiral áurea
    angulo = n * (np.pi * (3 - np.sqrt(5)))
    radio = np.sqrt(n + 1) * 2
    
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'categoria': [cat],
        'tamaño': [20],
        'simbolo': [simb],
        'color': [color_hex]
    })
    st.session_state.cosmos_df = pd.concat([st.session_state.cosmos_df, nueva], ignore_index=True)

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 5px;'>O R B E</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌀"): registrar_estrella("Físico", "#4fd1c5", "hexagram")
    st.caption("FÍSICO")
with col2:
    if st.button("💠"): registrar_estrella("Intelectual", "#d4af37", "diamond-tall")
    st.caption("INTELECTUAL")
with col3:
    if st.button("🕸️"): registrar_estrella("Ritual", "#9f7aea", "star-entrance")
    st.caption("RITUAL")

# --- LIENZO CORREGIDO ---
fig = go.Figure()

# Si hay estrellas, dibujarlas
if not st.session_state.cosmos_df.empty:
    # Líneas de conexión
    if len(st.session_state.cosmos_df) > 1:
        fig.add_trace(go.Scatter(
            x=st.session_state.cosmos_df['x'], y=st.session_state.cosmos_df['y'],
            mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=1)
        ))
    
    # Estrellas
    fig.add_trace(go.Scatter(
        x=st.session_state.cosmos_df['x'], 
        y=st.session_state.cosmos_df['y'],
        mode='markers',
        marker=dict(
            size=st.session_state.cosmos_df['tamaño'],
            color=st.session_state.cosmos_df['color'],
            symbol=st.session_state.cosmos_df['simbolo'],
            line=dict(width=1, color='white')
        )
    ))

fig.update_layout(
    showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    margin=dict(l=0, r=0, t=0, b=0), height=400
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
