#!/usr/bin/env python3
"""
Command-line interface for the Agentic Stock Analyzer.

This CLI provides easy access to stock analysis functionality with support for
single stock analysis, portfolio analysis, and interactive mode.
"""

import argparse
import asyncio
import sys
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Import configuration and agent classes
try:
    from common.config import get_config
    from lecture01.agent import StockAnalysisAgent
    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    import_error = str(e)


def show_cli_demo(mode: str, data=None) -> None:
    """Show a demonstration of what the CLI would do with proper setup."""
    console.print(Panel.fit("🎭 CLI Demo Mode", style="bold yellow"))
    
    if mode == "stock":
        console.print(f"""
[bold]Single Stock Analysis Demo[/bold]

Command executed: [cyan]python cli.py --stock {data}[/cyan]

What would happen with proper setup:
1. 🔍 Load configuration from .env file
2. 🤖 Initialize AI agent with specified model
3. 📊 Research {data} using Tavily API
4. 🧠 Analyze data using ReACT pattern
5. 📋 Generate comprehensive investment report
6. 🎨 Display results in rich format

[bold green]Sample Output Structure:[/bold green]
• Company Information (name, sector, industry)
• Financial Metrics (price, volume, P/E ratio)
• Investment Recommendation (buy/hold/sell)
• Risk Assessment (low/medium/high)
• Market Sentiment Analysis
• Recent News Summary
        """)
    
    elif mode == "portfolio":
        symbols = ", ".join(data) if isinstance(data, list) else str(data)
        console.print(f"""
[bold]Portfolio Analysis Demo[/bold]

Command executed: [cyan]python cli.py --portfolio {symbols}[/cyan]

What would happen with proper setup:
1. 🔍 Validate all stock symbols
2. 🤖 Initialize AI agent
3. 📊 Analyze each stock individually using ReACT pattern
4. 📈 Generate comparative portfolio summary
5. 📋 Create detailed reports for each stock
6. 🎨 Display results in rich table format

[bold green]Sample Output:[/bold green]
• Portfolio Summary Table
• Individual Stock Analysis Reports
• Risk Distribution Analysis
• Investment Recommendations Summary
        """)
    
    elif mode == "interactive":
        console.print("""
[bold]Interactive Mode Demo[/bold]

Command executed: [cyan]python cli.py --interactive[/cyan]

What would happen with proper setup:
1. 🎯 Launch interactive menu system
2. 📝 Prompt user for stock symbols
3. 🔄 Allow real-time analysis requests
4. 📊 Display results immediately
5. 🔁 Continue until user exits

[bold green]Interactive Menu Options:[/bold green]
1. Analyze single stock
2. Analyze portfolio (multiple stocks)
3. Run demo examples
4. Exit

User can input any valid stock symbols and get immediate analysis.
        """)
    
    elif mode == "demo":
        console.print("""
[bold]Demo Mode[/bold]

Command executed: [cyan]python cli.py --demo[/cyan]

What would happen with proper setup:
1. 🎓 Run educational demonstrations
2. 📈 Analyze AAPL (Apple) as single stock example
3. 📊 Analyze tech portfolio (AAPL, GOOGL, MSFT)
4. 🧠 Show ReACT pattern in action
5. 📚 Explain agentic communication concepts

[bold green]Educational Content:[/bold green]
• How ReACT pattern works (Reasoning, Acting, Observing)
• Real-time API integration examples
• Structured data processing
• Investment analysis methodology
        """)
    
    console.print(f"""
[bold blue]To enable full functionality:[/bold blue]
1. Ensure Python 3.12+ is installed
2. Set up .env file with API keys:
   - TAVILY_API_KEY=your_tavily_key
   - OPENAI_API_KEY=your_openai_key (or Anthropic)
3. Run: python cli.py {mode if mode != "stock" else f"--stock {data}"}

[bold cyan]Available CLI Options:[/bold cyan]
• --stock SYMBOL          (analyze single stock)
• --portfolio SYM1 SYM2   (analyze multiple stocks)
• --interactive           (interactive mode)
• --demo                  (educational demo)
• --format rich|json|csv  (output format)
• --debug                 (enable debug mode)
• --help                  (show all options)
    """)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="agentic-stock-analyzer",
        description="AI-powered stock analysis using agentic communication patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single stock
  python cli.py --stock AAPL
  
  # Analyze multiple stocks (portfolio)
  python cli.py --portfolio AAPL GOOGL MSFT
  
  # Run interactive mode
  python cli.py --interactive
  
  # Run demo with predefined examples
  python cli.py --demo
  
  # Analyze stocks with custom output format
  python cli.py --stock AAPL --format json
  
  # Enable debug mode for detailed logging
  python cli.py --stock AAPL --debug

