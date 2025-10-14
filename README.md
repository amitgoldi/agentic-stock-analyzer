# Tikal Lecture: Communication Patterns with AI Agents

This is a demo project for progressive live coding demonstrations showing different approaches to building AI agents for stock analysis.

## Project Structure

```
tikal-lecture-communication-patterns/
├── common/                 # Shared utilities and models
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic models for data structures
│   ├── tools.py           # Shared tools (web search)
│   └── utils.py           # Common utility functions
├── lecture01/             # Lecture 1: Simple Financial Assistant
│   ├── __init__.py
│   ├── agent.py           # Simple financial assistant agent
│   └── main.py            # Main entry point for demo
├── lecture02/             # Lecture 2: Single Agent Stock Analysis
│   ├── __init__.py
│   ├── agent.py           # Single agent implementation
│   └── main.py            # Main entry point for demo
├── lecture03/             # Lecture 3: Enhanced Financial Assistant
│   ├── __init__.py
│   ├── agent.py           # Enhanced financial assistant (lecture01 + stock_report tool)
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
make demo-lecture01  # Run lecture01 demo (simple financial assistant)
make demo-lecture02  # Run lecture02 demo with AAPL
make demo-lecture03  # Run lecture03 demo
```

## Lecture 01: Simple Financial Assistant

This lecture demonstrates a basic financial assistant agent that uses web search to answer financial questions with simple text-based input/output.

### Features

- **Simple Interface**: Text-based Q&A for financial questions
- **Web Search Integration**: Uses Tavily API for current financial information
- **Financial Knowledge**: Combines web search with internal financial expertise
- **Safety First**: Includes appropriate disclaimers and professional consultation reminders
- **Interactive & Demo Modes**: Both interactive sessions and pre-built example questions

### Usage

```bash
# Run interactive mode - ask your own questions
uv run lecture01

# Run demo mode with example questions
uv run lecture01 --demo

# Alternative: run as module
uv run python -m lecture01.main
uv run python -m lecture01.main --demo
```

### Example Questions

The demo mode showcases answers to:
- "What is the current price of Bitcoin?"
- "Should I invest in index funds or individual stocks?"
- "What are the current interest rates for savings accounts?"
- "Explain the concept of dollar-cost averaging"

### Architecture

The simple financial assistant:
- Uses a single agent with web search capabilities
- Provides comprehensive financial guidance with current market data
- Includes safety disclaimers and professional consultation reminders
- Has a clean console-based interface for easy interaction

## Lecture 02: Single Agent Stock Analysis

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
uv run lecture02 AAPL

# Or with any other stock symbol
uv run lecture02 TSLA
uv run lecture02 MSFT

# Alternative: run as module
uv run python -m lecture02.main AAPL
```

## Lecture 03: Enhanced Financial Assistant with Tool Delegation

This lecture demonstrates how to **extend a basic agent with specialized tools** by taking the simple financial assistant from Lecture 01 and enhancing it with a `stock_report` tool that internally delegates to the Lecture 02 stock analysis agent.

### Architecture Overview

This lecture showcases the **DRY principle** in agent development:
- **Base Agent**: Same as Lecture 01's financial assistant (web search + general financial knowledge)
- **Additional Tool**: `stock_report` tool that wraps the Lecture 02 agent
- **Tool Composition**: Demonstrates how to compose agents by wrapping them as tools

### Features

- **Extends Lecture 01**: Same base capabilities as the simple financial assistant
- **Additional Stock Analysis**: Can now provide detailed stock analysis reports
- **Tool Delegation**: The `stock_report` tool internally uses the Lecture 02 agent
- **Unified Interface**: Users get both general financial advice and detailed stock analysis in one place
- **Interactive & Demo Modes**: Both interactive sessions and pre-built example questions

### Usage

```bash
# Run interactive mode - ask your own questions
uv run lecture03

# Run demo mode with example questions showing both general and stock-specific queries
uv run lecture03 --demo

# Alternative: run as module
uv run python -m lecture03.main
uv run python -m lecture03.main --demo
```

### Example Questions

The demo mode showcases the enhanced capabilities:
- "What is the current price of Bitcoin?" - General web search
- "Can you give me a detailed analysis of Apple stock (AAPL)?" - Uses stock_report tool
- "Should I invest in index funds or individual stocks?" - General financial advice
- "Give me a comprehensive report on Tesla (TSLA)" - Uses stock_report tool

### What You'll See

When you run the demo, you'll observe:

1. **Enhanced Agent**: Same interface as Lecture 01 but with additional capabilities
2. **Tool Selection**: The agent intelligently chooses between web_search and stock_report
3. **Detailed Analysis**: When asked about specific stocks, it delegates to the Lecture 02 agent
4. **General Questions**: Regular financial questions still use web search
5. **Seamless Integration**: Both capabilities work together naturally

### Key Components

- **`enhanced_financial_agent`**: Lecture 01 agent + stock_report tool
- **`stock_report_tool`**: Wraps the Lecture 02 `analyze_stock` function
- **`ask_financial_question`**: Same interface as Lecture 01
- **Tool Composition Pattern**: Demonstrates how to enhance agents by adding specialized tools

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

This project can be extended with additional lectures covering:

- **Lecture 04**: Advanced agent communication patterns and coordination
- **Lecture 05**: Complex workflows and error handling
- **Lecture 06**: Performance optimization and scaling

Each lecture builds upon the previous ones, demonstrating increasingly sophisticated agent architectures and communication patterns.
