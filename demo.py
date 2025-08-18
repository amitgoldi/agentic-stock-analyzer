#!/usr/bin/env python3
"""
Demo script showcasing the Agentic Stock Analyzer capabilities.

This script demonstrates various usage patterns and features of the stock analysis system,
including single stock analysis, portfolio analysis, and different output formats.
"""

import asyncio
import sys
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import handling for Python version compatibility
try:
    from common.config import get_config
    from common.models import StockReport
    from lecture01.agent import StockAnalysisAgent
    IMPORTS_AVAILABLE = True
except Exception:
    IMPORTS_AVAILABLE = False

console = Console()


async def demo_single_stock_analysis(agent) -> None:
    """Demonstrate single stock analysis with detailed explanation."""
    console.print(Panel.fit("📈 Demo 1: Single Stock Analysis (ReACT Pattern)", style="bold blue"))
    
    console.print("""
[bold]What you'll see:[/bold]
This demo shows how a single AI agent uses the ReACT (Reasoning, Acting, Observing) pattern
to analyze a stock. The agent will:

1. [bold cyan]Reason[/bold cyan] about what information it needs
2. [bold green]Act[/bold green] by using research tools to gather data
3. [bold yellow]Observe[/bold yellow] the results and decide if more information is needed
4. [bold magenta]Generate[/bold magenta] a comprehensive investment recommendation

Let's analyze Apple Inc. (AAPL) as an example...
    """)
    
    input("Press Enter to continue...")
    
    symbol = "AAPL"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Analyzing {symbol}...", total=None)
        
        try:
            report = agent.analyze_stock_sync(symbol)
            progress.update(task, description=f"✅ Analysis complete for {symbol}")
            
            # Display the report with educational commentary
            console.print(f"\n🎯 [bold]Analysis Results for {symbol}[/bold]")
            console.print("="*60)
            
            # Show the structured data that the agent produced
            display_educational_report(report)
            
            console.print("""
[bold cyan]🧠 What happened behind the scenes:[/bold cyan]
1. The agent reasoned that it needed company info, financial metrics, and news
2. It acted by calling research tools to gather this information
3. It observed the results and synthesized them into a coherent analysis
4. It generated specific investment advice based on the gathered data

This is the ReACT pattern in action - a continuous loop of reasoning and acting!
            """)
            
        except Exception as e:
            progress.update(task, description=f"❌ Failed to analyze {symbol}")
            console.print(f"Error: {str(e)}")


async def demo_portfolio_analysis(agent) -> None:
    """Demonstrate portfolio analysis with multiple stocks."""
    console.print(Panel.fit("📊 Demo 2: Portfolio Analysis", style="bold green"))
    
    console.print("""
[bold]What you'll see:[/bold]
This demo shows how the same agent can analyze multiple stocks in sequence,
maintaining consistency in its analysis approach while adapting to different
companies and market conditions.

We'll analyze a tech-focused portfolio: Apple (AAPL), Google (GOOGL), and Microsoft (MSFT)
    """)
    
    input("Press Enter to continue...")
    
    portfolio = ["AAPL", "GOOGL", "MSFT"]
    reports = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        for i, symbol in enumerate(portfolio, 1):
            task = progress.add_task(f"[{i}/{len(portfolio)}] Analyzing {symbol}...", total=None)
            
            try:
                report = agent.analyze_stock_sync(symbol)
                reports.append(report)
                progress.update(task, description=f"✅ Completed {symbol}")
            except Exception as e:
                progress.update(task, description=f"❌ Failed {symbol}: {str(e)}")
    
    if reports:
        display_portfolio_comparison(reports)
        
        console.print("""
[bold cyan]🧠 Portfolio Analysis Insights:[/bold cyan]
• The agent applied the same analytical framework to each stock
• It identified sector-specific trends and company-specific factors
• Risk assessments varied based on each company's unique profile
• Investment recommendations reflect both individual merit and portfolio balance

This demonstrates how agentic patterns can scale across multiple tasks while
maintaining analytical consistency and quality.
        """)


