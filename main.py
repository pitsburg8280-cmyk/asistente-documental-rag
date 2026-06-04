"""
Punto de entrada principal del Asistente Documental Inteligente.
Ejecuta la interfaz de usuario de Streamlit.
"""

import sys
from pathlib import Path

# Asegurar que el directorio src esté en el path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui import render_ui

if __name__ == "__main__":
    render_ui()
