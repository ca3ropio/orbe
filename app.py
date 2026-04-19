import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from github import Github
import io

# --- ESTÉTICA ---
st.set_page_config(page_title="Orbe", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #E0E0E0; font-family: serif; }
    .stButton>button { 
        background-color: #121212; border: 1px solid #333; color: #E0E0E0;
        border-radius: 50%; width: 80px; height: 80px; font-size: 26px;
        display: block; margin: auto;
    }
    .label { text-align: center; font-size: 10px; opacity: 0.5; letter-spacing: 2px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMORIA ETERNA ---
def gestionar_github():
    try:
        g = Github(st.secrets["GITHUB_TOKEN"])
        return g.get_repo(st.secrets["REPO_NAME"])
    except:
        return None

def cargar_universo():
    repo = gestionar_github()
    if repo:
        try:
            file = repo.get_contents("estrellas.csv")
            return pd.read_csv(io.StringIO(file.decoded_content.decode()))
        except:
            # Si el archivo no existe, devolvemos un DataFrame limpio
            return pd.DataFrame(columns=['x', 'y', 'cat', 'color', 'simb'])
    return pd.DataFrame(columns=['x', 'y', 'cat', 'color', 'simb'])

def guardar_universo(df):
    repo = gestionar_github()
    if repo:
        csv_content = df.to_csv(index=False)
        try:
            file = repo.get_contents("estrellas.csv")
            repo.update_file("estrellas.csv", "Sincronización estelar", csv_content, file.sha)
        except:
            repo.create_file("estrellas.csv", "Nacimiento del Orbe", csv_content)

# Inicializar
if 'cosmos' not in st.session_state:
    st.session_state.cosmos = cargar_universo()

def registrar(cat, color, simb):
    # Lógica de espiral
    n = len(st.session_state.cosmos)
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 3
    
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
st.markdown("<h1 style='text-align: center; letter-spacing: 15px;'>O R B E</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌀"): registrar("Físico", "#4fd1c5", "hexagram")
    st.markdown("<p class='label'>FÍSICO</p>", unsafe_allow_html=True)
with c2:
    if st.button("💠"): registrar("Intelectual", "#d4af37", "diamond-tall")
    st.markdown("<p class='label'>INTELECTUAL</p>", unsafe_allow_html=True)
with c3:
    if st.button("✨"): registrar("Ritual", "#9f7aea", "star-entrance")
    st.markdown("<p class='label'>RITUAL</p>", unsafe_allow_html=True)

# --- VISUALIZACIÓN SEGURA ---
df = st.session_state.cosmos

# Solo intentamos graficar si el DataFrame tiene datos reales y no está vacío
if isinstance(df, pd.DataFrame) and not df.empty and len(df) > 0:
    fig = go.Figure()
    
    # Líneas
    if len(df) > 1:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'], mode='lines',
            line=dict(color='rgba(255,255,255,0.1)', width=1)
        ))
    
    # Estrellas
    fig.add_trace(go.Scatter(
        x=df['x'], y=df['y'], mode='markers',
        marker=dict(
            size=22, 
            color=df['color'].tolist(), 
            symbol=df['simb'].tolist(),
            line=dict(width=1, color='white')
        ),
        text=df['cat'],
        hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
        xaxis=dict(visible=False, range=[-25, 25]),
        yaxis=dict(visible=False, range=[-25, 25]),
        margin=dict(l=0, r=0, t=0, b=0), height=450
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
else:
    st.markdown("<p style='text-align: center; opacity: 0.2; margin-top: 100px;'>El orbe espera tu primera luz...</p>", unsafe_allow_html=True)
