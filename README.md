# Agentic Stock Analyzer

A comprehensive demo repository for teaching agentic communication patterns through practical stock analysis. This educational project demonstrates how AI agents can reason, act, and observe to solve real-world problems using the ReACT (Reasoning and Acting) pattern and other advanced agentic communication strategies.

## 🎯 Project Overview

This educational project showcases different agentic communication patterns through a practical stock analysis system:

- **Lecture 01**: Single Agent ReACT Pattern - A single AI agent that can reason, act, and observe to analyze stocks
- **Future Lectures**: Multi-agent patterns, hierarchical agents, and advanced communication strategies

### Educational Goals

- **Understand Agentic Patterns**: Learn how AI agents can autonomously reason and take actions
- **Practical Implementation**: See real-world applications of agent patterns in financial analysis
- **Extensible Architecture**: Build a foundation for exploring advanced agent communication patterns
- **Best Practices**: Learn proper error handling, testing, and documentation for agent systems

## 🧠 ReACT Pattern Implementation

### What is ReACT?

ReACT (Reasoning and Acting) is an agentic communication pattern where AI agents:

1. **Reason** about the current situation and what actions to take
2. **Act** by using available tools to gather information or perform tasks
3. **Observe** the results of their actions
4. **Repeat** the cycle until the goal is achieved

### Our Implementation

Our stock analysis agent demonstrates the ReACT pattern through:

```python
# The agent reasons about what information it needs
"I need to analyze AAPL. Let me gather company information, financial metrics, and recent news."

# The agent acts by using research tools
agent.use_tool("search_company_info", symbol="AAPL")
agent.use_tool("search_recent_news", symbol="AAPL")

# The agent observes the results
"I found that Apple has strong financials but recent news shows supply chain concerns."

# The agent reasons about the next action
"Based on this information, I can now provide an investment recommendation."
```

### Key Components

