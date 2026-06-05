# 🤖 Asistente Documental Inteligente (RAG)

Sistema de Generación Aumentada por Recuperación (RAG) completamente funcional y local. Permite interactuar con documentos PDF privados utilizando Modelos de Lenguaje de Gran Escala (LLMs) de código abierto, garantizando respuestas precisas y libres de alucinaciones.

**Repositorio:** [https://github.com/pitsburg8280-cmyk/asistente-documental-rag](https://github.com/pitsburg8280-cmyk/asistente-documental-rag)

---

## 🎯 Características Principales

| Característica | Descripción |
|----------------|-------------|
| **100% Local** | Sin dependencias de APIs comerciales ni compromiso de privacidad |
| **Procesamiento de PDFs** | Extracción robusta de texto con manejo de metadatos |
| **Embeddings Semánticos** | Codificación vectorial con `all-MiniLM-L6-v2` |
| **Base de Datos Vectorial** | ChromaDB persistente en disco para búsqueda de alta velocidad |
| **Mitigación de Alucinaciones** | Prompts estrictos que restringen respuestas al contexto documental |
| **Interfaz Profesional** | UI interactiva con Streamlit y manejo de historial |
| **Rendimiento Optimizado** | Compatible con hardware de gama media (GPU opcional) |
| **OCR Integrado** | Procesamiento de PDFs escaneados e imágenes con Tesseract |

---

## 🏗️ Arquitectura del Sistema

### Flujo de Datos

| Paso | Componente | Tecnología | Función |
|------|------------|------------|---------|
| 1 | 📄 PDFs Locales | PyPDFLoader / Tesseract OCR | Ingesta de documentos digitales o escaneados |
| 2 | ✂️ Chunking | RecursiveCharacterTextSplitter | Fragmentación semántica con solapamiento |
| 3 | 🧠 Embeddings | all-MiniLM-L6-v2 | Vectorización densa 384-dimensiones |
| 4 | 💾 Vector DB | ChromaDB | Almacenamiento e indexación por similitud de coseno |
| 5 | 🔍 Retriever | Similitud Coseno | Recuperación de top-k documentos relevantes |
| 6 | 🤖 LLM Local | Ollama + llama3.2:3b | Generación de respuestas fundamentadas |
| 7 | 🖥️ UI | Streamlit | Interfaz web interactiva |

**Flujo:** PDFs → Chunks → Embeddings → ChromaDB → Recuperación → LLM → Respuesta

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- [Ollama](https://ollama.com) instalado localmente
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (para PDFs escaneados)
- Git

### 1. Clonar el Repositorio

```bash
git clone https://github.com/pitsburg8280-cmyk/asistente-documental-rag.git
cd asistente-documental-rag


2. Crear Entorno Virtual
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate


3. Instalar Dependencias
pip install -r requirements.txt


4. Descargar Modelo LLM
ollama pull llama3.2:3b


5. Ejecutar la Aplicación
streamlit run main.py

La aplicación estará disponible en  http://localhost:8501


📋 Guía de Uso

Opción 1: Carga Directa desde el Navegador (Recomendada)
1. Abre la aplicación con  streamlit run main.py
2. Arrastra o selecciona tus PDFs en el panel lateral (sección "Cargar Documentos")
3. Haz clic en "Procesar Documentos Subidos"
4. Espera a que el sistema indexe los documentos
5. Comienza a hacer preguntas en la interfaz de chat

Opción 2: Carpeta Local (Avanzada)
1. Coloca tus PDFs en la carpeta  data/  (opcional)
2. Inicia la aplicación con  streamlit run main.py
3. Haz clic en "Procesar Documentos Locales" en el panel lateral
4. Realiza consultas en la interfaz de chat


Gestión de Documentos
 
Visualizar: Lista de PDFs cargados en el panel lateral
 
Eliminar: Botón 🗑️ junto a cada archivo para removerlo
 
Limpiar DB: Botón "Limpiar Base de Datos" para reiniciar el sistema


⚙️ Configuración Avanzada

Edita  config.py  para personalizar:
 
 CHUNK_SIZE : Tamaño de fragmentos (default: 500)
 
 CHUNK_OVERLAP : Solapamiento entre chunks (default: 100)
 
 TOP_K : Documentos a recuperar (default: 10)
 
 MODEL_NAME : Modelo de Ollama (default: llama3.2:3b)


🧪 Pruebas de Estrés
Ejecuta las pruebas de robustez:

python tests/test_stress.py


🛡️ Mitigación de Alucinaciones
El sistema implementa múltiples capas de seguridad:

1. Prompt del Sistema Estricto: "Responde ÚNICAMENTE basándote en el contexto proporcionado..."
2. Instrucción de Negación: "Si la respuesta no está en el contexto, responde: 'No tengo información...'"
3. Verificación de Contexto: El retriever debe encontrar documentos relevantes con similitud > umbral


## 📁 Estructura de Sesiones

## 📁 Estructura de Sesiones

![Estructura de Sesiones](https://mermaid.ink



📝 Licencia
Este proyecto es de uso académico y educativo.
