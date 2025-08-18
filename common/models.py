"""Pydantic models for stock analysis data validation and serialization."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class StockSymbol(BaseModel):
    """Stock ticker symbol with optional exchange information."""
    
    symbol: str = Field(..., description="Stock ticker symbol", min_length=1, max_length=10)
    exchange: Optional[str] = Field(None, description="Stock exchange")
    
    def __str__(self) -> str:
        if self.exchange:
            return f"{self.symbol}:{self.exchange}"
        return self.symbol


class CompanyInfo(BaseModel):
    """Company information and basic details."""
    
    name: str = Field(..., description="Company name", min_length=1)
    symbol: str = Field(..., description="Stock ticker symbol", min_length=1)
    sector: str = Field(..., description="Business sector", min_length=1)
    industry: str = Field(..., description="Industry classification", min_length=1)
    market_cap: Optional[float] = Field(None, description="Market capitalization in USD", ge=0)
    description: str = Field(..., description="Company description", min_length=1)


class FinancialMetrics(BaseModel):
    """Financial metrics and stock performance data."""
    
    current_price: Optional[float] = Field(None, description="Current stock price", ge=0)
    price_change: Optional[float] = Field(None, description="Price change from previous close")
    price_change_percent: Optional[float] = Field(None, description="Percentage price change")
    volume: Optional[int] = Field(None, description="Trading volume", ge=0)
    pe_ratio: Optional[float] = Field(None, description="Price-to-earnings ratio", ge=0)
    dividend_yield: Optional[float] = Field(None, description="Dividend yield percentage", ge=0, le=100)


class NewsItem(BaseModel):
    """News article or press release related to a stock."""
    
    title: str = Field(..., description="News article title", min_length=1)
    summary: str = Field(..., description="Article summary or excerpt", min_length=1)
    url: str = Field(..., description="Article URL")
    published_date: datetime = Field(..., description="Publication date and time")
    sentiment: Optional[str] = Field(
        None, 
        description="Sentiment analysis result",
        pattern="^(positive|negative|neutral)$"
    )


class MarketSentiment(BaseModel):
    """Overall market sentiment analysis for a stock."""
    
    overall_sentiment: str = Field(
        ..., 
        description="Overall sentiment classification",
        pattern="^(positive|negative|neutral)$"
    )
    confidence_score: float = Field(
        ..., 
        description="Confidence in sentiment analysis", 
        ge=0, 
        le=1
    )
    key_factors: List[str] = Field(
        ..., 
        description="Key factors influencing sentiment",
        min_length=1
    )


class RiskAssessment(BaseModel):
    """Risk assessment for investment decision."""
    
    risk_level: str = Field(
        ..., 
        description="Risk level classification",
        pattern="^(low|medium|high)$"
    )
    risk_factors: List[str] = Field(
        ..., 
        description="Identified risk factors",
        min_length=1
    )
    volatility_assessment: str = Field(
        ..., 
        description="Volatility analysis",
        min_length=1
    )


class InvestmentRecommendation(BaseModel):
    """Investment recommendation with reasoning."""
    
    recommendation: str = Field(
        ..., 
        description="Investment recommendation",
        pattern="^(buy|hold|sell)$"
    )
    confidence: float = Field(
        ..., 
        description="Confidence in recommendation", 
        ge=0, 
        le=1
    )
    reasoning: str = Field(
        ..., 
        description="Detailed reasoning for recommendation",
        min_length=1
    )
    target_price: Optional[float] = Field(
        None, 
        description="Target price for the stock", 
        ge=0
    )
    time_horizon: str = Field(
        ..., 
        description="Investment time horizon",
        min_length=1
    )


class StockReport(BaseModel):
    """Comprehensive stock analysis report."""
    
    symbol: str = Field(..., description="Stock ticker symbol", min_length=1)
    company_info: CompanyInfo = Field(..., description="Company information")
    financial_metrics: FinancialMetrics = Field(..., description="Financial metrics")
    recent_news: List[NewsItem] = Field(..., description="Recent news items")
    market_sentiment: MarketSentiment = Field(..., description="Market sentiment analysis")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment")
    investment_recommendation: InvestmentRecommendation = Field(..., description="Investment recommendation")
    analysis_timestamp: datetime = Field(
        default_factory=datetime.now, 
        description="When the analysis was performed"
    )