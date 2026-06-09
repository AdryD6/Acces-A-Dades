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

