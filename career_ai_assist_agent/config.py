"""Configuration management."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """Application configuration."""
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    PUSHOVER_TOKEN: Optional[str] = os.getenv("PUSHOVER_TOKEN")
    PUSHOVER_USER: Optional[str] = os.getenv("PUSHOVER_USER")
    
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LINKEDIN_PDF_PATH: Path = DATA_DIR / "linkedin.pdf"
    SUMMARY_TXT_PATH: Path = DATA_DIR / "summary.txt"
    
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Your Name")
    
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "7860"))
    SHARE: bool = os.getenv("SHARE", "false").lower() == "true"
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not cls.LINKEDIN_PDF_PATH.exists():
            raise FileNotFoundError(f"LinkedIn PDF not found at {cls.LINKEDIN_PDF_PATH}")
        
        if not cls.SUMMARY_TXT_PATH.exists():
            raise FileNotFoundError(f"Summary file not found at {cls.SUMMARY_TXT_PATH}")
