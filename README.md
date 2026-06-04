# 🤖 Asistente Documental Inteligente (RAG)

Sistema de Generación Aumentada por Recuperación (RAG) completamente funcional y local. Permite interactuar con documentos PDF privados utilizando Modelos de Lenguaje de Gran Escala (LLMs) de código abierto, garantizando respuestas precisas y libres de alucinaciones.

**Repositorio:** [https://github.com/pitsburg8280-cmyk/asistente-documental-rag](https://github.com/pitsburg8280-cmyk/asistente-documental-rag)

---

## 🎯 Características Principales

- **100% Local**: Sin dependencias de APIs comerciales ni compromiso de privacidad
- **Procesamiento de PDFs**: Extracción robusta de texto con manejo de metadatos
- **Embeddings Semánticos**: Codificación vectorial con `all-MiniLM-L6-v2`
- **Base de Datos Vectorial**: ChromaDB persistente en disco para búsqueda de alta velocidad
- **Mitigación de Alucinaciones**: Prompts estrictos que restringen respuestas al contexto documental
- **Interfaz Profesional**: UI interactiva con Streamlit y manejo de historial
- **Rendimiento Optimizado**: Compatible con hardware de gama media (GPU opcional)
- **OCR Integrado**: Procesamiento de PDFs escaneados e imágenes con Tesseract

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph LR
    subgraph "Ingesta y Procesamiento"
        A[("📄 PDFs<br/>Locales")] --> B["✂️ Chunking<br/>Avanzado"]
        B --> C["🧠 Embeddings<br/>all-MiniLM-L6-v2"]
    end
    
    C --> D[("💾 ChromaDB<br/>Vectorial")]
    
    subgraph "Recuperación y Generación"
        D --> E["🤖 LLM Local<br/>(Ollama)"]
        E --> F["🖥️ Streamlit<br/>UI"]
    end
    
    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style B fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style C fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style D fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px
    style E fill:#fce4ec,stroke:#c62828,stroke-width:2px
    style F fill:#e0f2f1,stroke:#00695c,stroke-width:3px





