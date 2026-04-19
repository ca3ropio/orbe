import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- ESTÉTICA ORBE ---
st.set_page_config(page_title="Orbe", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: serif; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 80px; height: 80px; font-size: 26px;
        display: block; margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMORIA TEMPORAL ---
if 'cosmos' not in st.session_state:
    st.session_state.cosmos = pd.DataFrame(columns=['x', 'y', 'cat', 'color'])

def registrar_luz(cat, color):
    n = len(st.session_state.cosmos)
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 3
    
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'cat': [cat],
        'color': [color]
    })
    st.session_state.cosmos = pd.concat([st.session_state.cosmos, nueva], ignore_index=True)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; letter-spacing: 15px;'>O R B E</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar_luz("Físico", "#4fd1c5")
with c2:
    if st.button("💠"): registrar_luz("Intelectual", "#d4af37")
with c3:
    if st.button("✨"): registrar_luz("Ritual", "#9f7aea")

# --- GRÁFICO SEGURO ---
df = st.session_state.cosmos
if not df.empty:
    fig = go.Figure()
    
    # Líneas de conexión sutiles
    if len(df) > 1:
        fig.add_trace(go.Scatter(x=df.x, y=df.y, mode='lines', 
                                 line=dict(color='rgba(255,255,255,0.1)', width=1)))

    # Estrellas (Círculos simples para evitar errores de renderizado en móvil)
    fig.add_trace(go.Scatter(
        x=df.x, y=df.y, mode='markers',
        marker=dict(size=20, color=df.color, line=dict(width=1, color='white')),
        text=df.cat, hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-25, 25]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-25, 25]),
        margin=dict(l=0, r=0, t=0, b=0), height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<p style='text-align:center; opacity:0.3;'><br>El orbe está en silencio.</p>", unsafe_allow_html=True)
