import streamlit as st
import numpy as np
import random
import io
from scipy.io.wavfile import write as write_wav # Importación clave para crear archivos WAV
import os 

# --- Configuración de la página ---
st.set_page_config(page_title="Juego del Sonido", layout="centered")

# --- Estilos Personalizados ---
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

# --- Configuración del Audio ---
SAMPLE_RATE = 44100 # Muestras por segundo
DURACION_SONIDO = 1.0 # Duración en segundos

# --- Clasificación de Sonidos para el Juego ---
CUALIDADES = {
    "ALTURA (Frecuencia)": {
        "GRAVE": (150, 250), # Tono bajo
        "AGUDO": (500, 800)  # Tono alto
    },
    "INTENSIDAD (Amplitud)": {
        "SUAVE": (0.1, 0.3), # Sonido suave
        "FUERTE": (0.6, 0.9) # Sonido fuerte
    }
}

# --- FUNCIÓN DE AUDIO CORREGIDA (SOLUCIÓN AL PortAudioError) ---

def play_sound(frecuencia, amplitud, duracion):
    """
    Genera una onda sinusoidal, la convierte a WAV y la reproduce con st.audio.
    """
    t = np.linspace(0, duracion, int(SAMPLE_RATE * duracion), endpoint=False)
    # Generación de la onda
    onda = amplitud * np.sin(2 * np.pi * frecuencia * t)
    
    # 1. Crear un búfer en memoria (archivo temporal en RAM)
    buffer = io.BytesIO()
    
    # 2. Escribir el audio en el búfer como un archivo WAV de 16-bit
    # Normalizamos (multiplicamos por 32767) y convertimos a int16 para el formato WAV
    escala_16bit = 32767
    audio_data = (onda * escala_16bit).astype(np.int16)
    write_wav(buffer, SAMPLE_RATE, audio_data) 
    
    # 3. Mover el "cursor" al inicio del búfer
    buffer.seek(0)
    
    # 4. Reproducir el audio usando la función de Streamlit
    st.audio(buffer.read(), format='audio/wav')

def generate_new_question():
    """Selecciona una cualidad y un valor (ej: Altura y Agudo) al azar."""
    cualidad_key, cualidad_params = random.choice(list(CUALIDADES.items()))
    valor_key, (min_val, max_val) = random.choice(list(cualidad_params.items()))
    
    # Seleccionamos la variable que se va a modificar
    if cualidad_key == "ALTURA (Frecuencia)":
        # Altura: Frecuencia variable, Amplitud fija (ej: 0.7)
        frecuencia = random.randint(min_val, max_val)
        amplitud = 0.7
    else: # INTENSIDAD (Amplitud)
        # Intensidad: Amplitud variable, Frecuencia fija (ej: 440 Hz)
        frecuencia = 440
        amplitud = random.uniform(min_val, max_val)

    # Guarda la información de la pregunta en el estado de la sesión
    st.session_state.correct_answer = valor_key
    st.session_state.question_type = cualidad_key
    st.session_state.frecuencia = frecuencia
    st.session_state.amplitud = amplitud
    st.session_state.feedback = ""
    
    # Reproduce el sonido
    play_sound(frecuencia, amplitud, DURACION_SONIDO)


# --- LÓGICA DEL JUEGO ---

def check_answer(user_answer):
    """Comprueba la respuesta del usuario."""
    if user_answer == st.session_state.correct_answer:
        st.session_state.feedback = f"¡Correcto! ✅ El sonido era: **{st.session_state.correct_answer}**."
        st.success(st.session_state.feedback)
        st.balloons()
    else:
        st.session_state.feedback = f"¡Incorrecto! ❌ La respuesta correcta era: **{st.session_state.correct_answer}**."
        st.error(st.session_state.feedback)
    
    # Después de responder, preparamos la interfaz para la siguiente pregunta
    st.session_state.game_active = False

# --- Inicialización del estado de la sesión ---
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.feedback = "Pulsa 'Empezar' para escuchar el primer sonido."
    st.session_state.correct_answer = ""
    st.session_state.question_type = ""

# --- Interfaz de Usuario ---
st.title("🎵 Juego de Sonido")
st.subheader("¡Escucha con atención y adivina la cualidad del sonido misterioso!")

if not st.session_state.game_active:
    st.markdown("---")
    if st.button("▶️ Empezar / Siguiente Sonido", use_container_width=True):
        st.session_state.game_active = True
        generate_new_question()
        st.rerun()
    
    st.info(st.session_state.feedback)
    st.markdown("---")

else:
    st.markdown(f"**Cualidad a adivinar:** {st.session_state.question_type}")
    st.markdown("---")
    
    # Opciones de respuesta para la cualidad actual
    opciones = list(CUALIDADES[st.session_state.question_type].keys())
    random.shuffle(opciones)
    
    st.info("👂 **Vuelve a escuchar el sonido** (si es necesario):")
    if st.button("Repetir Sonido", key="repeat_sound"):
        play_sound(st.session_state.frecuencia, st.session_state.amplitud, DURACION_SONIDO)
    
    # Muestra la pregunta y las opciones
    st.subheader("¿Cómo describirías este sonido según su **{}**?".format(st.session_state.question_type.split(' ')[0]))
    
    cols = st.columns(len(opciones))
    for i, opcion in enumerate(opciones):
        with cols[i]:
            if st.button(opcion, key=f"op_{opcion}", use_container_width=True):
                check_answer(opcion)
                st.rerun()