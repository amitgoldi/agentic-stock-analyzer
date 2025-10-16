"""
Agent-to-Agent (A2A) Protocol Communication: Financial Assistant

This demonstrates the A2A protocol where agents communicate over HTTP using
a standardized protocol introduced by Google for agent interoperability.

Key difference from Lecture 03:
- Lecture 03: Agent-as-tool pattern (wraps agent directly in code)
- Lecture 05: A2A protocol (agents communicate via HTTP using A2A standard)

The financial assistant agent communicates with the stock analysis agent
through HTTP requests following the A2A protocol specification.

Reference: https://ai.pydantic.dev/a2a/
"""

import asyncio
import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

from common.models import StockReport
from common.tools import web_search_tool
from common.utils import create_agent_model, get_current_date, validate_stock_symbol

logger = logging.getLogger(__name__)

# A2A server configuration
A2A_STOCK_SERVER_URL = "http://localhost:8001"


class A2ATaskRequest(BaseModel):
    """A2A protocol task request format."""

    messages: list[dict[str, Any]] = Field(
        description="Messages in A2A protocol format"
    )
    context_id: str | None = Field(
        default=None, description="Context ID for conversation continuity"
    )


class A2ATaskResponse(BaseModel):
    """A2A protocol task response format."""

    task_id: str = Field(description="Unique task identifier")
    status: str = Field(description="Task status")
    artifacts: list[dict[str, Any]] = Field(
        default_factory=list, description="Task output artifacts"
    )


