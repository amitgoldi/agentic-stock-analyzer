"""
Lecture 01: Single Agent Stock Analysis

This module demonstrates a single AI agent that uses web search to analyze stocks.
The agent gathers information from the web and provides comprehensive stock reports.

Usage:
    python -m lecture01.main [STOCK_SYMBOL]
    
Example:
    python -m lecture01.main AAPL
    python -m lecture01.main TSLA
"""

import sys
import asyncio
import logging
from typing import Optional

# Import logfire for observability
try:
    import logfire
    LOGFIRE_AVAILABLE = True
except ImportError:
    LOGFIRE_AVAILABLE = False
    print("Warning: logfire not available. Install with: pip install 'pydantic-ai-slim[logfire]'")

from common.config import config
from common.utils import setup_logging, print_section_header, print_subsection_header
from lecture01.agent import StockAnalysisAgent

logger = logging.getLogger(__name__)


def setup_logfire() -> None:
    """Set up Logfire integration if available and enabled."""
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
            environment='development',
            service_name='stock-analysis-lecture01',
            inspect_arguments=False,  # Suppress warnings in demo environment
        )
        
        # Instrument Pydantic AI
        logfire.instrument_pydantic_ai()
        
        # Optionally instrument HTTP requests to see API calls
        logfire.instrument_httpx(capture_all=True)
        
        # Send a test message to verify connection
        logfire.info("🚀 Tikal Lecture 01 - Stock Analysis Agent Started", extra={"stock_symbol": "demo"})
        
        logger.info("Logfire instrumentation configured successfully")
        logger.info(f"Logfire project: {config.LOGFIRE_PROJECT_ID}")
        logger.info(f"Logfire token configured: {config.LOGFIRE_API_KEY[:20]}...")
        logger.info("✅ Check your Logfire dashboard for traces!")
        
    except Exception as e:
        logger.warning(f"Failed to configure Logfire: {e}")
        logger.info("Logfire traces will still appear in console output")


def print_report(report, symbol: str) -> None:
    """Print the stock report in a formatted way."""
    print_section_header(f"STOCK ANALYSIS REPORT: {symbol}")
    
    print(f"Company: {report.company_name}")
    print(f"Symbol: {report.symbol}")
    print(f"Analysis Date: {report.analysis_date}")
    
    if report.current_price is not None:
        print(f"Current Price: ${report.current_price:.2f}")
    
    if report.price_change is not None and report.price_change_percent is not None:
        change_sign = "+" if report.price_change >= 0 else ""
        print(f"Price Change: {change_sign}${report.price_change:.2f} ({change_sign}{report.price_change_percent:.2f}%)")
    
    print_subsection_header("EXECUTIVE SUMMARY")
    print(report.executive_summary)
    
    if report.recent_news:
        print_subsection_header("RECENT NEWS")
        for i, news in enumerate(report.recent_news, 1):
            print(f"{i}. {news}")
    
    if report.financial_highlights:
        print_subsection_header("FINANCIAL HIGHLIGHTS")
        for i, highlight in enumerate(report.financial_highlights, 1):
            print(f"{i}. {highlight}")
    
    print_subsection_header("MARKET SENTIMENT")
    print(report.market_sentiment)
    
    if report.risk_factors:
        print_subsection_header("RISK FACTORS")
        for i, risk in enumerate(report.risk_factors, 1):
            print(f"{i}. {risk}")
    
    print_subsection_header("RECOMMENDATION")
    print(report.recommendation)
    
    if report.data_sources:
        print_subsection_header("DATA SOURCES")
        for i, source in enumerate(report.data_sources, 1):
            print(f"{i}. {source}")


async def analyze_stock_async(symbol: str) -> None:
    """Analyze a stock asynchronously."""
    try:
        print_section_header("INITIALIZING STOCK ANALYSIS AGENT")
        print(f"Model: {config.AGENT_MODEL}")
        print(f"Temperature: {config.AGENT_TEMPERATURE}")
        print(f"Max Results: {config.TAVILY_MAX_RESULTS}")
        print(f"Search Depth: {config.TAVILY_SEARCH_DEPTH}")
        
        # Create the agent
        agent = StockAnalysisAgent()
        
        print_section_header("STARTING ANALYSIS")
        print(f"Analyzing stock: {symbol}")
        print("This may take a few moments as the agent searches for information...")
        
        # Analyze the stock
        report = await agent.analyze_stock(symbol)
        
        # Print the results
        print_report(report, symbol)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"\nERROR: Analysis failed - {e}")
        sys.exit(1)


def analyze_stock_sync(symbol: str) -> None:
    """Analyze a stock synchronously."""
    try:
        print_section_header("INITIALIZING STOCK ANALYSIS AGENT")
        print(f"Model: {config.AGENT_MODEL}")
        print(f"Temperature: {config.AGENT_TEMPERATURE}")
        print(f"Max Results: {config.TAVILY_MAX_RESULTS}")
        print(f"Search Depth: {config.TAVILY_SEARCH_DEPTH}")
        
        # Create the agent
        agent = StockAnalysisAgent()
        
        print_section_header("STARTING ANALYSIS")
        print(f"Analyzing stock: {symbol}")
        print("This may take a few moments as the agent searches for information...")
        
        # Analyze the stock synchronously
        report = agent.analyze_stock_sync(symbol)
        
        # Print the results
        print_report(report, symbol)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"\nERROR: Analysis failed - {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    # Set up logging
    setup_logging()
    
    # Set up Logfire instrumentation
    setup_logfire()
    
    # Get stock symbol from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python -m lecture01.main <STOCK_SYMBOL>")
        print("Example: python -m lecture01.main AAPL")
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    
    print_section_header("TIKAL LECTURE 01: SINGLE AGENT STOCK ANALYSIS")
    print("This demo shows a single AI agent using web search to analyze stocks.")
    print(f"Target Stock: {symbol}")
    
    # Run the analysis synchronously for simplicity in demo
    analyze_stock_sync(symbol)


if __name__ == "__main__":
    main()
