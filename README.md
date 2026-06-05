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


🚀 Instalación y Configuración
Requisitos Previos
 
Python 3.9+
Ollama instalado localmente
Tesseract OCR (para PDFs escaneados)
Git


1. Clonar el Repositorio
git clone https://github.com/pitsburg8280-cmyk/asistente-documental-rag.git
cd asistente-documental-rag


2. Crear Entorno Virtual
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate


3. Instalar Dependencias
pip install -r requirements.txt


4. Descargar Modelo LLM
ollama pull llama3.2:3b


5. Ejecutar la Aplicación
streamlit run main.py

La aplicación estará disponible en  http://localhost:8501


📋 Guía de Uso

Opción 1: Carga Directa desde el Navegador (Recomendada)
1. Abre la aplicación con  streamlit run main.py
2. Arrastra o selecciona tus PDFs en el panel lateral (sección "Cargar Documentos")
3. Haz clic en "Procesar Documentos Subidos"
4. Espera a que el sistema indexe los documentos
5. Comienza a hacer preguntas en la interfaz de chat

Opción 2: Carpeta Local (Avanzada)
1. Coloca tus PDFs en la carpeta  data/  (opcional)
2. Inicia la aplicación con  streamlit run main.py
3. Haz clic en "Procesar Documentos Locales" en el panel lateral
4. Realiza consultas en la interfaz de chat


Gestión de Documentos
 
Visualizar: Lista de PDFs cargados en el panel lateral
 
Eliminar: Botón 🗑️ junto a cada archivo para removerlo
 
Limpiar DB: Botón "Limpiar Base de Datos" para reiniciar el sistema


⚙️ Configuración Avanzada

Edita  config.py  para personalizar:
 
 CHUNK_SIZE : Tamaño de fragmentos (default: 500)
 
 CHUNK_OVERLAP : Solapamiento entre chunks (default: 100)
 
 TOP_K : Documentos a recuperar (default: 10)
 
 MODEL_NAME : Modelo de Ollama (default: llama3.2:3b)


🧪 Pruebas de Estrés
Ejecuta las pruebas de robustez:

python tests/test_stress.py


🛡️ Mitigación de Alucinaciones
El sistema implementa múltiples capas de seguridad:

1. Prompt del Sistema Estricto: "Responde ÚNICAMENTE basándote en el contexto proporcionado..."
2. Instrucción de Negación: "Si la respuesta no está en el contexto, responde: 'No tengo información...'"
3. Verificación de Contexto: El retriever debe encontrar documentos relevantes con similitud > umbral


## 📁 Estructura de Sesiones

```mermaid
graph LR
    subgraph "Cronograma de 8 Sesiones"
        direction TB
       
        S1["📄 Sesión 1<br/>Ingesta de Documentos"] --> F1["src/document_loader.py"]
        S2["✂️ Sesión 2<br/>Chunking Avanzado"] --> F2["src/text_splitter.py"]
        S3["🧠 Sesión 3<br/>Embeddings Semánticos"] --> F3["src/embeddings.py"]
        S4["💾 Sesión 4<br/>Base de Datos Vectorial"] --> F4["src/vector_store.py"]
        S5["⚙️ Sesión 5<br/>Orquestación RAG"] --> F5["src/rag_chain.py"]
        S6["🛡️ Sesión 6<br/>Ingeniería de Prompts"] --> F6["src/prompt_templates.py"]
        S7["🖥️ Sesión 7<br/>Interfaz Web"] --> F7["src/ui.py"]
        S8["🧪 Sesión 8<br/>Pruebas de Estrés"] --> F8["tests/test_stress.py"]
    end
   
    style S1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style S2 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style S3 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style S4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style S5 fill:#fff8e1,stroke:#ff8f00,stroke-width:2px
    style S6 fill:#ffebee,stroke:#c62828,stroke-width:2px
    style S7 fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    style S8 fill:#fce4ec,stroke:#ad1457,stroke-width:2px


📝 Licencia
Este proyecto es de uso académico y educativo.
