"""
Main runner for Lecture 05: Agent-to-Agent (A2A) Protocol Communication

This script demonstrates the A2A protocol where agents communicate over HTTP
using a standardized protocol introduced by Google for agent interoperability.

The A2A protocol enables true inter-agent communication where:
- Stock analysis agent is exposed as an A2A server
- Financial assistant agent sends requests via A2A protocol
- Communication happens over HTTP following A2A standard

SETUP:
Before running this demo, you must start the A2A stock analysis server:
    uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001

Reference: https://ai.pydantic.dev/a2a/
"""

import asyncio
import sys

from common.utils import (
    print_section_header,
    print_subsection_header,
    setup_logfire,
    setup_logging,
)
from lecture05.agent import ask_financial_question, get_agent_info


def display_welcome():
    """Display welcome message and agent information."""
    agent_info = get_agent_info()

    print_section_header("Lecture 05: Agent-to-Agent (A2A) Protocol")
    print("🌐 A2A Protocol Financial Assistant\n")
    print(f"Description: {agent_info['description']}\n")

    print("Capabilities:")
    for capability in agent_info["capabilities"]:
        print(f"  • {capability}")

    print("\nCommunication Pattern:")
    for pattern in agent_info["communication_pattern"]:
        print(f"  • {pattern}")

    print("\nComparison with Lecture 03:")
    for comparison in agent_info["comparison_with_lecture03"]:
        print(f"  • {comparison}")

    print("\n⚠️  REQUIREMENTS:")
    for req in agent_info["requirements"]:
        print(f"  • {req}")

    print("\nLimitations:")
    for limitation in agent_info["limitations"]:
        print(f"  • {limitation}")

    print("\nType 'quit' or 'exit' to end the session.")


def check_server_startup():
    """Display instructions for starting the A2A server."""
    print("\n" + "=" * 70)
    print("⚠️  IMPORTANT: A2A Server Required")
    print("=" * 70)
    print("\nBefore using this demo, start the A2A stock analysis server:")
    print("\n  Terminal 1 (this terminal):")
    print("    # Will run the financial assistant demo")
    print("\n  Terminal 2 (new terminal):")
    print("    cd <project-root>")
    print("    uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001")
    print("\nWait for the server to start, then continue with this demo.")
    print("=" * 70 + "\n")


async def handle_question(question: str) -> None:
    """Handle a user question and display the response."""
    print(f"\nQuestion: {question}")

    # Show thinking indicator
    print("Processing (may involve A2A protocol communication)...")
    response = await ask_financial_question(question)

    # Display the response
    print_subsection_header("💡 A2A Financial Assistant Response")
    print(response)


async def interactive_session():
    """Run an interactive session with the A2A financial assistant."""
    display_welcome()

    while True:
        try:
            # Get user input
            question = input("\nAsk a financial question: ").strip()

            # Check for exit commands
            if question.lower() in ["quit", "exit", "q"]:
                print("\nThank you for using the A2A Financial Assistant! 👋")
                break

            # Handle empty input
            if not question:
                print("Please enter a question or 'quit' to exit.")
                continue

            # Process the question
            await handle_question(question)

        except KeyboardInterrupt:
            print("\n\nSession ended. Goodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            if "Cannot connect" in str(e):
                print(
                    "\n💡 Tip: Make sure the A2A server is running in another terminal"
                )


def run_example_questions():
    """Run some example questions to demonstrate the A2A protocol."""
    print_section_header("Demo Mode")
    print("Running example questions to demonstrate the A2A Protocol")
    print(
        "The financial assistant communicates with the stock analysis agent via A2A!\n"
    )

    example_questions = [
        "What is the current price of Bitcoin?",
        "Can you give me a detailed analysis of Apple stock (AAPL)?",
        "Should I invest in index funds or individual stocks?",
        "Give me a comprehensive report on Tesla (TSLA)",
    ]

    async def run_examples():
        for i, question in enumerate(example_questions, 1):
            print(f"\nExample {i}:")
            await handle_question(question)

            # Add a small delay between questions
            await asyncio.sleep(1)

    asyncio.run(run_examples())


def main():
    """Main entry point."""
    setup_logging()

    # Set up Logfire instrumentation
    setup_logfire(
        service_name="a2a-financial-assistant-lecture05",
        start_message="🚀 Tikal Lecture 05 - A2A Protocol Communication Started",
        extra_data={
            "mode": "interactive" if len(sys.argv) == 1 else "demo",
            "pattern": "Agent-to-Agent (A2A) protocol",
            "protocol_reference": "https://ai.pydantic.dev/a2a/",
        },
    )

    print_section_header("Lecture 05: Agent-to-Agent (A2A) Protocol Communication")
    print("This demonstrates the A2A protocol for standardized agent communication")
    print(
        "Agents communicate over HTTP following Google's A2A standard for interoperability\n"
    )

    # Show server startup instructions
    check_server_startup()

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run demo mode with example questions
        run_example_questions()
    else:
        # Run interactive mode
        try:
            asyncio.run(interactive_session())
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")


if __name__ == "__main__":
    main()
