"""
Módulo de Interfaz Web (Sesión 7)
Diseña una UI profesional con Streamlit para usuarios no técnicos.
"""

import logging
import time
from pathlib import Path

import streamlit as st

from config import (
    DATA_DIR, CHROMA_DIR, UI_TITLE, UI_SUBTITLE, 
    MAX_HISTORY, SYSTEM_MESSAGES
)
from src.document_loader import DocumentLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.rag_chain import RAGChain

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Asistente Documental RAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Inicializa las variables de estado de la sesión."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = False
    
    if "processing" not in st.session_state:
        st.session_state.processing = False


def save_uploaded_file(uploaded_file) -> Path:
    """
    Guarda un archivo subido en la carpeta data/.
    
    Args:
        uploaded_file: Objeto UploadedFile de Streamlit
        
    Returns:
        Ruta donde se guardó el archivo
    """
    try:
        file_path = DATA_DIR / uploaded_file.name
        
        # Guardar archivo
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        logger.info(f"✅ Archivo guardado: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"❌ Error al guardar archivo: {str(e)}")
        raise


def process_documents(uploaded_files=None):
    """
    Pipeline completo de procesamiento de documentos.
    Procesa tanto archivos locales como subidos desde la interfaz.
    
    Args:
        uploaded_files: Lista de archivos subidos desde Streamlit (opcional)
    """
    st.session_state.processing = True
    
    try:
        with st.spinner(SYSTEM_MESSAGES["processing"]):
            
            # 1. Guardar archivos subidos (si los hay)
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    save_uploaded_file(uploaded_file)
                st.success(f"📥 {len(uploaded_files)} archivo(s) subido(s) correctamente")
            
            # 2. Cargar documentos (locales + subidos)
            loader = DocumentLoader(DATA_DIR)
            documents = loader.load_all_pdfs()
            
            if not documents:
                st.error("No se encontraron PDFs para procesar")
                return
            
            # 3. Fragmentar
            splitter = TextSplitter()
            splits = splitter.split_documents(documents)
            
            # VERIFICAR QUE HAY CHUNKS
            if not splits:
                st.error("❌ No se pudieron extraer chunks del documento. El PDF puede estar vacío o ser una imagen no legible.")
                return
            
            st.info(f"📄 {len(splits)} chunks generados para indexación")

            
            # 4. Inicializar embeddings
            embedding_manager = EmbeddingManager()
            
            # 5. Crear vector store (sin limpiar primero para evitar errores)
            try:
                vector_store = VectorStore(embedding_manager, persist_directory=CHROMA_DIR)
                vector_store.clear()
            except Exception as e:
                logger.warning(f"⚠️ Saltando limpieza: {e}")
                vector_store = VectorStore(embedding_manager, persist_directory=CHROMA_DIR)
            
            # 6. Indexar
            vector_store.add_documents(splits)
            
            # 7. Inicializar cadena RAG
            rag_chain = RAGChain(vector_store)
            
            # Guardar en estado de sesión
            st.session_state.rag_chain = rag_chain
            st.session_state.documents_processed = True
            
            # Mostrar estadísticas
            stats = loader.get_document_stats()
            st.success(f"✅ Procesados {stats['total_documents']} fragmentos de {len(stats['sources'])} documentos")
            
    except Exception as e:
        st.error(f"❌ Error en procesamiento: {str(e)}")
        logger.error(f"Error en procesamiento: {str(e)}")
    
    finally:
        st.session_state.processing = False


def render_sidebar():
    """Renderiza el panel lateral con controles de configuración y carga de archivos."""
    with st.sidebar:
        st.header("⚙️ Panel de Control")
        
        # ==========================================
        # SECCIÓN DE CARGA DE ARCHIVOS
        # ==========================================
        st.subheader("📁 Cargar Documentos")
        
        # Componente de subida de archivos
        uploaded_files = st.file_uploader(
            "Arrastra o selecciona tus PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Los archivos se guardarán automáticamente en la carpeta data/"
        )
        
        # Mostrar PDFs existentes
        pdf_files = list(DATA_DIR.glob("*.pdf"))
        
        if pdf_files:
            st.write(f"📄 {len(pdf_files)} PDFs en el sistema:")
            for pdf in pdf_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"   • {pdf.name}")
                with col2:
                    if st.button("🗑️", key=f"del_{pdf.name}"):
                        try:
                            pdf.unlink()
                            st.success(f"Eliminado: {pdf.name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al eliminar: {e}")
        else:
            st.info("No hay PDFs procesados. Sube archivos o colócalos en data/")
        
        # Botón de procesamiento
        if uploaded_files:
            if st.button("🔄 Procesar Documentos Subidos", disabled=st.session_state.processing):
                process_documents(uploaded_files)
        else:
            if st.button("🔄 Procesar Documentos Locales", disabled=st.session_state.processing):
                process_documents()
        
        # Estado del sistema
        st.subheader("📊 Estado del Sistema")
        if st.session_state.documents_processed:
            st.success("✅ Sistema listo")
        else:
            st.info("⏳ Esperando procesamiento")
        
        # Información del modelo
        st.subheader("🧠 Modelo")
        st.write("• LLM: llama3.2:3b")
        st.write("• Embeddings: all-MiniLM-L6-v2")
        st.write("• VectorDB: ChromaDB")
        
        # Botón para limpiar historial
        if st.button("🗑️ Limpiar Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Botón para limpiar base de datos
        if st.button("⚠️ Limpiar Base de Datos"):
            try:
                vector_store = VectorStore(EmbeddingManager(), persist_directory=CHROMA_DIR)
                vector_store.clear()
                st.session_state.documents_processed = False
                st.session_state.rag_chain = None
                st.success("Base de datos limpiada")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


def render_chat_interface():
    """Renderiza la interfaz principal de chat."""
    st.title(UI_TITLE)
    st.markdown(f"*{UI_SUBTITLE}*")
    st.markdown("---")
    
    # Mostrar mensaje de estado si no hay documentos procesados
    if not st.session_state.documents_processed:
        st.info(SYSTEM_MESSAGES["no_documents"])
        st.markdown("""
        ### 🚀 Primeros Pasos:
        1. **Sube tus PDFs** desde el panel lateral (arrastra o selecciona archivos)
        2. Haz clic en **'Procesar Documentos Subidos'**
        3. Espera a que el sistema indexe los documentos
        4. Comienza a hacer preguntas sobre tus documentos
        
        💡 También puedes colocar PDFs directamente en la carpeta `data/` y procesarlos desde el panel lateral.
        """)
        return
    
    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Mostrar fuentes si existen
            if "sources" in message and message["sources"]:
                with st.expander("📚 Fuentes utilizadas"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"**{i}. {source['source']}** (Relevancia: {source['score']:.3f})")
                        st.markdown(f"```\n{source['content'][:300]}...\n```")
    
    # Input de usuario
    if prompt := st.chat_input("Escribe tu pregunta sobre los documentos..."):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("🔍 Buscando información..."):
                start_time = time.time()
                
                try:
                    # Verificar que Ollama esté disponible
                    if st.session_state.rag_chain is None:
                        st.error("❌ El sistema no está inicializado. Procesa los documentos primero.")
                        return
                    
                    # Ejecutar consulta RAG
                    result = st.session_state.rag_chain.invoke(prompt)
                    
                    # Calcular tiempo de respuesta
                    elapsed_time = time.time() - start_time
                    
                    # Mostrar respuesta
                    st.markdown(result["answer"])
                    
                    # Mostrar metadata de la respuesta
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"⏱️ {elapsed_time:.2f}s")
                    with col2:
                        status = "✅ Con contexto" if result["retrieval_successful"] else "⚠️ Sin contexto"
                        st.caption(status)
                    with col3:
                        st.caption(f"📄 {len(result['source_documents'])} fuentes")
                    
                    # Guardar respuesta en historial
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result.get("source_documents", []),
                        "retrieval_successful": result["retrieval_successful"],
                        "response_time": elapsed_time
                    })
                    
                    # Limitar historial
                    if len(st.session_state.messages) > MAX_HISTORY * 2:
                        st.session_state.messages = st.session_state.messages[-MAX_HISTORY * 2:]
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


def render_ui():
    """Función principal que renderiza toda la interfaz."""
    initialize_session_state()
    render_sidebar()
    render_chat_interface()


if __name__ == "__main__":
    render_ui()

