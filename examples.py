#!/usr/bin/env python3
"""
Usage examples for the Agentic Stock Analyzer CLI.

This script demonstrates various ways to use the command-line interface
with practical examples and explanations.
"""

import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def show_basic_examples():
    """Show basic CLI usage examples."""
    console.print(Panel.fit("📚 Basic Usage Examples", style="bold blue"))
    
    examples = [
        {
            "title": "Analyze a Single Stock",
            "command": "python cli.py --stock AAPL",
            "description": "Analyze Apple Inc. with rich formatted output"
        },
        {
            "title": "Analyze Multiple Stocks (Portfolio)",
            "command": "python cli.py --portfolio AAPL GOOGL MSFT",
            "description": "Analyze a tech portfolio with summary and detailed reports"
        },
        {
            "title": "Interactive Mode",
            "command": "python cli.py --interactive",
            "description": "Run in interactive mode for step-by-step analysis"
        },
        {
            "title": "Demo Mode",
            "command": "python cli.py --demo",
            "description": "Run predefined examples showcasing ReACT patterns"
        }
    ]
    
    for example in examples:
        console.print(f"\n[bold cyan]{example['title']}[/bold cyan]")
        console.print(f"[dim]{example['description']}[/dim]")
        
        syntax = Syntax(example['command'], "bash", theme="monokai", line_numbers=False)
        console.print(syntax)


def show_output_format_examples():
    """Show different output format examples."""
    console.print(Panel.fit("🎨 Output Format Examples", style="bold green"))
    
    formats = [
        {
            "format": "Rich (Default)",
            "command": "python cli.py --stock AAPL --format rich",
            "description": "Beautiful terminal output with colors and formatting",
            "use_case": "Human consumption, presentations"
        },
        {
            "format": "JSON",
            "command": "python cli.py --stock AAPL --format json",
            "description": "Machine-readable structured data",
            "use_case": "API integration, data processing"
        },
        {
            "format": "CSV",
            "command": "python cli.py --portfolio AAPL GOOGL MSFT --format csv",
            "description": "Spreadsheet-compatible tabular data",
            "use_case": "Excel analysis, data export"
        },
        {
            "format": "Summary",
            "command": "python cli.py --portfolio AAPL GOOGL MSFT --format summary",
            "description": "Concise overview for quick scanning",
            "use_case": "Quick checks, monitoring dashboards"
        }
    ]
    
    for fmt in formats:
        console.print(f"\n[bold yellow]{fmt['format']}[/bold yellow]")
        console.print(f"[dim]{fmt['description']}[/dim]")
        console.print(f"[blue]Use case:[/blue] {fmt['use_case']}")
        
        syntax = Syntax(fmt['command'], "bash", theme="monokai", line_numbers=False)
        console.print(syntax)


def show_advanced_examples():
    """Show advanced CLI usage examples."""
    console.print(Panel.fit("🚀 Advanced Usage Examples", style="bold magenta"))
    
    advanced = [
        {
            "title": "Custom AI Model",
            "command": "python cli.py --stock AAPL --model anthropic:claude-3-sonnet",
            "description": "Use a different AI model for analysis"
        },
        {
            "title": "Debug Mode",
            "command": "python cli.py --stock AAPL --debug",
            "description": "Enable detailed logging for troubleshooting"
        },
        {
            "title": "No Color Output",
            "command": "python cli.py --stock AAPL --no-color",
            "description": "Disable colors for plain text output"
        },
        {
            "title": "Export to File",
            "command": "python cli.py --portfolio AAPL GOOGL MSFT --format csv > portfolio_analysis.csv",
            "description": "Save analysis results to a CSV file"
        },
        {
            "title": "JSON Pipeline",
            "command": "python cli.py --stock AAPL --format json | jq '.investment_recommendation'",
            "description": "Extract specific data using jq (requires jq installed)"
        }
    ]
    
    for example in advanced:
        console.print(f"\n[bold cyan]{example['title']}[/bold cyan]")
        console.print(f"[dim]{example['description']}[/dim]")
        
        syntax = Syntax(example['command'], "bash", theme="monokai", line_numbers=False)
        console.print(syntax)