async def demo_error_handling(agent) -> None:
    """Demonstrate error handling and graceful degradation."""
    console.print(Panel.fit("⚠️  Demo 3: Error Handling & Resilience", style="bold yellow"))
    
    console.print("""
[bold]What you'll see:[/bold]
This demo shows how the agent handles various error conditions gracefully:
• Invalid stock symbols
• API failures
• Incomplete data
• Network issues

The agent is designed to provide useful analysis even when some data is unavailable.
    """)
    
    input("Press Enter to continue...")
    
    # Test with an invalid symbol
    invalid_symbol = "INVALID123"
    
    console.print(f"\n🧪 Testing with invalid symbol: {invalid_symbol}")
    
    try:
        report = agent.analyze_stock_sync(invalid_symbol)
        console.print("✅ Agent handled invalid symbol gracefully")
        display_educational_report(report)
    except Exception as e:
        console.print(f"❌ Error (as expected): {str(e)}")
    
    console.print("""
[bold cyan]🧠 Error Handling Strategy:[/bold cyan]
• The agent validates inputs before processing
• It provides fallback data when APIs are unavailable
• It continues analysis with partial information when possible
• It clearly communicates limitations and confidence levels

This resilience is crucial for production agentic systems!
    """)


def display_educational_report(report) -> None:
    """Display a stock report with educational annotations."""
    console.print(f"""
[bold blue]📋 Structured Analysis Report[/bold blue]

[bold]Company Information:[/bold] (Gathered via research tools)
• Name: {report.company_info.name}
• Sector: {report.company_info.sector}
• Industry: {report.company_info.industry}

[bold]Financial Metrics:[/bold] (Real-time market data)
• Current Price: ${report.financial_metrics.current_price or 'N/A'}
• Price Change: {report.financial_metrics.price_change or 'N/A'}%
• Volume: {f'{report.financial_metrics.volume:,}' if report.financial_metrics.volume else 'N/A'}
• P/E Ratio: {report.financial_metrics.pe_ratio or 'N/A'}

[bold]AI-Generated Investment Recommendation:[/bold]
• Recommendation: [bold]{report.investment_recommendation.recommendation.upper()}[/bold]
• Confidence Level: {report.investment_recommendation.confidence:.1%}
• Reasoning: {report.investment_recommendation.reasoning}
• Time Horizon: {report.investment_recommendation.time_horizon}

[bold]Risk Assessment:[/bold] (AI-powered analysis)
• Risk Level: {report.risk_assessment.risk_level.upper()}
• Key Risk Factors: {', '.join(report.risk_assessment.risk_factors)}

[bold]Market Sentiment:[/bold] (Derived from news analysis)
• Overall Sentiment: {report.market_sentiment.overall_sentiment.upper()}
• Confidence: {report.market_sentiment.confidence_score:.1%}
    """)


def display_portfolio_comparison(reports: List) -> None:
    """Display a comparative analysis of portfolio stocks."""
    from rich.table import Table
    
    table = Table(title="📊 Portfolio Comparison", show_header=True, header_style="bold magenta")
    table.add_column("Stock", style="cyan", no_wrap=True)
    table.add_column("Recommendation", style="bold")
    table.add_column("Confidence", style="blue", justify="right")
    table.add_column("Risk Level", style="red")
    table.add_column("Sentiment", style="green")
    table.add_column("Key Insight", style="white")
    
    for report in reports:
        # Extract key insight from reasoning
        reasoning = report.investment_recommendation.reasoning
        key_insight = reasoning[:50] + "..." if len(reasoning) > 50 else reasoning
        
        table.add_row(
            report.symbol,
            report.investment_recommendation.recommendation.upper(),
            f"{report.investment_recommendation.confidence:.1%}",
            report.risk_assessment.risk_level.upper(),
            report.market_sentiment.overall_sentiment.upper(),
            key_insight
        )
    
    console.print(table)


