import streamlit as st
import numpy as np
import sounddevice as sd
import random
import time

# --- Configuración de la página ---
st.set_page_config(page_title="Juego de Sonido", layout="centered")

# --- Estilos Personalizados (CSS) ---
COLOR_FONDO = "#FFF5F2"
COLOR_TEXTO = "#064232"
COLOR_ACENTO = "#568F87"
COLOR_SECUNDARIO = "#F5BABB"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_FONDO}; }}
    .stApp, .stButton>button, .stMarkdown, .stSubheader, .stTitle {{ color: {COLOR_TEXTO}; }}
    h1, h2, h3 {{ color: {COLOR_TEXTO} !important; }}
    .stButton>button {{
        background-color: {COLOR_ACENTO}; color: white; border: 2px solid {COLOR_TEXTO};
        border-radius: 10px; padding: 10px 24px; font-weight: bold;
    }}
    .stButton>button:hover {{ background-color: {COLOR_TEXTO}; color: white; border-color: {COLOR_ACENTO}; }}
    .stSuccess {{ background-color: #e6fff2; border-left: 5px solid {COLOR_ACENTO}; padding: 1rem; }}
    .stError {{ background-color: #ffe6e6; border-left: 5px solid {COLOR_SECUNDARIO}; padding: 1rem; }}
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO DE VERIFICACIÓN ---
st.title("🎵 Juego de Sonido (VERSIÓN CORREGIDA)")
st.write("¡Escucha con atención y adivina la cualidad del sonido misterioso!")

# --- Inicialización del estado del juego ---
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = ""
    st.session_state.question = ""

def play_sound(frecuencia, amplitud, duracion):
    sample_rate = 44100
    puntos_audio = int(duracion * sample_rate)
    tiempo = np.linspace(0, duracion, puntos_audio, endpoint=False)
    onda = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)
    sd.play(onda.astype(np.float32), sample_rate)
    time.sleep(duracion)

def generate_new_question():
    question_type = random.choice(['tono', 'duracion', 'intensidad'])
    frecuencia, amplitud, duracion = 440, 0.7, 0.8

    if question_type == 'tono':
        st.session_state.question = "¿El sonido es AGUDO o GRAVE?"
        is_high = random.choice([True, False])
        if is_high:
            frecuencia = 880
            st.session_state.correct_answer = "Agudo"
        else:
            frecuencia = 220
            st.session_state.correct_answer = "Grave" # <-- La palabra correcta
    elif question_type == 'duracion':
        st.session_state.question = "¿El sonido es LARGO o CORTO?"
        is_long = random.choice([True, False])
        if is_long:
            duracion = 1.5
            st.session_state.correct_answer = "Largo"
        else:
            duracion = 0.3
            st.session_state.correct_answer = "Corto"
    elif question_type == 'intensidad':
        st.session_state.question = "¿El sonido es FUERTE o DÉBIL?"
        is_loud = random.choice([True, False])
        if is_loud:
            amplitud = 0.9
            st.session_state.correct_answer = "Fuerte"
        else:
            amplitud = 0.2
            st.session_state.correct_answer = "Débil"

    play_sound(frecuencia, amplitud, duracion)

def check_answer(user_answer):
    if user_answer == st.session_state.correct_answer:
        st.success(f"¡Correcto! La respuesta era {st.session_state.correct_answer}.")
        st.balloons()
        st.session_state.question = "" 
    else:
        st.error("¡Incorrecto! Prueba a generar otro sonido.")

if st.button("🔊 Generar Sonido Misterioso"):
    generate_new_question()

if st.session_state.question:
    st.subheader(st.session_state.question)
    options = st.session_state.question.split("¿El sonido es ")[1].split(" o ")
    option1 = options[0].replace("?", "").strip().capitalize()
    option2 = options[1].replace("?", "").strip().capitalize()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(option1, use_container_width=True):
            check_answer(option1)
    with col2:
        if st.button(option2, use_container_width=True):
            check_answer(option2)