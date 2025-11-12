import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- 1. Configuración Inicial ---

# [cite_start]Cargar las variables de entorno (la API Key) [cite: 64-67]
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Verificar si la clave API existe
if not API_KEY:
    # Mostrar un error si no se encuentra la clave y salir
    messagebox.showerror("Error de Configuración", 
                         "No se encontró la API_KEY en el archivo .env.\n"
                         "Por favor, crea un archivo .env y añade: API_KEY=tu_clave_aqui")
    exit()

# Configurar la API de Gemini
try:
    genai.configure(api_key=API_KEY)
    # Configuración del modelo
    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    # Crear el modelo (puedes investigar otros modelos como se sugiere)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                                  generation_config=generation_config)
except Exception as e:
    messagebox.showerror("Error de API", f"No se pudo configurar la API de Gemini: {e}")
    exit()


# --- 2. Cargar Contexto de la Peluquería ---

# Cargar la información de 'servicios.txt' para usarla como contexto
try:
    with open("servicios.txt", "r", encoding="utf-8") as f:
        CONTEXTO_PELUQUERIA = f.read()
except FileNotFoundError:
    messagebox.showerror("Error de Archivo", 
                         "No se encontró el archivo 'servicios.txt'.\n"
                         "Asegúrate de que el archivo esté en la misma carpeta.")
    exit()

# Crear el 'prompt' base que se enviará a la IA
# [cite_start]Esta información se basa en la página 5 del documento [cite: 93-108]
PROMPT_BASE = f"""
Eres un asistente virtual amable y profesional para una peluquería llamada 'Peluquería Brillo Estelar'.
Tu única tarea es responder preguntas de los clientes basándote estrictamente en la siguiente información:

--- INFORMACIÓN DE LA PELUQUERÍA ---
{CONTEXTO_PELUQUERIA}
--- FIN DE LA INFORMACIÓN ---

Reglas para responder:
1.  Responde siempre basándote ÚNICAMENTE en la información proporcionada.
2.  Si te preguntan algo que no está en la información (como "cortes para mujer" o "color de tinte"), 
    debes indicar amablemente que no tienes esa información específica, pero puedes ofrecer la información que sí tienes (como los precios del tinte).
3.  No inventes servicios, precios ni horarios.
4.  Sé breve, amable y directo.

"""

# --- 3. Lógica del Asistente (Conexión GUI y API) ---

def enviar_pregunta():
    """
    Se ejecuta al presionar el botón 'Enviar'.
    Toma la pregunta del usuario, la envía a la API de Gemini y muestra la respuesta.
    """
    pregunta_usuario = entrada_usuario.get()
    if not pregunta_usuario.strip():
        messagebox.showwarning("Entrada Vacía", "Por favor, escribe una pregunta.")
        return

    # Deshabilitar botón y entrada mientras se genera la respuesta
    boton_enviar.config(state=tk.DISABLED)
    entrada_usuario.config(state=tk.DISABLED)
    
    # Mostrar la pregunta del usuario en el chat
    mostrar_mensaje("Tú: " + pregunta_usuario + "\n\n")

    try:
        # Construir el prompt final para la IA
        prompt_completo = PROMPT_BASE + f"PREGUNTA DEL CLIENTE: {pregunta_usuario}\nRESPUESTA DEL ASISTENTE:"

        # Enviar la consulta a la API de Gemini
        convo = model.start_chat(history=[])
        convo.send_message(prompt_completo)
        
        # El objeto 'convo.last' contiene la respuesta
        # Acceder a 'text' extrae la información relevante de la respuesta
        respuesta_ia = convo.last.text

        # Mostrar la respuesta de la IA en el chat
        mostrar_mensaje("Asistente: " + respuesta_ia + "\n\n")

    except Exception as e:
        messagebox.showerror("Error de API", f"Ocurrió un error al contactar a la API: {e}")
    finally:
        # Reactivar botón y entrada
        boton_enviar.config(state=tk.NORMAL)
        entrada_usuario.config(state=tk.NORMAL)
        # Limpiar el cuadro de entrada
        entrada_usuario.delete(0, tk.END)

def mostrar_mensaje(mensaje):
    """Inserta texto en el área de chat y hace scroll hasta el final."""
    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, mensaje)
    area_chat.see(tk.END) # Auto-scroll
    area_chat.config(state=tk.DISABLED)

# --- 4. Creación de la Interfaz Gráfica (Tkinter) ---

# Ventana principal
ventana = tk.Tk()
ventana.title("Asistente de Peluquería IA")
ventana.geometry("500x600")

# Frame principal
frame_principal = tk.Frame(ventana, padx=10, pady=10)
frame_principal.pack(expand=True, fill=tk.BOTH)

# Título
etiqueta_titulo = tk.Label(frame_principal, text="Asistente de Peluquería", font=("Helvetica", 16, "bold"))
etiqueta_titulo.pack(pady=5)

# Subtítulo
etiqueta_subtitulo = tk.Label(frame_principal, text="Escribe tu pregunta abajo y presiona 'Enviar'.", font=("Helvetica", 10))
etiqueta_subtitulo.pack(pady=5)

# [cite_start]Área de chat (Salida de respuestas) [cite: 55]
area_chat = scrolledtext.ScrolledText(frame_principal, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 11))
area_chat.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Frame para la entrada de usuario y el botón
frame_entrada = tk.Frame(frame_principal)
frame_entrada.pack(fill=tk.X, padx=10, pady=5)

# [cite_start]Cuadro de texto (Entrada de preguntas) [cite: 53]
entrada_usuario = tk.Entry(frame_entrada, font=("Helvetica", 11), width=40)
entrada_usuario.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=5)

# [cite_start]Botón de Enviar [cite: 56]
boton_enviar = tk.Button(frame_entrada, text="Enviar", command=enviar_pregunta, font=("Helvetica", 10, "bold"))
boton_enviar.pack(side=tk.RIGHT, padx=5)

# Hacer que el botón "Enter" también envíe la pregunta
ventana.bind('<Return>', lambda event: enviar_pregunta())

# Iniciar el bucle de la aplicación
ventana.mainloop()