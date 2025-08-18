"""Single agent ReACT implementation for stock analysis using Pydantic-AI."""

import logging
from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from common.config import AppConfig
from common.models import (
    CompanyInfo,
    FinancialMetrics,
    InvestmentRecommendation,
    MarketSentiment,
    NewsItem,
    RiskAssessment,
    StockReport,
)
from common.utils import TavilyResearchTool

logger = logging.getLogger(__name__)

# Set up LiteLLM environment variables if they exist
import os
from dotenv import load_dotenv
load_dotenv()

if os.getenv("LITELLM_BASE_URL") and os.getenv("LITELLM_API_KEY"):
    os.environ["OPENAI_BASE_URL"] = os.getenv("LITELLM_BASE_URL")
    os.environ["OPENAI_API_KEY"] = os.getenv("LITELLM_API_KEY")


class Dependencies(BaseModel):
    """Dependencies for the stock analysis agent."""
    
    model_config = {"arbitrary_types_allowed": True}
    
    tavily_tool: TavilyResearchTool
    config: AppConfig


# Instructions template for the stock analysis agent
STOCK_ANALYSIS_INSTRUCTIONS = """
Analyze the stock {symbol} using the ReACT (Reasoning and Acting) pattern.

You are a professional stock analyst AI agent. Follow the ReACT pattern:
1. REASON about what information you need
2. ACT by using the web_search tool to gather information
3. OBSERVE the results and decide if you need more information
4. REPEAT until you have enough information to make a recommendation

ANALYSIS APPROACH:
- Use web_search to find company information, financial data, recent news, and market sentiment for {symbol}
- Search for multiple aspects: company fundamentals, current stock price, recent news, analyst opinions
- Reason through each piece of information you gather
- Synthesize all information into a comprehensive investment recommendation

SEARCH STRATEGY:
- Start with basic company information and current stock data for {symbol}
- Search for recent news and market developments about {symbol}
- Look for analyst opinions and price targets for {symbol}
- Consider both positive and negative information

Your goal is to provide a comprehensive stock analysis as a structured StockReport with:
- Company information (name, sector, industry, description, market_cap)
- Financial metrics (current_price, price_change, price_change_percent, volume, pe_ratio, dividend_yield)
- Recent news with sentiment analysis
- Overall market sentiment assessment (overall_sentiment, confidence_score, key_factors)
- Risk assessment (risk_level, risk_factors, volatility_assessment)
- Clear investment recommendation (recommendation, confidence, reasoning, target_price, time_horizon)

Always explain your reasoning at each step and show how you're using the ReACT pattern.
Use the web_search tool to gather real, current information for each field.
Return your analysis as a properly structured StockReport object with all fields populated based on your web search findings for {symbol}.
"""

# Create a temporary agent for tool decoration (will be overridden in StockAnalysisAgent.__init__)
agent = Agent(
    model="gpt-4",  # Temporary, will be overridden
    deps_type=Dependencies,
)


@agent.tool
async def web_search(ctx: RunContext[Dependencies], query: str) -> str:
    """Search the web for information using Tavily.
    
    This is the primary tool for gathering information about stocks, companies, 
    financial data, news, and market sentiment.
    
    Args:
        query: Search query to find relevant information
        
    Returns:
        String containing search results and relevant information
    """
    try:
        logger.info(f"Performing web search: {query}")
        
        # Use the Tavily research tool to search for information
        search_results = await ctx.deps.tavily_tool.search(query)
        
        if not search_results:
            return f"No search results found for query: {query}"
        
        # Format the search results for the agent
        result = f"Search Results for: {query}\n\n"
        
        for i, item in enumerate(search_results[:5], 1):  # Limit to top 5 results
            result += f"{i}. {item.get('title', 'No title')}\n"
            result += f"   URL: {item.get('url', 'No URL')}\n"
            result += f"   Content: {item.get('content', 'No content')}\n\n"
        
        return result
        
    except Exception as e:
        error_msg = f"Web search failed for query '{query}': {str(e)}"
        logger.error(error_msg)

        return error_msg


