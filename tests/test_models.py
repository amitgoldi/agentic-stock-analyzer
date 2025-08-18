"""Unit tests for Pydantic data models."""

import pytest
from datetime import datetime
from pydantic import ValidationError

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


class TestStockSymbol:
    """Test StockSymbol model validation and behavior."""
    
    def test_valid_stock_symbol(self):
        """Test valid stock symbol creation."""
        symbol = StockSymbol(symbol="AAPL")
        assert symbol.symbol == "AAPL"
        assert symbol.exchange is None
        assert str(symbol) == "AAPL"
    
    def test_stock_symbol_with_exchange(self):
        """Test stock symbol with exchange."""
        symbol = StockSymbol(symbol="AAPL", exchange="NASDAQ")
        assert symbol.symbol == "AAPL"
        assert symbol.exchange == "NASDAQ"
        assert str(symbol) == "AAPL:NASDAQ"
    
    def test_empty_symbol_validation(self):
        """Test that empty symbol raises validation error."""
        with pytest.raises(ValidationError):
            StockSymbol(symbol="")
    
    def test_long_symbol_validation(self):
        """Test that overly long symbol raises validation error."""
        with pytest.raises(ValidationError):
            StockSymbol(symbol="VERYLONGSYMBOL")


class TestCompanyInfo:
    """Test CompanyInfo model validation."""
    
    def test_valid_company_info(self):
        """Test valid company info creation."""
        company = CompanyInfo(
            name="Apple Inc.",
            symbol="AAPL",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=3000000000000.0,
            description="Apple designs and manufactures consumer electronics."
        )
        assert company.name == "Apple Inc."
        assert company.symbol == "AAPL"
        assert company.market_cap == 3000000000000.0
    
    def test_company_info_without_market_cap(self):
        """Test company info without market cap."""
        company = CompanyInfo(
            name="Private Company",
            symbol="PRIV",
            sector="Technology",
            industry="Software",
            description="A private company."
        )
        assert company.market_cap is None
    
    def test_negative_market_cap_validation(self):
        """Test that negative market cap raises validation error."""
        with pytest.raises(ValidationError):
            CompanyInfo(
                name="Test Company",
                symbol="TEST",
                sector="Technology",
                industry="Software",
                market_cap=-1000.0,
                description="Test description"
            )
    
    def test_empty_required_fields_validation(self):
        """Test that empty required fields raise validation errors."""
        with pytest.raises(ValidationError):
            CompanyInfo(
                name="",
                symbol="TEST",
                sector="Technology",
                industry="Software",
                description="Test description"
            )


class TestFinancialMetrics:
    """Test FinancialMetrics model validation."""
    
    def test_valid_financial_metrics(self):
        """Test valid financial metrics creation."""
        metrics = FinancialMetrics(
            current_price=150.25,
            price_change=2.50,
            price_change_percent=1.69,
            volume=50000000,
            pe_ratio=25.5,
            dividend_yield=0.5
        )
        assert metrics.current_price == 150.25
        assert metrics.price_change == 2.50
        assert metrics.volume == 50000000
    
    def test_financial_metrics_with_none_values(self):
        """Test financial metrics with None values."""
        metrics = FinancialMetrics()
        assert metrics.current_price is None
        assert metrics.volume is None
    
    def test_negative_price_validation(self):
        """Test that negative price raises validation error."""
        with pytest.raises(ValidationError):
            FinancialMetrics(current_price=-10.0)
    
    def test_negative_volume_validation(self):
        """Test that negative volume raises validation error."""
        with pytest.raises(ValidationError):
            FinancialMetrics(volume=-1000)
    
    def test_invalid_dividend_yield_validation(self):
        """Test that invalid dividend yield raises validation error."""
        with pytest.raises(ValidationError):
            FinancialMetrics(dividend_yield=150.0)  # Over 100%


class TestNewsItem:
    """Test NewsItem model validation."""
    
    def test_valid_news_item(self):
        """Test valid news item creation."""
        news = NewsItem(
            title="Apple Reports Strong Q4 Earnings",
            summary="Apple exceeded expectations with strong iPhone sales.",
            url="https://example.com/news/apple-earnings",
            published_date=datetime(2024, 1, 15, 10, 30),
            sentiment="positive"
        )
        assert news.title == "Apple Reports Strong Q4 Earnings"
        assert news.sentiment == "positive"
    
    def test_news_item_without_sentiment(self):
        """Test news item without sentiment."""
        news = NewsItem(
            title="Market Update",
            summary="General market update.",
            url="https://example.com/news/market",
            published_date=datetime.now()
        )
        assert news.sentiment is None
    
    def test_invalid_sentiment_validation(self):
        """Test that invalid sentiment raises validation error."""
        with pytest.raises(ValidationError):
            NewsItem(
                title="Test News",
                summary="Test summary",
                url="https://example.com",
                published_date=datetime.now(),
                sentiment="invalid_sentiment"
            )


