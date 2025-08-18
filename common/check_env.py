#!/usr/bin/env python3
"""Environment configuration checker for the Agentic Stock Analyzer."""

import os
import sys
from typing import List, Tuple

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables from .env file
load_dotenv()

console = Console()


def check_environment() -> Tuple[bool, List[str]]:
    """Check if all required environment variables are set.
    
    Returns:
        Tuple of (success, list of issues)
    """
    issues = []
    
    # Check Tavily API key
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        issues.append("TAVILY_API_KEY is not set")
    elif tavily_key == "your_tavily_api_key_here":
        issues.append("TAVILY_API_KEY is still set to placeholder value")
    
    # Check LiteLLM configuration
    litellm_base_url = os.getenv("LITELLM_BASE_URL")
    litellm_api_key = os.getenv("LITELLM_API_KEY")
    
    if litellm_base_url and litellm_api_key:
        console.print("✅ LiteLLM configuration detected")
        console.print(f"   Base URL: {litellm_base_url}")
        console.print(f"   API Key: {litellm_api_key[:10]}...")
    else:
        # Check for standard API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not openai_key and not anthropic_key:
            issues.append("No AI provider configured. Set either LiteLLM credentials or OPENAI_API_KEY/ANTHROPIC_API_KEY")
    
    # Check agent model configuration
    agent_model = os.getenv("AGENT_MODEL", "gpt-4")
    console.print(f"📋 Agent model: {agent_model}")
    
    return len(issues) == 0, issues


def display_configuration():
    """Display current configuration."""
    table = Table(title="Current Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    table.add_column("Status", style="green")
    
    # Tavily configuration
    tavily_key = os.getenv("TAVILY_API_KEY", "Not set")
    tavily_status = "✅ Set" if tavily_key and tavily_key != "your_tavily_api_key_here" and tavily_key != "Not set" else "❌ Missing"
    table.add_row("TAVILY_API_KEY", f"{tavily_key[:10]}..." if len(tavily_key) > 10 and tavily_key != "Not set" else tavily_key, tavily_status)
    
    # LiteLLM configuration
    litellm_base_url = os.getenv("LITELLM_BASE_URL", "Not set")
    litellm_api_key = os.getenv("LITELLM_API_KEY", "Not set")
    
    if litellm_base_url != "Not set":
        table.add_row("LITELLM_BASE_URL", litellm_base_url, "✅ Set")
        litellm_key_status = "✅ Set" if litellm_api_key != "Not set" else "❌ Missing"
        table.add_row("LITELLM_API_KEY", f"{litellm_api_key[:10]}..." if len(litellm_api_key) > 10 else litellm_api_key, litellm_key_status)
    else:
        # Check standard API keys
        openai_key = os.getenv("OPENAI_API_KEY", "Not set")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "Not set")
        
        openai_status = "✅ Set" if openai_key != "Not set" else "❌ Missing"
        anthropic_status = "✅ Set" if anthropic_key != "Not set" else "❌ Missing"
        
        table.add_row("OPENAI_API_KEY", f"{openai_key[:10]}..." if len(openai_key) > 10 else openai_key, openai_status)
        table.add_row("ANTHROPIC_API_KEY", f"{anthropic_key[:10]}..." if len(anthropic_key) > 10 else anthropic_key, anthropic_status)
    
    # Agent configuration
    table.add_row("AGENT_MODEL", os.getenv("AGENT_MODEL", "gpt-4"), "✅ Set")
    table.add_row("AGENT_TEMPERATURE", os.getenv("AGENT_TEMPERATURE", "0.1"), "✅ Set")
    table.add_row("DEBUG", os.getenv("DEBUG", "false"), "✅ Set")
    
    console.print(table)


def main():
    """Main function to check environment configuration."""
    console.print(Panel.fit("🔧 Environment Configuration Check", style="bold blue"))
    
    # Display current configuration
    display_configuration()
    
    # Check for issues
    success, issues = check_environment()
    
    if success:
        console.print("\n✅ [bold green]Environment configuration is valid![/bold green]")
        console.print("\n🚀 You can now run:")
        console.print("   • python cli.py --demo")
        console.print("   • python cli.py --stock AAPL")
        console.print("   • python cli.py --interactive")
    else:
        console.print("\n❌ [bold red]Environment configuration issues found:[/bold red]")
        for issue in issues:
            console.print(f"   • {issue}")
        
        console.print("\n🔧 [bold yellow]To fix these issues:[/bold yellow]")
        console.print("   1. Edit your .env file")
        console.print("   2. Add the missing API keys")
        console.print("   3. Run this check again: python -m common.check_env")
        
        sys.exit(1)


if __name__ == "__main__":
    main()