import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from github import Github
import io

# --- ESTÉTICA ORBE (RESTAURADA) ---
st.set_page_config(page_title="Orbe", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300&display=swap');
    
    .stApp { background-color: #050505; color: #E0E0E0; font-family: 'Cormorant Garamond', serif; }
    
    /* Título con espaciado original */
    .titulo-orbe {
        text-align: center; 
        font-family: serif; 
        letter-spacing: 15px; 
        font-size: 3rem; 
        color: #fdfdfd;
        margin-bottom: 40px;
        font-weight: 200;
    }
    
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 85px; height: 85px; font-size: 30px;
        display: block; margin: auto; transition: all 0.4s ease;
    }
    .stButton>button:active { border-color: #70f3ff; transform: scale(0.9); }
    .label-orbe { text-align: center; font-size: 11px; opacity: 0.5; letter-spacing: 3px; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE MEMORIA ---
def cargar_universo():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(st.secrets["REPO_NAME"])
        file = repo.get_contents("estrellas.csv")
        return pd.read_csv(io.StringIO(file.decoded_content.decode()))
    except:
        return pd.DataFrame(columns=['x', 'y', 'cat', 'color', 'simb'])

def guardar_universo(df):
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(st.secrets["REPO_NAME"])
        csv_content = df.to_csv(index=False)
        try:
            file = repo.get_contents("estrellas.csv")
            repo.update_file("estrellas.csv", "Registro Orbe", csv_content, file.sha)
        except:
            repo.create_file("estrellas.csv", "Nacimiento Orbe", csv_content)
    except:
        pass

# Inicializar
if 'cosmos' not in st.session_state:
    st.session_state.cosmos = cargar_universo()

def registrar(cat, color, simb):
    n = len(st.session_state.cosmos)
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 2.8
    
    nueva = pd.DataFrame({
        'x': [radio * np.cos(angulo)],
        'y': [radio * np.sin(angulo)],
        'cat': [cat],
        'color': [color],
        'simb': [simb]
    })
    st.session_state.cosmos = pd.concat([st.session_state.cosmos, nueva], ignore_index=True)
    guardar_universo(st.session_state.cosmos)

# --- INTERFAZ ---
st.markdown("<h1 class='titulo-orbe'>O R B E</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5", "hexagram")
    st.markdown("<p class='label-orbe'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37", "diamond-tall")
    st.markdown("<p class='label-orbe'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("✨"): registrar("Ritual", "#9f7aea", "star-entrance")
    st.markdown("<p class='label-orbe'>RITUAL</p>", unsafe_allow_html=True)

# --- VISUALIZACIÓN ---
df = st.session_state.cosmos

if not df.empty:
    fig = go.Figure()
    
    # Filamentos
    if len(df) > 1:
        fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='lines', 
                                 line=dict(color='rgba(255,255,255,0.08)', width=1, shape='spline')))
    
    # Estrellas
    fig.add_trace(go.Scatter(
        x=df['x'], y=df['y'], mode='markers',
        marker=dict(
            size=24, 
            color=df['color'], 
            symbol=df['simb'], 
            line=dict(width=1, color='rgba(255,255,255,0.4)')
        ),
        text=df['cat'], hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
        xaxis=dict(visible=False, range=[-22, 22]),
        yaxis=dict(visible=False, range=[-22, 22]),
        margin=dict(l=0, r=0, t=0, b=0), height=480
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<div style='height: 350px; display: flex; align-items: center; justify-content: center; opacity: 0.2; font-style: italic; letter-spacing: 2px;'>El orbe espera un origen...</div>", unsafe_allow_html=True)
