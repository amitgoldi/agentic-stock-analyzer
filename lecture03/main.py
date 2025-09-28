"""
Lecture 03: Agent Delegation Pattern

This module demonstrates the Agent Delegation communication pattern where
a primary agent (StockRecommender) delegates specific tasks to specialized
agents (StockAnalysisAgent) through tool calls.

Usage:
    python -m lecture03.main

The agent will automatically:
1. Search for trending/up-and-coming stocks
2. Select 3 interesting candidates
3. Get detailed reports for each using StockAnalysisAgent
4. Compare and provide recommendations
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
from lecture03.agent import StockRecommender

logger = logging.getLogger(__name__)


def print_recommendation_report(report) -> None:
    """Print the stock recommendation report in a formatted way."""
    print_section_header("STOCK RECOMMENDATION REPORT")

    print(f"Analysis Date: {report.analysis_date}")
    print()

    print_subsection_header("MARKET OVERVIEW")
    print(report.market_overview)
    print()

    print_subsection_header("SELECTION CRITERIA")
    print(report.selection_criteria)
    print()

    # Print each recommendation
    for i, rec in enumerate(report.recommendations, 1):
        print_subsection_header(f"RECOMMENDATION #{i}: {rec.symbol}")
        print(f"Company: {rec.company_name}")
        print(f"Symbol: {rec.symbol}")
        print(f"Recommendation: {rec.recommendation_type}")
        print(f"Confidence Level: {rec.confidence_level}")
        print(f"Time Horizon: {rec.time_horizon}")

        if rec.potential_upside:
            print(f"Potential Upside: {rec.potential_upside}")

        if rec.key_reasons:
            print("\nKey Reasons:")
            for j, reason in enumerate(rec.key_reasons, 1):
                print(f"  {j}. {reason}")

        if rec.main_risks:
            print("\nMain Risks:")
            for j, risk in enumerate(rec.main_risks, 1):
                print(f"  {j}. {risk}")

        print()

    print_subsection_header("COMPARATIVE ANALYSIS")
    print(report.comparative_analysis)
    print()

    print_subsection_header("MARKET OUTLOOK")
    print(report.market_outlook)
    print()

    print_subsection_header("DISCLAIMER")
    print(report.disclaimer)


async def get_recommendations_async() -> None:
    """Get stock recommendations asynchronously."""
    try:
        print_section_header("INITIALIZING STOCK RECOMMENDER AGENT")
        print(f"Model: {config.AGENT_MODEL}")
        print(f"Temperature: {config.AGENT_TEMPERATURE}")
        print(f"Max Results: {config.TAVILY_MAX_RESULTS}")
        print(f"Search Depth: {config.TAVILY_SEARCH_DEPTH}")
        print()
        print("Agent Delegation Pattern:")
        print("- Primary Agent: StockRecommender (orchestrates workflow)")
        print("- Specialized Agent: StockAnalysisAgent (provides detailed analysis)")
        print("- Communication: Tool-based delegation")

        # Create the agent
        agent = StockRecommender()

        print_section_header("STARTING RECOMMENDATION PROCESS")
        print("The agent will:")
        print("1. Search for trending/up-and-coming stocks")
        print("2. Select 3 interesting candidates")
        print("3. Delegate detailed analysis to StockAnalysisAgent for each")
        print("4. Compare results and provide recommendations")
        print()
        print("This may take several minutes as the agent performs multiple searches")
        print("and delegates analysis to the specialized agent...")

        # Get recommendations
        report = await agent.get_recommendations()

        # Print the results
        print_recommendation_report(report)

    except Exception as e:
        logger.error(f"Recommendation process failed: {e}")
        print(f"\nERROR: Recommendation process failed - {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    # Set up logging
    setup_logging()

    # Set up Logfire instrumentation
    setup_logfire(
        service_name="stock-analysis-lecture03",
        start_message="🚀 Tikal Lecture 03 - Agent Delegation Pattern Started",
        extra_data={"pattern": "delegation"},
    )

    print_section_header("TIKAL LECTURE 03: AGENT DELEGATION PATTERN")
    print("This demo shows the Agent Delegation communication pattern where")
    print("a primary agent delegates specific tasks to specialized agents.")
    print()
    print("Architecture:")
    print("- StockRecommender: Primary agent that orchestrates the workflow")
    print("- StockAnalysisAgent: Specialized agent for detailed stock analysis")
    print(
        "- Communication: The primary agent calls the specialized agent through tools"
    )

    # Run the recommendation process asynchronously using asyncio
    asyncio.run(get_recommendations_async())


if __name__ == "__main__":
    main()
