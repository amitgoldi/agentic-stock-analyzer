"""
Workflow Pattern: Financial Assistant with Multi-Agent Stock Report

This demonstrates the workflow communication pattern where the stock_report_tool
orchestrates two specialized agents in sequence:

1. Stock Analysis Agent: Gathers comprehensive stock information (without recommendation)
2. Recommendation Agent: Generates investment recommendation based on the analysis

The workflow combines both outputs to create the final StockReport.
"""

import logging
from typing import Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from common.models import StockReport
from common.tools import web_search_tool
from common.utils import create_agent_model, get_current_date, validate_stock_symbol

logger = logging.getLogger(__name__)


# Intermediate model for stock analysis (without recommendation)
class StockAnalysis(BaseModel):
    """Stock analysis without recommendation - output from first agent."""

    symbol: str = Field(description="Stock symbol (e.g., AAPL, TSLA)")
    company_name: str = Field(description="Full company name")
    current_price: float | None = Field(description="Current stock price", default=None)
    price_change: float | None = Field(
        description="Price change from previous close", default=None
    )
    price_change_percent: float | None = Field(
        description="Price change percentage", default=None
    )
    executive_summary: str = Field(description="Brief executive summary of the stock")
    recent_news: list[str] = Field(
        description="Key recent news items affecting the stock", default_factory=list
    )
    financial_highlights: list[str] = Field(
        description="Key financial metrics and highlights", default_factory=list
    )
    market_sentiment: str = Field(description="Overall market sentiment analysis")
    risk_factors: list[str] = Field(
        description="Key risk factors to consider", default_factory=list
    )
    analysis_date: str = Field(description="Date when analysis was performed")
    data_sources: list[str] = Field(
        description="Sources used for the analysis", default_factory=list
    )


# Model for recommendation only
class StockRecommendationOnly(BaseModel):
    """Investment recommendation based on stock analysis."""

    recommendation: str = Field(description="Investment recommendation with reasoning")


# Create the stock analysis agent (Agent 1)
stock_analysis_agent = Agent(
    model=create_agent_model(),
    tools=[web_search_tool],
    output_type=StockAnalysis,
    system_prompt="""
You are an expert financial analyst specializing in stock research and data gathering.

Your task is to create comprehensive stock analysis by gathering current information about publicly traded companies.
You should gather ALL information EXCEPT for making investment recommendations - that will be done by a separate specialist.

CAPABILITIES:
- You have access to a web search tool for real-time information
- You can search for financial news, earnings reports, analyst opinions, and market data
- You should gather information from multiple reliable sources

ANALYSIS FRAMEWORK:
When analyzing a stock, you should:

1. **Company Overview**: Get basic company information, business model, and recent developments
2. **Financial Performance**: Look for recent earnings, revenue trends, and key financial metrics
3. **Market Position**: Research competitive landscape and market share
4. **Recent News**: Find recent news that could impact the stock price
5. **Market Sentiment**: Gauge overall market sentiment toward the stock
6. **Risk Assessment**: Identify potential risks and challenges

SEARCH STRATEGY:
- Use multiple targeted searches to gather comprehensive information
- Search for recent news (last 3-6 months) for current relevance
- Look for both positive and negative information to provide balanced analysis
- Verify information from multiple sources when possible
- Focus on reputable financial news sources and official company communications

OUTPUT REQUIREMENTS:
- Provide factual, objective analysis
- Include specific data points when available (prices, percentages, dates)
- Cite your sources and indicate when information is current
- Clearly distinguish between facts and opinions/projections
- If certain information is not available, acknowledge this rather than speculating

Remember: Focus on gathering and analyzing information. Do NOT provide investment recommendations.
    """.strip(),
)


# Create the recommendation agent (Agent 2)
recommendation_agent = Agent(
    model=create_agent_model(),
    output_type=StockRecommendationOnly,
    system_prompt="""
You are an expert investment advisor specializing in making stock recommendations.

Your task is to provide investment recommendations based on comprehensive stock analysis data
that has been prepared for you by a research team.

ANALYSIS APPROACH:
- Review the complete stock analysis provided to you
- Consider the financial performance, market sentiment, risks, and recent news
- Synthesize all information to form a clear investment recommendation

RECOMMENDATION FRAMEWORK:
Your recommendation should include:
1. Clear action (Buy, Hold, Sell, or variations like Strong Buy, etc.)
2. Reasoning based on the analysis data
3. Time horizon considerations
4. Key factors supporting your recommendation
5. Important caveats or conditions

GUIDELINES:
- Be specific and actionable
- Balance optimism with realism
- Acknowledge both opportunities and risks
- Provide context for your recommendation
- Include appropriate disclaimers about investment risks
- Your recommendation should be comprehensive (3-5 sentences minimum)

Remember: You're providing professional investment guidance based on thorough analysis.
Be thoughtful, balanced, and clear in your recommendations.
    """.strip(),
)


