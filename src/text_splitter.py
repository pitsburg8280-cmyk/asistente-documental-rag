"""
Módulo de Chunking Avanzado (Sesión 2)
Implementa estrategias de fragmentación con preservación de contexto semántico.
Maneja documentos de cualquier tamaño, incluso muy pequeños.
"""

import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_SEPARATORS

logger = logging.getLogger(__name__)


class TextSplitter:
    """
    Fragmentador de texto avanzado que optimiza la retención de contexto.
    Utiliza RecursiveCharacterTextSplitter con configuración matemática precisa.
    Maneja documentos pequeños sin errores.
    """
    
    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        separators: List[str] = None
    ):
        """
        Inicializa el fragmentador con parámetros optimizados.
        
        Args:
            chunk_size: Tamaño máximo de cada fragmento
            chunk_overlap: Tamaño del solapamiento entre fragmentos
            separators: Jerarquía de separadores para ruptura semántica
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = min(chunk_overlap, chunk_size - 1)  # Asegurar que overlap < chunk_size
        self.separators = separators or CHUNK_SEPARATORS
        
        # Inicializar el splitter con configuración avanzada
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False,
            add_start_index=True,
        )
        
        logger.info(f"✂️ TextSplitter inicializado: size={chunk_size}, overlap={self.chunk_overlap}")
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Fragmenta documentos manteniendo metadatos y contexto.
        
        Args:
            documents: Lista de documentos a fragmentar
            
        Returns:
            Lista de fragmentos con metadatos preservados
        """
        if not documents:
            logger.warning("⚠️ No hay documentos para fragmentar")
            return []
        
        try:
            logger.info(f"🔄 Fragmentando {len(documents)} documentos...")
            
            # Ejecutar fragmentación
            splits = self.splitter.split_documents(documents)
            
            # Si no se generaron chunks (documentos muy pequeños), forzar creación
            if not splits:
                logger.warning("⚠️ Splitter devolvió 0 chunks, forzando creación...")
                for i, doc in enumerate(documents):
                    content = doc.page_content.strip()
                    if len(content) > 0:
                        new_doc = Document(
                            page_content=content,
                            metadata=doc.metadata.copy()
                        )
                        new_doc.metadata.update({
                            "chunk_index": i,
                            "chunk_size": len(content),
                            "forced": True
                        })
                        splits.append(new_doc)
            
            # Enriquecer metadatos de cada fragmento
            for i, split in enumerate(splits):
                split.metadata.update({
                    "chunk_index": i,
                    "chunk_size": len(split.page_content),
                    "splitter_chunk_size": self.chunk_size,
                    "splitter_chunk_overlap": self.chunk_overlap
                })
            
            logger.info(f"✅ Fragmentación completada: {len(splits)} chunks generados")
            
            if splits:
                avg_size = sum(len(s.page_content) for s in splits) / len(splits)
                logger.info(f"📊 Promedio de tamaño: {avg_size:.0f} caracteres")
            else:
                logger.warning("⚠️ No se generaron chunks incluso con fallback")
            
            return splits
            
        except Exception as e:
            logger.error(f"❌ Error en fragmentación: {str(e)}")
            # Fallback radical: devolver documentos originales como chunks individuales
            logger.info("🔄 Fallback: usando documentos originales como chunks")
            for i, doc in enumerate(documents):
                doc.metadata.update({
                    "chunk_index": i,
                    "chunk_size": len(doc.page_content),
                    "splitter_chunk_size": self.chunk_size,
                    "splitter_chunk_overlap": self.chunk_overlap,
                    "fallback": True
                })
            return documents
    
    def get_split_stats(self, splits: List[Document]) -> dict:
        """
        Retorna estadísticas de la fragmentación.
        
        Returns:
            Diccionario con métricas de calidad
        """
        if not splits:
            return {
                "total_chunks": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0,
                "overlap_ratio": 0
            }
        
        sizes = [len(s.page_content) for s in splits]
        return {
            "total_chunks": len(splits),
            "avg_chunk_size": sum(sizes) / len(sizes),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes),
            "overlap_ratio": self.chunk_overlap / self.chunk_size if self.chunk_size > 0 else 0
        }
