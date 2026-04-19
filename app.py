import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# --- ESTÉTICA Y CONFIGURACIÓN ---
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: serif; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 85px; height: 85px; font-size: 28px;
        display: block; margin: auto; transition: all 0.4s ease;
    }
    .stButton>button:active { border-color: #70f3ff; transform: scale(0.92); }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE MEMORIA (Persistencia sutil) ---
# Por ahora usamos session_state, pero preparo el terreno para GitHub
if 'cosmos_data' not in st.session_state:
    st.session_state.cosmos_data = []

def registrar(cat, color_hex):
    n = len(st.session_state.cosmos_data)
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 2.5
    
    nueva_estrella = {
        'x': radio * np.cos(angulo),
        'y': radio * np.sin(angulo),
        'cat': cat,
        'color': color_hex
    }
    st.session_state.cosmos_data.append(nueva_estrella)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 15px; margin-bottom: 50px;'>O R B E</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5")
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37")
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("✨"): registrar("Ritual", "#9f7aea") # Símbolo cambiado para evitar el error
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6;'>RITUAL</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- EL COSMOS GRABADO ---
if st.session_state.cosmos_data:
    df = pd.DataFrame(st.session_state.cosmos_data)
    fig = go.Figure()

    # Capa de fondo: Polvo estelar
    fig.add_trace(go.Scatter(
        x=np.random.normal(0, 12, 40), y=np.random.normal(0, 12, 40),
        mode='markers', marker=dict(size=1, color='rgba(255,255,255,0.1)'), hoverinfo='none'
    ))

    # Filamentos sutiles
    if len(df) > 1:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'], mode='lines',
            line=dict(color='rgba(255,255,255,0.06)', width=1, shape='spline'),
            hoverinfo='none'
        ))

    # Estrellas con efecto de grabado
    for i, row in df.iterrows():
        # Aura puntillista
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']], mode='markers',
            marker=dict(size=25, color=f"{row['color']}1A", symbol='circle'),
            hoverinfo='none'
        ))
        # Núcleo radiante
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']], mode='markers',
            marker=dict(size=8, color=row['color'], line=dict(width=1, color='white')),
            text=f"Origen: {row['cat']}", hoverinfo='text'
        ))

    fig.update_layout(
        showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        margin=dict(l=0, r=0, t=0, b=0), height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; opacity: 0.3; font-style: italic;'>El orbe espera un origen...</div>", unsafe_allow_html=True)

# --- PIE DE PÁGINA ---
st.markdown(f"<p style='text-align: center; font-size: 10px; opacity: 0.2; letter-spacing: 3px;'>{len(st.session_state.cosmos_data)} LUCES REGISTRADAS</p>", unsafe_allow_html=True)
