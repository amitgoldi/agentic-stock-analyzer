"""Test fixtures with sample stock data and API responses."""

from datetime import datetime
from typing import Dict, List, Any

import pytest

from common.models import (
    StockSymbol,
    CompanyInfo,
    FinancialMetrics,
    NewsItem,
    MarketSentiment,
    RiskAssessment,
    InvestmentRecommendation,
    StockReport,
)


@pytest.fixture
def sample_stock_symbols() -> List[StockSymbol]:
    """Sample stock symbols for testing."""
    return [
        StockSymbol(symbol="AAPL", exchange="NASDAQ"),
        StockSymbol(symbol="GOOGL", exchange="NASDAQ"),
        StockSymbol(symbol="MSFT", exchange="NASDAQ"),
        StockSymbol(symbol="TSLA", exchange="NASDAQ"),
        StockSymbol(symbol="AMZN", exchange="NASDAQ"),
    ]


@pytest.fixture
def sample_company_info() -> CompanyInfo:
    """Sample company information for Apple Inc."""
    return CompanyInfo(
        name="Apple Inc.",
        symbol="AAPL",
        sector="Technology",
        industry="Consumer Electronics",
        market_cap=3000000000000.0,
        description="Apple Inc. designs, manufactures, and markets consumer electronics, computer software, and online services worldwide."
    )


@pytest.fixture
def sample_financial_metrics() -> FinancialMetrics:
    """Sample financial metrics for testing."""
    return FinancialMetrics(
        current_price=185.50,
        price_change=2.75,
        price_change_percent=1.51,
        volume=45200000,
        pe_ratio=28.5,
        dividend_yield=0.52
    )


@pytest.fixture
def sample_news_items() -> List[NewsItem]:
    """Sample news items for testing."""
    return [
        NewsItem(
            title="Apple Reports Strong Q4 Earnings Beat",
            summary="Apple Inc. reported fourth-quarter earnings that exceeded Wall Street expectations, driven by strong iPhone sales and services revenue growth.",
            url="https://finance.yahoo.com/news/apple-earnings-q4-beat",
            published_date=datetime(2024, 1, 15, 16, 30),
            sentiment="positive"
        ),
        NewsItem(
            title="Apple Announces New Product Line",
            summary="Apple unveiled its latest product innovations including updates to the iPhone and Mac lineup at its recent event.",
            url="https://bloomberg.com/news/apple-product-announcement",
            published_date=datetime(2024, 1, 14, 10, 15),
            sentiment="positive"
        ),
        NewsItem(
            title="Market Volatility Affects Tech Stocks",
            summary="Technology stocks including Apple faced pressure amid broader market volatility and economic uncertainty.",
            url="https://reuters.com/markets/tech-stocks-volatility",
            published_date=datetime(2024, 1, 13, 14, 45),
            sentiment="negative"
        )
    ]


@pytest.fixture
def sample_market_sentiment() -> MarketSentiment:
    """Sample market sentiment for testing."""
    return MarketSentiment(
        overall_sentiment="positive",
        confidence_score=0.78,
        key_factors=[
            "Strong quarterly earnings performance",
            "Positive analyst coverage and upgrades",
            "Robust product pipeline and innovation",
            "Strong brand loyalty and market position"
        ]
    )


@pytest.fixture
def sample_risk_assessment() -> RiskAssessment:
    """Sample risk assessment for testing."""
    return RiskAssessment(
        risk_level="medium",
        risk_factors=[
            "Market volatility and economic uncertainty",
            "Increased competition in consumer electronics",
            "Supply chain disruptions and component shortages",
            "Regulatory scrutiny and potential antitrust actions"
        ],
        volatility_assessment="Moderate volatility expected due to market conditions and sector-specific factors. Historical volatility suggests price swings of 15-25% are normal."
    )


@pytest.fixture
def sample_investment_recommendation() -> InvestmentRecommendation:
    """Sample investment recommendation for testing."""
    return InvestmentRecommendation(
        recommendation="buy",
        confidence=0.82,
        reasoning="Strong fundamentals, consistent revenue growth, robust cash flow, and innovative product pipeline support a positive investment outlook. Recent earnings beat and positive guidance indicate continued strength.",
        target_price=210.00,
        time_horizon="6-12 months"
    )