class StockAnalysisAgent:
    """Main stock analysis agent implementing ReACT pattern with web search."""
    
    def __init__(self, config: AppConfig):
        """Initialize the stock analysis agent.
        
        Args:
            config: Application configuration containing API keys and settings
        """
        self.config = config
        self.tavily_tool = TavilyResearchTool(config.tavily)
        
        # Set up model configuration for LiteLLM if base_url is provided
        if config.agent.base_url and config.agent.api_key:
            # For LiteLLM, we need to set environment variables that Pydantic-AI will use
            import os
            os.environ["OPENAI_BASE_URL"] = config.agent.base_url
            os.environ["OPENAI_API_KEY"] = config.agent.api_key
            
            # Use openai: prefix for LiteLLM compatibility
            model_name = f"openai:{config.agent.model_name}"
        else:
            # Use the model name as-is for direct API access
            model_name = config.agent.model_name
        
        # Configure the agent with the provided settings
        # In proper production code we will not use "globa" but rather have an Agent Catalog that will be our factory
        global agent
        agent = Agent(
            model=model_name,
            deps_type=Dependencies,
            output_type=StockReport,
            instrument=True,  # Enable built-in instrumentation
        )
    
    def analyze_stock_sync(self, symbol: str) -> StockReport:
        """Analyze a single stock synchronously using the ReACT pattern.
        
        Args:
            symbol: Stock ticker symbol to analyze
            
        Returns:
            StockReport containing comprehensive analysis and recommendation
            
        Raises:
            Exception: If analysis fails completely
        """
        try:
            logger.info(f"Starting stock analysis for {symbol}")
            
            # Create dependencies for the agent
            deps = Dependencies(
                tavily_tool=self.tavily_tool,
                config=self.config
            )
            
            # Format the instructions with the stock symbol
            instructions = STOCK_ANALYSIS_INSTRUCTIONS.format(symbol=symbol)
            
            # For debug mode, capture all messages to show the conversation
            if self.config.debug:
                from pydantic_ai import capture_run_messages
                
                with capture_run_messages() as messages:
                    result = agent.run_sync(instructions, deps=deps)
                    
                    # Print the conversation in a human-readable format
                    logger.info(f"💬 === CONVERSATION LOG FOR {symbol} ===")
                    for i, msg in enumerate(messages, 1):
                        if hasattr(msg, 'parts'):
                            for j, part in enumerate(msg.parts):
                                part_type = str(type(part).__name__)
                                if 'UserPromptPart' in part_type:
                                    logger.info(f"👤 USER: {part.content}")
                                elif 'TextPart' in part_type:
                                    logger.info(f"🤖 AGENT: {part.content}")
                                elif 'ToolCallPart' in part_type:
                                    logger.info(f"🔧 TOOL CALL: {part.tool_name}({part.args})")
                                elif 'ToolReturnPart' in part_type:
                                    logger.info(f"� TTOOL RESULT: {part.content}")
                    logger.info(f"💬 === END CONVERSATION LOG ===")
            else:
                result = agent.run_sync(instructions, deps=deps)
            
            # With output_type=StockReport, the agent returns structured data directly
            logger.info(f"Completed stock analysis for {symbol}")
            return result.output
            
        except Exception as e:
            logger.error(f"Failed to analyze stock {symbol}: {str(e)}")
            raise

    async def analyze_stock(self, symbol: str) -> StockReport:
        """Analyze a single stock using the ReACT pattern with web search.
        
        Args:
            symbol: Stock ticker symbol to analyze
            
        Returns:
            StockReport containing comprehensive analysis and recommendation
            
        Raises:
            Exception: If analysis fails completely
        """
        try:
            logger.info(f"Starting stock analysis for {symbol}")
            
            # Create dependencies for the agent
            deps = Dependencies(
                tavily_tool=self.tavily_tool,
                config=self.config
            )
            
            # Format the instructions with the stock symbol
            instructions = STOCK_ANALYSIS_INSTRUCTIONS.format(symbol=symbol)
            
            # For debug mode, capture all messages to show the conversation
            if self.config.debug:
                from pydantic_ai import capture_run_messages
                
                with capture_run_messages() as messages:
                    result = await agent.run(instructions, deps=deps)
                    
                    # Print the conversation in a human-readable format
                    logger.info(f"💬 === CONVERSATION LOG FOR {symbol} ===")
                    for i, msg in enumerate(messages, 1):
                        if hasattr(msg, 'parts'):
                            for j, part in enumerate(msg.parts):
                                part_type = str(type(part).__name__)
                                if 'UserPromptPart' in part_type:
                                    logger.info(f"👤 USER: {part.content}")
                                elif 'TextPart' in part_type:
                                    logger.info(f"� AGENT: {part.content}")
                                elif 'ToolCallPart' in part_type:
                                    logger.info(f"🔧 TOOL CALL: {part.tool_name}({part.args})")
                                elif 'ToolReturnPart' in part_type:
                                    logger.info(f"� TOOOL RESULT: {part.content}")
                    logger.info(f"💬 === END CONVERSATION LOG ===")
            else:
                result = await agent.run(instructions, deps=deps)
            
            # With output_type=StockReport, the agent returns structured data directly
            logger.info(f"Completed stock analysis for {symbol}")
            return result.output
            
        except Exception as e:
            logger.error(f"Failed to analyze stock {symbol}: {str(e)}")
            raise
    
    async def analyze_portfolio(self, symbols: List[str]) -> List[StockReport]:
        """Analyze multiple stocks and generate reports for each.
        
        Args:
            symbols: List of stock ticker symbols to analyze
            
        Returns:
            List of StockReport objects, one for each symbol
        """
        reports = []
        
        for symbol in symbols:
            try:
                report = await self.analyze_stock(symbol)
                reports.append(report)
            except Exception as e:
                logger.error(f"Failed to analyze {symbol}: {str(e)}")
                # Continue with other stocks even if one fails
                continue
        
        return reports
    
