"""Agent Delegation Pattern implementation for stock recommendations.

This module demonstrates the Agent Delegation communication pattern where
a primary agent (StockRecommender) delegates specific tasks to specialized
agents (StockAnalysisAgent) through tool calls.
"""

import logging

from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from common.config import config
from common.models import StockRecommendationReport, StockReport
from common.tools import web_search_tool
from common.utils import create_agent_model, get_current_date
from lecture01.agent import StockAnalysisAgent

logger = logging.getLogger(__name__)


def create_stock_analysis_tool() -> Tool:
    """Create a tool that wraps the StockAnalysisAgent for delegation."""

    # Create a single instance of the analysis agent to reuse
    analysis_agent = StockAnalysisAgent()

    async def get_stock_report(ctx: RunContext, symbol: str) -> StockReport:
        """
        Get a detailed stock analysis report for a given symbol.

        This tool delegates to the specialized StockAnalysisAgent to get
        comprehensive analysis of individual stocks.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

        Returns:
            StockReport: Detailed analysis report for the stock
        """
        logger.info(f"Delegating stock analysis for {symbol} to StockAnalysisAgent")
        return await analysis_agent.analyze_stock(symbol)

    return Tool(
        get_stock_report,
        description="Get detailed stock analysis report for a given symbol",
    )


class StockRecommender:
    """
    Primary agent that demonstrates the Agent Delegation pattern.

    This agent orchestrates the overall workflow by:
    1. Searching for trending/promising stocks
    2. Selecting candidates for analysis
    3. Delegating detailed analysis to StockAnalysisAgent
    4. Comparing results and providing recommendations
    """

    def __init__(self):
        """Initialize the stock recommender agent."""
        # Validate configuration
        config.validate_required_keys()

        # Create the stock analysis tool for delegation
        self.stock_analysis_tool = create_stock_analysis_tool()

        # System prompt for the recommender agent
        system_prompt = """
You are an expert investment strategist and portfolio manager specializing in identifying promising stock opportunities.

Your role is to orchestrate a comprehensive stock recommendation process by:

1. **Market Research**: Search for trending stocks, emerging opportunities, and market insights
2. **Stock Selection**: Identify 3 promising stocks based on current market conditions
3. **Detailed Analysis**: Delegate comprehensive analysis to specialized agents for each selected stock
4. **Comparative Analysis**: Compare the detailed reports and provide investment recommendations

DELEGATION STRATEGY:
- Use the get_stock_report tool to delegate detailed analysis to the specialized StockAnalysisAgent
- The specialized agent will provide comprehensive reports including financials, news, and analysis
- Focus your role on high-level strategy, selection criteria, and comparative analysis

SELECTION CRITERIA:
Consider stocks that show:
- Strong growth potential or value opportunities
- Positive market sentiment or contrarian opportunities
- Recent positive developments or catalysts
- Diverse sectors to provide portfolio balance
- Different risk/reward profiles

OUTPUT REQUIREMENTS:
- Provide a structured StockRecommendationReport
- Include clear market overview and selection rationale
- For each stock, provide specific recommendation type (Strong Buy, Buy, Hold, etc.)
- Include confidence levels and time horizons
- Provide comparative analysis highlighting relative strengths
- Include market outlook and investment implications

SEARCH STRATEGY:
- Search for "trending stocks 2024", "best stocks to buy now", "emerging market opportunities"
- Look for recent IPOs, earnings winners, or sector rotation opportunities
- Consider both growth and value opportunities
- Search for analyst upgrades and institutional buying

Remember: You are the orchestrator - delegate detailed analysis but provide strategic oversight and comparative insights.
        """.strip()

        # Create the model using shared utility
        model = create_agent_model()

        # Create the agent with delegation tools
        self.agent = Agent(
            model=model,
            tools=[web_search_tool, self.stock_analysis_tool],
            output_type=StockRecommendationReport,
            system_prompt=system_prompt,
        )

        logger.info("StockRecommender initialized with delegation capabilities")

    async def get_recommendations(self) -> StockRecommendationReport:
        """
        Get stock recommendations using the Agent Delegation pattern.

        This method demonstrates the delegation pattern by:
        1. Using web search to identify promising stocks
        2. Delegating detailed analysis to StockAnalysisAgent
        3. Providing comparative analysis and recommendations

        Returns:
            StockRecommendationReport: Comprehensive recommendation report
        """
        logger.info("Starting stock recommendation process with agent delegation")

        # Create the analysis prompt
        prompt = f"""
Please provide stock recommendations following this process:

1. **Market Research Phase**:
   - Search for trending stocks, market opportunities, and current market conditions
   - Look for stocks with recent positive catalysts or strong fundamentals
   - Consider different sectors and market caps for diversification

2. **Stock Selection Phase**:
   - Based on your research, select exactly 3 promising stocks
   - Choose stocks with different risk/reward profiles
   - Ensure they represent good investment opportunities in the current market

3. **Delegation Phase**:
   - For each selected stock, use the get_stock_report tool to get detailed analysis
   - The specialized agent will provide comprehensive reports with financials, news, and analysis
   - Collect all three detailed reports

4. **Recommendation Phase**:
   - Compare the three stocks based on the detailed reports
   - Provide specific recommendations (Strong Buy, Buy, Hold, etc.) for each
   - Include confidence levels and investment time horizons
   - Provide comparative analysis highlighting relative strengths and weaknesses

Current date: {get_current_date()}

Focus on actionable investment recommendations based on current market conditions and the detailed analysis from the specialized agent.
        """.strip()

        try:
            # Run the agent analysis with delegation
            result = await self.agent.run(prompt)

            logger.info("Stock recommendation process completed successfully")
            logger.debug(
                f"Generated {len(result.output.recommendations)} recommendations"
            )

            return result.output

        except Exception as e:
            logger.error(f"Error in recommendation process: {str(e)}")
            raise
