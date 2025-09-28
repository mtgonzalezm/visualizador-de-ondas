import streamlit as st
import random
import os

# --- Configuración de la página ---
st.set_page_config(page_title="Juego del Oído", layout="centered")

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

# --- Contenido y respuestas basadas en tu imagen ---
PARTES_OIDO_CON_NUMEROS = {
    1: "Oído externo (Oreja)",
    2: "Tímpano",
    3: "Martillo",
    4: "Cóclea",
    5: "Estribo",
    7: "Conducto auditivo"
}
# Lista de todas las partes para generar opciones aleatorias
TODAS_LAS_PARTES = ["Oído externo (Oreja)", "Conducto auditivo", "Tímpano", "Martillo", "Yunque", "Estribo", "Cóclea"]

# --- Inicialización del estado del juego ---
if 'current_question_num' not in st.session_state:
    st.session_state.current_question_num = None
    st.session_state.feedback = ""

def generate_question():
    """Genera una nueva pregunta eligiendo un número al azar de la imagen."""
    num_parte = random.choice(list(PARTES_OIDO_CON_NUMEROS.keys()))
    st.session_state.current_question_num = num_parte
    st.session_state.feedback = ""
    st.rerun()

def check_answer(user_answer):
    """Comprueba la respuesta del usuario."""
    correct_answer = PARTES_OIDO_CON_NUMEROS[st.session_state.current_question_num]
    if user_answer == correct_answer:
        st.session_state.feedback = "¡Correcto! ✅"
        st.success(st.session_state.feedback)
        st.balloons()
    else:
        st.session_state.feedback = f"¡Incorrecto! ❌ La respuesta correcta para el número {st.session_state.current_question_num} es: **{correct_answer}**."
        st.error(st.session_state.feedback)
    st.session_state.current_question_num = None # Resetea la pregunta

# --- Interfaz del Juego ---
st.title("👂 Juego: Las Partes del Oído")

# *** LÍNEA CORREGIDA PARA EL NOMBRE DE ARCHIVO EN MINÚSCULAS ***
image_path = "partes_oido.jpg"
# ***************************************************************

if not os.path.exists(image_path):
    # Esto ya no debería aparecer en Streamlit Cloud
    st.error(f"Error: La imagen '{image_path}' no se encuentra. Asegúrate de que esté guardada en la misma carpeta que el script.")
else:
    st.image(image_path, caption="Identifica la parte del oído señalada")

st.markdown("---")

if st.session_state.current_question_num is None:
    if st.button("Empezar / Siguiente Pregunta", use_container_width=True):
        generate_question()
else:
    st.subheader(f"¿Qué parte del oído es el número **{st.session_state.current_question_num}**?")
    
    # Prepara las opciones de respuesta (la correcta y 3 incorrectas)
    correct_answer = PARTES_OIDO_CON_NUMEROS[st.session_state.current_question_num]
    opciones = [correct_answer]
    distractores = [p for p in TODAS_LAS_PARTES if p != correct_answer]
    opciones.extend(random.sample(distractores, min(3, len(distractores))))
    random.shuffle(opciones)

    cols = st.columns(2)
    for i, opcion in enumerate(opciones):
        with cols[i % 2]:
            if st.button(opcion, key=f"op_{opcion}", use_container_width=True):
                check_answer(opcion)
    
    # Muestra el feedback si ya se ha respondido
    if st.session_state.feedback:
        st.info(st.session_state.feedback)