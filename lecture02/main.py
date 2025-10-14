"""
Lecture 02: Single Agent Stock Analysis

This module demonstrates a single AI agent that uses web search to analyze stocks.
The agent gathers information from the web and provides comprehensive stock reports.

Usage:
    python -m lecture02.main [STOCK_SYMBOL]

Example:
    python -m lecture02.main AAPL
    python -m lecture02.main TSLA
"""

import asyncio
import logging
import sys

from common.config import config
from common.utils import (
    print_section_header,
    print_subsection_header,
    setup_logfire,
    setup_logging,
)
from lecture02.agent import analyze_stock

logger = logging.getLogger(__name__)


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
        print(
            f"Price Change: {change_sign}${report.price_change:.2f} ({change_sign}{report.price_change_percent:.2f}%)"
        )

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

        print_section_header("STARTING ANALYSIS")
        print(f"Analyzing stock: {symbol}")
        print("This may take a few moments as the agent searches for information...")

        # Analyze the stock
        report = await analyze_stock(symbol)

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
    setup_logfire(
        service_name="stock-analysis-lecture02",
        start_message="🚀 Tikal Lecture 02 - Stock Analysis Agent Started",
        extra_data={"stock_symbol": "demo"},
    )

    # Get stock symbol from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python -m lecture02.main <STOCK_SYMBOL>")
        print("Example: python -m lecture02.main AAPL")
        sys.exit(1)

    symbol = sys.argv[1].upper()

    print_section_header("TIKAL LECTURE 02: SINGLE AGENT STOCK ANALYSIS")
    print("This demo shows a single AI agent using web search to analyze stocks.")
    print(f"Target Stock: {symbol}")

    # Run the analysis asynchronously using asyncio
    asyncio.run(analyze_stock_async(symbol))


if __name__ == "__main__":
    main()
