"""
Módulo de Ingesta de Documentos (Sesión 1)
Extrae texto desde archivos PDF, incluyendo soporte OCR para documentos escaneados.
"""

import logging
from pathlib import Path
from typing import List, Union
from io import BytesIO

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Intentar importar librerías OCR (opcional)
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
    logger.info("✅ OCR disponible para PDFs escaneados")
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("⚠️ OCR no disponible. Instala: pip install pytesseract pdf2image Pillow")


class DocumentLoader:
    """
    Cargador robusto de documentos PDF con soporte OCR.
    Maneja PDFs digitales, multi-columna, tablas y documentos escaneados (imágenes).
    """
    
    def __init__(self, data_dir: Path):
        """
        Inicializa el cargador con el directorio de datos.
        
        Args:
            data_dir: Ruta al directorio que contiene los PDFs
        """
        self.data_dir = Path(data_dir)
        self.documents: List[Document] = []
        
        # Configurar ruta de Tesseract en Windows
        if OCR_AVAILABLE:
            try:
                tesseract_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
                if tesseract_path.exists():
                    pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
                    logger.info(f"🔧 Tesseract configurado: {tesseract_path}")
            except Exception as e:
                logger.warning(f"⚠️ No se pudo configurar Tesseract: {e}")
        
    def is_scanned_pdf(self, file_path: Path) -> bool:
        """
        Detecta si un PDF es escaneado (imagen) o tiene texto seleccionable.
        También detecta si el texto extraído es muy corto (posible imagen mal escaneada).
        
        Args:
            file_path: Ruta al PDF
            
        Returns:
            True si es escaneado o texto muy corto, False si tiene texto real
        """
        try:
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            
            # Calcular texto total
            total_text = "".join([doc.page_content for doc in docs]).strip()
            
            # Si no extrae texto o es muy corto, probablemente es escaneado o imagen
            if len(total_text) < 200:  # Umbral: menos de 200 caracteres = escaneado
                logger.info(f"   Texto extraído muy corto ({len(total_text)} chars), probablemente es imagen")
                return True
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Error detectando tipo de PDF: {e}")
            return True  # Si hay error, asumir escaneado para intentar OCR
    
    def load_pdf_with_ocr(self, file_path: Path) -> List[Document]:
        """
        Carga un PDF escaneado usando OCR (Tesseract).
        
        Args:
            file_path: Ruta al PDF escaneado
            
        Returns:
            Lista de documentos con texto extraído por OCR
        """
        if not OCR_AVAILABLE:
            logger.error("❌ OCR no disponible. Instala: pip install pytesseract pdf2image Pillow")
            return []
        
        try:
            logger.info(f"🔍 OCR: Procesando PDF escaneado: {file_path.name}")
            
            # Convertir PDF a imágenes (300 DPI para buena calidad OCR)
            images = convert_from_path(str(file_path), dpi=300)
            
            documents = []
            for i, image in enumerate(images, 1):
                logger.info(f"   OCR página {i}/{len(images)}...")
                
                # Extraer texto con Tesseract (español + inglés)
                try:
                    text = pytesseract.image_to_string(image, lang='spa+eng')
                except:
                    # Si no tiene idioma español, usar inglés por defecto
                    text = pytesseract.image_to_string(image, lang='eng')
                
                # Limpiar texto (quitar líneas vacías excesivas)
                text = "\n".join(line for line in text.split("\n") if line.strip())
                
                # Crear documento LangChain
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "file_path": str(file_path),
                        "page": i,
                        "total_pages": len(images),
                        "document_type": "pdf_scanned",
                        "extraction_method": "ocr_tesseract"
                    }
                )
                documents.append(doc)
            
            logger.info(f"✅ OCR completado: {file_path.name} - {len(documents)} páginas procesadas")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Error en OCR para '{file_path.name}': {str(e)}")
            return []
    
    def load_pdf(self, file_path: Union[Path, str]) -> List[Document]:
        """
        Carga un PDF detectando automáticamente si es digital o escaneado.
        Si el texto es muy corto, fuerza OCR automáticamente.
        
        Args:
            file_path: Ruta al archivo PDF
            
        Returns:
            Lista de documentos LangChain con metadatos
        """
        file_path = Path(file_path)
        
        try:
            logger.info(f"📄 Analizando PDF: {file_path.name}")
            
            # Detectar si es escaneado o texto muy corto
            if self.is_scanned_pdf(file_path):
                logger.info(f"   Detectado: PDF escaneado o texto muy corto, usando OCR")
                ocr_docs = self.load_pdf_with_ocr(file_path)
                
                # Si OCR devuelve contenido, usarlo
                if ocr_docs and any(len(d.page_content.strip()) > 50 for d in ocr_docs):
                    return ocr_docs
                else:
                    logger.warning("⚠️ OCR no extrajo texto, intentando método digital como fallback")
                    return self.load_pdf_digital(file_path)
            else:
                logger.info(f"   Detectado: PDF digital (texto seleccionable)")
                return self.load_pdf_digital(file_path)
                
        except Exception as e:
            logger.error(f"❌ Error al procesar '{file_path.name}': {str(e)}")
            return []
    
    def load_pdf_digital(self, file_path: Path) -> List[Document]:
        """
        Carga un PDF digital con texto seleccionable.
        
        Args:
            file_path: Ruta al PDF
            
        Returns:
            Lista de documentos con metadatos
        """
        try:
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            
            # Enriquecer metadatos
            for doc in docs:
                doc.metadata.update({
                    "source": file_path.name,
                    "file_path": str(file_path),
                    "total_pages": len(docs),
                    "document_type": "pdf_digital",
                    "extraction_method": "pypdf"
                })
            
            logger.info(f"✅ PDF digital '{file_path.name}' procesado: {len(docs)} páginas")
            return docs
            
        except Exception as e:
            logger.error(f"❌ Error en PDF digital '{file_path.name}': {str(e)}")
            return []
    
    def load_pdf_from_bytes(self, file_bytes: bytes, file_name: str) -> List[Document]:
        """
        Carga un PDF desde bytes en memoria (para archivos subidos desde Streamlit).
        
        Args:
            file_bytes: Contenido del PDF en bytes
            file_name: Nombre del archivo para metadatos
            
        Returns:
            Lista de documentos LangChain
        """
        try:
            # Guardar temporalmente para procesar
            temp_path = self.data_dir / f"temp_{file_name}"
            with open(temp_path, "wb") as f:
                f.write(file_bytes)
            
            # Procesar con el mismo método (detecta automáticamente)
            docs = self.load_pdf(temp_path)
            
            # Actualizar metadatos con nombre original
            for doc in docs:
                doc.metadata["original_name"] = file_name
            
            # Limpiar temporal
            temp_path.unlink()
            
            return docs
            
        except Exception as e:
            logger.error(f"❌ Error al procesar '{file_name}' desde memoria: {str(e)}")
            return []
    
    def load_all_pdfs(self) -> List[Document]:
        """
        Carga todos los PDFs del directorio de datos.
        
        Returns:
            Lista consolidada de documentos
        """
        if not self.data_dir.exists():
            raise FileNotFoundError(f"El directorio {self.data_dir} no existe")
        
        pdf_files = list(self.data_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"⚠️ No se encontraron PDFs en {self.data_dir}")
            return []
        
        logger.info(f"📚 Encontrados {len(pdf_files)} archivos PDF")
        
        all_documents = []
        for pdf_file in pdf_files:
            docs = self.load_pdf(pdf_file)
            all_documents.extend(docs)
        
        self.documents = all_documents
        logger.info(f"📊 Total de páginas cargadas: {len(all_documents)}")
        return all_documents
    
    def get_document_stats(self) -> dict:
        """
        Retorna estadísticas de los documentos cargados.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.documents:
            return {"total_documents": 0, "total_pages": 0, "sources": [], "scanned_count": 0}
        
        sources = list(set(doc.metadata.get("source", "unknown") for doc in self.documents))
        total_pages = len(self.documents)
        scanned_count = sum(1 for doc in self.documents if doc.metadata.get("document_type") == "pdf_scanned")
        
        return {
            "total_documents": len(self.documents),
            "total_pages": total_pages,
            "sources": sources,
            "scanned_count": scanned_count,
            "digital_count": total_pages - scanned_count
        }