def show_workflow_examples():
    """Show real-world workflow examples."""
    console.print(Panel.fit("🔄 Workflow Examples", style="bold red"))
    
    workflows = [
        {
            "title": "Daily Portfolio Check",
            "description": "Quick morning check of your portfolio",
            "commands": [
                "# Check your portfolio with summary format",
                "python cli.py --portfolio AAPL GOOGL MSFT AMZN --format summary",
                "",
                "# Get detailed analysis for concerning stocks",
                "python cli.py --stock AAPL --format rich"
            ]
        },
        {
            "title": "Research New Investment",
            "description": "Thorough analysis of a potential investment",
            "commands": [
                "# Start with interactive mode for exploration",
                "python cli.py --interactive",
                "",
                "# Get detailed JSON data for further analysis",
                "python cli.py --stock NVDA --format json > nvda_analysis.json",
                "",
                "# Compare with similar stocks",
                "python cli.py --portfolio NVDA AMD INTC --format rich"
            ]
        },
        {
            "title": "Automated Reporting",
            "description": "Generate reports for automated systems",
            "commands": [
                "# Generate CSV report for spreadsheet analysis",
                "python cli.py --portfolio AAPL GOOGL MSFT --format csv > daily_report.csv",
                "",
                "# Create JSON data for web dashboard",
                "python cli.py --portfolio AAPL GOOGL MSFT --format json > dashboard_data.json",
                "",
                "# Quick status check with summary",
                "python cli.py --portfolio AAPL GOOGL MSFT --format summary | tee status.txt"
            ]
        }
    ]
    
    for workflow in workflows:
        console.print(f"\n[bold yellow]{workflow['title']}[/bold yellow]")
        console.print(f"[dim]{workflow['description']}[/dim]")
        
        command_text = "\n".join(workflow['commands'])
        syntax = Syntax(command_text, "bash", theme="monokai", line_numbers=False)
        console.print(syntax)


def show_help_and_tips():
    """Show helpful tips and troubleshooting."""
    console.print(Panel.fit("💡 Tips & Troubleshooting", style="bold cyan"))
    
    tips = [
        {
            "title": "Getting Help",
            "content": [
                "python cli.py --help                    # Show all available options",
                "python demo.py --help                   # Demo script help",
                "python cli.py --version                 # Show version information"
            ]
        },
        {
            "title": "Configuration",
            "content": [
                "# Set up your API key in .env file:",
                "TAVILY_API_KEY=your_api_key_here",
                "",
                "# Check if configuration is working:",
                "python cli.py --demo"
            ]
        },
        {
            "title": "Common Issues",
            "content": [
                "# API key not found:",
                "# → Make sure .env file exists with TAVILY_API_KEY",
                "",
                "# Invalid stock symbol:",
                "# → Use valid ticker symbols (e.g., AAPL, not Apple)",
                "",
                "# Network issues:",
                "# → Try --debug flag to see detailed error messages"
            ]
        },
        {
            "title": "Performance Tips",
            "content": [
                "# For large portfolios, use summary format first:",
                "python cli.py --portfolio AAPL GOOGL MSFT AMZN TSLA --format summary",
                "",
                "# Then get detailed analysis for specific stocks:",
                "python cli.py --stock AAPL --format rich"
            ]
        }
    ]
    
    for tip in tips:
        console.print(f"\n[bold green]{tip['title']}[/bold green]")
        
        content_text = "\n".join(tip['content'])
        syntax = Syntax(content_text, "bash", theme="monokai", line_numbers=False)
        console.print(syntax)


def main():
    """Main function to display all examples."""
    console.print(Panel.fit(
        "🎯 Agentic Stock Analyzer - Usage Examples\n"
        "Learn how to use the CLI effectively",
        style="bold blue"
    ))
    
    console.print("""
This guide shows you how to use the Agentic Stock Analyzer CLI for various
stock analysis tasks. Each example includes the command and explanation.

[bold]Quick Start:[/bold]
1. Set up your .env file with TAVILY_API_KEY
2. Try: python cli.py --demo
3. Explore: python cli.py --interactive
    """)
    
    # Show all example categories
    show_basic_examples()
    input("\nPress Enter to see output format examples...")
    
    show_output_format_examples()
    input("\nPress Enter to see advanced examples...")
    
    show_advanced_examples()
    input("\nPress Enter to see workflow examples...")
    
    show_workflow_examples()
    input("\nPress Enter to see tips and troubleshooting...")
    
    show_help_and_tips()
    
    console.print(Panel.fit(
        "🎉 Ready to analyze stocks!\n\n"
        "Start with: python cli.py --demo\n"
        "Or try: python cli.py --interactive",
        style="bold green"
    ))


if __name__ == "__main__":
    main()