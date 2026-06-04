"""
Módulo de Chunking Avanzado (Sesión 2)
Implementa estrategias de fragmentación con preservación de contexto semántico.
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
            chunk_size: Tamaño máximo de cada fragmento en tokens/caracteres
            chunk_overlap: Tamaño del solapamiento entre fragmentos consecutivos
            separators: Jerarquía de separadores para ruptura semántica
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or CHUNK_SEPARATORS
        
        # Inicializar el splitter con configuración avanzada
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,  # Función de longitud basada en caracteres
            is_separator_regex=False,
            add_start_index=True,  # Añadir índice de inicio para trazabilidad
        )
        
        logger.info(f"✂️ TextSplitter inicializado: size={chunk_size}, overlap={chunk_overlap}")
    
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
            
                        # Enriquecer metadatos de cada fragmento (valores simples solo)
            for i, split in enumerate(splits):
                split.metadata.update({
                    "chunk_index": i,
                    "chunk_size": len(split.page_content),
                    "splitter_chunk_size": self.chunk_size,
                    "splitter_chunk_overlap": self.chunk_overlap
                })


            
            logger.info(f"✅ Fragmentación completada: {len(splits)} chunks generados")
            logger.info(f"📊 Promedio de tamaño: {sum(len(s.page_content) for s in splits) / len(splits):.0f} caracteres")
            
            return splits
            
        except Exception as e:
            logger.error(f"❌ Error en fragmentación: {str(e)}")
            raise
    
    def get_split_stats(self, splits: List[Document]) -> dict:
        """
        Retorna estadísticas de la fragmentación.
        
        Returns:
            Diccionario con métricas de calidad
        """
        if not splits:
            return {}
        
        sizes = [len(s.page_content) for s in splits]
        return {
            "total_chunks": len(splits),
            "avg_chunk_size": sum(sizes) / len(sizes),
            "min_chunk_size": min(sizes),
            "max_chunk_size": max(sizes),
            "overlap_ratio": self.chunk_overlap / self.chunk_size
        }
