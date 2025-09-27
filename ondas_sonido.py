import tkinter as tk
from tkinter import ttk, font
import numpy as np
import sounddevice as sd

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- PALETA DE COLORES ---
COLOR_FONDO = "#FFF5F2"
COLOR_FONDO_GRAFICO = "#F5BABB"
COLOR_ACENTO = "#568F87"
COLOR_TEXTO = "#064232"

class AppOndas(tk.Tk):
    def __init__(self):
        super().__init__()
        # --- TÍTULO DE VERIFICACIÓN ---
        self.title("Visualizador de Ondas (VERSIÓN FINAL)")
        self.geometry("800x700")
        self.configure(bg=COLOR_FONDO)

        self.crear_estilo_personalizado()

        marco_controles = ttk.LabelFrame(self, text="Controles de la Onda", style="Custom.TLabelframe")
        marco_controles.pack(side="top", fill="x", padx=10, pady=10)

        self.freq_var = tk.DoubleVar(value=10) # Frecuencia inicial baja
        self.amp_var = tk.DoubleVar(value=0.8)
        self.dur_var = tk.DoubleVar(value=1.0)
        self.timbre_var = tk.BooleanVar()

        ttk.Label(marco_controles, text="Tono (Hz)", style="Custom.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # Rango de frecuencia ajustado para que sea más útil visualmente
        ttk.Scale(marco_controles, from_=1, to=50, orient="horizontal", variable=self.freq_var).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(marco_controles, text="Intensidad (Volumen)", style="Custom.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Scale(marco_controles, from_=0.1, to=1.0, orient="horizontal", variable=self.amp_var).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(marco_controles, text="Duración (s)", style="Custom.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Scale(marco_controles, from_=0.1, to=3.0, orient="horizontal", variable=self.dur_var).grid(row=2, column=1, sticky="ew", padx=5)
        
        ttk.Checkbutton(marco_controles, text="Añadir armónico (Timbre complejo)", variable=self.timbre_var, style="Custom.TCheckbutton").grid(row=3, column=0, columnspan=2, pady=10)

        marco_botones_accion = ttk.Frame(marco_controles, style="Custom.TFrame")
        marco_botones_accion.grid(row=4, column=0, columnspan=2)

        ttk.Button(marco_botones_accion, text="Dibujar Onda", command=self.actualizar_onda_visual, style="Custom.TButton").pack(side="left", padx=10, pady=10)
        ttk.Button(marco_botones_accion, text="▶ Reproducir Sonido", command=self.reproducir_sonido, style="Custom.TButton").pack(side="left", padx=10, pady=10)

        marco_controles.columnconfigure(1, weight=1)

        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor=COLOR_FONDO)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_facecolor(COLOR_FONDO_GRAFICO)

        self.lienzo = FigureCanvasTkAgg(self.fig, master=self)
        self.lienzo.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.actualizar_onda_visual()

    def crear_estilo_personalizado(self):
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure("Custom.TFrame", background=COLOR_FONDO)
        style.configure("Custom.TLabelframe", background=COLOR_FONDO, bordercolor=COLOR_ACENTO)
        style.configure("Custom.TLabelframe.Label", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=('Helvetica', 12, 'bold'))
        style.configure("Custom.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=('Helvetica', 11))
        style.configure("Custom.TButton", background=COLOR_ACENTO, foreground="white", bordercolor=COLOR_TEXTO, font=('Helvetica', 11, 'bold'))
        style.map("Custom.TButton", background=[('active', COLOR_TEXTO)])
        style.configure("Custom.Horizontal.TScale", background=COLOR_FONDO, troughcolor=COLOR_FONDO_GRAFICO)
        style.map('Custom.Horizontal.TScale', background=[('active', COLOR_ACENTO)])
        style.configure("Custom.TCheckbutton", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=('Helvetica', 11))
        style.map("Custom.TCheckbutton", indicatorcolor=[('selected', COLOR_ACENTO)])

    def actualizar_onda_visual(self):
        frecuencia = self.freq_var.get()
        amplitud = self.amp_var.get()
        duracion = self.dur_var.get()
        es_compleja = self.timbre_var.get()

        puntos_visuales = 2000
        tiempo = np.linspace(0, duracion, puntos_visuales)
        
        if es_compleja:
            onda_principal = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)
            armonico = (amplitud / 3) * np.sin(2 * np.pi * (frecuencia * 2) * tiempo)
            onda = onda_principal + armonico
            max_val = np.max(np.abs(onda))
            if max_val > 0: onda = (onda / max_val) * amplitud
        else:
            onda = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)

        self.ax.clear()
        self.ax.plot(tiempo, onda, color=COLOR_ACENTO, linewidth=2)
        titulo = "Onda Compleja" if es_compleja else "Onda Pura"
        self.ax.set_title(titulo, fontsize=14, color=COLOR_TEXTO)
        self.ax.set_xlabel("Tiempo (s)", color=COLOR_TEXTO)
        self.ax.set_ylabel("Amplitud", color=COLOR_TEXTO)
        self.ax.tick_params(colors=COLOR_TEXTO, which='both')
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_xlim(0, duracion)
        self.ax.grid(True, linestyle='--', alpha=0.6, color=COLOR_ACENTO)
        
        for spine in self.ax.spines.values():
            spine.set_edgecolor(COLOR_TEXTO)

        self.lienzo.draw()

    def reproducir_sonido(self):
        frecuencia = self.freq_var.get()
        amplitud = self.amp_var.get()
        duracion = self.dur_var.get()
        es_compleja = self.timbre_var.get()

        sample_rate = 44100
        puntos_audio = int(duracion * sample_rate)
        tiempo = np.linspace(0, duracion, puntos_audio, endpoint=False)
        
        if es_compleja:
            onda_principal = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)
            armonico = (amplitud / 3) * np.sin(2 * np.pi * (frecuencia * 2) * tiempo)
            onda = onda_principal + armonico
            max_val = np.max(np.abs(onda))
            if max_val > 0: onda = (onda / max_val) * amplitud
        else:
            onda = amplitud * np.sin(2 * np.pi * frecuencia * tiempo)
        
        sd.play(onda.astype(np.float32), sample_rate)

if __name__ == "__main__":
    app = AppOndas()
    app.mainloop()