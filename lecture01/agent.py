"""
Financial Assistant Agent

A simple agent that uses web search to answer financial questions.
Demonstrates basic agent functionality with tool integration.
"""

from typing import Any

from pydantic_ai import Agent

from common.tools import web_search_tool
from common.utils import create_agent_model

# Simple financial assistant - no context needed for this basic implementation


# Create the financial assistant agent
financial_agent = Agent(
    model=create_agent_model(),
    tools=[web_search_tool],
    system_prompt="""
You are a knowledgeable financial assistant. Your role is to help users with financial questions,
investment advice, market analysis, and general financial guidance.

When answering questions:
1. Use the web_search tool to get current, up-to-date financial information when relevant
2. Combine web search results with your financial knowledge
3. Provide clear, actionable advice
4. Always mention when information is based on web search vs. general knowledge
5. Include appropriate disclaimers for investment advice
6. Be helpful but remind users to consult with financial professionals for major decisions

Keep your responses informative but concise, and always prioritize accuracy and user safety.
""",
)


# The agent uses the web_search_tool directly from common.tools


async def ask_financial_question(question: str) -> str:
    """
    Ask the financial assistant a question.

    Args:
        question: The financial question to ask

    Returns:
        The assistant's response
    """
    try:
        result = await financial_agent.run(question)
        return result.output
    except Exception as e:
        return f"Error processing your question: {str(e)}"


def get_agent_info() -> dict[str, Any]:
    """Get information about the financial agent."""
    return {
        "name": "Financial Assistant",
        "description": "A simple financial assistant that uses web search to answer financial questions",
        "tools": ["web_search_tool"],
        "capabilities": [
            "Answer financial questions",
            "Provide investment guidance",
            "Search for current market information",
            "Offer general financial advice",
        ],
        "limitations": [
            "Not a replacement for professional financial advice",
            "Relies on web search for current data",
            "General guidance only, not personalized advice",
        ],
    }
