"""
Lecture 01: Single Agent ReACT Pattern

This module demonstrates a single AI agent that follows the ReACT
(Reasoning, Acting, Observing) pattern to analyze stocks.
"""

import asyncio
import logging
import sys
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from common.config import get_config
from common.models import StockReport
from lecture01.agent import StockAnalysisAgent

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rich console for beautiful output
console = Console()


async def analyze_single_stock(agent: StockAnalysisAgent, symbol: str) -> Optional[StockReport]:
    """Analyze a single stock using the ReACT agent.
    
    Args:
        agent: The stock analysis agent instance
        symbol: Stock ticker symbol to analyze
        
    Returns:
        StockReport if successful, None if analysis failed
    """
    try:
        console.print(f"\n🔍 Analyzing stock: [bold blue]{symbol}[/bold blue]")
        
        # Use agent.run_sync for synchronous execution as specified in requirements
        report = agent.analyze_stock_sync(symbol)
        
        console.print(f"✅ Successfully analyzed [bold green]{symbol}[/bold green]")
        return report
        
    except Exception as e:
        logger.error(f"Failed to analyze stock {symbol}: {str(e)}")
        console.print(f"❌ Failed to analyze [bold red]{symbol}[/bold red]: {str(e)}")
        return None


async def analyze_portfolio(agent: StockAnalysisAgent, symbols: List[str]) -> List[StockReport]:
    """Analyze multiple stocks in a portfolio.
    
    Args:
        agent: The stock analysis agent instance
        symbols: List of stock ticker symbols to analyze
        
    Returns:
        List of StockReport objects for successfully analyzed stocks
    """
    console.print(f"\n📊 Analyzing portfolio with {len(symbols)} stocks...")
    
    reports = []
    
    for i, symbol in enumerate(symbols, 1):
        console.print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        
        try:
            report = await analyze_single_stock(agent, symbol)
            if report:
                reports.append(report)
        except Exception as e:
            logger.error(f"Error in portfolio analysis for {symbol}: {str(e)}")
            console.print(f"⚠️  Skipping {symbol} due to error: {str(e)}")
            continue
    
    console.print(f"\n✅ Portfolio analysis complete: {len(reports)}/{len(symbols)} stocks analyzed successfully")
    return reports


def display_stock_report(report: StockReport) -> None:
    """Display a formatted stock report using Rich.
    
    Args:
        report: StockReport to display
    """
    # Create main report panel
    report_content = f"""
[bold]Company:[/bold] {report.company_info.name}
[bold]Sector:[/bold] {report.company_info.sector}
[bold]Industry:[/bold] {report.company_info.industry}

[bold]Financial Metrics:[/bold]
• Current Price: ${report.financial_metrics.current_price or 'N/A'}
• P/E Ratio: {report.financial_metrics.pe_ratio or 'N/A'}
• Volume: {f'{report.financial_metrics.volume:,}' if report.financial_metrics.volume else 'N/A'}

[bold]Investment Recommendation:[/bold] {report.investment_recommendation.recommendation.upper()}
[bold]Confidence:[/bold] {report.investment_recommendation.confidence:.1%}
[bold]Reasoning:[/bold] {report.investment_recommendation.reasoning}

[bold]Risk Level:[/bold] {report.risk_assessment.risk_level.upper()}
[bold]Market Sentiment:[/bold] {report.market_sentiment.overall_sentiment.upper()}
"""
    
    panel = Panel(
        report_content,
        title=f"📈 Stock Analysis: {report.symbol}",
        border_style="blue"
    )
    
    console.print(panel)


def display_portfolio_summary(reports: List[StockReport]) -> None:
    """Display a summary table of portfolio analysis results.
    
    Args:
        reports: List of StockReport objects to summarize
    """
    if not reports:
        console.print("❌ No successful stock analyses to display")
        return
    
    # Create summary table
    table = Table(title="📊 Portfolio Analysis Summary")
    table.add_column("Symbol", style="cyan", no_wrap=True)
    table.add_column("Company", style="magenta")
    table.add_column("Recommendation", style="green")
    table.add_column("Confidence", style="yellow")
    table.add_column("Risk Level", style="red")
    table.add_column("Sentiment", style="blue")
    
    for report in reports:
        table.add_row(
            report.symbol,
            report.company_info.name[:30] + "..." if len(report.company_info.name) > 30 else report.company_info.name,
            report.investment_recommendation.recommendation.upper(),
            f"{report.investment_recommendation.confidence:.1%}",
            report.risk_assessment.risk_level.upper(),
            report.market_sentiment.overall_sentiment.upper()
        )
    
    console.print(table)


