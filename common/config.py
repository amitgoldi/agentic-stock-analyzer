"""Configuration management for the application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Tavily API Configuration
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    TAVILY_MAX_RESULTS: int = int(os.getenv("TAVILY_MAX_RESULTS", "10"))
    TAVILY_SEARCH_DEPTH: str = os.getenv("TAVILY_SEARCH_DEPTH", "advanced")
    
    # LLM Configuration
    AGENT_MODEL: str = os.getenv("AGENT_MODEL", "gpt-4.1_2025-04-14")
    AGENT_TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.1"))
    AGENT_MAX_RETRIES: int = int(os.getenv("AGENT_MAX_RETRIES", "3"))
    
    # LiteLLM Configuration
    LITELLM_BASE_URL: str = os.getenv("LITELLM_BASE_URL", "")
    LITELLM_API_KEY: str = os.getenv("LITELLM_API_KEY", "")
    
    # Logfire Configuration
    LOGFIRE_API_KEY: str = os.getenv("LOGFIRE_API_KEY", "")
    LOGFIRE_PROJECT_ID: str = os.getenv("LOGFIRE_PROJECT_ID", "")
    ENABLE_LOGFIRE: bool = os.getenv("ENABLE_LOGFIRE", "true").lower() == "true"
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate_required_keys(cls) -> None:
        """Validate that all required configuration keys are present."""
        required_keys = [
            ("TAVILY_API_KEY", cls.TAVILY_API_KEY),
        ]
        
        missing_keys = []
        for key_name, key_value in required_keys:
            if not key_value:
                missing_keys.append(key_name)
        
        if missing_keys:
            error_msg = f"Missing required environment variables: {', '.join(missing_keys)}\n"
            error_msg += "Please copy .env.example to .env and configure your API keys."
            raise ValueError(error_msg)


# Global config instance
config = Config()