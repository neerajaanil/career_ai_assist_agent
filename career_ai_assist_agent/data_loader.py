"""Data loading utilities for career information."""

import logging
from pathlib import Path
from typing import Optional
from pypdf import PdfReader

logger = logging.getLogger(__name__)


class DataLoader:
    """Loads career-related data from various sources."""
    
    def __init__(self, linkedin_pdf_path: Path, summary_txt_path: Path):
        self.linkedin_pdf_path = linkedin_pdf_path
        self.summary_txt_path = summary_txt_path
        self._linkedin_content: Optional[str] = None
        self._summary_content: Optional[str] = None
    
    def load_linkedin_profile(self) -> str:
        """Load and extract text from LinkedIn PDF."""
        if self._linkedin_content is not None:
            return self._linkedin_content
        
        if not self.linkedin_pdf_path.exists():
            raise FileNotFoundError(f"LinkedIn PDF not found at {self.linkedin_pdf_path}")
        
        try:
            logger.info(f"Loading LinkedIn profile from {self.linkedin_pdf_path}")
            reader = PdfReader(str(self.linkedin_pdf_path))
            content = ""
            
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num}: {e}")
            
            self._linkedin_content = content.strip()
            logger.info(f"Successfully loaded LinkedIn profile ({len(self._linkedin_content)} characters)")
            return self._linkedin_content
        except Exception as e:
            logger.error(f"Failed to load LinkedIn PDF: {e}")
            raise
    
    def load_summary(self) -> str:
        """Load summary text from file."""
        if self._summary_content is not None:
            return self._summary_content
        
        if not self.summary_txt_path.exists():
            raise FileNotFoundError(f"Summary file not found at {self.summary_txt_path}")
        
        try:
            logger.info(f"Loading summary from {self.summary_txt_path}")
            with open(self.summary_txt_path, "r", encoding="utf-8") as f:
                self._summary_content = f.read().strip()
            
            logger.info(f"Successfully loaded summary ({len(self._summary_content)} characters)")
            return self._summary_content
        except Exception as e:
            logger.error(f"Failed to load summary file: {e}")
            raise
    
    def get_all_data(self) -> tuple[str, str]:
        """Load both LinkedIn profile and summary."""
        return self.load_linkedin_profile(), self.load_summary()
