"""Common utility functions."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from .config import config

# Import logfire for observability
try:
    import logfire

    LOGFIRE_AVAILABLE = True
except ImportError:
    LOGFIRE_AVAILABLE = False


def setup_logging() -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set specific loggers to appropriate levels
    if not config.DEBUG:
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """Format search results for display."""
    if not results:
        return "No search results found."

    formatted = []
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")

        formatted.append(
            f"{i}. **{title}**\n   URL: {url}\n   Content: {content[:200]}..."
        )

    return "\n\n".join(formatted)


def validate_stock_symbol(symbol: str) -> str:
    """Validate and normalize stock symbol."""
    if not symbol:
        raise ValueError("Stock symbol cannot be empty")

    # Convert to uppercase and remove whitespace
    normalized = symbol.strip().upper()

    # Basic validation - should be 1-5 characters, alphanumeric
    if not normalized.isalnum() or len(normalized) > 5:
        raise ValueError(f"Invalid stock symbol format: {symbol}")

    return normalized


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_subsection_header(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n{'-' * 40}")
    print(f" {title}")
    print(f"{'-' * 40}")


def create_agent_model() -> Union[OpenAIModel, str]:
    """
    Create a model instance for agents with LiteLLM configuration.

    This function centralizes the model creation logic to avoid duplication
    across different agent implementations.

    Returns:
        Union[OpenAIModel, str]: Configured OpenAI model or model name string
    """
    if config.LITELLM_BASE_URL and config.LITELLM_API_KEY:
        # Use LiteLLM proxy configuration
        provider = OpenAIProvider(
            base_url=config.LITELLM_BASE_URL,
            api_key=config.LITELLM_API_KEY,
        )
        model = OpenAIModel(
            config.AGENT_MODEL,
            provider=provider,
        )
        return model
    else:
        # Fallback to direct model name (will use default OpenAI provider)
        return config.AGENT_MODEL


def setup_logfire(
    service_name: str, start_message: str, extra_data: Optional[Dict[str, Any]] = None
) -> None:
    """Set up Logfire integration if available and enabled.

    Args:
        service_name: Name of the service for Logfire configuration
        start_message: Message to log when Logfire starts
        extra_data: Optional extra data to include in the start message
    """
    logger = logging.getLogger(__name__)

    if not LOGFIRE_AVAILABLE:
        logger.warning("Logfire not available - skipping instrumentation")
        return

    if not config.ENABLE_LOGFIRE:
        logger.info("Logfire disabled in configuration")
        return

    try:
        # Configure Logfire using environment variables
        logfire.configure(
            token=config.LOGFIRE_API_KEY,
            send_to_logfire=True,
            environment="development",
            service_name=service_name,
            inspect_arguments=False,  # Suppress warnings in demo environment
        )

        # Instrument Pydantic AI
        logfire.instrument_pydantic_ai()

        # Optionally instrument HTTP requests to see API calls
        logfire.instrument_httpx(capture_all=True)

        # Send a test message to verify connection
        logfire.info(start_message, extra=extra_data or {})

        logger.info("Logfire instrumentation configured successfully")
        logger.info(f"Logfire project: {config.LOGFIRE_PROJECT_ID}")
        logger.info(f"Logfire token configured: {config.LOGFIRE_API_KEY[:20]}...")
        logger.info("✅ Check your Logfire dashboard for traces!")

    except Exception as e:
        logger.warning(f"Failed to configure Logfire: {e}")
        logger.info("Logfire traces will still appear in console output")
