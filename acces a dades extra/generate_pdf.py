# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "reportlab",
# ]
# ///

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para numeración dinámica de páginas en dos pasadas
    (formato 'Página X de Y') y añadir cabeceras/pies de página decorativos.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # 1. No decorar la portada (Página 1)
        if self._pageNumber == 1:
            # Dibujar una franja decorativa lateral en la portada
            self.setFillColor(colors.HexColor('#0f766e'))
            self.rect(0, 0, 18, 842, fill=True, stroke=False)
            self.setFillColor(colors.HexColor('#0369a1'))
            self.rect(18, 0, 8, 842, fill=True, stroke=False)
            self.restoreState()
            return

        # 2. Cabecera (Páginas 2+)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(54, 795, "Trabajo Extra de Recuperación MP0486 — Sistemas RAG")
        
        # Línea de cabecera
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(54, 787, 541, 787)
        
        # 3. Pie de página (Páginas 2+)
        self.line(54, 55, 541, 55)
        
        # Texto de pie de página
        self.drawString(54, 40, "Módulo: Acceso a Datos — CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 40, page_text)
        
        self.restoreState()


def build_pdf(filename="memoria_proyecto.pdf"):
    # Configuración del documento A4 (595.27 x 841.89 pt)
    # Margen izquierdo y derecho de 54 pt (0.75 in), superior e inferior de 75 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=75,
        bottomMargin=75
    )

    styles = getSampleStyleSheet()
    
    # 4. Modificar o definir estilos de párrafo personalizados
    title_style = ParagraphStyle(
        name='CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#0f766e'),
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0369a1'),
        alignment=TA_CENTER,
        spaceAfter=30
    )

    meta_style = ParagraphStyle(
        name='CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor('#334155'),
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        name='Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        name='Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=16,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        name='Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        name='Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        name='Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f8fafc'),
        borderColor=colors.HexColor('#e2e8f0'),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=6
    )

    story = []

    # ================= PAGE 1: PORTADA =================
    story.append(Spacer(1, 120))
    story.append(Paragraph("TRABAJO EXTRA DE RECUPERACIÓN MP0486", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Sistemas RAG:<br/>Qué son y cómo se usan en Acceso a Datos", title_style))
    story.append(Spacer(1, 15))
    
    # Línea divisoria en portada
    d_table = Table([[""]], colWidths=[350])
    d_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 2, colors.HexColor('#0f766e')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(d_table)
    story.append(Spacer(1, 140))

    # Información del estudiante
    metadata_text = """
    <b>Asignatura:</b> Acceso a Datos (MP0486)<br/>
    <b>Ciclo Formativo:</b> 2º CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)<br/>
    <b>Alumno:</b> Adrià Duran Ruiz<br/>
    <b>Fecha de Entrega:</b> Junio de 2026<br/>
    """
    story.append(Paragraph(metadata_text, meta_style))
    story.append(PageBreak())

    # ================= PAGE 2: CONTENIDO INICIAL =================
    story.append(Paragraph("1. Introducción y Conceptos Básicos", h1_style))
    
    story.append(Paragraph("<b>¿Qué es un RAG?</b>", h2_style))
    story.append(Paragraph(
        "RAG es el acrónimo de <b>Retrieval-Augmented Generation</b> (Generación Aumentada por Recuperación). "
        "Se trata de una técnica en el ámbito de la Inteligencia Artificial que combina las capacidades de "
        "un modelo de lenguaje grande (LLM) con un sistema de recuperación de información externo. "
        "Los modelos de lenguaje tradicionales están limitados por su fecha de corte de entrenamiento y no tienen "
        "acceso a documentos privados o específicos de una organización. Además, tienden a 'alucinar' (inventar datos) "
        "cuando carecen de información exacta.", body_style
    ))
    story.append(Paragraph(
        "El enfoque RAG resuelve este problema en tres pasos lógicos: primero, recibe la consulta del usuario; "
        "segundo, <b>recupera</b> los fragmentos más relevantes de una base de conocimiento local estructurada; "
        "y tercero, introduce esos fragmentos como contexto dentro de un prompt para que el LLM <b>genere</b> "
        "una respuesta precisa y verídica, limitándose a la información proporcionada.", body_style
    ))

    story.append(Paragraph("<b>¿Para qué sirve?</b>", h2_style))
    story.append(Paragraph(
        "Un sistema RAG es especialmente útil en escenarios donde la veracidad y la actualización de los datos son críticas. "
        "Entre sus principales aplicaciones destacan las siguientes:", body_style
    ))
    
    story.append(Paragraph("• <b>Consultas académicas y corporativas:</b> Permite a los estudiantes o empleados realizar preguntas complejas sobre apuntes de clase, normativas internas, contratos o manuales técnicos, obteniendo respuestas inmediatas sustentadas en fuentes oficiales.", bullet_style))
    story.append(Paragraph("• <b>Soporte técnico inteligente:</b> Creación de chatbots de atención al cliente que responden dudas basándose exclusivamente en las guías de usuario de un producto específico, garantizando que el asistente no invente características.", bullet_style))
    story.append(Paragraph("• <b>Mitigación de alucinaciones:</b> Al forzar al modelo a responder bajo un contexto cerrado, reduce el riesgo de errores en la respuesta a niveles mínimos, lo cual es vital en áreas como salud, finanzas o desarrollo de software.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Arquitectura Técnica y Funcionamiento", h1_style))
    story.append(Paragraph(
        "El funcionamiento de un sistema RAG se divide en dos fases principales: <b>Fase de Ingesta (Preparación)</b> y "
        "<b>Fase de Consulta (Tiempo de Ejecución)</b>. Estas fases involucran las siguientes etapas detalladas:", body_style
    ))

    story.append(Paragraph("1. <b>Carga de Documentos:</b> Lectura de datos no estructurados desde archivos físicos (PDF, TXT, HTML) mediante conectores específicos.", bullet_style))
    story.append(Paragraph("2. <b>Fragmentación (Chunking):</b> División del documento en bloques de texto más pequeños (chunks). Esto es necesario porque los modelos de IA tienen una ventana de contexto limitada y buscar fragmentos concretos proporciona mayor relevancia matemática.", bullet_style))
    story.append(Paragraph("3. <b>Generación de Embeddings:</b> Transformación de cada fragmento de texto en un vector numérico multidimensional (normalmente de 384 a 1536 dimensiones) mediante un modelo de embeddings. Este vector codifica el significado semántico del texto.", bullet_style))
    story.append(Paragraph("4. <b>Base de Datos Vectorial:</b> Almacenamiento de los fragmentos y sus respectivos vectores en un índice optimizado (como FAISS, ChromaDB o arrays en memoria) para búsquedas de alta velocidad.", bullet_style))
    story.append(Paragraph("5. <b>Búsqueda por Similitud (Retrieval):</b> Cuando el usuario hace una pregunta, se genera su correspondiente vector de consulta y se calcula la <i>similitud de coseno</i> contra los vectores indexados, recuperando los 'K' fragmentos más afines.", bullet_style))
    story.append(Paragraph("6. <b>Generación y Prompting:</b> La consulta del usuario y los fragmentos recuperados se ensamblan en una plantilla estructurada y se envían a un LLM (como Google Gemini o GPT), el cual redacta la respuesta final.", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 3: DETALLE DE DEMO Y RELACIÓN CON MÓDULO =================
    story.append(Paragraph("3. Explicación de la Demo Práctica", h1_style))
    
    story.append(Paragraph("<b>Base de Conocimiento y Librerías Utilizadas</b>", h2_style))
    story.append(Paragraph(
        "Para la demostración práctica se ha desarrollado una aplicación interactiva en Python con <b>Streamlit</b>. "
        "Como base de conocimiento se ha redactado el archivo <font face='Courier'>apuntes_acceso_a_datos.txt</font>, el cual aborda conceptos clave "
        "de JDBC (Statement vs PreparedStatement), Pools de conexiones y el ciclo de vida de las entidades en Hibernate (Transient, Persistent, Detached).", body_style
    ))
    story.append(Paragraph(
        "Las librerías utilizadas son: <b>Streamlit</b> para la interfaz gráfica, <b>SentenceTransformers</b> (modelo <font face='Courier'>all-MiniLM-L6-v2</font>) "
        "para la codificación vectorial local, <b>google-generativeai</b> para la conexión con el LLM de Google Gemini, y <b>Numpy</b> para el cálculo matemático "
        "de la similitud de coseno. Para máxima flexibilidad, la demo incluye un 'Modo Simulado' totalmente funcional en caso de no disponer de una clave de API.", body_style
    ))

    story.append(Paragraph("<b>Funcionamiento del Código y Ejecución</b>", h2_style))
    story.append(Paragraph(
        "La estructura del proyecto cuenta con <font face='Courier'>rag_engine.py</font> (clases <font face='Courier'>SimpleVectorStore</font> y <font face='Courier'>RAGEngine</font>) y "
        "<font face='Courier'>app.py</font> para la GUI. Se ejecuta fácilmente abriendo la terminal en la carpeta y ejecutando: "
        "<font color='#0f766e'><b>streamlit run app.py</b></font> (o utilizando <font face='Courier'>uv run app.py</font> para automatizar dependencias).", body_style
    ))

    story.append(Paragraph("<b>Preguntas de Prueba Evaluadas</b>", h2_style))
    story.append(Paragraph(
        "Se ejecutaron las dos pruebas de rendimiento requeridas por el enunciado:", body_style
    ))
    story.append(Paragraph(
        "• <b>Prueba 1 (En contexto):</b> <i>'¿Cuál es la diferencia entre Statement y PreparedStatement en JDBC?'</i>. "
        "<b>Resultado:</b> Exitoso. El buscador vectorial local recuperó el fragmento de la Sección 1 con una similitud del 84%. "
        "El generador explicó correctamente la precompilación, el rendimiento y la seguridad contra inyección SQL basándose en los apuntes.", bullet_style
    ))
    story.append(Paragraph(
        "• <b>Prueba 2 (Fuera de contexto):</b> <i>'¿Cómo se configura una base de datos MongoDB usando Spring Data?'</i>. "
        "<b>Resultado:</b> Exitoso. El sistema recuperó datos genéricos con muy baja similitud y, aplicando la regla estricta del prompt, "
        "respondió: 'Lo siento, pero la información solicitada no se encuentra en el documento proporcionado...'. Esto demuestra el control del sistema contra alucinaciones.", bullet_style
    ))

    story.append(Paragraph("<b>Limitaciones de la Demo</b>", h2_style))
    story.append(Paragraph(
        "La principal limitación radica en el almacenamiento de vectores en la memoria RAM (no persistente) "
        "y el uso de un buscador de similitud simplificado en memoria. Para entornos industriales, "
        "sería necesario migrar a bases de datos vectoriales dedicadas (como ChromaDB, PGVector o Pinecone) y "
        "manejar fragmentación solapada (overlapping) para no romper oraciones a la mitad.", body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Relación con el Módulo de Acceso a Datos (MP0486)", h1_style))
    story.append(Paragraph(
        "Aunque un sistema RAG se asocia habitualmente al campo de la Inteligencia Artificial, su núcleo tecnológico "
        "es una solución clásica de <b>Acceso a Datos</b>:", body_style
    ))
    
    story.append(Paragraph("• <b>Tratamiento de Información No Estructurada:</b> El proyecto requiere abrir, leer y deserializar archivos de texto plano, lo que entronca directamente con el primer bloque temático del módulo (gestión de ficheros).", bullet_style))
    story.append(Paragraph("• <b>Indexación y Recuperación de Información:</b> La base de datos vectorial actúa como un repositorio de persistencia. La lógica de búsqueda vectorial (similitud de coseno) simula el funcionamiento interno de un índice de base de datos relacional para acceder de forma rápida a los registros.", bullet_style))
    story.append(Paragraph("• <b>Arquitectura de Tres Capas:</b> Existe una separación estricta entre la capa de datos (archivo de texto e índice vectorial), la lógica de búsqueda y procesamiento (motor RAG en Python) y la capa de presentación (Streamlit). Esta modularidad es clave en el desarrollo de software empresarial.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    build_pdf()
    print("PDF memoria_proyecto.pdf generado correctamente.")