class TestMarketSentiment:
    """Test MarketSentiment model validation."""
    
    def test_valid_market_sentiment(self):
        """Test valid market sentiment creation."""
        sentiment = MarketSentiment(
            overall_sentiment="positive",
            confidence_score=0.85,
            key_factors=["Strong earnings", "Market optimism", "Positive analyst coverage"]
        )
        assert sentiment.overall_sentiment == "positive"
        assert sentiment.confidence_score == 0.85
        assert len(sentiment.key_factors) == 3
    
    def test_invalid_sentiment_validation(self):
        """Test that invalid sentiment raises validation error."""
        with pytest.raises(ValidationError):
            MarketSentiment(
                overall_sentiment="invalid",
                confidence_score=0.5,
                key_factors=["Factor 1"]
            )
    
    def test_invalid_confidence_score_validation(self):
        """Test that invalid confidence score raises validation error."""
        with pytest.raises(ValidationError):
            MarketSentiment(
                overall_sentiment="positive",
                confidence_score=1.5,  # Over 1.0
                key_factors=["Factor 1"]
            )
    
    def test_empty_key_factors_validation(self):
        """Test that empty key factors raises validation error."""
        with pytest.raises(ValidationError):
            MarketSentiment(
                overall_sentiment="positive",
                confidence_score=0.5,
                key_factors=[]
            )


class TestRiskAssessment:
    """Test RiskAssessment model validation."""
    
    def test_valid_risk_assessment(self):
        """Test valid risk assessment creation."""
        risk = RiskAssessment(
            risk_level="medium",
            risk_factors=["Market volatility", "Regulatory changes"],
            volatility_assessment="Moderate volatility expected due to market conditions"
        )
        assert risk.risk_level == "medium"
        assert len(risk.risk_factors) == 2
    
    def test_invalid_risk_level_validation(self):
        """Test that invalid risk level raises validation error."""
        with pytest.raises(ValidationError):
            RiskAssessment(
                risk_level="extreme",
                risk_factors=["Factor 1"],
                volatility_assessment="Assessment"
            )
    
    def test_empty_risk_factors_validation(self):
        """Test that empty risk factors raises validation error."""
        with pytest.raises(ValidationError):
            RiskAssessment(
                risk_level="low",
                risk_factors=[],
                volatility_assessment="Assessment"
            )


class TestInvestmentRecommendation:
    """Test InvestmentRecommendation model validation."""
    
    def test_valid_investment_recommendation(self):
        """Test valid investment recommendation creation."""
        recommendation = InvestmentRecommendation(
            recommendation="buy",
            confidence=0.8,
            reasoning="Strong fundamentals and positive market outlook",
            target_price=175.0,
            time_horizon="6-12 months"
        )
        assert recommendation.recommendation == "buy"
        assert recommendation.confidence == 0.8
        assert recommendation.target_price == 175.0
    
    def test_recommendation_without_target_price(self):
        """Test recommendation without target price."""
        recommendation = InvestmentRecommendation(
            recommendation="hold",
            confidence=0.6,
            reasoning="Neutral outlook",
            time_horizon="3-6 months"
        )
        assert recommendation.target_price is None
    
    def test_invalid_recommendation_validation(self):
        """Test that invalid recommendation raises validation error."""
        with pytest.raises(ValidationError):
            InvestmentRecommendation(
                recommendation="maybe",
                confidence=0.5,
                reasoning="Uncertain",
                time_horizon="1 year"
            )
    
    def test_invalid_confidence_validation(self):
        """Test that invalid confidence raises validation error."""
        with pytest.raises(ValidationError):
            InvestmentRecommendation(
                recommendation="buy",
                confidence=1.5,  # Over 1.0
                reasoning="Strong buy",
                time_horizon="1 year"
            )
    
    def test_negative_target_price_validation(self):
        """Test that negative target price raises validation error."""
        with pytest.raises(ValidationError):
            InvestmentRecommendation(
                recommendation="sell",
                confidence=0.9,
                reasoning="Overvalued",
                target_price=-10.0,
                time_horizon="3 months"
            )