1. **Agent Definition**: Using Pydantic-AI framework for type-safe agent implementation
2. **Tool Integration**: Tavily research tool for real-time financial data
3. **Structured Output**: Pydantic models ensure consistent, validated responses
4. **Error Handling**: Graceful degradation when tools fail or data is incomplete

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** (required for modern async features and type hints)
- **[UV package manager](https://docs.astral.sh/uv/getting-started/installation/)** (fast, modern Python package management)
- **API Keys**:
  - [Tavily API](https://tavily.com/) for web search and financial data
  - [OpenAI](https://openai.com/) or [Anthropic](https://anthropic.com/) for AI models

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd agentic-stock-analyzer
   make setup
   ```

2. **Configure your API keys:**
   Edit the `.env` file created by setup:
   
   **Option A: Using LiteLLM Proxy (Recommended for custom deployments)**
   ```bash
   # Required: Tavily API for web search
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # LiteLLM Configuration
   LITELLM_BASE_URL=http://litellm.litellm.svc.cluster.local:4000
   LITELLM_API_KEY=sk-wandlitellm
   AGENT_MODEL=gpt-4
   ```
   
   **Option B: Direct API Access**
   ```bash
   # Required: Tavily API for web search
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Choose one AI provider
   OPENAI_API_KEY=your_openai_api_key_here
   # OR
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   AGENT_MODEL=openai:gpt-4o
   ```

3. **Verify your setup:**
   ```bash
   make check-env
   ```

4. **Try the system:**
   ```bash
   # Run educational demo (recommended first step)
   python cli.py --demo
   
   # Analyze a single stock
   python cli.py --stock AAPL
   
   # Interactive exploration
   python cli.py --interactive
   ```

## 📁 Project Architecture

### Directory Structure

```
agentic-stock-analyzer/
├── common/                    # Shared utilities and models
│   ├── __init__.py
│   ├── config.py             # Pydantic-based configuration management
│   ├── models.py             # Data models for stock analysis
│   ├── utils.py              # Tavily integration and utilities
│   └── check_env.py          # Environment validation
├── lecture01/                # Single Agent ReACT Pattern
│   ├── __init__.py
│   ├── agent.py              # Agent definition and tools
│   └── main.py               # Main lecture implementation
├── tests/                    # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── fixtures.py           # Test data and mocks
│   ├── test_models.py        # Unit tests for data models
│   ├── test_config.py        # Configuration testing
│   ├── test_utils.py         # Utility function tests
│   ├── test_agent_integration.py  # Agent workflow tests
│   └── test_end_to_end.py    # Complete pipeline tests
├── .env.template             # Environment variables template
├── .env                      # Your API keys (created by setup)
├── cli.py                    # Command-line interface
├── demo.py                   # Educational demo script
├── examples.py               # Usage examples
├── run_tests.py              # Test runner with multiple modes
├── Makefile                  # Project automation
├── pyproject.toml            # Project configuration
└── README.md                 # This documentation
```

### Key Components

#### 1. Data Models (`common/models.py`)
Pydantic models ensuring type safety and data validation:
- `StockSymbol`: Stock ticker validation
- `CompanyInfo`: Company details and metadata
- `FinancialMetrics`: Real-time financial data
- `NewsItem`: News articles with sentiment analysis
- `MarketSentiment`: Aggregated market sentiment
- `RiskAssessment`: Investment risk evaluation
- `InvestmentRecommendation`: AI-generated investment advice
- `StockReport`: Complete analysis report

#### 2. Agent Implementation (`lecture01/agent.py`)
Single agent using ReACT pattern:
- Pydantic-AI framework integration
- Tool registration and management
- Structured reasoning and action loops
- Error handling and graceful degradation

#### 3. Research Tools (`common/utils.py`)
Tavily API integration for real-time data:
- Company information lookup
- Recent news and sentiment analysis
- Financial metrics gathering
- Market trend analysis

## 🖥️ Command Line Interface

### Basic Usage

```bash
# Analyze a single stock with rich output
python cli.py --stock AAPL

# Analyze multiple stocks (portfolio analysis)
python cli.py --portfolio AAPL GOOGL MSFT

# Interactive mode for exploration
python cli.py --interactive

# Educational demo with explanations
python cli.py --demo
```

### Output Formats

The CLI supports multiple output formats for different use cases:

```bash
# Rich terminal output (default) - Beautiful, human-readable
python cli.py --stock AAPL --format rich

# JSON format - Machine-readable, API-friendly
python cli.py --stock AAPL --format json

# CSV format - Spreadsheet-compatible
python cli.py --portfolio AAPL GOOGL MSFT --format csv

# Summary format - Quick overview
python cli.py --portfolio AAPL GOOGL MSFT --format summary
```

### Advanced Options

```bash
# Use different AI model
python cli.py --stock AAPL --model anthropic:claude-3-sonnet

# Enable debug mode for troubleshooting
python cli.py --stock AAPL --debug

# Disable colors for plain text output
python cli.py --stock AAPL --no-color

# Export results to file
python cli.py --portfolio AAPL GOOGL MSFT --format csv > portfolio_analysis.csv
```

### Getting Help

```bash
# Show all CLI options
python cli.py --help

# Show usage examples with explanations
python examples.py

# Run comprehensive demo with educational content
python demo.py
```

## 📊 Example Outputs

### Single Stock Analysis (Rich Format)

```
📈 Stock Analysis: AAPL
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│ Company: Apple Inc.                                                         │
│ Symbol: AAPL                                                                │
│ Sector: Technology                                                          │
│ Industry: Consumer Electronics                                              │
│                                                                             │
│ Financial Metrics                                                           │
│ • Current Price: $185.92                                                   │
│ • Price Change: $2.15                                                      │
│ • Price Change %: +1.17%                                                   │
│ • Volume: 45,123,456                                                       │
│ • P/E Ratio: 28.5                                                          │
│ • Dividend Yield: 0.52%                                                    │
│                                                                             │
│ Investment Recommendation                                                   │
│ • Recommendation: BUY                                                      │
│ • Confidence: 85%                                                          │
│ • Time Horizon: 6-12 months                                               │
│ • Reasoning: Strong fundamentals with innovative product pipeline and      │
│   solid financial position despite recent market volatility               │
│                                                                             │
│ Risk Assessment                                                             │
│ • Risk Level: MEDIUM                                                       │
│ • Volatility: Moderate with seasonal patterns                             │
│ • Risk Factors: Supply chain dependencies, regulatory scrutiny            │
│                                                                             │
│ Market Sentiment                                                            │
│ • Overall Sentiment: POSITIVE                                              │
│ • Confidence: 78%                                                          │
│ • Key Factors: Strong earnings, product innovation, market leadership     │
│                                                                             │
│ Recent News                                                                 │
│ • Apple announces new AI features in latest iOS update                    │
│   Sentiment: Positive                                                      │
│ • Supply chain concerns ease as production ramps up                       │
│   Sentiment: Positive                                                      │
│ • Regulatory challenges in EU markets continue                            │
│   Sentiment: Negative                                                      │
│                                                                             │
│ Analysis performed: 2024-08-14 15:30:22                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Portfolio Analysis (Summary Format)

```
📋 Analysis Summary (3 stocks)
==================================================
AAPL | BUY (85%) | Risk: MEDIUM | $185.92
GOOGL | HOLD (72%) | Risk: MEDIUM | $142.35
MSFT | BUY (91%) | Risk: LOW | $378.85
```

### JSON Output Example

```json
{
  "symbol": "AAPL",
  "company_info": {
    "name": "Apple Inc.",
    "symbol": "AAPL",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "market_cap": 2850000000000,
    "description": "Apple Inc. designs, manufactures, and markets smartphones..."
  },
  "financial_metrics": {
    "current_price": 185.92,
    "price_change": 2.15,
    "price_change_percent": 1.17,
    "volume": 45123456,
    "pe_ratio": 28.5,
    "dividend_yield": 0.52
  },
  "investment_recommendation": {
    "recommendation": "buy",
    "confidence": 0.85,
    "reasoning": "Strong fundamentals with innovative product pipeline...",
    "target_price": 205.0,
    "time_horizon": "6-12 months"
  },
  "risk_assessment": {
    "risk_level": "medium",
    "risk_factors": ["Supply chain dependencies", "Regulatory scrutiny"],
    "volatility_assessment": "Moderate with seasonal patterns"
  },
  "market_sentiment": {
    "overall_sentiment": "positive",
    "confidence_score": 0.78,
    "key_factors": ["Strong earnings", "Product innovation", "Market leadership"]
  },
  "recent_news": [
    {
      "title": "Apple announces new AI features in latest iOS update",
      "summary": "Apple unveiled significant AI enhancements...",
      "url": "https://example.com/news/apple-ai-features",
      "published_date": "2024-08-14T10:30:00Z",
      "sentiment": "positive"
    }
  ],
  "analysis_timestamp": "2024-08-14T15:30:22Z"
}
```

## 🛠️ Development Commands

### Quick Reference

| Command | Description |
|---------|-------------|
| `make setup` | Setup project (install dependencies, create .env) |
| `make run1` | Run lecture 1 (Single Agent ReACT Pattern) |
| `make test` | Run all tests with coverage |
| `make test-fast` | Run fast tests (exclude slow/e2e) |
| `make test-unit` | Run unit tests only |
| `make test-integration` | Run integration tests only |
| `make test-e2e` | Run end-to-end tests only |
| `make test-quality` | Run quality checks (type checking, formatting) |
| `make test-full` | Run complete test suite |
| `make lint` | Run linting (mypy, black --check, isort --check) |
| `make format` | Format code (black, isort) |
| `make clean` | Clean up temporary files |
| `make install-dev` | Install development dependencies |
| `make check-env` | Check if required environment variables are set |
| `make help` | Show all available commands |

### Testing

The project includes a comprehensive test suite with 90+ tests:

```bash
# Run all tests with coverage report
make test

# Run specific test categories
make test-unit          # Unit tests (models, config, utils)
make test-integration   # Integration tests (agent workflow)
make test-e2e          # End-to-end tests (complete pipeline)

# Run quality checks
make test-quality       # Type checking, formatting, imports

# Run everything
make test-full         # Quality checks + all tests
```

### Code Quality

```bash
# Check code quality
make lint

# Format code automatically
make format

# Check specific issues
uv run mypy common/ lecture01/     # Type checking
uv run black --check .             # Code formatting
uv run isort --check-only .        # Import sorting
```

## 🎓 Educational Content

### Lecture 01: Single Agent ReACT Pattern

**Status**: ✅ Complete

**Learning Objectives**:
- Understand the ReACT pattern (Reasoning, Acting, Observing)
- Learn how agents use tools to gather information
- See how structured output ensures consistent results
- Practice error handling in agentic systems

**Key Concepts Demonstrated**:

1. **Agent Reasoning**: The agent analyzes what information it needs
2. **Tool Usage**: Integration with external APIs (Tavily) for data gathering
3. **Structured Output**: Pydantic models ensure consistent, validated responses
4. **Error Handling**: Graceful degradation when tools fail or data is incomplete

**Run the Lecture**:
```bash
# Educational demo with explanations
python cli.py --demo

# Interactive exploration
python cli.py --interactive

# Direct analysis
python cli.py --stock AAPL

# Module execution
make run1
```

### Future Lectures (Planned)

- **Lecture 02**: Multi-Agent Collaboration - Multiple agents working together
- **Lecture 03**: Hierarchical Agent Systems - Supervisor and worker agents
- **Lecture 04**: Agent Communication Protocols - Advanced messaging patterns

## ⚙️ Configuration

### Environment Variables

The project uses environment-based configuration with validation:

**LiteLLM Configuration (Recommended for custom deployments):**
```bash
# Core API Configuration
TAVILY_API_KEY=your_tavily_api_key_here    # Required for research

# LiteLLM Proxy Configuration
LITELLM_BASE_URL=http://litellm.litellm.svc.cluster.local:4000  # LiteLLM proxy URL
LITELLM_API_KEY=sk-wandlitellm             # LiteLLM proxy API key

# Agent Configuration
AGENT_MODEL=gpt-4                          # Model name as configured in LiteLLM
AGENT_TEMPERATURE=0.1                      # Model temperature (0.0-1.0)
AGENT_MAX_RETRIES=3                        # Maximum retry attempts

# Tavily Search Configuration
TAVILY_MAX_RESULTS=10                      # Maximum search results
TAVILY_SEARCH_DEPTH=advanced               # Search depth (basic/advanced)

# Application Settings
DEBUG=false                                # Enable debug mode
LOG_LEVEL=INFO                            # Logging level
```

**Direct API Configuration (Alternative):**
```bash
# Core API Configuration
TAVILY_API_KEY=your_tavily_api_key_here    # Required for research
OPENAI_API_KEY=your_openai_api_key_here    # Required for AI (or Anthropic)
ANTHROPIC_API_KEY=your_anthropic_key_here  # Alternative to OpenAI

# Agent Configuration
AGENT_MODEL=openai:gpt-4o                  # AI model to use
AGENT_TEMPERATURE=0.1                      # Model temperature (0.0-1.0)
AGENT_MAX_RETRIES=3                        # Maximum retry attempts

# Other settings same as above...
```

### Configuration Validation

The system validates all configuration on startup:

```bash
# Check your configuration
make check-env

# Or directly
python -m common.check_env
```

### Supported AI Models

**With LiteLLM Proxy:**
- Any model configured in your LiteLLM proxy (e.g., `gpt-4`, `gpt-3.5-turbo`, `claude-3-sonnet`)
- Model names should match your LiteLLM configuration

**Direct API Access:**
- **OpenAI**: `openai:gpt-4o`, `openai:gpt-4o-mini`, `openai:gpt-3.5-turbo`
- **Anthropic**: `anthropic:claude-3-sonnet`, `anthropic:claude-3-haiku`

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Configuration Issues

**"Configuration error" when running commands:**
```bash
# Check if .env file exists and has correct format
make check-env

# Recreate .env from template
cp .env.template .env
# Then edit .env with your API keys
```

**"TAVILY_API_KEY not found":**
```bash
# Ensure your .env file contains:
TAVILY_API_KEY=your_actual_api_key_here

# Verify the key is valid by running:
python cli.py --demo
```

#### Installation Issues

**"Module not found" errors:**
```bash
# Ensure UV is installed and project is set up
make setup

# Verify Python version (requires 3.12+)
python --version

# Reinstall dependencies
uv sync
```

**UV not found:**
```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### Runtime Issues

**API key issues:**
```bash
# Verify API keys are correct and have sufficient quota
# Check Tavily dashboard: https://tavily.com/
# Check OpenAI usage: https://platform.openai.com/usage
```

**Network/timeout errors:**
```bash
# Enable debug mode to see detailed error messages
python cli.py --stock AAPL --debug

# Try with a different stock symbol
python cli.py --stock MSFT --debug
```

**Invalid stock symbols:**
```bash
# Use valid ticker symbols (e.g., AAPL, not Apple)
# Check symbol validity on financial websites
python cli.py --stock AAPL  # ✅ Valid
python cli.py --stock Apple # ❌ Invalid
```

#### Performance Issues

**Slow analysis:**
```bash
# Use summary format for quick checks
python cli.py --portfolio AAPL GOOGL MSFT --format summary

# Analyze stocks individually for detailed reports
python cli.py --stock AAPL --format rich
```

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Enable debug mode
python cli.py --stock AAPL --debug

# Check environment variables
DEBUG=true python cli.py --stock AAPL

# View detailed logs
LOG_LEVEL=DEBUG python cli.py --stock AAPL
```

### Getting Help

1. **Check Configuration**: `make check-env`
2. **Run Tests**: `make test` to verify system health
3. **Try Demo**: `python cli.py --demo` for guided experience
4. **Enable Debug**: Add `--debug` flag to any command
5. **Check Documentation**: Review `.env.template` for required variables

## 🔄 Workflow Examples

### Daily Portfolio Monitoring

```bash
# Morning routine: Quick portfolio check
python cli.py --portfolio AAPL GOOGL MSFT AMZN --format summary

# Detailed analysis for concerning stocks
python cli.py --stock AAPL --format rich

# Export for spreadsheet analysis
python cli.py --portfolio AAPL GOOGL MSFT --format csv > daily_report.csv
```

### Investment Research

```bash
# Interactive exploration of new stock
python cli.py --interactive

# Detailed analysis with data export
python cli.py --stock NVDA --format json > nvda_analysis.json

# Competitive analysis
python cli.py --portfolio NVDA AMD INTC --format rich
```

### Automated Reporting

```bash
# Generate reports for automated systems
python cli.py --portfolio AAPL GOOGL MSFT --format json > dashboard_data.json

# Create CSV for Excel analysis
python cli.py --portfolio AAPL GOOGL MSFT --format csv > portfolio_analysis.csv

# Quick status updates
python cli.py --portfolio AAPL GOOGL MSFT --format summary | tee status.txt
```

## 🚀 Adding Future Lecture Patterns

### Architecture for Extensibility

The project is designed to easily accommodate new agentic communication patterns:

#### 1. Create New Lecture Directory

```bash
# Create lecture directory
mkdir lecture02
touch lecture02/__init__.py
touch lecture02/main.py
touch lecture02/agent.py
```

#### 2. Implement New Pattern

```python
# lecture02/agent.py - Example multi-agent pattern
from pydantic_ai import Agent
from common.models import StockReport
from common.config import AppConfig

class MultiAgentSystem:
    def __init__(self, config: AppConfig):
        self.research_agent = Agent(...)  # Specialized for research
        self.analysis_agent = Agent(...)  # Specialized for analysis
        self.coordinator = Agent(...)     # Coordinates other agents
    
    async def analyze_stock(self, symbol: str) -> StockReport:
        # Multi-agent collaboration logic
        research_data = await self.research_agent.run(symbol)
        analysis = await self.analysis_agent.run(research_data)
        return await self.coordinator.synthesize(analysis)
```

#### 3. Update Project Configuration

```toml
# pyproject.toml - Add new package
[tool.hatch.build.targets.wheel]
packages = ["common", "lecture01", "lecture02"]
```

```makefile
# Makefile - Add new command
run2: check-env
	@echo "🎓 Running Lecture 2: Multi-Agent Pattern..."
	uv run python -m lecture02.main
```

#### 4. Add Tests

```python
# tests/test_lecture02.py
import pytest
from lecture02.agent import MultiAgentSystem

class TestMultiAgentSystem:
    def test_agent_coordination(self):
        # Test multi-agent coordination
        pass
    
    def test_specialized_agents(self):
        # Test individual agent specialization
        pass
```

#### 5. Update Documentation

```markdown
# README.md - Add new lecture section
### Lecture 02: Multi-Agent Collaboration

**Status**: 🚧 In Development

**Concept**: Multiple specialized agents working together:
- Research Agent: Gathers financial data
- Analysis Agent: Performs technical analysis  
- Coordinator Agent: Synthesizes results

**Run**: `make run2` or `python -m lecture02.main`
```

### Design Patterns for New Lectures

#### Common Interface Pattern

```python
# common/interfaces.py
from abc import ABC, abstractmethod
from common.models import StockReport

class StockAnalyzer(ABC):
    @abstractmethod
    async def analyze_stock(self, symbol: str) -> StockReport:
        pass
    
    @abstractmethod
    async def analyze_portfolio(self, symbols: list[str]) -> list[StockReport]:
        pass
```

#### Shared Utilities

```python
# common/agent_utils.py
def create_agent_with_tools(config: AppConfig, tools: list):
    """Create agent with common tool setup"""
    pass

def setup_logging_for_agent(agent_name: str, debug: bool):
    """Setup consistent logging across agents"""
    pass
```

#### Configuration Extension

```python
# common/config.py - Extend for new patterns
class MultiAgentConfig(BaseModel):
    research_agent_model: str = "openai:gpt-4o-mini"
    analysis_agent_model: str = "openai:gpt-4o"
    coordinator_model: str = "openai:gpt-4o"
    max_coordination_rounds: int = 3

class AppConfig(BaseModel):
    # ... existing config ...
    multi_agent: MultiAgentConfig = MultiAgentConfig()
```

### Testing New Patterns

```python
# tests/test_new_pattern.py
import pytest
from lecture02.agent import MultiAgentSystem

class TestNewPattern:
    @pytest.fixture
    def multi_agent_system(self, test_config):
        return MultiAgentSystem(test_config)
    
    def test_pattern_implementation(self, multi_agent_system):
        # Test the new communication pattern
        pass
    
    def test_error_handling(self, multi_agent_system):
        # Test error scenarios specific to the pattern
        pass
```

## 📚 Learning Resources

### Core Technologies

- **[Pydantic AI Documentation](https://ai.pydantic.dev/)** - Modern Python AI framework
- **[Tavily API Documentation](https://docs.tavily.com/)** - Web search and research API
- **[UV Package Manager](https://docs.astral.sh/uv/)** - Fast Python package management

### Agentic Patterns

- **[ReACT Pattern Paper](https://arxiv.org/abs/2210.03629)** - Original ReACT research
- **[Agent Communication Patterns](https://arxiv.org/abs/2308.08155)** - Multi-agent communication
- **[Tool-Using Agents](https://arxiv.org/abs/2302.04761)** - Agents with external tools

### Python Development

- **[Python 3.12 Features](https://docs.python.org/3.12/whatsnew/3.12.html)** - Latest Python features
- **[Pydantic Documentation](https://docs.pydantic.dev/)** - Data validation and settings
- **[Rich Documentation](https://rich.readthedocs.io/)** - Terminal formatting

## 🤝 Contributing

This is an educational project designed for learning and experimentation. Contributions are welcome!

### Ways to Contribute

1. **Add New Lecture Patterns**: Implement additional agentic communication patterns
2. **Improve Existing Code**: Enhance error handling, performance, or documentation
3. **Add Tests**: Expand test coverage or add new test scenarios
4. **Documentation**: Improve explanations, add examples, or fix typos
5. **Bug Reports**: Report issues or unexpected behavior

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/agentic-stock-analyzer.git
cd agentic-stock-analyzer

# Set up development environment
make setup
make install-dev

# Run tests to ensure everything works
make test-full

# Make your changes and test
make test
make lint

# Submit a pull request
```

### Code Standards

- **Python 3.12+**: Use modern Python features and type hints
- **Type Safety**: All code should pass mypy type checking
- **Testing**: Add tests for new functionality
- **Documentation**: Update README and docstrings
- **Code Style**: Use black and isort for formatting

## 📄 License

This project is for educational purposes. Please check individual API provider terms for commercial usage.

### API Provider Terms

- **Tavily**: Check [Tavily Terms of Service](https://tavily.com/terms)
- **OpenAI**: Check [OpenAI Usage Policies](https://openai.com/policies/usage-policies)
- **Anthropic**: Check [Anthropic Usage Policy](https://www.anthropic.com/usage-policy)

---

## 🎉 Ready to Start Learning?

1. **Set up the project**: `make setup`
2. **Configure your API keys**: Edit `.env` file
3. **Run the demo**: `python cli.py --demo`
4. **Explore interactively**: `python cli.py --interactive`
5. **Analyze your first stock**: `python cli.py --stock AAPL`

Happy learning! 🚀