@pytest.fixture
def sample_stock_report(
    sample_company_info: CompanyInfo,
    sample_financial_metrics: FinancialMetrics,
    sample_news_items: List[NewsItem],
    sample_market_sentiment: MarketSentiment,
    sample_risk_assessment: RiskAssessment,
    sample_investment_recommendation: InvestmentRecommendation
) -> StockReport:
    """Complete sample stock report for testing."""
    return StockReport(
        symbol="AAPL",
        company_info=sample_company_info,
        financial_metrics=sample_financial_metrics,
        recent_news=sample_news_items,
        market_sentiment=sample_market_sentiment,
        risk_assessment=sample_risk_assessment,
        investment_recommendation=sample_investment_recommendation,
        analysis_timestamp=datetime.now()
    )


@pytest.fixture
def mock_tavily_company_response() -> Dict[str, Any]:
    """Mock Tavily API response for company information search."""
    return {
        "results": [
            {
                "title": "Apple Inc. (AAPL) Company Profile - Yahoo Finance",
                "content": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California. Apple is the world's largest technology company by revenue and the world's most valuable company. The company operates in the Technology sector and Consumer Electronics industry. Apple designs, develops, and sells consumer electronics, computer software, and online services.",
                "url": "https://finance.yahoo.com/quote/AAPL/profile",
                "score": 0.95
            },
            {
                "title": "AAPL Stock Information - MarketWatch",
                "content": "Apple Inc. (AAPL) is headquartered in Cupertino, California. The company has a market capitalization of over $3 trillion and operates globally in the technology sector. Apple's primary business segments include iPhone, Mac, iPad, Wearables, Home and Accessories, and Services.",
                "url": "https://marketwatch.com/investing/stock/aapl",
                "score": 0.92
            },
            {
                "title": "Apple Inc. Business Overview - Bloomberg",
                "content": "Apple Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other related services. The company operates through geographical segments including Americas, Europe, Greater China, Japan, and Rest of Asia Pacific.",
                "url": "https://bloomberg.com/quote/AAPL:US",
                "score": 0.89
            }
        ],
        "query": "AAPL company information sector industry market cap description",
        "response_time": 1.23
    }


@pytest.fixture
def mock_tavily_news_response() -> Dict[str, Any]:
    """Mock Tavily API response for news search."""
    return {
        "results": [
            {
                "title": "Apple Reports Strong Q4 Earnings Beat",
                "content": "Apple Inc. reported fourth-quarter earnings that exceeded Wall Street expectations, with revenue of $89.5 billion and earnings per share of $1.46. The company saw strong performance across all product categories, particularly iPhone sales which grew 3% year-over-year.",
                "url": "https://finance.yahoo.com/news/apple-earnings-q4-beat-2024",
                "score": 0.98,
                "published_date": "2024-01-15T16:30:00Z"
            },
            {
                "title": "Apple Announces New Product Innovations",
                "content": "At its latest event, Apple unveiled significant updates to its product lineup including new iPhone models with enhanced AI capabilities and updated Mac computers with improved performance. Analysts are optimistic about the potential impact on future sales.",
                "url": "https://bloomberg.com/news/apple-product-announcement-2024",
                "score": 0.94,
                "published_date": "2024-01-14T10:15:00Z"
            },
            {
                "title": "Tech Stocks Face Market Pressure",
                "content": "Technology stocks including Apple, Microsoft, and Google faced selling pressure today amid concerns about rising interest rates and economic uncertainty. Apple shares declined 2.1% in afternoon trading.",
                "url": "https://reuters.com/markets/tech-stocks-pressure-2024",
                "score": 0.87,
                "published_date": "2024-01-13T14:45:00Z"
            }
        ],
        "query": "AAPL stock news earnings financial results recent",
        "response_time": 0.89
    }