def create_workflow_stock_report_tool() -> Tool:
    """
    Create a stock_report tool that implements a workflow pattern.

    This tool orchestrates two agents in sequence:
    1. Stock Analysis Agent - Gathers comprehensive stock information
    2. Recommendation Agent - Generates investment recommendation

    The workflow combines both outputs to create the final StockReport.
    """

    async def stock_report(ctx: RunContext, symbol: str) -> StockReport:
        """
        Get a detailed stock analysis report using a multi-agent workflow.

        This tool implements a workflow pattern where multiple specialized agents
        work in sequence to create a comprehensive stock report:

        Workflow Steps:
        1. Agent 1 (Analysis): Gathers all stock information except recommendation
        2. Agent 2 (Recommendation): Generates investment advice based on step 1
        3. Workflow: Combines both results into complete StockReport

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

        Returns:
            StockReport: Complete analysis report with recommendation
        """
        # Validate and normalize the stock symbol
        normalized_symbol = validate_stock_symbol(symbol)

        logger.info(f"Starting workflow for stock report: {normalized_symbol}")

        # Step 1: Run the stock analysis agent to gather information
        logger.info(f"Step 1: Running stock analysis agent for {normalized_symbol}")

        analysis_prompt = f"""
Please analyze the stock {normalized_symbol} and provide comprehensive information.

The analysis date should be: {get_current_date()}
        """.strip()

        analysis_result = await stock_analysis_agent.run(analysis_prompt)
        stock_analysis = analysis_result.output

        logger.info(f"Step 1 completed: Analysis gathered for {normalized_symbol}")

        # Step 2: Run the recommendation agent based on the analysis
        logger.info(f"Step 2: Running recommendation agent for {normalized_symbol}")

        recommendation_prompt = f"""
Based on the following comprehensive stock analysis for {normalized_symbol},
please provide your investment recommendation.

STOCK ANALYSIS:
Symbol: {stock_analysis.symbol}
Company: {stock_analysis.company_name}

Current Price: {stock_analysis.current_price if stock_analysis.current_price else 'N/A'}
Price Change: {stock_analysis.price_change if stock_analysis.price_change else 'N/A'} ({stock_analysis.price_change_percent if stock_analysis.price_change_percent else 'N/A'}%)

Executive Summary:
{stock_analysis.executive_summary}

Recent News:
{chr(10).join(f"- {news}" for news in stock_analysis.recent_news)}

Financial Highlights:
{chr(10).join(f"- {highlight}" for highlight in stock_analysis.financial_highlights)}

Market Sentiment:
{stock_analysis.market_sentiment}

Risk Factors:
{chr(10).join(f"- {risk}" for risk in stock_analysis.risk_factors)}

Data Sources:
{', '.join(stock_analysis.data_sources)}

Based on this analysis, what is your investment recommendation?
        """.strip()

        recommendation_result = await recommendation_agent.run(recommendation_prompt)
        recommendation_only = recommendation_result.output

        logger.info(
            f"Step 2 completed: Recommendation generated for {normalized_symbol}"
        )

        # Step 3: Combine both results into final StockReport
        logger.info(f"Step 3: Composing final report for {normalized_symbol}")

        final_report = StockReport(
            symbol=stock_analysis.symbol,
            company_name=stock_analysis.company_name,
            current_price=stock_analysis.current_price,
            price_change=stock_analysis.price_change,
            price_change_percent=stock_analysis.price_change_percent,
            executive_summary=stock_analysis.executive_summary,
            recent_news=stock_analysis.recent_news,
            financial_highlights=stock_analysis.financial_highlights,
            market_sentiment=stock_analysis.market_sentiment,
            risk_factors=stock_analysis.risk_factors,
            recommendation=recommendation_only.recommendation,
            analysis_date=stock_analysis.analysis_date,
            data_sources=stock_analysis.data_sources,
        )

        logger.info(f"Workflow completed: Final report ready for {normalized_symbol}")

        return final_report

    return Tool(
        stock_report,
        description="Get a detailed stock analysis report using a multi-agent workflow. "
        "Returns comprehensive analysis including financials, news, sentiment, and recommendations.",
    )


# Create the workflow stock_report tool instance
workflow_stock_report_tool = create_workflow_stock_report_tool()


# Create the enhanced financial assistant agent with workflow pattern
workflow_financial_agent = Agent(
    model=create_agent_model(),
    tools=[web_search_tool, workflow_stock_report_tool],
    system_prompt="""
You are a knowledgeable financial assistant. Your role is to help users with financial questions,
investment advice, market analysis, and general financial guidance.

When answering questions:
1. Use the web_search tool to get current, up-to-date financial information when relevant
2. Use the stock_report tool when users ask for detailed analysis of specific stocks
   - The stock_report tool uses a sophisticated multi-agent workflow to provide comprehensive reports
   - It combines specialized analysis from research and recommendation experts
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
    Ask the financial assistant a question using workflow-based stock analysis.

    Args:
        question: The financial question to ask

    Returns:
        The assistant's response
    """
    try:
        result = await workflow_financial_agent.run(question)
        return result.output
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return f"Error processing your question: {str(e)}"


def get_agent_info() -> dict[str, Any]:
    """Get information about the workflow-based financial agent."""
    return {
        "name": "Workflow-Based Financial Assistant",
        "description": "Financial assistant using workflow pattern for stock analysis",
        "tools": ["web_search_tool", "workflow_stock_report_tool"],
        "capabilities": [
            "Answer financial questions",
            "Provide investment guidance",
            "Search for current market information",
            "Generate detailed stock analysis reports using multi-agent workflow",
            "Offer general financial advice",
        ],
        "workflow_pattern": [
            "Stock report tool orchestrates two specialized agents",
            "Agent 1: Gathers comprehensive stock information",
            "Agent 2: Generates investment recommendations",
            "Results are combined into a complete report",
        ],
        "limitations": [
            "Not a replacement for professional financial advice",
            "Relies on web search and analysis tools for current data",
            "General guidance only, not personalized advice",
        ],
    }
