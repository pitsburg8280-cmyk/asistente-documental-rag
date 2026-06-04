"""
Módulo de Ingesta de Documentos (Sesión 1)
Extrae texto plano desde archivos PDF manteniendo metadatos estructurados.
"""

import logging
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Cargador robusto de documentos PDF.
    Maneja PDFs multi-columna, tablas y metadatos sin pérdida de información.
    """
    
    def __init__(self, data_dir: Path):
        """
        Inicializa el cargador con el directorio de datos.
        
        Args:
            data_dir: Ruta al directorio que contiene los PDFs
        """
        self.data_dir = Path(data_dir)
        self.documents: List[Document] = []
        
    def load_pdf(self, file_path: Path) -> List[Document]:
        """
        Carga un único archivo PDF con manejo de excepciones.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Lista de documentos LangChain con metadatos
        """
        try:
            logger.info(f"Procesando PDF: {file_path.name}")
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            
            # Enriquecer metadatos con información del archivo
            for doc in docs:
                doc.metadata.update({
                    "source": file_path.name,
                    "file_path": str(file_path),
                    "total_pages": len(docs),
                    "document_type": "pdf"
                })
            
            logger.info(f"✅ PDF '{file_path.name}' procesado: {len(docs)} páginas")
            return docs
            
        except Exception as e:
            logger.error(f"❌ Error al procesar '{file_path.name}': {str(e)}")
            return []
    
    def load_all_pdfs(self) -> List[Document]:
        """
        Carga todos los PDFs del directorio de datos.
        
        Returns:
            Lista consolidada de documentos de todos los PDFs
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"El directorio {self.data_dir} no existe")
        
        pdf_files = list(self.data_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"⚠️ No se encontraron PDFs en {self.data_dir}")
            return []
        
        logger.info(f"📚 Encontrados {len(pdf_files)} archivos PDF")
        
        all_documents = []
        for pdf_file in pdf_files:
            docs = self.load_pdf(pdf_file)
            all_documents.extend(docs)
        
        self.documents = all_documents
        logger.info(f"📊 Total de fragmentos cargados: {len(all_documents)}")
        return all_documents
    
    def get_document_stats(self) -> dict:
        """
        Retorna estadísticas de los documentos cargados.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.documents:
            return {"total_documents": 0, "total_pages": 0, "sources": []}
        
        sources = list(set(doc.metadata.get("source", "unknown") for doc in self.documents))
        total_pages = sum(doc.metadata.get("total_pages", 0) for doc in self.documents)
        
        return {
            "total_documents": len(self.documents),
            "total_pages": total_pages,
            "sources": sources
        }