def create_a2a_stock_analysis_tool() -> Tool:
    """
    Create a tool that communicates with the stock analysis agent via A2A protocol.

    This tool makes HTTP requests to the A2A stock analysis server, demonstrating
    true agent-to-agent communication using the standardized A2A protocol.
    """

    async def request_stock_analysis_a2a(ctx: RunContext, symbol: str) -> StockReport:
        """
        Request stock analysis from the A2A stock analysis server.

        This function demonstrates the A2A protocol by:
        1. Formatting a request in A2A protocol format
        2. Sending an HTTP request to the A2A stock analysis server
        3. Receiving and parsing the A2A protocol response
        4. Extracting the StockReport from the response artifacts

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')

        Returns:
            StockReport: Detailed analysis report from the A2A stock analysis agent

        Raises:
            RuntimeError: If the A2A server is not available or returns an error
        """
        normalized_symbol = validate_stock_symbol(symbol)

        logger.info(
            f"A2A Protocol: Preparing request for stock analysis of {normalized_symbol}"
        )

        # Prepare A2A protocol request
        analysis_prompt = f"""
Please analyze the stock {normalized_symbol} and provide a comprehensive report.

The analysis date should be: {get_current_date()}
        """.strip()

        # Generate unique IDs for the request
        import uuid

        message_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        # A2A protocol uses JSON-RPC 2.0 format
        a2a_request = {
            "jsonrpc": "2.0",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": analysis_prompt}],
                    "kind": "message",
                    "messageId": message_id,
                },
                "configuration": {"acceptedOutputModes": ["application/json"]},
            },
            "id": request_id,
        }

        logger.info(f"A2A Protocol: Sending HTTP request to {A2A_STOCK_SERVER_URL}/")

        try:
            # Send request to A2A server
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{A2A_STOCK_SERVER_URL}/",
                    json=a2a_request,
                )

                if response.status_code != 200:
                    error_msg = f"A2A server returned status {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise RuntimeError(
                        f"Failed to communicate with A2A stock analysis server. "
                        f"Make sure the server is running at {A2A_STOCK_SERVER_URL}. "
                        f"Error: {error_msg}"
                    )

                json_rpc_response = response.json()

                # Check for JSON-RPC error
                if "error" in json_rpc_response:
                    error = json_rpc_response["error"]
                    error_msg = (
                        f"A2A RPC error: {error.get('message', 'Unknown error')}"
                    )
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)

                # Get the task result
                task_result = json_rpc_response.get("result", {})
                task_id = task_result.get("id")

                logger.info(
                    f"A2A Protocol: Task created with ID {task_id}, polling for completion..."
                )

                # Poll for task completion
                max_attempts = 60  # 60 seconds max
                for attempt in range(max_attempts):
                    await asyncio.sleep(1)

                    # Get task status
                    task_status_request = {
                        "jsonrpc": "2.0",
                        "method": "tasks/get",
                        "params": {"id": task_id},
                        "id": str(uuid.uuid4()),
                    }

                    status_response = await client.post(
                        f"{A2A_STOCK_SERVER_URL}/", json=task_status_request
                    )

                    if status_response.status_code != 200:
                        logger.warning(
                            f"Failed to get task status: {status_response.status_code}"
                        )
                        continue

                    status_data = status_response.json()
                    if "error" in status_data:
                        raise RuntimeError(
                            f"Task status error: {status_data['error'].get('message')}"
                        )

                    task = status_data.get("result", {})
                    task_state = task.get("status", {}).get("state")

                    logger.debug(
                        f"A2A Protocol: Task {task_id} state: {task_state} (attempt {attempt + 1}/{max_attempts})"
                    )

                    if task_state == "completed":
                        logger.info(
                            f"A2A Protocol: Task {task_id} completed successfully"
                        )

                        # Extract the agent's response from the history
                        history = task.get("history", [])
                        if history:
                            # Find the last agent message
                            for msg in reversed(history):
                                if msg.get("role") == "agent":
                                    parts = msg.get("parts", [])
                                    for part in parts:
                                        if part.get("kind") == "data":
                                            # Found structured data response
                                            data = part.get("data", {})
                                            # A2A wraps structured data in {"result": {...}}
                                            if (
                                                isinstance(data, dict)
                                                and "result" in data
                                            ):
                                                stock_data = data["result"]
                                                logger.info(
                                                    f"A2A Protocol: Successfully extracted StockReport from history for {normalized_symbol}"
                                                )
                                                return StockReport(**stock_data)
                                            elif isinstance(data, dict):
                                                # Try direct data if no "result" wrapper
                                                logger.info(
                                                    f"A2A Protocol: Successfully extracted StockReport from history (direct) for {normalized_symbol}"
                                                )
                                                return StockReport(**data)

                        # If we didn't find structured data in history, check artifacts
                        artifacts = task.get("artifacts", [])
                        for artifact in artifacts:
                            # Check parts within artifact
                            parts = artifact.get("parts", [])
                            for part in parts:
                                if part.get("kind") == "data":
                                    data = part.get("data", {})
                                    # A2A wraps structured output in {"result": {...}}
                                    if isinstance(data, dict) and "result" in data:
                                        stock_data = data["result"]
                                        logger.info(
                                            f"A2A Protocol: Successfully extracted StockReport from artifacts for {normalized_symbol}"
                                        )
                                        return StockReport(**stock_data)
                                    elif isinstance(data, dict):
                                        # Try direct data if no "result" wrapper
                                        logger.info(
                                            f"A2A Protocol: Successfully extracted StockReport from artifacts (direct) for {normalized_symbol}"
                                        )
                                        return StockReport(**data)

                        raise RuntimeError(
                            "Task completed but no StockReport found in response"
                        )

                    elif task_state == "failed":
                        error_msg = task.get("status", {}).get("error", "Unknown error")
                        raise RuntimeError(f"Task failed: {error_msg}")

                    elif task_state == "canceled":
                        raise RuntimeError("Task was canceled")

                    # Still in progress, continue polling

                raise RuntimeError(
                    f"Task did not complete within {max_attempts} seconds"
                )

        except httpx.ConnectError:
            error_msg = (
                f"Cannot connect to A2A stock analysis server at {A2A_STOCK_SERVER_URL}. "
                f"Please ensure the server is running:\n"
                f"  uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001"
            )
            logger.error(f"A2A Protocol: {error_msg}")
            raise RuntimeError(error_msg)
        except httpx.TimeoutException:
            error_msg = "Request to A2A server timed out after 120 seconds"
            logger.error(f"A2A Protocol: {error_msg}")
            raise RuntimeError(error_msg)
        except Exception as e:
            logger.error(f"A2A Protocol: Unexpected error: {str(e)}")
            raise

    return Tool(
        request_stock_analysis_a2a,
        description="Request detailed stock analysis via A2A protocol from the stock analysis agent. "
        "Use this when users ask for comprehensive stock analysis. "
        "Provide the stock symbol (e.g., AAPL, TSLA) and the request will be sent to the A2A server.",
    )


