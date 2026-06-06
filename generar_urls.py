import base64

def generar_url_mermaid(codigo_diagrama):
    """Convierte código Mermaid a URL de imagen directa"""
    # Codificar en base64
    encoded = base64.b64encode(codigo_diagrama.encode('utf-8')).decode('ascii')
    # Generar URL
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=white"
    return url


# ==========================================
# DIAGRAMA 2: ESTRUCTURA DE SESIONES
# ==========================================
diagrama_sesiones = """graph LR
    subgraph "Cronograma de 8 Sesiones"
        direction TB
        S1["Sesion 1: Ingesta"] --> F1["document_loader.py"]
        S2["Sesion 2: Chunking"] --> F2["text_splitter.py"]
        S3["Sesion 3: Embeddings"] --> F3["embeddings.py"]
        S4["Sesion 4: Vector DB"] --> F4["vector_store.py"]
        S5["Sesion 5: RAG"] --> F5["rag_chain.py"]
        S6["Sesion 6: Prompts"] --> F6["prompt_templates.py"]
        S7["Sesion 7: UI"] --> F7["ui.py"]
        S8["Sesion 8: Tests"] --> F8["test_stress.py"]
    end
    style S1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style S2 fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    style S3 fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    style S4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style S5 fill:#fff8e1,stroke:#ff8f00,stroke-width:2px
    style S6 fill:#ffebee,stroke:#c62828,stroke-width:2px
    style S7 fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    style S8 fill:#fce4ec,stroke:#ad1457,stroke-width:2px"""

print("=" * 80)
print("URL DEL DIAGRAMA DE SESIONES:")
print("=" * 80)
print(generar_url_mermaid(diagrama_sesiones))
print()

print("✅ Copia estas URLs y úsalas en tu README.md como imágenes!")
print("Formato: ![Arquitectura](URL_AQUI)")
