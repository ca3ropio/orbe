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
    /* Botones Circulares Alquímicos */
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 80px; height: 80px; font-size: 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { border-color: #70f3ff; box-shadow: 0 0 15px #70f3ff33; }
    </style>
    """, unsafe_allow_html=True)

if 'cosmos_df' not in st.session_state:
    st.session_state.cosmos_df = pd.DataFrame(columns=['x', 'y', 'categoria', 'tamaño', 'fecha', 'simbolo'])

def registrar_estrella(cat, color_hex, simb):
    # Lógica de posición: Espiral áurea sutil
    n = len(st.session_state.cosmos_df)
    angulo = n * (np.pi * (3 - np.sqrt(5))) # Ángulo de oro
    radio = np.sqrt(n + 1) * 2
    
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'categoria': [cat],
        'tamaño': [np.random.randint(12, 25)],
        'fecha': [datetime.now()],
        'simbolo': [simb],
        'color': [color_hex]
    })
    st.session_state.cosmos_df = pd.concat([st.session_state.cosmos_df, nueva], ignore_index=True)

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 10px; color: #f0f0f0;'>O R B E</h1>", unsafe_allow_html=True)

# Panel de Botones con tus iconos
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

# --- LIENZO DE GRABADO ---
if not st.session_state.cosmos_df.empty:
    fig = go.Figure()

    # 1. Polvo estelar de fondo (Puntillismo)
    bg_x = np.random.uniform(-15, 15, 100)
    bg_y = np.random.uniform(-15, 15, 100)
    fig.add_trace(go.Scatter(x=bg_x, y=bg_y, mode='markers', 
                             marker=dict(size=1, color='rgba(255,255,255,0.1)'), hoverinfo='none'))

    # 2. Filamentos (Aristas orgánicas)
    if len(st.session_state.cosmos_df) > 1:
        fig.add_trace(go.Scatter(
            x=st.session_state.cosmos_df['x'], y=st.session_state.cosmos_df['y'],
            mode='lines', line=dict(color='rgba(255, 255, 255, 0.15)', width=0.8, shape='spline'),
            hoverinfo='none'
        ))

    # 3. Estrellas Grabadas
    for cat in st.session_state.cosmos_df['categoria'].unique():
        df_cat = st.session_state.cosmos_df[st.session_state.cosmos_df['categoria'] == cat]
        fig.add_trace(go.Scatter(
            x=df_cat['x'], y=df_cat['y'],
            mode='markers',
            marker=dict(
                size=df_cat['tamaño'],
                color=df_cat['color'],
                symbol=df_cat['simbolo'],
                line=dict(width=1, color='rgba(255,255,255,0.5)')
            ),
            name=cat
        ))

    fig.update_layout(
        showlegend=False, uirevision='constant',
        plot_bgcolor='black', paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-15, 15]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-15, 15]),
        margin=dict(l=0, r=0, t=0, b=0), height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown(f"<p style='text-align: center; font-size: 12px; opacity: 0.4;'>{datetime.now().strftime('%d · %m · %Y')} | {len(st.session_state.cosmos_df)} LUCES REGISTRADAS</p>", unsafe_allow_html=True)
