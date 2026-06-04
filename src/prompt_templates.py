"""
Módulo de Ingeniería de Prompts (Sesión 6)
Diseña plantillas avanzadas que restringen el comportamiento del LLM para evitar alucinaciones.
"""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class PromptManager:
    """
    Gestor de prompts que condiciona las respuestas del modelo mediante 
    instrucciones estrictas del sistema y plantillas de control.
    """
    
    @staticmethod
    def get_rag_prompt() -> ChatPromptTemplate:
        """
        Plantilla principal del sistema RAG con restricciones anti-alucinación.
        
        Returns:
            ChatPromptTemplate configurado con mensajes de sistema y humano
        """
        
        # Mensaje del sistema: Restricciones absolutas de comportamiento
        system_template = """Eres un Asistente Documental Inteligente especializado en responder preguntas basándote EXCLUSIVAMENTE en el contexto proporcionado.

REGLAS ESTRICTAS:
1. Responde ÚNICAMENTE usando la información del contexto proporcionado.
2. Si la respuesta no está en el contexto, responde EXACTAMENTE: "No tengo información suficiente en los documentos proporcionados para responder esta pregunta. Por favor, verifica si el tema está cubierto en los PDFs cargados."
3. NO inventes, supongas ni generes información que no esté en el contexto.
4. NO uses conocimiento externo, por muy obvio que te parezca.
5. Mantén las respuestas concisas, precisas y directas.
6. Cita la fuente del documento cuando sea relevante.
7. Si el contexto es insuficiente o ambiguo, indica explícitamente la limitación.

Contexto proporcionado:
{context}
"""

        # Mensaje humano: Formato de la pregunta
        human_template = """Pregunta: {question}

Responde basándote ÚNICAMENTE en el contexto proporcionado arriba. Si no encuentras la respuesta, indica que no tienes la información."""
        
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
    
    @staticmethod
    def get_validation_prompt() -> ChatPromptTemplate:
        """
        Prompt para validar si una respuesta está fundamentada en el contexto.
        
        Returns:
            ChatPromptTemplate para verificación de fundamentación
        """
        template = """Evalúa si la siguiente respuesta está fundamentada en el contexto proporcionado.

Contexto: {context}
Respuesta: {answer}

La respuesta está fundamentada en el contexto? Responde solo 'SÍ' o 'NO' y explica brevemente por qué."""
        
        return ChatPromptTemplate.from_template(template)
