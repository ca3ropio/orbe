import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Configuración visual profunda
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 80px; height: 80px; font-size: 26px;
        display: block; margin: auto; transition: all 0.4s ease;
    }
    .stButton>button:active { border-color: #70f3ff; transform: scale(0.9); }
    </style>
    """, unsafe_allow_html=True)

# Inicializar memoria de sesión
if 'cosmos_data' not in st.session_state:
    st.session_state.cosmos_data = []

def registrar(cat, color, simb):
    n = len(st.session_state.cosmos_data)
    # Lógica de Espiral Áurea
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 2.5
    
    st.session_state.cosmos_data.append({
        'x': radio * np.cos(angulo),
        'y': radio * np.sin(angulo),
        'cat': cat,
        'color': color,
        'simb': simb
    })

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 12px; margin-bottom: 40px;'>O R B E</h1>", unsafe_allow_html=True)

# Botones con la estética de tus imágenes
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5", "hexagram")
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37", "diamond-tall")
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("🕸️"): registrar("Ritual", "#9f7aea", "star-entrance")
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>RITUAL</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- REPRESENTACIÓN DEL COSMOS ---
if st.session_state.cosmos_data:
    df = pd.DataFrame(st.session_state.cosmos_data)
    
    fig = go.Figure()

    # Filamentos de conexión (Grabado)
    if len(df) > 1:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.1)', width=0.8, shape='spline'),
            hoverinfo='none'
        ))

    # Luces (Estrellas)
    fig.add_trace(go.Scatter(
        x=df['x'], y=df['y'],
        mode='markers',
        marker=dict(
            size=24,
            color=df['color'],
            symbol=df['simb'],
            line=dict(width=1, color='rgba(255,255,255,0.4)')
        ),
        text=df['cat'],
        hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-25, 25]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-25, 25]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center;'><p style='opacity: 0.4; font-style: italic;'>El orbe está en silencio.<br>Presiona un origen para comenzar.</p></div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 10px; opacity: 0.2; letter-spacing: 3px;'>{len(st.session_state.cosmos_data)} LUCES EN MEMORIA</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 10px; opacity: 0.3;'>{len(st.session_state.cosmos)} LUCES EN MEMORIA</p>", unsafe_allow_html=True)
