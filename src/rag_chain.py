"""
Módulo de Orquestación RAG (Sesión 5)
Integra el retriever vectorial con el LLM local mediante LangChain.
"""

import logging
from typing import List, Optional, Dict, Any

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from config import MODEL_NAME, MODEL_TEMPERATURE, MODEL_TIMEOUT, TOP_K
from src.vector_store import VectorStore
from src.prompt_templates import PromptManager

logger = logging.getLogger(__name__)


class RAGChain:
    """
    Pipeline lógico unificado que conecta recuperación de información con inferencia generativa.
    """
    
    def __init__(
        self,
        vector_store: VectorStore,
        model_name: str = MODEL_NAME,
        temperature: float = MODEL_TEMPERATURE
    ):
        """
        Inicializa la cadena RAG.
        
        Args:
            vector_store: Instancia de la base de datos vectorial
            model_name: Modelo de Ollama a utilizar
            temperature: Temperatura de generación
        """
        self.vector_store = vector_store
        self.model_name = model_name
        self.temperature = temperature
        
        try:
            logger.info(f"🤖 Inicializando LLM: {model_name}")
            
            # Configurar LLM local con Ollama
            self.llm = ChatOllama(
                model=model_name,
                temperature=temperature,
                timeout=MODEL_TIMEOUT,
                format="",
                num_ctx=4096,
                num_predict=512,
            )
            
            # Inicializar prompts
            self.prompt_manager = PromptManager()
            self.rag_prompt = self.prompt_manager.get_rag_prompt()
            
            # Construir la cadena RAG
            self.chain = self._build_chain()
            
            logger.info("✅ Cadena RAG construida exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error al inicializar RAG Chain: {str(e)}")
            raise
    
    def _format_context(self, docs: List[Any]) -> str:
        """
        Formatea los documentos recuperados en un string de contexto.
        
        Args:
            docs: Lista de documentos o tuplas (doc, score)
            
        Returns:
            String formateado con el contexto
        """
        if not docs:
            return "No se encontraron documentos relevantes."
        
        formatted = []
        for i, item in enumerate(docs, 1):
            # Manejar tanto documentos como tuplas (doc, score)
            if isinstance(item, tuple):
                doc, score = item
                source = doc.metadata.get("source", "Desconocido")
                content = doc.page_content
                formatted.append(f"[Documento {i} | Fuente: {source} | Relevancia: {score:.3f}]\n{content}\n")
            else:
                doc = item
                source = doc.metadata.get("source", "Desconocido")
                content = doc.page_content
                formatted.append(f"[Documento {i} | Fuente: {source}]\n{content}\n")
        
        return "\n---\n".join(formatted)
    
    def _build_chain(self):
        """
        Construye el pipeline RAG completo.
        
        Returns:
            Cadena ejecutable de LangChain
        """
        # Componente de recuperación
        retriever = RunnableLambda(lambda x: self.vector_store.similarity_search(
            x["question"], 
            k=TOP_K
        ))
        
        # Función para formatear contexto
        format_context = RunnableLambda(lambda x: {
            "context": self._format_context(x["retrieved_docs"]),
            "question": x["question"]
        })
        
        # Cadena completa: Recuperar -> Formatear -> Prompt -> LLM -> Parsear
        chain = (
            {
                "question": RunnablePassthrough(),
                "retrieved_docs": retriever
            }
            | format_context
            | self.rag_prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def invoke(self, question: str) -> Dict[str, Any]:
        """
        Ejecuta la cadena RAG con una pregunta.
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            Diccionario con respuesta, documentos recuperados y metadatos
        """
        try:
            logger.info(f"❓ Pregunta recibida: '{question[:60]}...'")
            
            # Recuperar documentos relevantes
            retrieved_docs = self.vector_store.similarity_search(question, k=TOP_K)
            
            # Formatear contexto
            context = self._format_context(retrieved_docs)
            
            # Si hay documentos, SIEMPRE intentar responder
            if retrieved_docs:
                logger.info(f"✅ Recuperados {len(retrieved_docs)} documentos, generando respuesta...")
                
                # Ejecutar cadena
                answer = self.chain.invoke({"question": question})
                
                result = {
                    "answer": answer,
                    "source_documents": [
                        {
                            "content": doc.page_content[:200] + "...",
                            "source": doc.metadata.get("source", "Desconocido"),
                            "score": float(score)
                        }
                        for doc, score in retrieved_docs
                    ],
                    "retrieval_successful": True,
                    "context_used": context[:500] + "..." if len(context) > 500 else context
                }
                
                logger.info(f"✅ Respuesta generada: {len(answer)} caracteres")
                return result
            
            else:
                # Solo si NO hay documentos en absoluto
                logger.warning("⚠️ No se encontraron documentos relevantes")
                return {
                    "answer": "No se encontraron documentos relevantes. Por favor, verifica que los PDFs contengan información sobre este tema.",
                    "source_documents": [],
                    "retrieval_successful": False
                }
                
        except Exception as e:
            logger.error(f"❌ Error en ejecución RAG: {str(e)}")
            return {
                "answer": f"Error en el sistema: {str(e)}",
                "source_documents": [],
                "retrieval_successful": False,
                "error": str(e)
            }
    
    def get_chain_info(self) -> dict:
        """
        Retorna información de configuración de la cadena.
        
        Returns:
            Diccionario con parámetros técnicos
        """
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "top_k": TOP_K,
            "timeout": MODEL_TIMEOUT,
            "prompt_type": "permissive-rag"
        }
