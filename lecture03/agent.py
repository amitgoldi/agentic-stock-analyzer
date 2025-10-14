"""
Enhanced Financial Assistant Agent

This is the lecture01 Financial Assistant enhanced with an additional tool:
the stock_report tool that internally delegates to the lecture02 stock analysis agent.

This demonstrates how to extend a basic agent with additional capabilities by
adding specialized tools without modifying the core agent structure.
"""

import logging
from typing import Any

from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from common.models import StockReport
from common.tools import web_search_tool
from common.utils import create_agent_model
from lecture02.agent import analyze_stock

logger = logging.getLogger(__name__)


def create_stock_report_tool() -> Tool:
    """
    Create a stock_report tool that delegates to lecture02's stock analysis agent.

    This tool wraps the analyze_stock function from lecture02, allowing our
    enhanced financial assistant to provide detailed stock analysis on demand.
    """

    async def stock_report(ctx: RunContext, symbol: str) -> StockReport:
        """
        Get a detailed stock analysis report for a given symbol.

        This tool delegates to the lecture02 stock analysis agent to get
        comprehensive analysis of individual stocks.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

        Returns:
            StockReport: Detailed analysis report for the stock
        """
        logger.info(f"Delegating stock analysis for {symbol} to lecture02 agent")
        return await analyze_stock(symbol)

    return Tool(
        stock_report,
        description="Get a detailed stock analysis report for a given stock symbol (e.g., AAPL, TSLA). "
        "Returns comprehensive analysis including financials, news, sentiment, and recommendations.",
    )


# Create the stock_report tool instance
stock_report_tool = create_stock_report_tool()


# Create the enhanced financial assistant agent
# This is identical to lecture01's agent but with the additional stock_report_tool
enhanced_financial_agent = Agent(
    model=create_agent_model(),
    tools=[web_search_tool, stock_report_tool],  # Same as lecture01 + stock_report_tool
    system_prompt="""
You are a knowledgeable financial assistant. Your role is to help users with financial questions,
investment advice, market analysis, and general financial guidance.

When answering questions:
1. Use the web_search tool to get current, up-to-date financial information when relevant
2. Use the stock_report tool when users ask for detailed analysis of specific stocks
   - The stock_report tool provides comprehensive reports including financials, news, sentiment, and recommendations
   - Use it whenever someone asks for detailed information about a specific stock
3. Combine web search results and stock reports with your financial knowledge
4. Provide clear, actionable advice
5. Always mention when information is based on web search vs. stock reports vs. general knowledge
6. Include appropriate disclaimers for investment advice
7. Be helpful but remind users to consult with financial professionals for major decisions

Keep your responses informative but concise, and always prioritize accuracy and user safety.
""",
)


async def ask_financial_question(question: str) -> str:
    """
    Ask the enhanced financial assistant a question.

    This function is identical to lecture01's version but uses the enhanced agent
    that has access to the stock_report tool.

    Args:
        question: The financial question to ask

    Returns:
        The assistant's response
    """
    try:
        result = await enhanced_financial_agent.run(question)
        return result.output
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return f"Error processing your question: {str(e)}"


def get_agent_info() -> dict[str, Any]:
    """Get information about the enhanced financial agent."""
    return {
        "name": "Enhanced Financial Assistant",
        "description": "Financial assistant from lecture01 enhanced with stock_report tool from lecture02",
        "tools": ["web_search_tool", "stock_report_tool"],
        "capabilities": [
            "Answer financial questions",
            "Provide investment guidance",
            "Search for current market information",
            "Generate detailed stock analysis reports",  # NEW capability
            "Offer general financial advice",
        ],
        "enhancements": [
            "Can provide comprehensive stock analysis using the lecture02 agent",
            "Combines web search with specialized stock analysis",
        ],
        "limitations": [
            "Not a replacement for professional financial advice",
            "Relies on web search and analysis tools for current data",
            "General guidance only, not personalized advice",
        ],
    }
