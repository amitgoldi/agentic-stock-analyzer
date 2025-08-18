"""Configuration management for the agentic stock analyzer."""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class TavilyConfig(BaseModel):
    """Configuration for Tavily API integration."""

    api_key: str = Field(..., description="Tavily API key")
    max_results: int = Field(default=10, description="Maximum search results to return")
    search_depth: str = Field(default="advanced", description="Search depth level")


class AgentConfig(BaseModel):
    """Configuration for the AI agent."""
    
    model_config = {"protected_namespaces": ()}

    model_name: str = Field(
        default="gpt-4.1", description="Model to use for the agent"
    )
    temperature: float = Field(
        default=0.1, ge=0.0, le=2.0, description="Model temperature"
    )
    max_retries: int = Field(default=3, ge=1, description="Maximum number of retries")
    
    # LiteLLM configuration
    base_url: Optional[str] = Field(
        default=None, description="Custom base URL for LiteLLM proxy"
    )
    api_key: Optional[str] = Field(
        default=None, description="API key for LiteLLM proxy"
    )


class AppConfig(BaseModel):
    """Main application configuration."""

    tavily: TavilyConfig
    agent: AgentConfig
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            tavily=TavilyConfig(
                api_key=os.getenv("TAVILY_API_KEY", ""),
                max_results=int(os.getenv("TAVILY_MAX_RESULTS", "10")),
                search_depth=os.getenv("TAVILY_SEARCH_DEPTH", "advanced"),
            ),
            agent=AgentConfig(
                model_name=os.getenv("AGENT_MODEL", "gpt-4.1"),
                temperature=float(os.getenv("AGENT_TEMPERATURE", "0.1")),
                max_retries=int(os.getenv("AGENT_MAX_RETRIES", "3")),
                base_url=os.getenv("LITELLM_BASE_URL"),
                api_key=os.getenv("LITELLM_API_KEY"),
            ),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


def get_config() -> AppConfig:
    """Get the application configuration."""
    return AppConfig.from_env()
