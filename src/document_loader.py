"""
Módulo de Ingesta de Documentos (Sesión 1)
Extrae texto plano desde archivos PDF manteniendo metadatos estructurados.
Soporta tanto archivos locales como objetos de memoria (BytesIO).
"""

import logging
from pathlib import Path
from typing import List, Optional, Union
from io import BytesIO

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Cargador robusto de documentos PDF.
    Maneja PDFs multi-columna, tablas y metadatos sin pérdida de información.
    Soporta archivos locales y objetos de memoria (BytesIO).
    """
    
    def __init__(self, data_dir: Path):
        """
        Inicializa el cargador con el directorio de datos.
        
        Args:
            data_dir: Ruta al directorio que contiene los PDFs
        """
        self.data_dir = Path(data_dir)
        self.documents: List[Document] = []
        
    def load_pdf(self, file_path: Union[Path, str]) -> List[Document]:
        """
        Carga un único archivo PDF con manejo de excepciones.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Lista de documentos LangChain con metadatos
        """
        try:
            file_path = Path(file_path)
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
    
    def load_pdf_from_bytes(self, file_bytes: bytes, file_name: str) -> List[Document]:
        """
        Carga un PDF desde bytes en memoria (útil para archivos subidos desde Streamlit).
        
        Args:
            file_bytes: Contenido del PDF en bytes
            file_name: Nombre del archivo para metadatos
            
        Returns:
            Lista de documentos LangChain con metadatos
        """
        try:
            logger.info(f"Procesando PDF desde memoria: {file_name}")
            
            # Guardar temporalmente para PyPDFLoader
            temp_path = self.data_dir / f"temp_{file_name}"
            with open(temp_path, "wb") as f:
                f.write(file_bytes)
            
            # Cargar con PyPDFLoader
            loader = PyPDFLoader(str(temp_path))
            docs = loader.load()
            
            # Enriquecer metadatos
            for doc in docs:
                doc.metadata.update({
                    "source": file_name,
                    "file_path": str(temp_path),
                    "total_pages": len(docs),
                    "document_type": "pdf",
                    "loaded_from": "memory"
                })
            
            # Limpiar archivo temporal
            temp_path.unlink()
            
            logger.info(f"✅ PDF '{file_name}' procesado desde memoria: {len(docs)} páginas")
            return docs
            
        except Exception as e:
            logger.error(f"❌ Error al procesar '{file_name}' desde memoria: {str(e)}")
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

