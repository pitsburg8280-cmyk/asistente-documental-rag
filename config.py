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
MODEL_TEMPERATURE = 0.7  # Aumentado para más flexibilidad
MODEL_TIMEOUT = 60  # Más tiempo para respuestas

# Configuración de Chunking (Sesión 2)
CHUNK_SIZE = 500  # AUMENTADO: Más contenido por fragmento
CHUNK_OVERLAP = 100  # Aumentado para mejor contexto
CHUNK_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]  # Jerarquía de separación

# Configuración de Embeddings (Sesión 3)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"  # Cambiar a "cuda" si hay GPU disponible

# Configuración de ChromaDB (Sesión 4)
COLLECTION_NAME = "documentos_academicos"
SIMILARITY_THRESHOLD = 0.1  # 🔴 BAJADO RADICALMENTE: Aceptar casi cualquier similitud
TOP_K = 10  # Aumentado para recuperar más contexto

# Configuración de la UI (Sesión 7)
UI_TITLE = "🤖 Asistente Documental Inteligente"
UI_SUBTITLE = "Sistema RAG 100% Local - Responde con el contexto disponible"
MAX_HISTORY = 10  # Mensajes de historial a mantener

# Mensajes del sistema
SYSTEM_MESSAGES = {
    "no_documents": "⚠️ No hay documentos procesados. Por favor, sube PDFs en el panel lateral y procesa los documentos.",
    "processing": "⏳ Procesando documentos... Esto puede tardar unos minutos.",
    "ready": "✅ Sistema listo. Puedes realizar consultas sobre tus documentos.",
    "no_context": "El documento proporcionado tiene información limitada. Te comparto lo que encontré en el contexto disponible.",
}