# Create the A2A communication tool
a2a_stock_analysis_tool = create_a2a_stock_analysis_tool()


# Create the financial assistant agent with A2A communication capability
a2a_financial_agent = Agent(
    model=create_agent_model(),
    tools=[web_search_tool, a2a_stock_analysis_tool],
    system_prompt="""
You are a knowledgeable financial assistant with the ability to communicate with specialized agents via the A2A protocol.

Your role is to help users with financial questions, investment advice, market analysis, and general financial guidance.

IMPORTANT - A2A Protocol Communication:
You have access to a specialized stock analysis agent through the A2A protocol.
When users ask for detailed stock analysis:
1. Use the request_stock_analysis_a2a tool to communicate with the stock analysis agent
2. This tool uses the A2A (Agent-to-Agent) protocol for standardized agent communication
3. The stock analysis agent runs as a separate service and responds with comprehensive reports
4. Present the analysis results to the user in a clear, helpful format

When answering questions:
1. Use web_search for general financial information and market updates
2. Use request_stock_analysis_a2a to communicate with the stock analysis agent via A2A protocol
3. Combine information from both sources with your financial knowledge
4. Provide clear, actionable advice
5. Always mention when you're using the A2A protocol to communicate with other agents
6. Include appropriate disclaimers for investment advice
7. Remind users to consult with financial professionals for major decisions

Communication Style:
- Be explicit about using the A2A protocol (e.g., "Let me request analysis via our A2A stock analysis service")
- Acknowledge when communication with other agents is happening
- Present agent results clearly and integrate them into your response

Keep your responses informative but concise, and always prioritize accuracy and user safety.
""",
)


async def ask_financial_question(question: str) -> str:
    """
    Ask the financial assistant a question using A2A protocol communication.

    The financial assistant can communicate with the stock analysis agent
    via HTTP using the standardized A2A protocol.

    Args:
        question: The financial question to ask

    Returns:
        The assistant's response
    """
    try:
        result = await a2a_financial_agent.run(question)
        return result.output
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return f"Error processing your question: {str(e)}"


def get_agent_info() -> dict[str, Any]:
    """Get information about the A2A financial agent."""
    return {
        "name": "A2A Protocol Financial Assistant",
        "description": "Financial assistant using Agent-to-Agent (A2A) protocol communication",
        "tools": ["web_search_tool", "a2a_stock_analysis_tool"],
        "capabilities": [
            "Answer financial questions",
            "Provide investment guidance",
            "Search for current market information",
            "Request stock analysis via A2A protocol",
            "Offer general financial advice",
        ],
        "communication_pattern": [
            "Agent-to-Agent (A2A) protocol communication",
            "Agents communicate over HTTP using standardized A2A format",
            "Stock analysis agent runs as separate A2A server",
            "Financial assistant sends A2A protocol requests",
            "True inter-agent communication following Google's A2A standard",
        ],
        "comparison_with_lecture03": [
            "Lecture 03: Agent-as-tool pattern (direct code integration)",
            "Lecture 05: A2A protocol (HTTP-based standardized communication)",
            "A2A enables agent interoperability across frameworks and vendors",
            "A2A follows open standard for agent communication",
        ],
        "requirements": [
            "Requires A2A stock analysis server to be running",
            "Server: uvicorn lecture05.stock_a2a_server:app --port 8001",
            "Server must be accessible at http://localhost:8001",
        ],
        "limitations": [
            "Not a replacement for professional financial advice",
            "Requires A2A server to be running for stock analysis",
            "General guidance only, not personalized advice",
        ],
    }
