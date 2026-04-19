import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Configuración visual
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 75px; height: 75px; font-size: 24px;
        display: block; margin: auto;
    }
    .stButton>button:active { border-color: #70f3ff; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar memoria temporal
if 'cosmos' not in st.session_state:
    st.session_state.cosmos = []

def registrar(cat, color, simb):
    n = len(st.session_state.cosmos)
    # Lógica de Espiral
    angulo = n * (np.pi * (3 - np.sqrt(5)))
    radio = np.sqrt(n + 1) * 3
    
    nueva_estrella = {
        'x': radio * np.cos(angulo),
        'y': radio * np.sin(angulo),
        'cat': cat,
        'color': color,
        'simb': simb
    }
    st.session_state.cosmos.append(nueva_estrella)

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 10px;'>O R B E</h1>", unsafe_allow_html=True)

# Botones en horizontal para iPhone
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5", "hexagram")
    st.markdown("<p style='text-align:center; font-size:10px;'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37", "diamond-tall")
    st.markdown("<p style='text-align:center; font-size:10px;'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("🕸️"): registrar("Ritual", "#9f7aea", "star-entrance")
    st.markdown("<p style='text-align:center; font-size:10px;'>RITUAL</p>", unsafe_allow_html=True)

# --- VISUALIZACIÓN ---
if len(st.session_state.cosmos) > 0:
    # Convertimos la lista de dicts a DataFrame solo para graficar
    df = pd.DataFrame(st.session_state.cosmos)
    
    fig = go.Figure()

    # Filamentos (Solo si hay más de una estrella)
    if len(df) > 1:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.1)', width=1, shape='spline'),
            hoverinfo='none'
        ))

    # Estrellas Grabadas
    fig.add_trace(go.Scatter(
        x=df['x'], y=df['y'],
        mode='markers',
        marker=dict(
            size=22,
            color=df['color'],
            symbol=df['simb'],
            line=dict(width=1, color='rgba(255,255,255,0.5)')
        ),
        hoverinfo='text',
        text=df['cat']
    ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<br><p style='text-align: center; opacity: 0.5;'>El orbe está en silencio.<br>Presiona un origen para comenzar.</p>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 10px; opacity: 0.3;'>{len(st.session_state.cosmos)} LUCES EN MEMORIA</p>", unsafe_allow_html=True)
