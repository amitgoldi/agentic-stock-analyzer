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
├── .env.example           # Environment variables template
├── .env                   # Environment variables (create from .env.example, not in git)
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   # or
   pip install -e .
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
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

### What You'll See

When you run the demo, you'll observe:

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

- **Lecture 02**: Multi-agent systems with specialized roles
- **Lecture 03**: Agent communication patterns and coordination
- **Lecture 04**: Advanced workflows and error handling
- **Lecture 05**: Performance optimization and scaling

Each lecture will build upon the previous ones, demonstrating increasingly sophisticated agent architectures and communication patterns.