For more information, visit: https://github.com/your-repo/agentic-stock-analyzer
        """
    )
    
    # Main action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    
    action_group.add_argument(
        "--stock", "-s",
        type=str,
        metavar="SYMBOL",
        help="Analyze a single stock by ticker symbol (e.g., AAPL, GOOGL)"
    )
    
    action_group.add_argument(
        "--portfolio", "-p",
        nargs="+",
        metavar="SYMBOL",
        help="Analyze multiple stocks as a portfolio (e.g., AAPL GOOGL MSFT)"
    )
    
    action_group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode for step-by-step analysis"
    )
    
    action_group.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run demo with predefined examples showcasing different patterns"
    )
    
    # Output format options
    parser.add_argument(
        "--format", "-f",
        choices=["rich", "json", "csv", "summary"],
        default="rich",
        help="Output format (default: rich)"
    )
    
    # Configuration options
    parser.add_argument(
        "--model",
        type=str,
        help="Override the AI model to use (e.g., openai:gpt-4o, anthropic:claude-3-sonnet)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with detailed logging"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    return parser


def validate_stock_symbols(symbols: List[str]) -> List[str]:
    """Validate and normalize stock symbols.
    
    Args:
        symbols: List of stock symbols to validate
        
    Returns:
        List of validated and normalized symbols
        
    Raises:
        ValueError: If any symbol is invalid
    """
    validated = []
    
    for symbol in symbols:
        # Basic validation
        symbol = symbol.strip().upper()
        
        if not symbol:
            raise ValueError("Empty stock symbol provided")
        
        if len(symbol) > 10:
            raise ValueError(f"Stock symbol '{symbol}' is too long (max 10 characters)")
        
        if not symbol.isalnum():
            raise ValueError(f"Stock symbol '{symbol}' contains invalid characters")
        
        validated.append(symbol)
    
    return validated


async def analyze_single_stock(agent, symbol: str) -> Optional:
    """Analyze a single stock and handle errors gracefully."""
    try:
        console.print(f"🔍 Analyzing [bold blue]{symbol}[/bold blue]...")
        report = await agent.analyze_stock(symbol)
        console.print(f"✅ Analysis complete for [bold green]{symbol}[/bold green]")
        return report
    except Exception as e:
        console.print(f"❌ Failed to analyze [bold red]{symbol}[/bold red]: {str(e)}")
        return None


async def analyze_portfolio(agent, symbols: List[str]) -> List:
    """Analyze multiple stocks in a portfolio."""
    console.print(f"📊 Analyzing portfolio with {len(symbols)} stocks...")
    
    reports = []
    for i, symbol in enumerate(symbols, 1):
        console.print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        report = await analyze_single_stock(agent, symbol)
        if report:
            reports.append(report)
    
    console.print(f"\n✅ Portfolio analysis complete: {len(reports)}/{len(symbols)} stocks analyzed")
    return reports


def display_report_rich(report) -> None:
    """Display a stock report using Rich formatting."""
    # Main report content
    content = f"""
[bold]Company:[/bold] {report.company_info.name}
[bold]Symbol:[/bold] {report.symbol}
[bold]Sector:[/bold] {report.company_info.sector}
[bold]Industry:[/bold] {report.company_info.industry}

[bold cyan]Financial Metrics[/bold cyan]
• Current Price: ${report.financial_metrics.current_price or 'N/A'}
• Price Change: ${report.financial_metrics.price_change or 'N/A'}
• Price Change %: {report.financial_metrics.price_change_percent or 'N/A'}%
• Volume: {f'{report.financial_metrics.volume:,}' if report.financial_metrics.volume else 'N/A'}
• P/E Ratio: {report.financial_metrics.pe_ratio or 'N/A'}
• Dividend Yield: {report.financial_metrics.dividend_yield or 'N/A'}%

[bold green]Investment Recommendation[/bold green]
• Recommendation: [bold]{report.investment_recommendation.recommendation.upper()}[/bold]
• Confidence: {report.investment_recommendation.confidence:.1%}
• Time Horizon: {report.investment_recommendation.time_horizon}
• Reasoning: {report.investment_recommendation.reasoning}

