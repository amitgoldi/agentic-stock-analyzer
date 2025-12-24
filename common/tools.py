"""Shared tools for all agents."""

import logging

from pydantic_ai import Tool
from pydantic_ai.common_tools.tavily import tavily_search_tool

from .config import config

logger = logging.getLogger(__name__)


def create_web_search_tool() -> Tool:
    """
    Create a web search tool using Tavily API.

    Returns:
        Tool: Configured Tavily search tool
    """
    if not config.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is required for web search functionality")

    tool = tavily_search_tool(config.TAVILY_API_KEY)
    tool.name = "web_search"
    return tool


# Create a shared instance of the web search tool
web_search_tool = create_web_search_tool()