async def run_demo() -> None:
    """Run the stock analysis demo."""
    console.print(Panel.fit("🎓 Lecture 01: Single Agent ReACT Pattern", style="bold blue"))
    
    try:
        # Load configuration
        config = get_config()
        
        # Validate configuration
        if not config.tavily.api_key:
            console.print("❌ [bold red]Error:[/bold red] TAVILY_API_KEY not found in environment variables")
            console.print("Please set your Tavily API key in the .env file")
            return
        
        console.print(f"📊 Agent Model: [bold]{config.agent.model_name}[/bold]")
        console.print(f"🔍 Search Provider: [bold]Tavily[/bold]")
        console.print(f"🐛 Debug Mode: [bold]{config.debug}[/bold]")
        
        # Initialize the stock analysis agent
        console.print("\n🤖 Initializing Stock Analysis Agent...")
        agent = StockAnalysisAgent(config)
        
        # Demo 1: Single stock analysis
        console.print("\n" + "="*60)
        console.print("📈 [bold]Demo 1: Single Stock Analysis[/bold]")
        console.print("="*60)
        
        demo_symbol = "AAPL"  # Apple Inc. as a demo stock
        single_report = await analyze_single_stock(agent, demo_symbol)
        
        if single_report:
            display_stock_report(single_report)
        
        # Demo 2: Portfolio analysis
        console.print("\n" + "="*60)
        console.print("📊 [bold]Demo 2: Portfolio Analysis[/bold]")
        console.print("="*60)
        
        demo_portfolio = ["AAPL", "GOOGL", "MSFT"]  # Tech portfolio
        portfolio_reports = await analyze_portfolio(agent, demo_portfolio)
        
        if portfolio_reports:
            display_portfolio_summary(portfolio_reports)
            
            # Show detailed reports for each stock
            console.print("\n📋 [bold]Detailed Reports:[/bold]")
            for report in portfolio_reports:
                display_stock_report(report)
        
        console.print("\n✅ [bold green]Demo completed successfully![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        console.print(f"\n❌ [bold red]Demo failed:[/bold red] {str(e)}")
        if config.debug:
            console.print_exception()


async def interactive_mode() -> None:
    """Run interactive stock analysis mode."""
    console.print(Panel.fit("🎯 Interactive Stock Analysis Mode", style="bold green"))
    
    try:
        # Load configuration and initialize agent
        config = get_config()
        
        if not config.tavily.api_key:
            console.print("❌ [bold red]Error:[/bold red] TAVILY_API_KEY not found in environment variables")
            return
        
        agent = StockAnalysisAgent(config)
        
        while True:
            console.print("\n" + "="*50)
            console.print("Choose an option:")
            console.print("1. Analyze single stock")
            console.print("2. Analyze portfolio (multiple stocks)")
            console.print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
                if symbol:
                    report = await analyze_single_stock(agent, symbol)
                    if report:
                        display_stock_report(report)
                else:
                    console.print("❌ Please enter a valid stock symbol")
            
            elif choice == "2":
                symbols_input = input("Enter stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT): ").strip()
                if symbols_input:
                    symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]
                    if symbols:
                        reports = await analyze_portfolio(agent, symbols)
                        if reports:
                            display_portfolio_summary(reports)
                    else:
                        console.print("❌ Please enter valid stock symbols")
                else:
                    console.print("❌ Please enter stock symbols")
            
            elif choice == "3":
                console.print("👋 Goodbye!")
                break
            
            else:
                console.print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Interactive mode failed: {str(e)}")
        console.print(f"\n❌ [bold red]Error:[/bold red] {str(e)}")


def main() -> None:
    """Main entry point for Lecture 01."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Run in interactive mode
        asyncio.run(interactive_mode())
    else:
        # Run demo mode
        asyncio.run(run_demo())


if __name__ == "__main__":
    main()
