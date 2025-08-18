"""Utility functions and tools for stock analysis."""

import logging
from datetime import datetime
from typing import List, Optional

from tavily import TavilyClient

from .config import TavilyConfig
from .models import CompanyInfo, FinancialMetrics, NewsItem

logger = logging.getLogger(__name__)


class StockAnalysisError(Exception):
    """Base exception for stock analysis errors."""
    pass


class InsufficientDataError(StockAnalysisError):
    """Raised when insufficient data is available for analysis."""
    pass


class APIError(StockAnalysisError):
    """Raised when external API calls fail."""
    pass


class TavilyResearchTool:
    """Generic web search tool using Tavily API."""
    
    def __init__(self, config: TavilyConfig):
        """Initialize the Tavily research tool.
        
        Args:
            config: Tavily configuration containing API key and settings
        """
        self.config = config
        self.client = TavilyClient(api_key=config.api_key)
    
    async def search(self, query: str) -> List[dict]:
        """Perform a web search using Tavily.
        
        Args:
            query: Search query string
            
        Returns:
            List of search result dictionaries with keys: title, url, content
            
        Raises:
            APIError: If the Tavily API call fails
        """
        try:
            logger.info(f"Performing web search: {query}")
            
            response = self.client.search(
                query=query,
                search_depth=self.config.search_depth,
                max_results=self.config.max_results
            )
            
            if not response or not response.get("results"):
                logger.warning(f"No search results found for query: {query}")
                return []
            
            results = response["results"]
            logger.info(f"Found {len(results)} search results for query: {query}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error performing web search for query '{query}': {str(e)}")
            raise APIError(f"Failed to perform web search: {str(e)}")