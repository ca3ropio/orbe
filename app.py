import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Configuración visual profunda
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'serif'; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 85px; height: 85px; font-size: 28px;
        display: block; margin: auto; transition: all 0.4s ease;
    }
    .stButton>button:active { border-color: #70f3ff; transform: scale(0.92); }
    </style>
    """, unsafe_allow_html=True)

# Inicializar memoria de sesión
if 'cosmos_data' not in st.session_state:
    st.session_state.cosmos_data = []

# Símbolos orgánicos/concéntricos de grabado
# Usamos una técnica de capas para emular el grabado
def registrar(cat, color_hex):
    n = len(st.session_state.cosmos_data)
    # Lógica de Espiral Áurea
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 2.5
    
    st.session_state.cosmos_data.append({
        'x': radio * np.cos(angulo),
        'y': radio * np.sin(angulo),
        'cat': cat,
        'color': color_hex
    })

st.markdown("<h1 style='text-align: center; font-family: serif; letter-spacing: 15px; margin-bottom: 50px; color: #fdfdfd;'>O R B E</h1>", unsafe_allow_html=True)

# Panel de Botones
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5") # Turquesa
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6; letter-spacing: 1px;'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37") # Dorado
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6; letter-spacing: 1px;'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("🕸️"): registrar("Ritual", "#9f7aea") # Púrpura
    st.markdown("<p style='text-align:center; font-size:10px; opacity:0.6; letter-spacing: 1px;'>RITUAL</p>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- REPRESENTACIÓN DEL COSMOS (ESTÉTICA DE GRABADO ORGANICO) ---
if st.session_state.cosmos_data:
    df = pd.DataFrame(st.session_state.cosmos_data)
    
    fig = go.Figure()

    # Capa 1: Polvo estelar puntillista de fondo (Técnica Stippling)
    bg_points = 50 # Número de puntos
    fig.add_trace(go.Scatter(
        x=np.random.normal(0, 10, bg_points), 
        y=np.random.normal(0, 10, bg_points),
        mode='markers', 
        marker=dict(size=1.2, color='rgba(200,200,200,0.1)'), hoverinfo='none'
    ))

    # Capa 2: Filamentos de conexión orgánicos (Como raíces sutiles)
    if len(df) > 1:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.08)', width=0.8, shape='spline'),
            hoverinfo='none'
        ))

    # Capa 3: Capas de Grabado Concétrico para cada Luz
    # Iteramos sobre cada registro para aplicar capas orgánicas
    for i, row in df.iterrows():
        # A. Aura Puntillista de Grabado (Color sutil)
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']],
            mode='markers',
            marker=dict(
                size=30, 
                color=f"{row['color']}1A", # Añadimos transparencia sutil
                symbol='circle',
                line=dict(width=0, color='rgba(0,0,0,0)')
            ), hoverinfo='none'
        ))
        
        # B. Círculo Concétrico Interior (Puntillista)
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']],
            mode='markers',
            marker=dict(
                size=12, 
                color='rgba(0,0,0,0)', 
                symbol='circle',
                line=dict(width=1, color=row['color'], dash='dot') # Grabado por puntos concéntrico
            ), hoverinfo='none'
        ))

        # C. Punto Central Radiante
        fig.add_trace(go.Scatter(
            x=[row['x']], y=[row['y']],
            mode='markers',
            marker=dict(
                size=6, 
                color=row['color'], # Brillo puro
                symbol='circle',
                line=dict(width=1, color='rgba(255,255,255,0.5)')
            ),
            hoverinfo='text',
            text=f"{row['cat']}<br>{len(df)} Reg."
        ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='black',
        paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-20, 20]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=480
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<div style='height: 350px; display: flex; align-items: center; justify-content: center; text-align: center;'><p style='opacity: 0.35; font-style: italic; letter-spacing: 1px; line-height: 1.5;'>El orbe está en silencio.<br>Presiona un origen para comenzar.<br><br>...<br><br>Diseño de estrellas orgánico activado.</p></div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; font-size: 10px; opacity: 0.15; letter-spacing: 4px; font-weight: bold;'>MEMORIA DE SESIÓN DETECTADA</p>", unsafe_allow_html=True)
