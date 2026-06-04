"""
Configuración centralizada del Asistente Documental Inteligente.
Todas las constantes y parámetros del sistema se definen aquí.
"""

import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Asegurar que existan los directorios
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# Configuración del Modelo LLM
MODEL_NAME = "llama3.2:3b"  # Alternativa: "phi3:mini"
MODEL_TEMPERATURE = 0.1  # Baja temperatura para respuestas deterministas
MODEL_TIMEOUT = 30  # Segundos de timeout para Ollama

# Configuración de Chunking (Sesión 2)
CHUNK_SIZE = 512  # Tamaño óptimo para contexto del modelo 3B
CHUNK_OVERLAP = 128  # Solapamiento para retención de contexto semántico
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Jerarquía de separación

# Configuración de Embeddings (Sesión 3)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"  # Cambiar a "cuda" si hay GPU disponible

# Configuración de ChromaDB (Sesión 4)
COLLECTION_NAME = "documentos_academicos"
SIMILARITY_THRESHOLD = 0.7  # Umbral mínimo de similitud de coseno
TOP_K = 4  # Número de documentos a recuperar

# Configuración de la UI (Sesión 7)
UI_TITLE = "🤖 Asistente Documental Inteligente"
UI_SUBTITLE = "Sistema RAG 100% Local - Sin alucinaciones garantizado"
MAX_HISTORY = 10  # Mensajes de historial a mantener

# Mensajes del sistema
SYSTEM_MESSAGES = {
    "no_documents": "⚠️ No hay documentos procesados. Por favor, carga PDFs en la carpeta 'data/' y procesa los documentos.",
    "processing": "⏳ Procesando documentos... Esto puede tardar unos minutos.",
    "ready": "✅ Sistema listo. Puedes realizar consultas sobre tus documentos.",
    "no_context": "No tengo información suficiente en los documentos proporcionados para responder esta pregunta. Por favor, verifica si el tema está cubierto en los PDFs cargados.",
}
