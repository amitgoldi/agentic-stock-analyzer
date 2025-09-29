"""
Main runner for Lecture 01: Simple Financial Assistant Agent

This script demonstrates a basic financial assistant that uses web search
to answer financial questions with simple text input/output.
"""

import asyncio
import sys

from common.utils import print_section_header, print_subsection_header, setup_logging
from lecture01.agent import ask_financial_question, get_agent_info


def display_welcome():
    """Display welcome message and agent information."""
    agent_info = get_agent_info()

    print_section_header("Lecture 01: Simple Financial Assistant")
    print("🏦 Financial Assistant Agent\n")
    print(f"Description: {agent_info['description']}\n")

    print("Capabilities:")
    for capability in agent_info["capabilities"]:
        print(f"  • {capability}")

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
    print_subsection_header("💡 Financial Assistant Response")
    print(response)


async def interactive_session():
    """Run an interactive session with the financial assistant."""
    display_welcome()

    while True:
        try:
            # Get user input
            question = input("\nAsk a financial question: ").strip()

            # Check for exit commands
            if question.lower() in ["quit", "exit", "q"]:
                print("\nThank you for using the Financial Assistant! 👋")
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
    """Run some example questions to demonstrate the agent."""
    print_section_header("Demo Mode")
    print("Running example questions to demonstrate the Financial Assistant")

    example_questions = [
        "What is the current price of Bitcoin?",
        "Should I invest in index funds or individual stocks?",
        "What are the current interest rates for savings accounts?",
        "Explain the concept of dollar-cost averaging",
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
    print("Lecture 01: Simple Financial Assistant Agent\n")

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
