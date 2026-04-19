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
        border-radius: 50%; width: 75px; height: 75px; font-size: 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { border-color: #70f3ff; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar el contenedor de estrellas
if 'cosmos_df' not in st.session_state:
    st.session_state.cosmos_df = pd.DataFrame(columns=['x', 'y', 'categoria', 'tamaño', 'simbolo', 'color'])

def registrar_estrella(cat, color_hex, simb):
    n = len(st.session_state.cosmos_df)
    # Lógica de Espiral Áurea para el posicionamiento
    angulo = n * (np.pi * (3 - np.sqrt(5)))
    radio = np.sqrt(n + 1) * 3
    
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'categoria': [cat],
        'tamaño': [25],
        'simbolo': [simb],
        'color': [color_hex]
    })
    st.session_state.cosmos_df = pd.concat([st.session_state.cosmos_df, nueva], ignore_index=True)

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 8px;'>O R B E</h1>", unsafe_allow_html=True)

# Panel de botones
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

# --- RENDERIZADO DEL COSMOS ---
# Solo intentamos dibujar si el DataFrame NO está vacío
if not st.session_state.cosmos_df.empty:
    fig = go.Figure()

    # Añadir líneas de conexión (filamentos)
    if len(st.session_state.cosmos_df) > 1:
        fig.add_trace(go.Scatter(
            x=st.session_state.cosmos_df['x'], 
            y=st.session_state.cosmos_df['y'],
            mode='lines',
            line=dict(color='rgba(255, 255, 255, 0.15)', width=1, shape='spline'),
            hoverinfo='none'
        ))

    # Añadir las estrellas
    fig.add_trace(go.Scatter(
        x=st.session_state.cosmos_df['x'], 
        y=st.session_state.cosmos_df['y'],
        mode='markers',
        marker=dict(
            size=st.session_state.cosmos_df['tamaño'],
            color=st.session_state.cosmos_df['color'],
            symbol=st.session_state.cosmos_df['simbolo'],
            line=dict(width=1, color='rgba(255,255,255,0.6)')
        ),
        text=st.session_state.cosmos_df['categoria']
    ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=10, r=10, t=10, b=10),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.info("El orbe está esperando su primera luz. Presiona un botón para comenzar.")

st.markdown(f"<p style='text-align: center; opacity: 0.3; font-size: 10px;'>{len(st.session_state.cosmos_df)} REGISTROS EN ESTA SESIÓN</p>", unsafe_allow_html=True)
