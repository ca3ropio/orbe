import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from github import Github

# --- ESTÉTICA ---
st.set_page_config(page_title="Orbe", layout="centered")
st.markdown("<style>.stApp { background-color: #050505; color: #E0E0E0; }</style>", unsafe_allow_html=True)

# --- CONEXIÓN DE MEMORIA ---
def conectar_github():
    g = Github(st.secrets["GITHUB_TOKEN"])
    return g.get_repo(st.secrets["REPO_NAME"])

def cargar_universo():
    try:
        repo = conectar_github()
        file = repo.get_contents("estrellas.csv")
        return pd.read_csv(file.download_url)
    except:
        return pd.DataFrame(columns=['x', 'y', 'cat', 'color', 'simb'])

def guardar_estrella(df):
    repo = conectar_github()
    csv_content = df.to_csv(index=False)
    try:
        file = repo.get_contents("estrellas.csv")
        repo.update_file("estrellas.csv", "Registro estelar", csv_content, file.sha)
    except:
        repo.create_file("estrellas.csv", "Nacimiento del orbe", csv_content)

# Inicializar
if 'cosmos' not in st.session_state:
    st.session_state.cosmos = cargar_universo()

def registrar(cat, color, simb):
    n = len(st.session_state.cosmos)
    phi = (1 + np.sqrt(5)) / 2
    angulo = n * (2 * np.pi / (phi**2))
    radio = np.sqrt(n + 1) * 2.5
    
    nueva = pd.DataFrame({'x':[radio*np.cos(angulo)], 'y':[radio*np.sin(angulo)], 
                          'cat':[cat], 'color':[color], 'simb':[simb]})
    
    st.session_state.cosmos = pd.concat([st.session_state.cosmos, nueva], ignore_index=True)
    guardar_estrella(st.session_state.cosmos)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; letter-spacing: 15px;'>O R B E</h1>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.button("🌀", on_click=registrar, args=("Físico", "#4fd1c5", "hexagram"))
with c2: st.button("💠", on_click=registrar, args=("Intelectual", "#d4af37", "diamond-tall"))
with c3: st.button("✨", on_click=registrar, args=("Ritual", "#9f7aea", "star-entrance"))

# Dibujar el Orbe
if not st.session_state.cosmos.empty:
    df = st.session_state.cosmos
    fig = go.Figure()
    if len(df) > 1:
        fig.add_trace(go.Scatter(x=df.x, y=df.y, mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=1)))
    fig.add_trace(go.Scatter(x=df.x, y=df.y, mode='markers', 
                             marker=dict(size=22, color=df.color, symbol=df.simb, line=dict(width=1, color='white'))))
    fig.update_layout(showlegend=False, plot_bgcolor='black', paper_bgcolor='black',
                      xaxis=dict(visible=False), yaxis=dict(visible=False), margin=dict(l=0,r=0,t=0,b=0), height=450)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
