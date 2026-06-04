"""
Módulo de Embeddings Semánticos (Sesión 3)
Transforma texto en representaciones vectoriales densas usando modelos locales.
"""

import logging
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL, EMBEDDING_DEVICE

logger = logging.getLogger(__name__)


class EmbeddingManager:
    """
    Gestor de embeddings que codifica significado semántico en vectores densos.
    Utiliza all-MiniLM-L6-v2 optimizado para ejecución local.
    """
    
    def __init__(self, model_name: str = EMBEDDING_MODEL, device: str = EMBEDDING_DEVICE):
        """
        Inicializa el modelo de embeddings.
        
        Args:
            model_name: Nombre del modelo en HuggingFace
            device: Dispositivo de ejecución ('cpu' o 'cuda')
        """
        self.model_name = model_name
        self.device = device
        
        try:
            logger.info(f"🧠 Cargando modelo de embeddings: {model_name}")
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': device},
                encode_kwargs={'normalize_embeddings': True}  # Normalización L2
            )
            
            # Obtener dimensión del vector
            test_vector = self.embeddings.embed_query("test")
            self.vector_dimension = len(test_vector)
            
            logger.info(f"✅ Modelo cargado: dimensión={self.vector_dimension}, dispositivo={device}")
            
        except Exception as e:
            logger.error(f"❌ Error al cargar embeddings: {str(e)}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Genera embeddings para una lista de textos.
        
        Args:
            texts: Lista de textos a vectorizar
            
        Returns:
            Lista de vectores densos
        """
        if not texts:
            return []
        
        try:
            logger.info(f"🔢 Generando embeddings para {len(texts)} textos...")
            vectors = self.embeddings.embed_documents(texts)
            logger.info(f"✅ Embeddings generados: {len(vectors)} vectores de dimensión {len(vectors[0])}")
            return vectors
            
        except Exception as e:
            logger.error(f"❌ Error en generación de embeddings: {str(e)}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """
        Genera embedding para una consulta de usuario.
        
        Args:
            text: Texto de la consulta
            
        Returns:
            Vector denso de la consulta
        """
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"❌ Error en embedding de consulta: {str(e)}")
            raise
    
    def get_model_info(self) -> dict:
        """
        Retorna información del modelo de embeddings.
        
        Returns:
            Diccionario con especificaciones técnicas
        """
        return {
            "model_name": self.model_name,
            "vector_dimension": self.vector_dimension,
            "device": self.device,
            "normalization": True,
            "framework": "sentence-transformers"
        }
