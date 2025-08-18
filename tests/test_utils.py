"""Tests for utility functions and Tavily research tool integration."""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

from common.config import TavilyConfig
from common.models import CompanyInfo, FinancialMetrics, NewsItem
from common.utils import TavilyResearchTool, APIError, InsufficientDataError


class TestTavilyResearchTool:
    """Test cases for TavilyResearchTool."""
    
    @pytest.fixture
    def tavily_config(self):
        """Create a test Tavily configuration."""
        return TavilyConfig(
            api_key="test_api_key",
            max_results=5,
            search_depth="basic"
        )
    
    @pytest.fixture
    def research_tool(self, tavily_config):
        """Create a TavilyResearchTool instance for testing."""
        return TavilyResearchTool(tavily_config)
    
    @pytest.fixture
    def mock_company_response(self):
        """Mock response for company information search."""
        return {
            "results": [
                {
                    "title": "Apple Inc. (AAPL) Company Profile",
                    "content": "Apple Inc. is a technology company that designs, manufactures, and markets consumer electronics, computer software, and online services. The company operates in the Technology sector and Consumer Electronics industry. Apple is known for its innovative products including iPhone, iPad, Mac, and services.",
                    "url": "https://finance.yahoo.com/quote/AAPL/profile"
                },
                {
                    "title": "AAPL Stock Information",
                    "content": "Apple Inc. (AAPL) is headquartered in Cupertino, California. The company has a market capitalization of over $3 trillion and operates globally in the technology sector.",
                    "url": "https://marketwatch.com/investing/stock/aapl"
                }
            ]
        }
    
    @pytest.fixture
    def mock_news_response(self):
        """Mock response for news search."""
        return {
            "results": [
                {
                    "title": "Apple Reports Strong Q4 Earnings",
                    "content": "Apple Inc. reported better-than-expected earnings for the fourth quarter, driven by strong iPhone sales and services revenue growth. The company's revenue increased 8% year-over-year.",
                    "url": "https://finance.yahoo.com/news/apple-earnings-q4"
                },
                {
                    "title": "Apple Announces New Product Line",
                    "content": "Apple unveiled its latest product innovations at the recent event, including updates to the iPhone and Mac lineup. Analysts are optimistic about the impact on future sales.",
                    "url": "https://bloomberg.com/news/apple-product-announcement"
                }
            ]
        }
    
    @pytest.fixture
    def mock_financial_response(self):
        """Mock response for financial metrics search."""
        return {
            "results": [
                {
                    "title": "AAPL Financial Metrics",
                    "content": "Apple (AAPL) current price: $185.50, PE ratio: 28.5, dividend yield: 0.5%, trading volume: 45.2M shares. The stock has shown strong performance with positive momentum.",
                    "url": "https://finance.yahoo.com/quote/AAPL"
                }
            ]
        }
    
    @pytest.fixture
    def empty_response(self):
        """Mock empty response."""
        return {"results": []}
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_company_info_success(self, mock_tavily_client, research_tool, mock_company_response):
        """Test successful company information search."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = mock_company_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute
        result = await tool.search_company_info("AAPL")
        
        # Verify
        assert isinstance(result, CompanyInfo)
        assert result.symbol == "AAPL"
        assert result.name == "AAPL Corporation"  # Based on our placeholder implementation
        assert result.sector == "Technology"
        assert result.industry == "Software"
        
        # Verify API call
        mock_client_instance.search.assert_called_once()
        call_args = mock_client_instance.search.call_args
        assert "AAPL" in call_args.kwargs["query"]
        assert call_args.kwargs["search_depth"] == "basic"
        assert call_args.kwargs["max_results"] == 5
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_company_info_insufficient_data(self, mock_tavily_client, research_tool, empty_response):
        """Test company information search with insufficient data."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = empty_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute and verify exception
        with pytest.raises(InsufficientDataError) as exc_info:
            await tool.search_company_info("INVALID")
        
        assert "No company information found for INVALID" in str(exc_info.value)
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_company_info_api_error(self, mock_tavily_client, research_tool):
        """Test company information search with API error."""
        # Setup mock to raise exception
        mock_client_instance = Mock()
        mock_client_instance.search.side_effect = Exception("API connection failed")
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute and verify exception
        with pytest.raises(APIError) as exc_info:
            await tool.search_company_info("AAPL")
        
        assert "Failed to search company information for AAPL" in str(exc_info.value)
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_recent_news_success(self, mock_tavily_client, research_tool, mock_news_response):
        """Test successful recent news search."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = mock_news_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute
        result = await tool.search_recent_news("AAPL")
        
        # Verify
        assert isinstance(result, list)
        assert len(result) == 2
        
        for news_item in result:
            assert isinstance(news_item, NewsItem)
            assert news_item.title
            assert news_item.summary
            assert news_item.url
            assert isinstance(news_item.published_date, datetime)
        
        # Check specific content
        assert "Apple Reports Strong Q4 Earnings" in result[0].title
        assert "Apple Announces New Product Line" in result[1].title
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_recent_news_empty_results(self, mock_tavily_client, research_tool, empty_response):
        """Test recent news search with empty results."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = empty_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute
        result = await tool.search_recent_news("UNKNOWN")
        
        # Verify
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_recent_news_api_error(self, mock_tavily_client, research_tool):
        """Test recent news search with API error."""
        # Setup mock to raise exception
        mock_client_instance = Mock()
        mock_client_instance.search.side_effect = Exception("Network timeout")
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute and verify exception
        with pytest.raises(APIError) as exc_info:
            await tool.search_recent_news("AAPL")
        
        assert "Failed to search recent news for AAPL" in str(exc_info.value)
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_financial_metrics_success(self, mock_tavily_client, research_tool, mock_financial_response):
        """Test successful financial metrics search."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = mock_financial_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute
        result = await tool.search_financial_metrics("AAPL")
        
        # Verify
        assert isinstance(result, FinancialMetrics)
        # Note: Our current implementation returns None values as it's a placeholder
        # In a real implementation, these would be parsed from the content
    
    @patch('common.utils.TavilyClient')
    @pytest.mark.asyncio
    async def test_search_financial_metrics_insufficient_data(self, mock_tavily_client, research_tool, empty_response):
        """Test financial metrics search with insufficient data."""
        # Setup mock
        mock_client_instance = Mock()
        mock_client_instance.search.return_value = empty_response
        mock_tavily_client.return_value = mock_client_instance
        
        # Create new tool instance to use mocked client
        tool = TavilyResearchTool(research_tool.config)
        
        # Execute and verify exception
        with pytest.raises(InsufficientDataError) as exc_info:
            await tool.search_financial_metrics("INVALID")
        
        assert "No financial metrics found for INVALID" in str(exc_info.value)
    
    def test_extract_company_info(self, research_tool):
        """Test company information extraction from search results."""
        results = [
            {
                "title": "Apple Inc. Profile",
                "content": "Apple Inc. is a technology company in the consumer electronics industry.",
                "url": "https://example.com"
            }
        ]
        
        company_info = research_tool._extract_company_info("AAPL", results)
        
        assert isinstance(company_info, CompanyInfo)
        assert company_info.symbol == "AAPL"
        assert company_info.name == "AAPL Corporation"
        assert company_info.sector == "Technology"
        assert company_info.industry == "Software"
    
    def test_extract_news_items(self, research_tool):
        """Test news items extraction from search results."""
        results = [
            {
                "title": "Test News Title",
                "content": "This is test news content that should be extracted properly.",
                "url": "https://example.com/news1"
            },
            {
                "title": "Another News Item",
                "content": "Another piece of news content for testing extraction.",
                "url": "https://example.com/news2"
            }
        ]
        
        news_items = research_tool._extract_news_items(results)
        
        assert len(news_items) == 2
        assert all(isinstance(item, NewsItem) for item in news_items)
        assert news_items[0].title == "Test News Title"
        assert news_items[1].title == "Another News Item"
        assert all(item.url for item in news_items)
    
    def test_extract_news_items_invalid_data(self, research_tool):
        """Test news items extraction with invalid data."""
        results = [
            {"title": "", "content": "", "url": ""},  # Empty data
            {"title": "Valid Title"},  # Missing content
            {"content": "Valid content"},  # Missing title
        ]
        
        news_items = research_tool._extract_news_items(results)
        
        # Should skip invalid items
        assert len(news_items) == 0
    
    def test_extract_financial_metrics(self, research_tool):
        """Test financial metrics extraction from search results."""
        results = [
            {
                "title": "AAPL Financial Data",
                "content": "Apple stock price $185.50, PE ratio 28.5, volume 45M",
                "url": "https://example.com"
            }
        ]
        
        metrics = research_tool._extract_financial_metrics("AAPL", results)
        
        assert isinstance(metrics, FinancialMetrics)
        # Note: Current implementation returns None values as it's a placeholder
    
    def test_extract_field(self, research_tool):
        """Test field extraction from content."""
        content = "Apple Inc. is a technology company in the software industry."
        
        # Test company name extraction
        name = research_tool._extract_field(content, "AAPL", "company name")
        assert name == "AAPL Corporation"
        
        # Test with default value
        unknown_field = research_tool._extract_field(content, "AAPL", "unknown_field", "default_value")
        assert unknown_field == "default_value"
        
        # Test without default value
        another_field = research_tool._extract_field(content, "AAPL", "another_field")
        assert another_field == "Unknown another_field"
    
    @pytest.mark.asyncio
    async def test_search_with_network_timeout(self, research_tool):
        """Test handling of network timeouts."""
        with patch('common.utils.TavilyClient') as mock_tavily_client:
            mock_client_instance = Mock()
            mock_client_instance.search.side_effect = TimeoutError("Network timeout")
            mock_tavily_client.return_value = mock_client_instance
            
            tool = TavilyResearchTool(research_tool.config)
            
            with pytest.raises(APIError) as exc_info:
                await tool.search_company_info("AAPL")
            
            assert "Failed to search company information" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_search_with_rate_limit(self, research_tool):
        """Test handling of API rate limits."""
        with patch('common.utils.TavilyClient') as mock_tavily_client:
            mock_client_instance = Mock()
            mock_client_instance.search.side_effect = Exception("Rate limit exceeded")
            mock_tavily_client.return_value = mock_client_instance
            
            tool = TavilyResearchTool(research_tool.config)
            
            with pytest.raises(APIError) as exc_info:
                await tool.search_recent_news("AAPL")
            
            assert "Failed to search recent news" in str(exc_info.value)
    
    def test_tavily_config_validation(self):
        """Test TavilyConfig validation."""
        # Test valid config
        config = TavilyConfig(api_key="test_key")
        tool = TavilyResearchTool(config)
        assert tool.config.api_key == "test_key"
        assert tool.config.max_results == 10
        assert tool.config.search_depth == "advanced"
    
    @pytest.mark.asyncio
    async def test_search_with_malformed_response(self, research_tool):
        """Test handling of malformed API responses."""
        with patch('common.utils.TavilyClient') as mock_tavily_client:
            mock_client_instance = Mock()
            # Return malformed response
            mock_client_instance.search.return_value = {"invalid": "response"}
            mock_tavily_client.return_value = mock_client_instance
            
            tool = TavilyResearchTool(research_tool.config)
            
            with pytest.raises(InsufficientDataError):
                await tool.search_company_info("AAPL")
    
    def test_extract_company_info_edge_cases(self, research_tool):
        """Test company info extraction with edge cases."""
        # Test with empty results
        empty_results = []
        company_info = research_tool._extract_company_info("AAPL", empty_results)
        assert company_info.symbol == "AAPL"
        assert company_info.name == "AAPL Corporation"
        
        # Test with results containing minimal data
        minimal_results = [{"title": "Test", "content": "", "url": ""}]
        company_info = research_tool._extract_company_info("GOOGL", minimal_results)
        assert company_info.symbol == "GOOGL"
        assert company_info.name == "GOOGL Corporation"
    
    def test_extract_news_items_edge_cases(self, research_tool):
        """Test news extraction with edge cases."""
        # Test with malformed results
        malformed_results = [
            {"title": "Valid Title"},  # Missing content and url
            {"content": "Valid content"},  # Missing title
            {"url": "https://example.com"},  # Missing title and content
            {"title": "", "content": "", "url": ""},  # Empty strings
        ]
        
        news_items = research_tool._extract_news_items(malformed_results)
        assert len(news_items) == 0  # Should skip all malformed items
    
    def test_extract_financial_metrics_edge_cases(self, research_tool):
        """Test financial metrics extraction with edge cases."""
        # Test with empty results
        empty_results = []
        metrics = research_tool._extract_financial_metrics("AAPL", empty_results)
        assert isinstance(metrics, FinancialMetrics)
        # All fields should be None in current implementation
        assert metrics.current_price is None
        assert metrics.volume is None
        
        # Test with results containing no financial data
        no_data_results = [{"title": "News", "content": "No financial data", "url": ""}]
        metrics = research_tool._extract_financial_metrics("AAPL", no_data_results)
        assert isinstance(metrics, FinancialMetrics)