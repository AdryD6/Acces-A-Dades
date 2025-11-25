import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox  # ttk da un aspecto más moderno a los botones y entradas

class ConversorBCE:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor Divisas - Datos BCE")
        self.root.geometry("450x400")
        
        # Diccionario para guardar las monedas (Ej: 'USD': 1.08)
        self.tasas = {} 
        self.fecha_datos = "Sin datos"

        # 1. CARGA DE DATOS (Backend)
        # Se ejecuta automáticamente al arrancar
        self.descargar_xml_bce()

        # 2. INTERFAZ GRÁFICA (Frontend)
        self.configurar_diseno()

    def descargar_xml_bce(self):
        """Descarga y procesa el XML del Banco Central Europeo"""
        url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                # Convertimos el texto recibido en una estructura XML navegable
                arbol_xml = ET.fromstring(response.content)
                
                # Namespaces: Son necesarios para encontrar las etiquetas correctas en este XML específico
                ns = {'gesmes': 'http://www.gesmes.org/xml/2002-08-01', 
                      'ecb': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
                
                # Buscamos el nodo que contiene la fecha y las monedas
                nodo_cubo = arbol_xml.find(".//ecb:Cube/ecb:Cube", ns)
                self.fecha_datos = nodo_cubo.attrib['time']
                
                # TRUCO IMPORTANTE: El XML no trae el Euro, así que lo añadimos manualmente
                # para poder convertir DESDE o HACIA Euros.
                self.tasas['EUR'] = 1.0
                
                # Recorremos todas las monedas del XML
                for moneda in nodo_cubo:
                    codigo = moneda.attrib['currency']
                    valor = float(moneda.attrib['rate']) # Convertimos texto a número decimal
                    self.tasas[codigo] = valor
            else:
                messagebox.showerror("Error", "El servidor del BCE no responde.")
                
        except Exception as e:
            messagebox.showerror("Error Crítico", f"Fallo de conexión: {e}")

    def configurar_diseno(self):
        """Configura la ventana con un diseño limpio usando Grid y Frames"""
        
        # --- Cabecera ---
        frame_header = tk.Frame(self.root, bg="#333", height=60)
        frame_header.pack(fill="x")
        
        lbl_titulo = tk.Label(frame_header, text="Conversor Oficial BCE", 
                              fg="white", bg="#333", font=("Helvetica", 14, "bold"))
        lbl_titulo.pack(pady=10)

        # --- Panel Principal (Tarjeta central) ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Fila 1: Cantidad
        ttk.Label(main_frame, text="Cantidad a convertir:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_cantidad = ttk.Entry(main_frame, font=("Arial", 11))
        self.entrada_cantidad.grid(row=0, column=1, sticky="ew", pady=5)
        self.entrada_cantidad.insert(0, "100") # Valor inicial

        # Fila 2: Moneda Origen
        ttk.Label(main_frame, text="Moneda de Origen:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_origen = ttk.Combobox(main_frame, values=sorted(self.tasas.keys()), state="readonly")
        self.combo_origen.grid(row=1, column=1, sticky="ew", pady=5)
        self.combo_origen.set("EUR")

        # Fila 3: Moneda Destino
        ttk.Label(main_frame, text="Moneda de Destino:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_destino = ttk.Combobox(main_frame, values=sorted(self.tasas.keys()), state="readonly")
        self.combo_destino.grid(row=2, column=1, sticky="ew", pady=5)
        self.combo_destino.set("USD")

        # Fila 4: Botón Grande
        btn_convertir = tk.Button(main_frame, text="CALCULAR AHORA", 
                                  bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                                  command=self.realizar_calculo)
        btn_convertir.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")

        # Fila 5: Resultado
        self.lbl_resultado = tk.Label(main_frame, text="0.00", font=("Arial", 20, "bold"), fg="#007bff")
        self.lbl_resultado.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Pie de página (Barra de estado) ---
        barra_estado = tk.Label(self.root, text=f"Última actualización BCE: {self.fecha_datos}", 
                                bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0")
        barra_estado.pack(side=tk.BOTTOM, fill=tk.X)

        # Configuración de peso para que se vea bien al estirar
        main_frame.columnconfigure(1, weight=1)

    def realizar_calculo(self):
        """Lógica matemática de conversión cruzada"""
        try:
            # 1. Obtener datos del usuario
            cantidad = float(self.entrada_cantidad.get())
            moneda_origen = self.combo_origen.get()
            moneda_destino = self.combo_destino.get()

            # 2. Obtener las tasas de cambio base EUR
            tasa_origen = self.tasas[moneda_origen]
            tasa_destino = self.tasas[moneda_destino]

            # 3. FÓRMULA DE CONVERSIÓN CRUZADA
            # Como todas las tasas son 1 EUR = X Moneda:
            # Primero pasamos la moneda origen a Euros (Dividir)
            # Luego pasamos esos Euros a la moneda destino (Multiplicar)
            resultado = (cantidad / tasa_origen) * tasa_destino

            # 4. Mostrar resultado
            self.lbl_resultado.config(text=f"{resultado:.2f} {moneda_destino}")

        except ValueError:
            # Esto salta si el usuario escribe letras en vez de números
            messagebox.showwarning("Error de Entrada", "Por favor, introduce solo números.")

# Arranque de la app
if __name__ == "__main__":
    ventana = tk.Tk()
    app = ConversorBCE(ventana)
    ventana.mainloop()