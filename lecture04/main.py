"""
Main runner for Lecture 04: Workflow Communication Pattern

This script demonstrates the workflow pattern where a single tool orchestrates
multiple specialized agents in sequence.

The stock_report tool implements a workflow that:
1. Calls a stock analysis agent to gather information
2. Calls a recommendation agent to generate investment advice
3. Combines both results into a complete StockReport

This pattern is useful for complex tasks that can be broken down into
sequential steps where each step's output feeds into the next.
"""

import asyncio
import sys

from common.utils import (
    print_section_header,
    print_subsection_header,
    setup_logfire,
    setup_logging,
)
from lecture04.agent import ask_financial_question, get_agent_info


def display_welcome():
    """Display welcome message and agent information."""
    agent_info = get_agent_info()

    print_section_header("Lecture 04: Workflow Communication Pattern")
    print("🔄 Workflow-Based Financial Assistant Agent\n")
    print(f"Description: {agent_info['description']}\n")

    print("Capabilities:")
    for capability in agent_info["capabilities"]:
        print(f"  • {capability}")

    print("\nWorkflow Pattern:")
    for step in agent_info["workflow_pattern"]:
        print(f"  • {step}")

    print("\nLimitations:")
    for limitation in agent_info["limitations"]:
        print(f"  • {limitation}")

    print("\nType 'quit' or 'exit' to end the session.")


async def handle_question(question: str) -> None:
    """Handle a user question and display the response."""
    print(f"\nQuestion: {question}")

    # Show thinking indicator
    print("Running workflow: Analysis → Recommendation → Final Report...")
    response = await ask_financial_question(question)

    # Display the response
    print_subsection_header("💡 Workflow-Based Financial Assistant Response")
    print(response)


async def interactive_session():
    """Run an interactive session with the workflow-based financial assistant."""
    display_welcome()

    while True:
        try:
            # Get user input
            question = input("\nAsk a financial question: ").strip()

            # Check for exit commands
            if question.lower() in ["quit", "exit", "q"]:
                print(
                    "\nThank you for using the Workflow-Based Financial Assistant! 👋"
                )
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


def run_example_questions():
    """Run some example questions to demonstrate the workflow pattern."""
    print_section_header("Demo Mode")
    print("Running example questions to demonstrate the Workflow Pattern")
    print(
        "Notice how the stock_report tool orchestrates multiple agents in sequence!\n"
    )

    example_questions = [
        "What is the current market sentiment?",
        "Can you give me a detailed analysis of Microsoft stock (MSFT)?",
        "Give me a comprehensive report on NVIDIA (NVDA)",
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
        service_name="workflow-financial-assistant-lecture04",
        start_message="🚀 Tikal Lecture 04 - Workflow Pattern Started",
        extra_data={
            "mode": "interactive" if len(sys.argv) == 1 else "demo",
            "pattern": "workflow with multi-agent orchestration",
        },
    )

    print_section_header("Lecture 04: Workflow Communication Pattern")
    print("This demonstrates orchestrating multiple agents in sequence")
    print(
        "The stock_report tool runs: Analysis Agent → Recommendation Agent → Final Report\n"
    )

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
