"""
Módulo de Ingeniería de Prompts (Sesión 6)
Diseña plantillas que permiten respuestas con contexto limitado.
"""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class PromptManager:
    """
    Gestor de prompts que permite respuestas con el contexto disponible,
    incluso si es limitado.
    """
    
    @staticmethod
    def get_rag_prompt() -> ChatPromptTemplate:
        """
        Plantilla principal del sistema RAG - PERMISIVA.
        Responde con lo que tenga, sin rechazar por poco contexto.
        
        Returns:
            ChatPromptTemplate configurado con mensajes de sistema y humano
        """
        
        # Mensaje del sistema: PERMISIVO
        system_template = """Eres un Asistente Documental Inteligente. Tu trabajo es analizar el contexto proporcionado y responder basándote en él.

INSTRUCCIONES:
1. Analiza el contexto proporcionado cuidadosamente.
2. Responde usando la información del contexto, aunque sea breve o limitada.
3. Si el contexto es corto, resume o describe lo que contiene.
4. NO inventes información que no esté en el contexto.
5. Si realmente no hay NADA de información relevante, indica: "El documento no contiene información sobre este tema específico."
6. Sé conciso pero completo con la información disponible.

Contexto del documento:
{context}
"""

        # Mensaje humano: Formato de la pregunta
        human_template = """Pregunta: {question}

Responde basándote en el contexto proporcionado arriba. Si el contexto es limitado, indica qué información contiene."""
        
        # Construir el prompt template
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template)
        ]
        
        return ChatPromptTemplate.from_messages(messages)
    
    @staticmethod
    def get_condensed_question_prompt() -> ChatPromptTemplate:
        """
        Prompt para condensar preguntas con historial de conversación.
        
        Returns:
            ChatPromptTemplate para reformular preguntas
        """
        template = """Dado el siguiente historial de conversación y una pregunta de seguimiento, 
reformula la pregunta de seguimiento para que sea una pregunta independiente que incluya el contexto necesario.

Historial de conversación:
{chat_history}

Pregunta de seguimiento: {question}

Pregunta independiente:"""
        
        return ChatPromptTemplate.from_template(template)

