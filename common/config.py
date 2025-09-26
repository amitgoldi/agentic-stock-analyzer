"""Configuration management for the application."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration using Pydantic Settings."""

    # Tavily API Configuration
    TAVILY_API_KEY: str = Field(default="", description="Tavily API key for web search")
    TAVILY_MAX_RESULTS: int = Field(
        default=10, description="Maximum search results from Tavily"
    )
    TAVILY_SEARCH_DEPTH: str = Field(
        default="advanced", description="Tavily search depth"
    )

    # LLM Configuration
    AGENT_MODEL: str = Field(
        default="gpt-4.1_2025-04-14", description="LLM model to use"
    )
    AGENT_TEMPERATURE: float = Field(default=0.1, description="LLM temperature setting")
    AGENT_MAX_RETRIES: int = Field(
        default=3, description="Maximum retries for LLM calls"
    )

    # LiteLLM Configuration
    LITELLM_BASE_URL: str = Field(default="", description="LiteLLM proxy base URL")
    LITELLM_API_KEY: str = Field(default="", description="LiteLLM API key")

    # Logfire Configuration
    LOGFIRE_API_KEY: str = Field(
        default="", description="Logfire API key for observability"
    )
    LOGFIRE_PROJECT_ID: str = Field(default="", description="Logfire project ID")
    ENABLE_LOGFIRE: bool = Field(default=True, description="Enable Logfire integration")

    # Application Configuration
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def validate_required_keys(self) -> None:
        """Validate that all required configuration keys are present."""
        if not self.TAVILY_API_KEY:
            error_msg = (
                "Missing required environment variable: TAVILY_API_KEY\n"
                "Please copy .env.example to .env and configure your API keys."
            )
            raise ValueError(error_msg)


# Global config instance
config = Config()
