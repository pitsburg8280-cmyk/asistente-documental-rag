"""
Módulo de Base de Datos Vectorial (Sesión 4)
Implementa ChromaDB persistente con indexación de alta velocidad.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import COLLECTION_NAME, SIMILARITY_THRESHOLD, TOP_K, CHROMA_DIR
from src.embeddings import EmbeddingManager

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Motor de indexación vectorial especializado en búsqueda por similitud semántica.
    """
    
    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        persist_directory: Path = CHROMA_DIR,
        collection_name: str = COLLECTION_NAME
    ):
        """
        Inicializa la base de datos vectorial.
        
        Args:
            embedding_manager: Instancia del gestor de embeddings
            persist_directory: Ruta de persistencia en disco
            collection_name: Nombre de la colección ChromaDB
        """
        self.embedding_manager = embedding_manager
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        
        # Asegurar que el directorio existe
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        try:
            logger.info(f"💾 Inicializando ChromaDB en: {self.persist_directory}")
            
            # Intentar cargar colección existente o crear nueva
            try:
                self.vectorstore = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embedding_manager.embeddings,
                    persist_directory=str(self.persist_directory)
                )
                logger.info(f"✅ ChromaDB lista: colección='{collection_name}'")
            except Exception as e:
                logger.warning(f"⚠️ Creando nueva colección: {e}")
                self.vectorstore = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=self.embedding_manager.embeddings,
                    persist_directory=str(self.persist_directory)
                )
                logger.info(f"✅ Nueva colección creada: '{collection_name}'")
            
        except Exception as e:
            logger.error(f"❌ Error al inicializar ChromaDB: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Inserta documentos en la base de datos vectorial.
        
        Args:
            documents: Lista de documentos a indexar
        """
        if not documents:
            logger.warning("⚠️ No hay documentos para indexar")
            return
        
        try:
            logger.info(f"📥 Indexando {len(documents)} documentos...")
            
            # Añadir documentos en batches para optimizar memoria
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self.vectorstore.add_documents(batch)
                logger.info(f"   Progreso: {min(i + batch_size, len(documents))}/{len(documents)}")
            
            logger.info(f"✅ Indexación completada: {len(documents)} vectores almacenados")
            
        except Exception as e:
            logger.error(f"❌ Error en indexación: {str(e)}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = TOP_K,
        score_threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Tuple[Document, float]]:
        """
        Búsqueda por similitud de coseno con umbral de confianza.
        
        Args:
            query: Consulta del usuario
            k: Número máximo de resultados
            score_threshold: Umbral mínimo de similitud (0-1)
            
        Returns:
            Lista de tuplas (documento, score) filtradas por umbral
        """
        try:
            logger.info(f"🔍 Buscando similitudes para: '{query[:50]}...'")
            
            # Realizar búsqueda con scores
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Filtrar por umbral de similitud
            filtered_results = [
                (doc, score) for doc, score in results 
                if score >= score_threshold
            ]
            
            logger.info(f"✅ Búsqueda completada: {len(filtered_results)} resultados válidos (umbral={score_threshold})")
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {str(e)}")
            return []
    
    def clear(self) -> None:
        """
        Elimina todos los vectores de la colección.
        Maneja el caso de colección no inicializada.
        """
        try:
            # Intentar eliminar la colección existente
            self.vectorstore.delete_collection()
            logger.info("🗑️ Colección anterior eliminada")
            
            # Reinicializar el vectorstore limpio después de eliminar
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding_manager.embeddings,
                persist_directory=str(self.persist_directory)
            )
            logger.info("✅ Colección reinicializada limpia")
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Si la colección no existe o no está inicializada, solo reinicializar
            if "not initialized" in error_msg or "does not exist" in error_msg:
                logger.warning("⚠️ Colección no inicializada, creando nueva...")
                try:
                    self.vectorstore = Chroma(
                        collection_name=self.collection_name,
                        embedding_function=self.embedding_manager.embeddings,
                        persist_directory=str(self.persist_directory)
                    )
                    logger.info("✅ Nueva colección creada")
                except Exception as e2:
                    logger.error(f"❌ Error al crear nueva colección: {str(e2)}")
                    raise
            else:
                logger.error(f"❌ Error al limpiar colección: {str(e)}")
                raise
    
    def get_collection_stats(self) -> dict:
        """
        Retorna estadísticas de la colección.
        
        Returns:
            Diccionario con métricas de la base de datos
        """
        try:
            count = self.vectorstore._collection.count()
            return {
                "total_vectors": count,
                "collection_name": self.collection_name,
                "persist_directory": str(self.persist_directory),
                "embedding_dimension": self.embedding_manager.vector_dimension
            }
        except Exception as e:
            logger.error(f"❌ Error al obtener estadísticas: {str(e)}")
            return {}


