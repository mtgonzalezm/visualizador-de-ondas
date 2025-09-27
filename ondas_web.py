import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# --- Configuración de la página web ---
st.set_page_config(page_title="Visualizador de Ondas", layout="wide")

# --- PALETA DE COLORES ---
COLOR_FONDO_GRAFICO = "#F5BABB"
COLOR_ACENTO = "#568F87"
COLOR_TEXTO = "#064232"

st.title("🌊 Visualizador de Ondas Sonoras Interactivo")
st.write("Usa los controles de la barra lateral para crear y explorar las cualidades del sonido.")

# --- Barra lateral con los controles ---
with st.sidebar:
    st.header("Parámetros de la Onda")

    frecuencia = st.slider("Tono (Hz)", min_value=1.0, max_value=50.0, value=10.0, step=0.5)
    amplitud = st.slider("Intensidad (Volumen)", min_value=0.1, max_value=1.0, value=0.8)
    duracion = st.slider("Duración (s)", min_value=0.1, max_value=3.0, value=1.0)
    es_compleja = st.checkbox("Añadir armónico (Timbre complejo)")

    # Botón para reproducir el sonido
    if st.button("▶️ Reproducir Sonido"):
        # Generar datos para el audio (alta calidad)
        sample_rate = 44100
        puntos_audio = int(duracion * sample_rate)
        tiempo_audio = np.linspace(0, duracion, puntos_audio, endpoint=False)

        if es_compleja:
            onda_principal = amplitud * np.sin(2 * np.pi * frecuencia * tiempo_audio)
            armonico = (amplitud / 3) * np.sin(2 * np.pi * (frecuencia * 2) * tiempo_audio)
            onda_audio = onda_principal + armonico
            max_val = np.max(np.abs(onda_audio))
            if max_val > 0: onda_audio = (onda_audio / max_val) * amplitud
        else:
            onda_audio = amplitud * np.sin(2 * np.pi * frecuencia * tiempo_audio)

        sd.play(onda_audio.astype(np.float32), sample_rate)

# --- Área principal para el gráfico ---
st.header("Visualización de la Onda")

# Generar datos para el gráfico (baja densidad para que se vea bien)
puntos_visuales = 2000
tiempo_visual = np.linspace(0, duracion, puntos_visuales)

if es_compleja:
    onda_principal_v = amplitud * np.sin(2 * np.pi * frecuencia * tiempo_visual)
    armonico_v = (amplitud / 3) * np.sin(2 * np.pi * (frecuencia * 2) * tiempo_visual)
    onda_visual = onda_principal_v + armonico_v
    max_val_v = np.max(np.abs(onda_visual))
    if max_val_v > 0: onda_visual = (onda_visual / max_val_v) * amplitud
    titulo = "Onda Compleja"
else:
    onda_visual = amplitud * np.sin(2 * np.pi * frecuencia * tiempo_visual)
    titulo = "Onda Pura"

# Dibujar el gráfico
fig, ax = plt.subplots()
fig.patch.set_facecolor('#FFF5F2') # Fondo exterior
ax.set_facecolor(COLOR_FONDO_GRAFICO) # Fondo interior
ax.plot(tiempo_visual, onda_visual, color=COLOR_ACENTO, linewidth=2)

ax.set_title(titulo, fontsize=14, color=COLOR_TEXTO)
ax.set_xlabel("Tiempo (s)", color=COLOR_TEXTO)
ax.set_ylabel("Amplitud", color=COLOR_TEXTO)
ax.tick_params(colors=COLOR_TEXTO, which='both')
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, duracion)
ax.grid(True, linestyle='--', alpha=0.6, color=COLOR_ACENTO)
for spine in ax.spines.values():
    spine.set_edgecolor(COLOR_TEXTO)

st.pyplot(fig)