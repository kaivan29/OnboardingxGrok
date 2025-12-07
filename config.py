"""
Configuration Management
========================

Purpose:
    Centralized configuration management for the application. Loads environment variables
    from .env file and provides a Config class with all application settings.

Key Responsibilities:
    - Load environment variables using python-dotenv
    - Provide default values for configuration options
    - Validate required configuration (API keys)
    - Store Grok API settings (API key, model, base URL)
    - Store GitHub token for repository cloning
    - Define default file patterns and analysis parameters

Configuration Variables:
    - XAI_API_KEY: Grok API key (required)
    - XAI_MODEL: Model name (default: grok-code-fast-1)
    - XAI_BASE_URL: API base URL (default: https://api.x.ai/v1)
    - GITHUB_TOKEN: Optional GitHub token for private repos
    - DEFAULT_MAX_FILE_SIZE: Maximum file size in bytes (default: 100KB)

Usage:
    from config import Config
    api_key = Config.XAI_API_KEY
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Grok API Configuration
    XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")
    XAI_MODEL: str = os.getenv("XAI_MODEL", "grok-3")
    XAI_BASE_URL: str = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
    
    # GitHub Configuration
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # Analysis Defaults
    DEFAULT_MAX_FILE_SIZE: int = int(os.getenv("DEFAULT_MAX_FILE_SIZE", "100000"))  # 100KB
    DEFAULT_INCLUDE_PATTERNS: list = ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx"]
    DEFAULT_EXCLUDE_PATTERNS: list = ["**/node_modules/**", "**/__pycache__/**", "**/.git/**"]
    
    # API Configuration
    API_TITLE: str = "Grok Code Tutorial Backend API"
    API_VERSION: str = "1.0.0"
    
    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.XAI_API_KEY:
            raise ValueError("XAI_API_KEY environment variable is required")


# Validate configuration on import
try:
    Config.validate()
except ValueError:
    # Allow import without validation for setup purposes
    pass