[bold yellow]Risk Assessment[/bold yellow]
• Risk Level: [bold]{report.risk_assessment.risk_level.upper()}[/bold]
• Volatility: {report.risk_assessment.volatility_assessment}
• Risk Factors: {', '.join(report.risk_assessment.risk_factors)}

[bold blue]Market Sentiment[/bold blue]
• Overall Sentiment: [bold]{report.market_sentiment.overall_sentiment.upper()}[/bold]
• Confidence: {report.market_sentiment.confidence_score:.1%}
• Key Factors: {', '.join(report.market_sentiment.key_factors)}

[bold magenta]Recent News[/bold magenta]
"""
    
    if report.recent_news:
        for i, news in enumerate(report.recent_news[:3], 1):
            content += f"• {news.title}\n"
            if news.sentiment:
                content += f"  Sentiment: {news.sentiment.title()}\n"
    else:
        content += "• No recent news available\n"
    
    content += f"\n[dim]Analysis performed: {report.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
    
    panel = Panel(
        content,
        title=f"📈 Stock Analysis: {report.symbol}",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)


def display_portfolio_summary_rich(reports: List) -> None:
    """Display a portfolio summary table using Rich."""
    if not reports:
        console.print("❌ No successful analyses to display")
        return
    
    table = Table(title="📊 Portfolio Analysis Summary", show_header=True, header_style="bold magenta")
    table.add_column("Symbol", style="cyan", no_wrap=True)
    table.add_column("Company", style="white")
    table.add_column("Price", style="green", justify="right")
    table.add_column("Change %", style="yellow", justify="right")
    table.add_column("Recommendation", style="bold")
    table.add_column("Confidence", style="blue", justify="right")
    table.add_column("Risk", style="red")
    table.add_column("Sentiment", style="magenta")
    
    for report in reports:
        # Color code recommendation
        rec = report.investment_recommendation.recommendation.upper()
        if rec == "BUY":
            rec_style = "[bold green]BUY[/bold green]"
        elif rec == "SELL":
            rec_style = "[bold red]SELL[/bold red]"
        else:
            rec_style = "[bold yellow]HOLD[/bold yellow]"
        
        # Color code sentiment
        sentiment = report.market_sentiment.overall_sentiment.upper()
        if sentiment == "POSITIVE":
            sentiment_style = "[green]POSITIVE[/green]"
        elif sentiment == "NEGATIVE":
            sentiment_style = "[red]NEGATIVE[/red]"
        else:
            sentiment_style = "[yellow]NEUTRAL[/yellow]"
        
        table.add_row(
            report.symbol,
            report.company_info.name[:25] + "..." if len(report.company_info.name) > 25 else report.company_info.name,
            f"${report.financial_metrics.current_price:.2f}" if report.financial_metrics.current_price else "N/A",
            f"{report.financial_metrics.price_change_percent:+.2f}%" if report.financial_metrics.price_change_percent else "N/A",
            rec_style,
            f"{report.investment_recommendation.confidence:.1%}",
            report.risk_assessment.risk_level.upper(),
            sentiment_style
        )
    
    console.print(table)


def display_report_json(report) -> None:
    """Display a stock report in JSON format."""
    import json
    print(json.dumps(report.model_dump(), indent=2, default=str))


def display_report_csv(reports: List) -> None:
    """Display stock reports in CSV format."""
    import csv
    import sys
    
    if not reports:
        return
    
    writer = csv.writer(sys.stdout)
    
    # Header
    writer.writerow([
        "Symbol", "Company", "Sector", "Industry", "Current_Price", "Price_Change_Percent",
        "Volume", "PE_Ratio", "Dividend_Yield", "Recommendation", "Confidence",
        "Risk_Level", "Market_Sentiment", "Analysis_Date"
    ])
    
    # Data rows
    for report in reports:
        writer.writerow([
            report.symbol,
            report.company_info.name,
            report.company_info.sector,
            report.company_info.industry,
            report.financial_metrics.current_price or "",
            report.financial_metrics.price_change_percent or "",
            report.financial_metrics.volume or "",
            report.financial_metrics.pe_ratio or "",
            report.financial_metrics.dividend_yield or "",
            report.investment_recommendation.recommendation,
            f"{report.investment_recommendation.confidence:.3f}",
            report.risk_assessment.risk_level,
            report.market_sentiment.overall_sentiment,
            report.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])


def display_report_summary(reports: List) -> None:
    """Display a brief summary of stock reports."""
    if not reports:
        console.print("❌ No reports to summarize")
        return
    
    console.print(f"\n📋 [bold]Analysis Summary[/bold] ({len(reports)} stocks)")
    console.print("=" * 50)
    
    for report in reports:
        rec = report.investment_recommendation.recommendation.upper()
        confidence = report.investment_recommendation.confidence
        risk = report.risk_assessment.risk_level.upper()
        
        # Color coding
        if rec == "BUY":
            rec_color = "green"
        elif rec == "SELL":
            rec_color = "red"
        else:
            rec_color = "yellow"
        
        console.print(
            f"[bold cyan]{report.symbol}[/bold cyan] | "
            f"[{rec_color}]{rec}[/{rec_color}] "
            f"({confidence:.0%}) | "
            f"Risk: {risk} | "
            f"${report.financial_metrics.current_price or 'N/A'}"
        )


async def run_interactive_mode() -> None:
    """Run the interactive analysis mode."""
    console.print(Panel.fit("🎯 Interactive Stock Analysis Mode", style="bold green"))
    
    try:
        config = get_config()
        if not config.tavily.api_key:
            console.print("❌ [bold red]Error:[/bold red] TAVILY_API_KEY not found")
            console.print("Please set your Tavily API key in the .env file")
            return
        
        agent = StockAnalysisAgent(config)
        
        while True:
            console.print("\n" + "="*50)
            console.print("[bold]Choose an option:[/bold]")
            console.print("1. 📈 Analyze single stock")
            console.print("2. 📊 Analyze portfolio (multiple stocks)")
            console.print("3. 🎓 Run demo examples")
            console.print("4. ❌ Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
                if symbol:
                    try:
                        validated = validate_stock_symbols([symbol])
                        report = await analyze_single_stock(agent, validated[0])
                        if report:
                            display_report_rich(report)
                    except ValueError as e:
                        console.print(f"❌ Invalid symbol: {e}")
                else:
                    console.print("❌ Please enter a valid stock symbol")
            
            elif choice == "2":
                symbols_input = input("Enter stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT): ").strip()
                if symbols_input:
                    try:
                        symbols = [s.strip() for s in symbols_input.split(",") if s.strip()]
                        validated = validate_stock_symbols(symbols)
                        reports = await analyze_portfolio(agent, validated)
                        if reports:
                            display_portfolio_summary_rich(reports)
                            
                            # Ask if user wants detailed reports
                            show_details = input("\nShow detailed reports? (y/N): ").strip().lower()
                            if show_details in ['y', 'yes']:
                                for report in reports:
                                    display_report_rich(report)
                    except ValueError as e:
                        console.print(f"❌ Invalid symbols: {e}")
                else:
                    console.print("❌ Please enter stock symbols")
            
            elif choice == "3":
                await run_demo_mode()
            
            elif choice == "4":
                console.print("👋 Goodbye!")
                break
            
            else:
                console.print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        console.print(f"\n❌ [bold red]Error:[/bold red] {str(e)}")


async def run_demo_mode() -> None:
    """Run the demo mode with predefined examples."""
    console.print(Panel.fit("🎓 Demo Mode: Agentic Communication Patterns", style="bold blue"))
    
    try:
        config = get_config()
        if not config.tavily.api_key:
            console.print("❌ [bold red]Error:[/bold red] TAVILY_API_KEY not found")
            return
        
        agent = StockAnalysisAgent(config)
        
        # Demo 1: Single stock analysis
        console.print("\n" + "="*60)
        console.print("📈 [bold]Demo 1: Single Agent ReACT Pattern[/bold]")
        console.print("Analyzing Apple Inc. (AAPL) using ReACT loop")
        console.print("="*60)
        
        demo_symbol = "AAPL"
        report = await analyze_single_stock(agent, demo_symbol)
        if report:
            display_report_rich(report)
        
        # Demo 2: Portfolio analysis
        console.print("\n" + "="*60)
        console.print("📊 [bold]Demo 2: Portfolio Analysis[/bold]")
        console.print("Analyzing a tech portfolio: AAPL, GOOGL, MSFT")
        console.print("="*60)
        
        demo_portfolio = ["AAPL", "GOOGL", "MSFT"]
        reports = await analyze_portfolio(agent, demo_portfolio)
        if reports:
            display_portfolio_summary_rich(reports)
        
        console.print("\n✅ [bold green]Demo completed![/bold green]")
        console.print("This demonstrates the ReACT pattern where the agent:")
        console.print("1. [bold]Reasons[/bold] about what information it needs")
        console.print("2. [bold]Acts[/bold] by using research tools")
        console.print("3. [bold]Observes[/bold] the results and decides next steps")
        
    except Exception as e:
        console.print(f"❌ [bold red]Demo failed:[/bold red] {str(e)}")


async def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Configure console based on arguments
    if args.no_color:
        console._color_system = None
    
    try:
        # For demo purposes, we'll show the CLI interface without requiring full setup
        console.print("🤖 [bold blue]Agentic Stock Analyzer CLI[/bold blue]")
        console.print("This is a demonstration of the command-line interface.")
        
        # Check if we can load the actual implementation
        try:
            from common.config import get_config
            from lecture01.agent import StockAnalysisAgent
            
            # Load and validate configuration
            config = get_config()
            
            # Override model if specified
            if args.model:
                config.agent.model_name = args.model
            
            # Set debug mode
            if args.debug:
                config.debug = True
                console.print(f"🐛 Debug mode enabled - using Pydantic-AI instrumentation")
                
                # Configure logging to show our debug messages
                import logging
                logging.basicConfig(
                    level=logging.INFO,
                    format='%(message)s',  # Simple format for clean output
                    force=True  # Override any existing configuration
                )
                
                # Enable Pydantic-AI's built-in instrumentation for debug mode
                try:
                    from pydantic_ai import Agent
                    from pydantic_ai.models.instrumented import InstrumentationSettings
                    
                    # Enable instrumentation for all agents
                    Agent.instrument_all()
                    console.print("✅ Pydantic-AI instrumentation enabled")
                except ImportError:
                    console.print("⚠️  Pydantic-AI instrumentation not available")
            
            # Validate API key
            if not config.tavily.api_key and not args.demo:
                console.print("❌ [bold red]Error:[/bold red] TAVILY_API_KEY not found in environment")
                console.print("Please create a .env file with your Tavily API key:")
                console.print("TAVILY_API_KEY=your_api_key_here")
                sys.exit(1)
            
            # Initialize agent
            agent = StockAnalysisAgent(config)
            
        except Exception as e:
            console.print(f"⚠️  [yellow]Note:[/yellow] Full functionality requires Python 3.12+ and proper setup")
            console.print(f"Current demo shows CLI interface structure only.")
            if args.debug:
                console.print(f"Error details: {str(e)}")
            
            # Create a mock agent for demonstration
            agent = None
        
        # Execute based on arguments
        if args.interactive:
            if agent:
                await run_interactive_mode()
            else:
                show_cli_demo("interactive")
        
        elif args.demo:
            if agent:
                await run_demo_mode()
            else:
                show_cli_demo("demo")
        
        elif args.stock:
            # Single stock analysis
            try:
                validated = validate_stock_symbols([args.stock])
                symbol = validated[0]
                
                if agent:
                    console.print(f"🔍 Analyzing {symbol}...")
                    report = await analyze_single_stock(agent, symbol)
                    
                    if report:
                        if args.format == "rich":
                            display_report_rich(report)
                        elif args.format == "json":
                            display_report_json(report)
                        elif args.format == "csv":
                            display_report_csv([report])
                        elif args.format == "summary":
                            display_report_summary([report])
                    else:
                        console.print(f"❌ Failed to analyze {symbol}")
                        sys.exit(1)
                else:
                    show_cli_demo("stock", symbol)
                    
            except ValueError as e:
                console.print(f"❌ Invalid stock symbol: {e}")
                sys.exit(1)
        
        elif args.portfolio:
            # Portfolio analysis
            try:
                validated = validate_stock_symbols(args.portfolio)
                
                if agent:
                    console.print(f"📊 Analyzing portfolio: {', '.join(validated)}")
                    reports = await analyze_portfolio(agent, validated)
                    
                    if reports:
                        if args.format == "rich":
                            display_portfolio_summary_rich(reports)
                            console.print("\n📋 [bold]Detailed Reports:[/bold]")
                            for report in reports:
                                display_report_rich(report)
                        elif args.format == "json":
                            import json
                            print(json.dumps([r.model_dump() for r in reports], indent=2, default=str))
                        elif args.format == "csv":
                            display_report_csv(reports)
                        elif args.format == "summary":
                            display_report_summary(reports)
                    else:
                        console.print("❌ No successful analyses")
                        sys.exit(1)
                else:
                    show_cli_demo("portfolio", validated)
                    
            except ValueError as e:
                console.print(f"❌ Invalid stock symbols: {e}")
                sys.exit(1)
    
    except KeyboardInterrupt:
        console.print("\n👋 Operation cancelled by user")
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {str(e)}")
        if args.debug:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())