async def demo_output_formats() -> None:
    """Demonstrate different output formats available."""
    console.print(Panel.fit("🎨 Demo 4: Output Format Options", style="bold magenta"))
    
    console.print("""
[bold]Available Output Formats:[/bold]

The CLI supports multiple output formats for different use cases:

1. [bold cyan]Rich Format[/bold cyan] (default) - Beautiful terminal output with colors and formatting
2. [bold green]JSON Format[/bold green] - Machine-readable structured data
3. [bold yellow]CSV Format[/bold yellow] - Spreadsheet-compatible tabular data
4. [bold blue]Summary Format[/bold blue] - Concise overview for quick scanning

[bold]Usage Examples:[/bold]
• python cli.py --stock AAPL --format rich
• python cli.py --portfolio AAPL GOOGL --format json
• python cli.py --stock MSFT --format csv > analysis.csv
• python cli.py --portfolio AAPL GOOGL MSFT --format summary

Each format serves different needs - from human consumption to data processing!
    """)


async def run_comprehensive_demo() -> None:
    """Run the complete demo showcasing all features."""
    console.print(Panel.fit(
        "🎓 Agentic Stock Analyzer - Comprehensive Demo\n"
        "Teaching AI Communication Patterns Through Stock Analysis",
        style="bold blue"
    ))
    
    console.print("""
[bold]Welcome to the Agentic Stock Analyzer Demo![/bold]

This demo will walk you through the key concepts and capabilities of our
AI-powered stock analysis system, which demonstrates various agentic
communication patterns.

[bold cyan]What you'll learn:[/bold cyan]
• How the ReACT pattern works in practice
• How agents handle real-world data and uncertainty
• How to scale agentic patterns across multiple tasks
• How to build resilient AI systems

Let's get started!
    """)
    
    input("Press Enter to begin the demo...")
    
    try:
        if not IMPORTS_AVAILABLE:
            console.print("""
⚠️  [bold yellow]Demo Mode - Educational Version[/bold yellow]

Full functionality requires Python 3.12+ and proper setup.
This demo shows the concepts and structure of the agentic system.

For full functionality:
1. Ensure Python 3.12+ is installed
2. Set up .env file with API keys
3. Run the demo again

For now, we'll show you the available features...
            """)
            await demo_output_formats()
            return
        
        # Load configuration
        config = get_config()
        
        if not config.tavily.api_key:
            console.print("""
❌ [bold red]Configuration Required[/bold red]

To run the full demo, you need to set up your Tavily API key:

1. Copy .env.template to .env
2. Add your Tavily API key: TAVILY_API_KEY=your_key_here
3. Run the demo again

For now, we'll show you the available features...
            """)
            await demo_output_formats()
            return
        
        # Initialize agent
        console.print("🤖 Initializing AI agent...")
        agent = StockAnalysisAgent(config)
        console.print("✅ Agent ready!")
        
        # Run demos in sequence
        await demo_single_stock_analysis(agent)
        input("\nPress Enter to continue to portfolio analysis...")
        
        await demo_portfolio_analysis(agent)
        input("\nPress Enter to continue to error handling demo...")
        
        await demo_error_handling(agent)
        input("\nPress Enter to see output format options...")
        
        await demo_output_formats()
        
        console.print(Panel.fit(
            "🎉 Demo Complete!\n\n"
            "You've seen how agentic communication patterns can be applied to real-world problems.\n"
            "Try the CLI yourself: python cli.py --help",
            style="bold green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n👋 Demo interrupted. Thanks for watching!")
    except Exception as e:
        console.print(f"\n❌ Demo error: {str(e)}")
        console.print("This might be due to API configuration or network issues.")


def main() -> None:
    """Main entry point for the demo script."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        console.print("""
[bold]Agentic Stock Analyzer Demo Script[/bold]

Usage:
  python demo.py              # Run comprehensive demo
  python demo.py --help       # Show this help message

This demo script showcases the key features and concepts of the
Agentic Stock Analyzer, including:

• ReACT pattern implementation
• Portfolio analysis capabilities  
• Error handling and resilience
• Multiple output formats
• Educational explanations

For interactive usage, try:
  python cli.py --interactive

For specific analysis, try:
  python cli.py --stock AAPL
  python cli.py --portfolio AAPL GOOGL MSFT
        """)
        return
    
    asyncio.run(run_comprehensive_demo())


if __name__ == "__main__":
    main()