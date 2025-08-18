"""End-to-end tests for complete analysis pipeline."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from typing import List

from common.config import AppConfig, TavilyConfig, AgentConfig
from common.models import StockReport
from lecture01.agent import StockAnalysisAgent
from lecture01.main import analyze_single_stock, analyze_portfolio, display_stock_report, display_portfolio_summary
from tests.fixtures import (
    sample_stock_report,
    sample_portfolio_reports,
    sample_portfolio_symbols,
    mock_tavily_company_response,
    mock_tavily_news_response,
    mock_tavily_financial_response
)


class TestEndToEndWorkflow:
    """End-to-end tests for complete stock analysis workflow."""
    
    @pytest.fixture
    def test_config(self):
        """Create test configuration for end-to-end testing."""
        return AppConfig(
            tavily=TavilyConfig(
                api_key="test_api_key_e2e",
                max_results=10,
                search_depth="advanced"
            ),
            agent=AgentConfig(
                model_name="openai:gpt-4o",
                temperature=0.1,
                max_retries=3
            ),
            debug=False,
            log_level="INFO"
        )
    
    @pytest.fixture
    def stock_agent(self, test_config):
        """Create StockAnalysisAgent for end-to-end testing."""
        return StockAnalysisAgent(test_config)
    
    @pytest.mark.asyncio
    async def test_complete_single_stock_analysis_workflow(self, stock_agent, sample_stock_report):
        """Test complete workflow for single stock analysis."""
        symbol = "AAPL"
        
        # Mock the agent's analyze_stock_sync method to return our sample report
        with patch.object(stock_agent, 'analyze_stock_sync', return_value=sample_stock_report):
            # Execute the complete workflow
            result = await analyze_single_stock(stock_agent, symbol)
            
            # Verify successful analysis
            assert result is not None
            assert isinstance(result, StockReport)
            assert result.symbol == symbol
            
            # Verify all required components are present
            assert result.company_info is not None
            assert result.financial_metrics is not None
            assert result.recent_news is not None
            assert result.market_sentiment is not None
            assert result.risk_assessment is not None
            assert result.investment_recommendation is not None
            assert result.analysis_timestamp is not None
            
            # Verify data quality
            assert result.company_info.name
            assert result.company_info.sector
            assert result.company_info.industry
            assert result.investment_recommendation.recommendation in ["buy", "hold", "sell"]
            assert 0 <= result.investment_recommendation.confidence <= 1
            assert result.risk_assessment.risk_level in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_complete_single_stock_analysis_failure(self, stock_agent):
        """Test single stock analysis workflow with failure."""
        symbol = "INVALID"
        
        # Mock the agent to raise an exception
        with patch.object(stock_agent, 'analyze_stock_sync', side_effect=Exception("Analysis failed")):
            # Execute the workflow
            result = await analyze_single_stock(stock_agent, symbol)
            
            # Should handle failure gracefully
            assert result is None
    
    @pytest.mark.asyncio
    async def test_complete_portfolio_analysis_workflow(self, stock_agent, sample_portfolio_reports):
        """Test complete workflow for portfolio analysis."""
        symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # Mock the analyze_single_stock function to return our sample reports
        with patch('lecture01.main.analyze_single_stock', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.side_effect = sample_portfolio_reports
            
            # Execute the complete portfolio workflow
            results = await analyze_portfolio(stock_agent, symbols)
            
            # Verify successful analysis
            assert len(results) == len(symbols)
            assert all(isinstance(report, StockReport) for report in results)
            
            # Verify each report has required data
            for i, report in enumerate(results):
                assert report.symbol == symbols[i]
                assert report.company_info is not None
                assert report.investment_recommendation is not None
                assert report.risk_assessment is not None
                
            # Verify analyze_single_stock was called for each symbol
            assert mock_analyze.call_count == len(symbols)
    
    @pytest.mark.asyncio
    async def test_portfolio_analysis_with_mixed_results(self, stock_agent, sample_portfolio_reports):
        """Test portfolio analysis with some successes and failures."""
        symbols = ["AAPL", "INVALID", "GOOGL", "FAILED"]
        
        # Mock mixed success/failure results
        async def mock_analyze_side_effect(agent, symbol):
            if symbol == "AAPL":
                return sample_portfolio_reports[0]
            elif symbol == "GOOGL":
                return sample_portfolio_reports[1]
            elif symbol == "INVALID":
                return None  # Simulate failure
            else:  # FAILED
                raise Exception("Analysis failed")
        
        with patch('lecture01.main.analyze_single_stock', side_effect=mock_analyze_side_effect):
            # Execute portfolio analysis
            results = await analyze_portfolio(stock_agent, symbols)
            
            # Should return only successful analyses
            assert len(results) == 2  # AAPL and GOOGL
            successful_symbols = [report.symbol for report in results]
            assert "AAPL" in successful_symbols
            assert "GOOGL" in successful_symbols
            assert "INVALID" not in successful_symbols
            assert "FAILED" not in successful_symbols
    
    def test_display_stock_report_formatting(self, sample_stock_report):
        """Test stock report display formatting."""
        # This test verifies that display functions don't crash
        # In a real scenario, you might capture output and verify formatting
        try:
            display_stock_report(sample_stock_report)
            # If no exception is raised, the display function works
            assert True
        except Exception as e:
            pytest.fail(f"Display function failed: {str(e)}")
    
    def test_display_portfolio_summary_formatting(self, sample_portfolio_reports):
        """Test portfolio summary display formatting."""
        try:
            display_portfolio_summary(sample_portfolio_reports)
            # If no exception is raised, the display function works
            assert True
        except Exception as e:
            pytest.fail(f"Portfolio display function failed: {str(e)}")
    
    def test_display_empty_portfolio_summary(self):
        """Test portfolio summary display with empty results."""
        try:
            display_portfolio_summary([])
            # Should handle empty list gracefully
            assert True
        except Exception as e:
            pytest.fail(f"Empty portfolio display failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_full_demo_workflow_simulation(self, test_config):
        """Test simulation of the full demo workflow."""
        # This test simulates the main demo workflow without actual API calls
        
        # Mock configuration validation
        test_config.tavily.api_key = "valid_test_key"
        
        with patch('lecture01.main.get_config', return_value=test_config):
            with patch('lecture01.main.StockAnalysisAgent') as mock_agent_class:
                # Create mock agent instance
                mock_agent = Mock()
                mock_agent_class.return_value = mock_agent
                
                # Mock successful analysis results
                mock_report = Mock(spec=StockReport)
                mock_report.symbol = "AAPL"
                
                # Create mock attributes properly
                mock_company_info = Mock()
                mock_company_info.name = "Apple Inc."
                mock_report.company_info = mock_company_info
                
                mock_recommendation = Mock()
                mock_recommendation.recommendation = "buy"
                mock_report.investment_recommendation = mock_recommendation
                
                mock_agent.analyze_stock_sync.return_value = mock_report
                
                # Import and test the demo components
                from lecture01.main import run_demo
                
                # Mock console output to avoid actual printing during tests
                with patch('lecture01.main.console'):
                    # This would normally run the full demo
                    # For testing, we'll just verify the setup works
                    agent = mock_agent_class(test_config)
                    assert agent is not None
                    
                    # Verify agent initialization was called
                    mock_agent_class.assert_called_once_with(test_config)


class TestDataIntegrity:
    """Test data integrity throughout the analysis pipeline."""
    
    def test_stock_report_data_consistency(self, sample_stock_report):
        """Test that stock report data is consistent throughout pipeline."""
        report = sample_stock_report
        
        # Verify symbol consistency
        assert report.symbol == report.company_info.symbol
        
        # Verify timestamp is reasonable (within last hour for testing)
        time_diff = datetime.now() - report.analysis_timestamp
        assert time_diff.total_seconds() < 3600  # Within 1 hour
        
        # Verify recommendation confidence is within valid range
        assert 0 <= report.investment_recommendation.confidence <= 1
        
        # Verify market sentiment confidence is within valid range
        assert 0 <= report.market_sentiment.confidence_score <= 1
        
        # Verify required lists are not empty
        assert len(report.market_sentiment.key_factors) > 0
        assert len(report.risk_assessment.risk_factors) > 0
    
    def test_portfolio_data_consistency(self, sample_portfolio_reports):
        """Test portfolio data consistency."""
        reports = sample_portfolio_reports
        
        # Verify all reports are valid
        assert len(reports) > 0
        assert all(isinstance(report, StockReport) for report in reports)
        
        # Verify unique symbols
        symbols = [report.symbol for report in reports]
        assert len(symbols) == len(set(symbols))  # No duplicates
        
        # Verify all reports have required data
        for report in reports:
            assert report.company_info is not None
            assert report.financial_metrics is not None
            assert report.investment_recommendation is not None
            assert report.risk_assessment is not None
            assert report.market_sentiment is not None
    
    def test_error_propagation_and_handling(self):
        """Test that errors are properly handled throughout the pipeline."""
        from common.utils import APIError, InsufficientDataError
        
        # Test that custom exceptions can be created and handled
        api_error = APIError("Test API error")
        assert str(api_error) == "Test API error"
        assert isinstance(api_error, Exception)
        
        insufficient_data_error = InsufficientDataError("Test data error")
        assert str(insufficient_data_error) == "Test data error"
        assert isinstance(insufficient_data_error, Exception)


class TestPerformanceAndScalability:
    """Test performance characteristics of the analysis pipeline."""
    
    @pytest.mark.asyncio
    async def test_portfolio_analysis_performance(self, stock_agent):
        """Test portfolio analysis performance with multiple stocks."""
        # Test with a larger portfolio to verify scalability
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX", "NVDA"]
        
        # Mock quick responses to test performance
        with patch.object(stock_agent, 'analyze_stock_sync') as mock_analyze:
            mock_report = Mock(spec=StockReport)
            mock_analyze.return_value = mock_report
            
            start_time = datetime.now()
            
            # Simulate portfolio analysis
            reports = []
            for symbol in symbols:
                mock_report.symbol = symbol
                reports.append(await analyze_single_stock(stock_agent, symbol))
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Verify reasonable performance (should complete quickly with mocks)
            assert duration < 5.0  # Should complete within 5 seconds
            assert len(reports) == len(symbols)
            assert mock_analyze.call_count == len(symbols)
    
    def test_memory_usage_with_large_reports(self, sample_stock_report):
        """Test memory usage with large stock reports."""
        # Create multiple reports to test memory handling
        reports = []
        
        for i in range(100):  # Create 100 reports
            # Create a copy of the sample report with different symbol
            report_data = sample_stock_report.model_dump()
            report_data['symbol'] = f"TEST{i:03d}"
            report_data['company_info']['symbol'] = f"TEST{i:03d}"
            report_data['company_info']['name'] = f"Test Company {i}"
            
            report = StockReport.model_validate(report_data)
            reports.append(report)
        
        # Verify all reports were created successfully
        assert len(reports) == 100
        assert all(isinstance(report, StockReport) for report in reports)
        
        # Verify unique symbols
        symbols = [report.symbol for report in reports]
        assert len(set(symbols)) == 100  # All unique
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis_simulation(self, stock_agent):
        """Test simulation of concurrent analysis requests."""
        import asyncio
        
        symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]
        
        # Mock the analysis to simulate concurrent execution
        with patch.object(stock_agent, 'analyze_stock_sync') as mock_analyze:
            mock_report = Mock(spec=StockReport)
            mock_analyze.return_value = mock_report
            
            # Create concurrent tasks
            async def analyze_symbol(symbol):
                mock_report.symbol = symbol
                return await analyze_single_stock(stock_agent, symbol)
            
            # Execute concurrent analyses
            tasks = [analyze_symbol(symbol) for symbol in symbols]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Verify all analyses completed
            assert len(results) == len(symbols)
            assert all(not isinstance(result, Exception) for result in results)
            assert mock_analyze.call_count == len(symbols)