"""Common utility functions."""

import logging
from datetime import datetime
from typing import Any, Dict, List

from .config import config


def setup_logging() -> None:
    """Set up logging configuration."""
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
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
        
        formatted.append(f"{i}. **{title}**\n   URL: {url}\n   Content: {content[:200]}...")
    
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
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subsection_header(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")
