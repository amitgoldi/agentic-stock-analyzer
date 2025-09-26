# Tikal Lecture: Communication Patterns with AI Agents

This is a demo project for progressive live coding demonstrations showing different approaches to building AI agents for stock analysis.

## Project Structure

```
tikal-lecture-communication-patterns/
├── common/                 # Shared utilities and models
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models for data structures
│   └── utils.py           # Common utility functions
├── lecture01/             # Lecture 1: Single Agent
│   ├── __init__.py
│   ├── agent.py           # Single agent implementation
│   └── main.py            # Main entry point for demo
├── lecture02/             # Lecture 2: Agent Delegation
│   ├── __init__.py
│   ├── agent.py           # StockRecommender agent implementation
│   └── main.py            # Main entry point for demo
├── .env.example           # Environment variables template
├── .env                   # Environment variables (create from .env.example, not in git)
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Setup

1. **Quick setup with make:**
   ```bash
   make setup
   # This will install dependencies and set up pre-commit hooks
   ```

2. **Manual setup (alternative):**
   ```bash
   # Install dependencies
   uv sync --extra dev

   # Set up pre-commit hooks
   uv run pre-commit install
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Development Workflow

This project includes a simple development workflow with formatting, linting, and type checking:

### Make Commands

```bash
make            # Run all checks (setup, format, lint, type-check)
make setup      # Install dependencies and set up pre-commit hooks
make format     # Format code with black and isort
make lint       # Run linting with ruff
make type-check # Run type checking with mypy
make check      # Run format + lint + type-check
make clean      # Clean up cache files
make help       # Show all available commands
```

### Pre-commit Hooks

Pre-commit hooks are automatically installed with `make setup` and will run:
- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast linting and additional formatting
- **MyPy**: Static type checking
- **Basic checks**: Trailing whitespace, file endings, YAML/TOML validation

### Demo Commands

```bash
make demo-lecture01  # Run lecture01 demo with AAPL
make demo-lecture02  # Run lecture02 demo
```

## Lecture 01: Single Agent with Web Search

This lecture demonstrates a single AI agent that uses web search to analyze stocks and generate comprehensive reports.

### Features

- **Single Agent Architecture**: One agent handles the entire stock analysis workflow
- **Web Search Integration**: Uses Tavily API for real-time web search capabilities
- **Structured Output**: Returns well-formatted stock analysis reports using Pydantic models
- **Observability**: Integrated with Logfire for monitoring agent behavior and tool usage
- **Error Handling**: Robust error handling and logging

### Usage

```bash
# Run the demo with a stock symbol using the script entrypoint
uv run lecture01 AAPL

# Or with any other stock symbol
uv run lecture01 TSLA
uv run lecture01 MSFT

# Alternative: run as module
uv run python -m lecture01.main AAPL
```

## Lecture 02: Agent Delegation Pattern

This lecture demonstrates the **Agent Delegation** communication pattern, where one agent delegates specific tasks to specialized agents through tool calls.

### Architecture Overview

The **Agent Delegation** pattern showcases:
- **Primary Agent**: `StockRecommender` - orchestrates the overall workflow
- **Specialized Agent**: `StockAnalysisAgent` - provides detailed stock analysis
- **Tool-based Communication**: The primary agent calls the specialized agent through a tool interface

### Features

- **Multi-Agent Coordination**: StockRecommender delegates stock analysis to StockAnalysisAgent
- **Shared Tools**: Common web search functionality moved to shared utilities
- **Agent-as-Tool Pattern**: StockAnalysisAgent is wrapped as a tool for delegation
- **Comparative Analysis**: Analyzes multiple stocks and provides recommendations
- **Structured Workflow**: Search → Analyze → Compare → Recommend

### Usage

```bash
# Run the agent delegation demo
uv run lecture02

# The agent will:
# 1. Search for trending/up-and-coming stocks
# 2. Select 3 interesting candidates
# 3. Get detailed reports for each using StockAnalysisAgent
# 4. Compare and provide recommendations
```