class TestStockReport:
    """Test StockReport model validation and serialization."""
    
    @pytest.fixture
    def sample_company_info(self):
        """Sample company info for testing."""
        return CompanyInfo(
            name="Apple Inc.",
            symbol="AAPL",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=3000000000000.0,
            description="Apple designs and manufactures consumer electronics."
        )
    
    @pytest.fixture
    def sample_financial_metrics(self):
        """Sample financial metrics for testing."""
        return FinancialMetrics(
            current_price=150.25,
            price_change=2.50,
            price_change_percent=1.69,
            volume=50000000,
            pe_ratio=25.5,
            dividend_yield=0.5
        )
    
    @pytest.fixture
    def sample_news_items(self):
        """Sample news items for testing."""
        return [
            NewsItem(
                title="Apple Reports Strong Earnings",
                summary="Apple exceeded expectations.",
                url="https://example.com/news1",
                published_date=datetime(2024, 1, 15, 10, 30),
                sentiment="positive"
            ),
            NewsItem(
                title="Market Analysis",
                summary="General market update.",
                url="https://example.com/news2",
                published_date=datetime(2024, 1, 14, 15, 45),
                sentiment="neutral"
            )
        ]
    
    @pytest.fixture
    def sample_market_sentiment(self):
        """Sample market sentiment for testing."""
        return MarketSentiment(
            overall_sentiment="positive",
            confidence_score=0.85,
            key_factors=["Strong earnings", "Market optimism"]
        )
    
    @pytest.fixture
    def sample_risk_assessment(self):
        """Sample risk assessment for testing."""
        return RiskAssessment(
            risk_level="medium",
            risk_factors=["Market volatility", "Competition"],
            volatility_assessment="Moderate volatility expected"
        )
    
    @pytest.fixture
    def sample_investment_recommendation(self):
        """Sample investment recommendation for testing."""
        return InvestmentRecommendation(
            recommendation="buy",
            confidence=0.8,
            reasoning="Strong fundamentals",
            target_price=175.0,
            time_horizon="6-12 months"
        )
    
    def test_valid_stock_report(
        self,
        sample_company_info,
        sample_financial_metrics,
        sample_news_items,
        sample_market_sentiment,
        sample_risk_assessment,
        sample_investment_recommendation
    ):
        """Test valid stock report creation."""
        report = StockReport(
            symbol="AAPL",
            company_info=sample_company_info,
            financial_metrics=sample_financial_metrics,
            recent_news=sample_news_items,
            market_sentiment=sample_market_sentiment,
            risk_assessment=sample_risk_assessment,
            investment_recommendation=sample_investment_recommendation
        )
        
        assert report.symbol == "AAPL"
        assert report.company_info.name == "Apple Inc."
        assert len(report.recent_news) == 2
        assert report.market_sentiment.overall_sentiment == "positive"
        assert report.investment_recommendation.recommendation == "buy"
        assert isinstance(report.analysis_timestamp, datetime)
    
    def test_stock_report_serialization(
        self,
        sample_company_info,
        sample_financial_metrics,
        sample_news_items,
        sample_market_sentiment,
        sample_risk_assessment,
        sample_investment_recommendation
    ):
        """Test stock report JSON serialization."""
        report = StockReport(
            symbol="AAPL",
            company_info=sample_company_info,
            financial_metrics=sample_financial_metrics,
            recent_news=sample_news_items,
            market_sentiment=sample_market_sentiment,
            risk_assessment=sample_risk_assessment,
            investment_recommendation=sample_investment_recommendation
        )
        
        # Test serialization to dict
        report_dict = report.model_dump()
        assert report_dict["symbol"] == "AAPL"
        assert "analysis_timestamp" in report_dict
        
        # Test JSON serialization
        json_str = report.model_dump_json()
        assert isinstance(json_str, str)
        assert "AAPL" in json_str
    
    def test_stock_report_deserialization(
        self,
        sample_company_info,
        sample_financial_metrics,
        sample_news_items,
        sample_market_sentiment,
        sample_risk_assessment,
        sample_investment_recommendation
    ):
        """Test stock report deserialization from dict."""
        original_report = StockReport(
            symbol="AAPL",
            company_info=sample_company_info,
            financial_metrics=sample_financial_metrics,
            recent_news=sample_news_items,
            market_sentiment=sample_market_sentiment,
            risk_assessment=sample_risk_assessment,
            investment_recommendation=sample_investment_recommendation
        )
        
        # Serialize to dict and back
        report_dict = original_report.model_dump()
        reconstructed_report = StockReport.model_validate(report_dict)
        
        assert reconstructed_report.symbol == original_report.symbol
        assert reconstructed_report.company_info.name == original_report.company_info.name
        assert len(reconstructed_report.recent_news) == len(original_report.recent_news)