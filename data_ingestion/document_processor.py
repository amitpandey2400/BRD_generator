"""
Document processing for uploaded files (PDF, DOCX, PPTX, TXT)
"""
import os
from typing import Dict, Optional
from pathlib import Path
import PyPDF2
from docx import Document
from pptx import Presentation

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class DocumentProcessor:
    """Processor for various document types"""
    
    @staticmethod
    def process_file(file_path: str) -> Dict:
        """
        Process a file and extract text content
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with extracted content and metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = Path(file_path).suffix.lower()
        
        processors = {
            '.pdf': DocumentProcessor._process_pdf,
            '.docx': DocumentProcessor._process_docx,
            '.doc': DocumentProcessor._process_docx,
            '.pptx': DocumentProcessor._process_pptx,
            '.ppt': DocumentProcessor._process_pptx,
            '.txt': DocumentProcessor._process_txt,
            '.md': DocumentProcessor._process_txt,
        }
        
        processor = processors.get(file_extension)
        if not processor:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        try:
            content = processor(file_path)
            metadata = DocumentProcessor._extract_metadata(file_path)
            
            return {
                'content': content,
                'metadata': metadata,
                'file_type': file_extension[1:],
                'file_name': Path(file_path).name
            }
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            raise
    
    @staticmethod
    def _process_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text_parts = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    @staticmethod
    def _process_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        
        text_parts = []
        
        # Extract paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        
        # Extract tables
        for table in doc.tables:
            for row in table.rows:
                row_text = ' | '.join(cell.text.strip() for cell in row.cells)
                if row_text.strip():
                    text_parts.append(row_text)
        
        return "\n\n".join(text_parts)
    
    @staticmethod
    def _process_pptx(file_path: str) -> str:
        """Extract text from PPTX file"""
        prs = Presentation(file_path)
        text_parts = []
        
        for slide_num, slide in enumerate(prs.slides, 1):
            slide_text = [f"--- Slide {slide_num} ---"]
            
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text)
            
            text_parts.append("\n".join(slide_text))
        
        return "\n\n".join(text_parts)
    
    @staticmethod
    def _process_txt(file_path: str) -> str:
        """Extract text from TXT/MD file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    @staticmethod
    def _extract_metadata(file_path: str) -> Dict:
        """Extract file metadata"""
        stat = os.stat(file_path)
        
        return {
            'file_size': stat.st_size,
            'created_at': stat.st_ctime,
            'modified_at': stat.st_mtime,
            'file_path': file_path
        }
    
    @staticmethod
    def save_uploaded_file(file_content: bytes, filename: str) -> str:
        """
        Save an uploaded file to storage
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Path to saved file
        """
        # Create storage directory if it doesn't exist
        storage_path = Path(settings.DOCUMENT_STORAGE_PATH)
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = int(os.time())
        safe_filename = f"{timestamp}_{filename}"
        file_path = storage_path / safe_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        logger.info(f"Saved uploaded file: {file_path}")
        return str(file_path)
