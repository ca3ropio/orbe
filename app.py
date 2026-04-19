import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Configuración de página con estilo oscuro
st.set_page_config(page_title="Orbe", layout="centered")

# Inyectar CSS para que se vea como un grabado antiguo
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; }
    .stButton>button { 
        background-color: #1a1a1a; border: 1px solid #444; color: #E0E0E0;
        border-radius: 50%; width: 70px; height: 70px; font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'cosmos_df' not in st.session_state:
    # Creamos un DataFrame inicial para que no esté vacío
    st.session_state.cosmos_df = pd.DataFrame(columns=['x', 'y', 'categoria', 'intensidad', 'fecha'])

def registrar_estrella(cat):
    # Generar posición "orbital" aleatoria
    angulo = np.random.uniform(0, 2*np.pi)
    radio = np.random.uniform(1, 10)
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'categoria': [cat],
        'intensidad': [np.random.choice([10, 20, 30])],
        'fecha': [datetime.now()]
    })
    st.session_state.cosmos_df = pd.concat([st.session_state.cosmos_df, nueva], ignore_index=True)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; font-family: serif;'>O R B E</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌀"): registrar_estrella("Físico")
    st.caption("Físico")
with col2:
    if st.button("💠"): registrar_estrella("Intelectual")
    st.caption("Intelectual")
with col3:
    if st.button("🕸️"): registrar_estrella("Ritual")
    st.caption("Ritual")

# --- VISUALIZACIÓN DEL COSMOS (EL GRABADO) ---
if not st.session_state.cosmos_df.empty:
    fig = go.Figure()

    # Dibujar filamentos (Conexiones)
    if len(st.session_state.cosmos_df) > 1:
        fig.add_trace(go.Scatter(
            x=st.session_state.cosmos_df['x'], y=st.session_state.cosmos_df['y'],
            mode='lines',
            line=dict(color='rgba(200, 200, 200, 0.2)', width=0.5),
            hoverinfo='none'
        ))

    # Dibujar Estrellas (Nodos)
    for cat, color in zip(["Físico", "Intelectual", "Ritual"], ["#70f3ff", "#ffcc33", "#b388ff"]):
        df_cat = st.session_state.cosmos_df[st.session_state.cosmos_df['categoria'] == cat]
        fig.add_trace(go.Scatter(
            x=df_cat['x'], y=df_cat['y'],
            mode='markers',
            marker=dict(
                size=df_cat['intensidad'], 
                color=color,
                symbol='star-diamond',
                line=dict(width=1, color='white')
            ),
            name=cat
        ))

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<p style='text-align: center; opacity: 0.5;'>Constelaciones activas: {len(st.session_state.cosmos_df)}</p>", unsafe_allow_html=True)
