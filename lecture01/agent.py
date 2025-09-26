"""Single agent implementation for stock analysis using web search."""

import logging

from pydantic_ai import Agent

from common.config import config
from common.models import StockReport
from common.tools import web_search_tool
from common.utils import create_agent_model, get_current_date, validate_stock_symbol

logger = logging.getLogger(__name__)


class StockAnalysisAgent:
    """Single agent for comprehensive stock analysis using web search."""

    def __init__(self):
        """Initialize the stock analysis agent."""
        # Validate configuration
        config.validate_required_keys()

        # Use the shared web search tool
        self.search_tool = web_search_tool

        # System prompt for the agent
        system_prompt = """
You are an expert financial analyst specializing in stock analysis and market research.

Your task is to create comprehensive stock reports by gathering and analyzing current information about publicly traded companies.

CAPABILITIES:
- You have access to a web search tool that can find real-time information about stocks, companies, and market conditions
- You can search for financial news, earnings reports, analyst opinions, and market data
- You should gather information from multiple reliable sources

ANALYSIS FRAMEWORK:
When analyzing a stock, you should:

1. **Company Overview**: Get basic company information, business model, and recent developments
2. **Financial Performance**: Look for recent earnings, revenue trends, and key financial metrics
3. **Market Position**: Research competitive landscape and market share
4. **Recent News**: Find recent news that could impact the stock price
5. **Analyst Opinions**: Look for professional analyst ratings and price targets
6. **Risk Assessment**: Identify potential risks and challenges
7. **Market Sentiment**: Gauge overall market sentiment toward the stock

SEARCH STRATEGY:
- Use multiple targeted searches to gather comprehensive information
- Search for recent news (last 3-6 months) for current relevance
- Look for both positive and negative information to provide balanced analysis
- Verify information from multiple sources when possible
- Focus on reputable financial news sources and official company communications

OUTPUT REQUIREMENTS:
- Provide a structured analysis following the StockReport format
- Include specific data points when available (prices, percentages, dates)
- Cite your sources and indicate when information is current
- Be objective and balanced in your analysis
- Clearly distinguish between facts and opinions/projections
- If certain information is not available, acknowledge this rather than speculating

Remember: Your analysis should be thorough, factual, and useful for investment decision-making.
        """.strip()

        # Create the model using shared utility
        model = create_agent_model()

        # Create the agent
        self.agent = Agent(
            model=model,
            tools=[self.search_tool],
            output_type=StockReport,
            system_prompt=system_prompt,
        )

        logger.info(f"StockAnalysisAgent initialized with model: {config.AGENT_MODEL}")

    async def analyze_stock(self, symbol: str) -> StockReport:
        """
        Analyze a stock and generate a comprehensive report.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

        Returns:
            StockReport: Comprehensive analysis report
        """
        # Validate and normalize the stock symbol
        normalized_symbol = validate_stock_symbol(symbol)

        logger.info(f"Starting stock analysis for: {normalized_symbol}")

        # Create the analysis prompt
        prompt = f"""
Please analyze the stock {normalized_symbol} and provide a comprehensive report.

I need you to research and analyze:
1. Current stock price and recent performance
2. Company overview and recent business developments
3. Recent financial results and key metrics
4. Latest news and market sentiment
5. Analyst opinions and recommendations
6. Risk factors and challenges
7. Investment recommendation with reasoning

Please use the web search tool to gather current, accurate information from reliable financial sources.
Make sure to search for multiple aspects of the company and stock performance.

The analysis date should be: {get_current_date()}
        """.strip()

        try:
            # Run the agent analysis
            result = await self.agent.run(prompt)

            logger.info(f"Stock analysis completed for {normalized_symbol}")
            logger.debug(f"Analysis result: {result.output}")

            return result.output

        except Exception as e:
            logger.error(f"Error analyzing stock {normalized_symbol}: {str(e)}")
            raise
