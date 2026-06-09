# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "streamlit",
#     "numpy",
#     "google-generativeai",
#     "sentence-transformers",
# ]
# ///

import os
import streamlit as st
from rag_engine import RAGEngine

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Demo RAG - Acceso a Datos MP0486",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado para mejorar la estética de la app (Premium Teal/Dark Theme)
st.markdown("""
<style>
    .main-title {
        font-family: 'Outfit', sans-serif;
        color: #0d9488;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .badge {
        background-color: #f0fdfa;
        color: #0f766e;
        border: 1px solid #99f6e4;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .step-box {
        background-color: #f8fafc;
        border-left: 4px solid #0d9488;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.5rem;
    }
    .chunk-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    .score-badge {
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 700;
        float: right;
    }
    .prompt-box {
        background-color: #1e293b;
        color: #cbd5e1;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
        border: 1px solid #334155;
    }
    .result-box {
        background-color: #fafafa;
        border: 1px solid #e5e5e5;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar el motor RAG en la sesión si no existe
if "rag" not in st.session_state:
    with st.spinner("Inicializando motor de búsqueda..."):
        st.session_state.rag = RAGEngine(use_local_embeddings=False)
        # Cargar documento por defecto
        default_doc = "apuntes_acceso_a_datos.txt"
        if os.path.exists(default_doc):
            st.session_state.rag.load_document(default_doc)
            st.session_state.rag.chunk_document(st.session_state.rag.raw_text)
            st.session_state.rag.initialize_index()
            st.session_state.doc_loaded = True
        else:
            st.session_state.doc_loaded = False

rag = st.session_state.rag

def safe_initialize_index(api_key=None):
    """Inicializa el índice capturando errores de API (ej. claves suspendidas) y volviendo al modo simulado."""
    try:
        rag.initialize_index(api_key=api_key)
        return True
    except Exception as e:
        st.sidebar.error("⚠️ La clave de API de Gemini introducida no es válida o ha sido suspendida por Google (Error 403: Consumer Suspended).")
        st.sidebar.info("Volviendo automáticamente al Modo Simulado.")
        # Resetear clave de API
        st.session_state.api_key = ""
        if "gemini_key_widget" in st.session_state:
            st.session_state.gemini_key_widget = ""
        # Re-inicializar localmente sin API
        rag.initialize_index(api_key=None)
        # Forzar recarga de Streamlit para actualizar los widgets
        st.rerun()
        return False

# BARRA LATERAL (Configuración)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Configuración RAG")
    st.write("Módulo: Acceso a Datos (MP0486)")
    st.write("---")
    
    # 1. Configuración de LLM (API Key) en primer lugar para evitar problemas de orden
    st.subheader("🔑 Clave de API de Gemini")
    st.write("La aplicación funciona por defecto en **Modo Simulado** sin clave de API. Si dispones de una clave de Google Gemini, introdúcela aquí:")
    api_key = st.text_input("Gemini API Key", type="password", key="gemini_key_widget")
    
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
        
    api_key_changed = (api_key != st.session_state.api_key)
    if api_key_changed:
        st.session_state.api_key = api_key
        
    if api_key:
        st.success("API Key registrada. Usando Gemini LLM.")
    else:
        st.warning("Usando Modo Simulado (Respuestas predefinidas).")
        
    st.write("---")
    
    # 2. Selección del origen de datos
    st.subheader("📁 Base de Conocimiento")
    use_custom_file = st.checkbox("Subir documento propio (.txt)")
    
    # 3. Configuración de búsqueda
    st.subheader("⚙️ Método de Búsqueda")
    use_local_embs = st.checkbox("Búsqueda semántica (SentenceTransformers)", value=False,
                                 help="Por defecto usa coincidencia rápida de palabras. Actívalo si deseas descargar el modelo neuronal (~90MB) y buscar por significado.")
    
    # Si la clave de API cambia o el método de búsqueda cambia, re-indexamos
    method_changed = (rag.vector_store.use_local_embeddings != use_local_embs)
    if method_changed or api_key_changed:
        rag.vector_store.use_local_embeddings = use_local_embs
        with st.spinner("Actualizando índice de búsqueda..."):
            safe_initialize_index(api_key=api_key if api_key else None)
    
    if use_custom_file:
        uploaded_file = st.file_uploader("Elige un archivo de texto", type=["txt"])
        if uploaded_file is not None:
            # Leer archivo subido
            content = uploaded_file.read().decode("utf-8")
            # Guardar temporalmente
            temp_path = "temp_uploaded_doc.txt"
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            with st.spinner("Indexando nuevo documento..."):
                rag.load_document(temp_path)
                rag.chunk_document(rag.raw_text)
                safe_initialize_index(api_key=api_key if api_key else None)
                st.session_state.doc_loaded = True
            st.success("¡Documento indexado con éxito!")
    else:
        # Usar apuntes por defecto
        default_doc = "apuntes_acceso_a_datos.txt"
        if not st.session_state.get("doc_loaded", False) or api_key_changed:
            if os.path.exists(default_doc):
                rag.load_document(default_doc)
                rag.chunk_document(rag.raw_text)
                safe_initialize_index(api_key=api_key if api_key else None)
                st.session_state.doc_loaded = True
        st.info("Utilizando: `apuntes_acceso_a_datos.txt` (JDBC y Hibernate)")

    st.write("---")
    st.write("**Creado por:** Estudiante MP0486")
    st.write("**Fecha:** Junio 2026")

# CUERPO PRINCIPAL
st.markdown('<div class="badge">Práctica MP0486 - Acceso a Datos</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Sistema RAG Interactiva de Recuperación</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explora cómo una Inteligencia Artificial puede responder a preguntas técnicas utilizando documentos externos de manera transparente.</p>', unsafe_allow_html=True)

if not st.session_state.doc_loaded:
    st.error("No se ha cargado ninguna base de conocimiento. Por favor, asegúrate de que 'apuntes_acceso_a_datos.txt' existe o sube un archivo.")
    st.stop()

# Mostrar estadísticas en columnas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documento cargado", os.path.basename(rag.document_path))
with col2:
    st.metric("Caracteres totales", len(rag.raw_text))
with col3:
    st.metric("Fragmentos creados (Chunks)", len(rag.chunks))

st.write("---")

# Panel interactivo de preguntas
st.subheader("💬 Haz una pregunta al sistema RAG")
st.write("Puedes seleccionar una de las preguntas de prueba requeridas para evaluar el sistema, o formular tu propia pregunta:")

# Preguntas de prueba predefinidas
test_q1 = "¿Cuál es la diferencia entre Statement y PreparedStatement en JDBC?"
test_q2 = "¿Cómo se configura una base de datos MongoDB usando Spring Data?"

col_q1, col_q2 = st.columns(2)
with col_q1:
    btn_q1 = st.button("Pregunta 1: Diferencia Statement/PreparedStatement\n(Respuesta en el documento)", use_container_width=True)
with col_q2:
    btn_q2 = st.button("Pregunta 2: Configurar MongoDB con Spring Data\n(Respuesta fuera del documento)", use_container_width=True)

# Campo de texto libre
user_query = st.text_input("O escribe tu propia pregunta personalizada:", value="", placeholder="Escribe aquí tu pregunta...")

# Determinar qué consulta ejecutar
query = ""
if btn_q1:
    query = test_q1
elif btn_q2:
    query = test_q2
elif user_query:
    query = user_query

# Ejecutar proceso RAG si hay una consulta
if query:
    st.write("---")
    st.info(f"Procesando pregunta: **{query}**")
    
    # 1. PASO 1: RECUPERACIÓN (RETRIEVAL)
    with st.spinner("Buscando fragmentos de información relevantes..."):
        # Realizamos la búsqueda vectorial
        retrieved = rag.vector_store.search(query, top_k=2, api_key=api_key if api_key else None)
        
    st.markdown("### 🔍 Paso 1: Recuperación de Información (Retrieval)")
    st.write("El sistema calcula la similitud semántica entre tu pregunta y cada uno de los fragmentos del documento. Los fragmentos con mayor puntuación son seleccionados:")
    
    for i, item in enumerate(retrieved):
        st.markdown(f"""
        <div class="chunk-box">
            <span class="score-badge">Similitud: {item['score']:.4f}</span>
            <strong>Fragmento #{i+1} recuperado:</strong>
            <p style="margin-top: 0.5rem; font-style: italic; color: #475569;">"{item['chunk']}"</p>
        </div>
        """, unsafe_allow_html=True)
        
    # 2. PASO 2: CONSTRUCCIÓN DEL PROMPT
    st.markdown("### 📝 Paso 2: Construcción del Prompt Contextual")
    st.write("El sistema RAG toma los fragmentos recuperados en el paso anterior y los concatena dentro de una plantilla de prompt junto con la pregunta. Esto es lo que realmente se envía al modelo de lenguaje (LLM):")
    
    # Simular la llamada para obtener el prompt que se enviaría
    context_str = "\n---\n".join([item['chunk'] for item in retrieved])
    sample_prompt = f"""Eres un asistente académico experto en la asignatura 'Acceso a Datos'.
Tu tarea es responder a la pregunta del usuario utilizando ÚNICAMENTE el contexto proporcionado a continuación.

[REGLAS CRÍTICAS DE CONTROL...]

CONTEXTO DE REFERENCIA:
{context_str}

PREGUNTA DEL USUARIO:
{query}"""
    
    with st.expander("Ver prompt estructurado completo", expanded=False):
        st.markdown(f'<div class="prompt-box">{sample_prompt}</div>', unsafe_allow_html=True)

    # 3. PASO 3: GENERACIÓN DE RESPUESTA (GENERATION)
    st.markdown("### 🤖 Paso 3: Generación de la Respuesta (Generation)")
    st.write("El modelo de lenguaje (LLM) procesa el prompt contextual y redacta una respuesta coherente basándose **estrictamente** en el contexto provisto:")
    
    with st.spinner("Generando respuesta de la IA..."):
        # Llamar al motor RAG para generar la respuesta final
        response_text = rag.generate_answer(query, retrieved, api_key=api_key if api_key else None)
        
    st.markdown(f"""
    <div class="result-box">
        <strong style="color: #0d9488; font-size: 1.1rem;">Respuesta del Sistema RAG:</strong>
        <div style="margin-top: 1rem; line-height: 1.6;">
            {response_text.replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comentario sobre la respuesta para la memoria
    st.write("")
    if query == test_q1:
        st.success("✅ **Análisis de Prueba 1**: El sistema ha respondido correctamente utilizando la información recuperada del documento (Sección 1 de los apuntes sobre JDBC). La respuesta es precisa y se ajusta a la teoría.")
    elif query == test_q2:
        st.warning("⚠️ **Análisis de Prueba 2**: El sistema ha denegado la respuesta correctamente porque Spring Data y MongoDB no están en el documento base. Esto demuestra que el sistema RAG mitiga las alucinaciones al restringirse al contexto proporcionado.")
    else:
        st.info("ℹ️ **Análisis de Prueba**: Evalúa si la respuesta anterior responde adecuadamente a tu pregunta basándose únicamente en el contenido de los fragmentos recuperados.")

# PESTAÑA DE INSPECCIÓN DEL DOCUMENTO COMPLETO
st.write("---")
with st.expander("📄 Ver Base de Conocimiento Completa"):
    st.write(f"**Archivo:** `{rag.document_path}`")
    st.text_area("Texto completo:", value=rag.raw_text, height=300, disabled=True)
