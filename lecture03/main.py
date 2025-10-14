"""
Main runner for Lecture 03: Enhanced Financial Assistant Agent

This script demonstrates the lecture01 Financial Assistant enhanced with an
additional stock_report tool that internally delegates to the lecture02 agent.

This shows how to extend a basic agent with specialized capabilities by simply
adding new tools without modifying the core agent structure.
"""

import asyncio
import sys

from common.utils import (
    print_section_header,
    print_subsection_header,
    setup_logfire,
    setup_logging,
)
from lecture03.agent import ask_financial_question, get_agent_info


def display_welcome():
    """Display welcome message and agent information."""
    agent_info = get_agent_info()

    print_section_header("Lecture 03: Enhanced Financial Assistant")
    print("🏦 Enhanced Financial Assistant Agent\n")
    print(f"Description: {agent_info['description']}\n")

    print("Capabilities:")
    for capability in agent_info["capabilities"]:
        print(f"  • {capability}")

    print("\nEnhancements over Lecture 01:")
    for enhancement in agent_info["enhancements"]:
        print(f"  • {enhancement}")

    print("\nLimitations:")
    for limitation in agent_info["limitations"]:
        print(f"  • {limitation}")

    print("\nType 'quit' or 'exit' to end the session.")


async def handle_question(question: str) -> None:
    """Handle a user question and display the response."""
    print(f"\nQuestion: {question}")

    # Show thinking indicator
    print("Thinking and searching for information...")
    response = await ask_financial_question(question)

    # Display the response
    print_subsection_header("💡 Enhanced Financial Assistant Response")
    print(response)


async def interactive_session():
    """Run an interactive session with the enhanced financial assistant."""
    display_welcome()

    while True:
        try:
            # Get user input
            question = input("\nAsk a financial question: ").strip()

            # Check for exit commands
            if question.lower() in ["quit", "exit", "q"]:
                print("\nThank you for using the Enhanced Financial Assistant! 👋")
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
    """Run some example questions to demonstrate the enhanced agent."""
    print_section_header("Demo Mode")
    print("Running example questions to demonstrate the Enhanced Financial Assistant")
    print(
        "Notice how it can handle both general questions AND detailed stock analysis!\n"
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
        service_name="enhanced-financial-assistant-lecture03",
        start_message="🚀 Tikal Lecture 03 - Enhanced Financial Assistant Started",
        extra_data={
            "mode": "interactive" if len(sys.argv) == 1 else "demo",
            "enhancement": "stock_report_tool from lecture02",
        },
    )

    print_section_header("Lecture 03: Enhanced Financial Assistant Agent")
    print("This is the lecture01 agent enhanced with the stock_report tool")
    print("The stock_report tool internally uses the lecture02 agent for analysis\n")

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
