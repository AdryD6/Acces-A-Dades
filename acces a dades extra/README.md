# Práctica RAG - Acceso a Datos (MP0486)

Este proyecto consiste en una **demostración interactiva de un sistema RAG (Retrieval-Augmented Generation)** y la generación automatizada de su memoria técnica. Está especialmente diseñado para el módulo de **Acceso a Datos** del ciclo superior de **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

El objetivo principal es ilustrar cómo una Inteligencia Artificial puede responder a preguntas específicas sobre un documento de base de conocimiento (apuntes sobre JDBC, Connection Pools e Hibernate) sin incurrir en alucinaciones, recuperando información de forma estructurada antes de generar la respuesta.

---

## 📂 Estructura del Proyecto

*   `app.py`: La interfaz gráfica interactiva del proyecto construida con **Streamlit**.
*   `rag_engine.py`: El núcleo del sistema RAG. Contiene la lógica de carga, fragmentación (chunking), cálculo de similitud vectorial y llamada al LLM (Gemini) con soporte para un modo simulado sin API Keys.
*   `generate_pdf.py`: Script automatizado con **ReportLab** para compilar y generar la memoria de la práctica en formato PDF (`memoria_proyecto.pdf`).
*   `apuntes_acceso_a_datos.txt`: El documento propio utilizado como base de conocimiento de la demo.
*   `requirements.txt`: Archivo con las dependencias necesarias.
*   `README.md`: Este archivo explicativo.

---

## 🛠️ Instalación y Requisitos

El proyecto está preparado para ejecutarse de forma ágil utilizando **Python 3.10+**.

### Opción Rápida con `uv` (Recomendada)
Si dispones de `uv` (el gestor ultra-rápido de Python), puedes ejecutar la aplicación directamente sin instalar dependencias globales:
```bash
# Ejecutar la demo interactiva en Streamlit
uv run app.py

# Generar la memoria del proyecto en PDF
uv run generate_pdf.py
```

### Opción Estándar con `pip`
Si prefieres usar el instalador clásico de Python:
```bash
# 1. Instalar las dependencias
pip install -r requirements.txt

# 2. Ejecutar la demo de Streamlit
streamlit run app.py

# 3. Generar la memoria en PDF
python generate_pdf.py
```

---

## 🤖 ¿Cómo utilizar la Demo?

1.  Ejecuta la aplicación de Streamlit (`app.py`).
2.  Se abrirá automáticamente una ventana en tu navegador web (normalmente en `http://localhost:8501`).
3.  **Configurar la API Key (Opcional):** En la barra lateral izquierda, puedes introducir tu clave de API de Google Gemini si deseas obtener respuestas de IA real. Si no la tienes, no te preocupes; la app utiliza un **Modo Simulado** robusto que recrea las respuestas del RAG en base al contexto exacto.
4.  **Preguntas de Prueba:** Haz clic en cualquiera de los dos botones de pregunta predefinidos en la parte central:
    *   **Pregunta 1 (En el documento):** *¿Cuál es la diferencia entre Statement y PreparedStatement en JDBC?*
        *   *Comportamiento:* El sistema recuperará el fragmento correspondiente a la sección 1 del documento y el LLM generará una respuesta muy precisa y detallada.
    *   **Pregunta 2 (Fuera del documento):** *¿Cómo se configura una base de datos MongoDB usando Spring Data?*
        *   *Comportamiento:* El sistema detectará que la información sobre MongoDB no existe en nuestros apuntes (que son de bases de datos relacionales en Java), e indicará amigablemente que no puede responder basándose exclusivamente en el contexto. Esto demuestra la robustez del RAG para evitar alucinaciones.

---

## 📹 Guía y Guion para Grabar tu Vídeo (3-6 minutos)

El trabajo requiere un vídeo explicativo corto. Aquí tienes una estructura idónea de **4 minutos** para tu explicación mientras grabas tu pantalla:

### Minuto 0:00 - 1:00 | Introducción Teórica
*   **Qué decir:** "¡Hola! En este vídeo voy a explicar mi trabajo práctico sobre sistemas RAG para el módulo de Acceso a Datos. RAG significa *Retrieval-Augmented Generation*. Básicamente, consiste en proporcionarle a un modelo de Inteligencia Artificial información externa y fiable contenida en documentos locales para que responda a nuestras preguntas basándose únicamente en ella, evitando que invente cosas o cometa alucinaciones."
*   **Qué mostrar:** La pantalla de inicio de la aplicación de Streamlit y el archivo `apuntes_acceso_a_datos.txt` abierto en el editor.

### Minuto 1:00 - 2:00 | Estructura del Proyecto
*   **Qué decir:** "El proyecto consta de tres partes lógicas: 1) Los datos: representados por este archivo de apuntes técnicos sobre JDBC, Pools de conexiones e Hibernate. 2) La lógica de recuperación y acceso a datos: implementada en `rag_engine.py`, que lee el archivo, lo divide en fragmentos y calcula qué fragmentos se parecen más a la pregunta del usuario mediante similitud de coseno. Y 3) La interfaz de usuario en `app.py` hecha con Streamlit."
*   **Qué mostrar:** Abre brevemente el código en el editor (`rag_engine.py` y `app.py`) destacando las funciones clave (como la segmentación o la búsqueda de similitud coseno).

### Minuto 2:00 - 3:30 | Demostración en Vivo
*   **Qué decir:** "Vamos a probar la aplicación en directo. En primer lugar, haré la Pregunta de Prueba 1: *¿Cuál es la diferencia entre Statement y PreparedStatement?* Como vemos en la pantalla, el sistema realiza el paso 1 de Recuperación y encuentra los fragmentos semánticos adecuados de nuestros apuntes con puntuaciones de similitud altas. Después, en el paso 2, monta el Prompt Contextual enviando esos fragmentos al modelo. Y finalmente, en el paso 3, genera una respuesta impecable detallando la precompilación, el rendimiento y la seguridad contra inyección SQL. Todo extraído de nuestros apuntes."
*   **Qué mostrar:** Haz clic en el botón de la Pregunta 1 en Streamlit. Despliega los expanders de "Paso 1", "Paso 2" y muestra el resultado final.
*   **Qué decir:** "Ahora probaremos la Pregunta de Prueba 2 sobre cómo configurar MongoDB con Spring Data. Dado que nuestros apuntes tratan de JDBC y Hibernate relacional, y MongoDB es no-relacional y no figura en la base de conocimiento, vemos cómo el sistema recupera fragmentos irrelevantes y el modelo deniega la respuesta con seguridad, en lugar de inventarse información sobre MongoDB. Esto valida el control de alucinaciones."
*   **Qué mostrar:** Haz clic en el botón de la Pregunta 2 en Streamlit y muestra la respuesta de denegación.

### Minuto 3:30 - 4:00 | Relación con el Módulo y Despedida
*   **Qué decir:** "Como conclusión, considero que esta práctica encaja perfectamente en el módulo de Acceso a Datos. Para que el RAG funcione, la parte fundamental no es el modelo de IA, sino cómo gestionamos el almacenamiento, lectura e indexación de los ficheros no estructurados, y cómo programamos el algoritmo de recuperación para buscar información semántica en memoria de manera ágil. Muchas gracias por su atención."
*   **Qué mostrar:** Muestra de nuevo la aplicación de Streamlit y despídete a la cámara/micrófono.