### What You'll See

When you run the demo, you'll observe:

1. **Primary Agent Initialization**: StockRecommender sets up with delegation tools
2. **Web Search Phase**: Searching for trending stocks and market opportunities
3. **Stock Selection**: Agent reasoning about which 3 stocks to analyze
4. **Delegation in Action**: Multiple calls to StockAnalysisAgent for detailed reports
5. **Comparative Analysis**: Agent comparing the three stock reports
6. **Final Recommendations**: Structured recommendations for each stock

### Key Components

- **`StockRecommender`**: Primary agent that orchestrates the workflow
- **`get_stock_report` tool**: Wraps StockAnalysisAgent as a callable tool
- **Shared `web_search` tool**: Moved to common utilities for reuse
- **Agent Delegation Pattern**: Demonstrates how agents can call other agents as tools

1. **Agent Initialization**: The agent sets up with the configured model and tools
2. **Search Process**: Multiple web searches being executed to gather information
3. **Thought Process**: The agent's reasoning as it analyzes the gathered data
4. **Tool Execution**: Web search tool calls and their results (visible in Logfire traces)
5. **Final Report**: A comprehensive, structured stock analysis report

### Architecture

The single agent:
- Uses a comprehensive system prompt that guides the analysis process
- Has access to the Tavily web search tool for gathering real-time information
- Follows a structured analysis framework covering all aspects of stock analysis
- Returns results in a validated Pydantic model format
- Uses LiteLLM for model access with custom configuration

### Key Components

- **`StockAnalysisAgent`**: Main agent class that orchestrates the analysis
- **`tavily_search_tool`**: Web search tool for gathering information
- **`StockReport`**: Pydantic model defining the output structure
- **Logfire Integration**: Observability for monitoring agent behavior

## Environment Variables

Copy `.env.example` to `.env` and configure the following required variables:

```bash
# Tavily API Configuration
TAVILY_API_KEY=your_tavily_api_key_here

# LiteLLM Configuration (if using LiteLLM proxy)
LITELLM_BASE_URL=http://your-litellm-endpoint:4000
LITELLM_API_KEY=your_litellm_api_key_here

# Agent Model Configuration
AGENT_MODEL=gpt-4.1_2025-04-14
AGENT_TEMPERATURE=0.1

# Logfire Configuration (optional, for observability)
LOGFIRE_API_KEY=your_logfire_api_key_here
LOGFIRE_PROJECT_ID=your_project_id_here
ENABLE_LOGFIRE=true
```

### Required API Keys

1. **Tavily API Key**: Sign up at [tavily.com](https://tavily.com) to get your API key for web search functionality
2. **LiteLLM Setup**: Configure your LiteLLM proxy endpoint and API key, or use OpenAI directly
3. **Logfire Setup** (optional, for web UI observability):

   **Option A: Use Console Traces (Recommended for Demos)**
   - No additional setup needed
   - Perfect real-time visibility during live coding
   - All traces appear in terminal output

   **Option B: Web UI Setup**
   ```bash
   # Authenticate with Logfire
   uv run logfire auth

   # Set up project (interactive - choose from existing projects)
   cd /path/to/project
   uv run logfire projects use
   # Select: 1 (for amit-goldstein/starter-project)
   ```

   **Note**: Console traces provide excellent visibility and are ideal for live demonstrations.

## Dependencies

- **pydantic-ai**: AI agent framework with Pydantic integration
- **tavily**: Web search API integration
- **logfire**: Observability and monitoring
- **python-dotenv**: Environment variable management

## Future Lectures

This project will be extended with additional lectures covering:

- **Lecture 03**: Agent communication patterns and coordination
- **Lecture 04**: Advanced workflows and error handling
- **Lecture 05**: Performance optimization and scaling

Each lecture will build upon the previous ones, demonstrating increasingly sophisticated agent architectures and communication patterns.
