"""Common data models for stock analysis."""

from typing import List, Optional
from pydantic import BaseModel, Field


class StockReport(BaseModel):
    """Comprehensive stock analysis report."""
    
    symbol: str = Field(description="Stock symbol (e.g., AAPL, TSLA)")
    company_name: str = Field(description="Full company name")
    current_price: Optional[float] = Field(description="Current stock price", default=None)
    price_change: Optional[float] = Field(description="Price change from previous close", default=None)
    price_change_percent: Optional[float] = Field(description="Price change percentage", default=None)
    
    # Analysis sections
    executive_summary: str = Field(description="Brief executive summary of the stock")
    recent_news: List[str] = Field(description="Key recent news items affecting the stock", default_factory=list)
    financial_highlights: List[str] = Field(description="Key financial metrics and highlights", default_factory=list)
    market_sentiment: str = Field(description="Overall market sentiment analysis")
    risk_factors: List[str] = Field(description="Key risk factors to consider", default_factory=list)
    recommendation: str = Field(description="Investment recommendation with reasoning")
    
    # Metadata
    analysis_date: str = Field(description="Date when analysis was performed")
    data_sources: List[str] = Field(description="Sources used for the analysis", default_factory=list)


class SearchResult(BaseModel):
    """Web search result structure."""
    
    title: str = Field(description="Title of the search result")
    url: str = Field(description="URL of the source")
    content: str = Field(description="Content snippet from the search result")
    relevance_score: Optional[float] = Field(description="Relevance score if available", default=None)