@pytest.fixture
def mock_tavily_financial_response() -> Dict[str, Any]:
    """Mock Tavily API response for financial metrics search."""
    return {
        "results": [
            {
                "title": "AAPL Stock Quote - Yahoo Finance",
                "content": "Apple Inc. (AAPL) stock price: $185.50, up $2.75 (+1.51%) in today's trading. Trading volume: 45.2M shares. Key metrics: P/E ratio 28.5, dividend yield 0.52%, market cap $2.89T. 52-week range: $164.08 - $199.62.",
                "url": "https://finance.yahoo.com/quote/AAPL",
                "score": 0.97
            },
            {
                "title": "Apple Financial Metrics - MarketWatch",
                "content": "AAPL financial data shows strong fundamentals with revenue growth of 8% year-over-year. The company maintains healthy profit margins and strong cash flow generation. Current P/E ratio of 28.5 is in line with sector averages.",
                "url": "https://marketwatch.com/investing/stock/aapl/financials",
                "score": 0.91
            }
        ],
        "query": "AAPL stock price financial metrics PE ratio dividend yield volume",
        "response_time": 0.76
    }


@pytest.fixture
def mock_tavily_empty_response() -> Dict[str, Any]:
    """Mock empty Tavily API response."""
    return {
        "results": [],
        "query": "INVALID stock symbol",
        "response_time": 0.45
    }


@pytest.fixture
def mock_agent_analysis_response() -> str:
    """Mock agent analysis response for testing."""
    return """
    Based on my comprehensive analysis of AAPL, here are my findings:

    Company Analysis:
    Apple Inc. is a leading technology company with strong market position in consumer electronics.
    The company operates in multiple segments including iPhone, Services, Mac, iPad, and Wearables.

    Financial Performance:
    - Current stock price shows positive momentum with recent gains
    - Strong revenue growth and healthy profit margins
    - Robust cash flow generation and balance sheet strength

    Market Sentiment:
    Recent news indicates positive investor sentiment driven by strong earnings performance
    and new product announcements. Analyst coverage remains largely positive.

    Risk Assessment:
    Moderate risk level due to market volatility and competitive pressures.
    Key risks include supply chain disruptions and regulatory scrutiny.

    Investment Recommendation:
    BUY recommendation with high confidence based on strong fundamentals,
    positive market sentiment, and growth prospects. Target price $210 over 6-12 months.
    """


@pytest.fixture
def sample_portfolio_symbols() -> List[str]:
    """Sample portfolio symbols for testing."""
    return ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]


@pytest.fixture
def sample_portfolio_reports(
    sample_stock_report: StockReport,
    sample_company_info: CompanyInfo,
    sample_financial_metrics: FinancialMetrics,
    sample_news_items: List[NewsItem],
    sample_market_sentiment: MarketSentiment,
    sample_risk_assessment: RiskAssessment
) -> List[StockReport]:
    """Sample portfolio reports for testing."""
    # Create variations of the base report for different stocks
    reports = []
    
    symbols = ["AAPL", "GOOGL", "MSFT"]
    recommendations = ["buy", "hold", "sell"]
    risk_levels = ["low", "medium", "high"]
    
    for i, symbol in enumerate(symbols):
        # Create modified company info
        company_info = CompanyInfo(
            name=f"{symbol} Corporation",
            symbol=symbol,
            sector="Technology",
            industry="Software" if symbol != "AAPL" else "Consumer Electronics",
            market_cap=2000000000000.0 + (i * 500000000000.0),
            description=f"Mock company data for {symbol}"
        )
        
        # Create modified recommendation
        recommendation = InvestmentRecommendation(
            recommendation=recommendations[i],
            confidence=0.7 + (i * 0.1),
            reasoning=f"Analysis-based recommendation for {symbol}",
            target_price=150.0 + (i * 25.0),
            time_horizon="6-12 months"
        )
        
        # Create modified risk assessment
        risk = RiskAssessment(
            risk_level=risk_levels[i],
            risk_factors=[f"Risk factor 1 for {symbol}", f"Risk factor 2 for {symbol}"],
            volatility_assessment=f"Volatility assessment for {symbol}"
        )
        
        report = StockReport(
            symbol=symbol,
            company_info=company_info,
            financial_metrics=sample_financial_metrics,
            recent_news=sample_news_items,
            market_sentiment=sample_market_sentiment,
            risk_assessment=risk,
            investment_recommendation=recommendation,
            analysis_timestamp=datetime.now()
        )
        
        reports.append(report)
    
    return reports