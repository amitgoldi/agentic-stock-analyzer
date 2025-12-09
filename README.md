# Tikal Lecture: Communication Patterns with AI Agents

This is a demo project for progressive live coding demonstrations showing different approaches to building AI agents for stock analysis.

## 📓 Jupyter Notebooks (Recommended)

Each lecture is available as an interactive Jupyter notebook for easy learning and experimentation. See **[NOTEBOOKS.md](NOTEBOOKS.md)** for setup instructions.

Quick start:
```bash
uv run jupyter notebook  # Then open lecture01.ipynb, lecture02.ipynb, etc.
```

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
├── lecture04/             # Lecture 4: Workflow Communication Pattern
│   ├── __init__.py
│   ├── agent.py           # Workflow-based financial assistant with multi-agent orchestration
│   └── main.py            # Main entry point for demo
├── lecture05/             # Lecture 5: Agent-to-Agent (A2A) Communication
│   ├── __init__.py
│   ├── agent.py           # A2A financial assistant with explicit agent communication
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

**Option A: Jupyter Notebooks** (Recommended for learning)
```bash
uv run jupyter notebook  # Open lecture01.ipynb, lecture02.ipynb, etc.
```
See [NOTEBOOKS.md](NOTEBOOKS.md) for detailed instructions.

**Option B: CLI Demos** (Original format)
```bash
make demo-lecture01  # Run lecture01 demo (simple financial assistant)
make demo-lecture02  # Run lecture02 demo with AAPL
make demo-lecture03  # Run lecture03 demo (enhanced financial assistant)
make demo-lecture04  # Run lecture04 demo (workflow pattern)
make demo-lecture05  # Run lecture05 demo (A2A communication)
make a2a-server      # Start A2A stock analysis server for lecture05
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

## Lecture 04: Workflow Communication Pattern

This lecture demonstrates the **workflow pattern** where a single tool orchestrates multiple specialized agents in sequence to accomplish a complex task. The stock_report tool now uses a multi-agent workflow instead of delegating to a single agent.

### Architecture Overview

This lecture showcases the **workflow communication pattern**:
- **Orchestration Layer**: The `stock_report` tool acts as a workflow orchestrator
- **Agent 1 (Analysis)**: Specialized in gathering stock information (all fields except recommendation)
- **Agent 2 (Recommendation)**: Specialized in generating investment recommendations
- **Sequential Execution**: Agent 2 receives Agent 1's output as input
- **Result Composition**: The workflow combines both outputs into a complete StockReport

### Features

- **Workflow Pattern**: Tool orchestrates multiple agents in sequence
- **Separation of Concerns**: Different agents handle different aspects of analysis
- **Data Flow**: Output from one agent feeds into the next
- **Specialized Agents**: Each agent is optimized for its specific task
- **Comprehensive Analysis**: Multi-step process creates more detailed reports
- **Interactive & Demo Modes**: Both interactive sessions and pre-built example questions

### Usage

```bash
# Run interactive mode - ask your own questions
uv run lecture04

# Run demo mode with example questions showing the workflow in action
uv run lecture04 --demo

# Alternative: run as module
uv run python -m lecture04.main
uv run python -m lecture04.main --demo
```

### Example Questions

The demo mode showcases the workflow pattern:
- "What is the current market sentiment?" - General web search
- "Can you give me a detailed analysis of Microsoft stock (MSFT)?" - Uses workflow
- "Give me a comprehensive report on NVIDIA (NVDA)" - Uses workflow

### What You'll See

When you run the demo, you'll observe:

1. **Workflow Execution**: The stock_report tool orchestrates multiple agents
2. **Step 1 - Analysis**: First agent gathers comprehensive stock information
3. **Step 2 - Recommendation**: Second agent generates investment advice based on analysis
4. **Step 3 - Composition**: Workflow combines both results into final report
5. **Enhanced Quality**: Multi-agent approach provides more thorough analysis

### Key Components

- **`workflow_stock_report_tool`**: Orchestrates the multi-agent workflow
- **`stock_analysis_agent`**: Gathers all stock information except recommendation
- **`recommendation_agent`**: Generates investment recommendations
- **`StockAnalysis`**: Intermediate model for passing data between agents
- **Workflow Pattern**: Demonstrates sequential agent communication and orchestration

### Comparison with Lecture 03

| Aspect | Lecture 03 | Lecture 04 |
|--------|-----------|-----------|
| Pattern | Tool delegation | Workflow orchestration |
| Agents | Single agent | Multiple specialized agents |
| Execution | One agent does everything | Sequential agent execution |
| Data Flow | Direct output | Intermediate data passed between agents |
| Specialization | General-purpose | Task-specific agents |

## Lecture 05: Agent-to-Agent (A2A) Protocol Communication

This lecture demonstrates the **Agent-to-Agent (A2A) protocol** - an open standard introduced by Google that enables communication and interoperability between AI agents, regardless of framework or vendor.

**Reference**: [Pydantic AI A2A Documentation](https://ai.pydantic.dev/a2a/)

### Architecture Overview

This lecture showcases **true A2A protocol communication**:
- **Protocol-Based**: Uses Google's A2A standard for agent interoperability
- **HTTP Communication**: Agents communicate over HTTP using A2A protocol format
- **Server/Client Model**: Stock analysis agent runs as A2A server, financial assistant is client
- **Standardized Format**: Messages follow A2A protocol specification with tasks and artifacts
- **Task Management**: Each request creates a task with unique ID and status tracking
- **Context Continuity**: Supports conversation threads across multiple tasks

### Features

- **A2A Protocol**: Implements Google's standardized agent communication protocol
- **Agent Interoperability**: Agents can communicate across frameworks/vendors
- **HTTP-Based**: Communication happens over HTTP (port 8001)
- **Standardized Messages**: Uses A2A message format with roles, parts, and artifacts
- **Server Architecture**: Stock analysis agent exposed as ASGI A2A server
- **Client Integration**: Financial assistant sends A2A protocol requests
- **Interactive & Demo Modes**: Both interactive sessions and pre-built example questions

### Setup Requirements

**Before running this lecture, you need to start the A2A server:**

```bash
# Terminal 1 - Start the A2A stock analysis server
uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001

# Terminal 2 - Run the financial assistant demo
uv run lecture05
# or
uv run lecture05 --demo
```

The A2A server exposes the stock analysis agent at `http://localhost:8001` following the A2A protocol specification.

### Usage

```bash
# Step 1: Start the A2A server (in one terminal)
uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001

# Step 2: Run the demo (in another terminal)
uv run lecture05              # Interactive mode
uv run lecture05 --demo       # Demo mode with examples

# Alternative: run as module
uv run python -m lecture05.main
```

### Example Questions

The demo mode showcases the A2A protocol:
- "What is the current price of Bitcoin?" - General web search
- "Can you give me a detailed analysis of Apple stock (AAPL)?" - A2A protocol communication
- "Should I invest in index funds or individual stocks?" - General financial advice
- "Give me a comprehensive report on Tesla (TSLA)" - A2A protocol communication

### What You'll See

When you run the demo, you'll observe:

1. **Protocol Communication**: HTTP requests sent to A2A server following A2A standard
2. **Task Creation**: Each request creates a task with unique ID
3. **Artifact Extraction**: StockReport extracted from A2A response artifacts
4. **Server Logging**: A2A server logs task processing
5. **True Interoperability**: Agents communicate via standardized protocol

### Key Components

- **`stock_a2a_server.py`**: Exposes stock analysis agent as A2A server using `agent.to_a2a()`
- **`a2a_financial_agent`**: Financial assistant that sends A2A protocol requests
- **`a2a_stock_analysis_tool`**: Tool that makes HTTP requests using A2A protocol format
- **A2A Protocol**: Follows Google's standard for agent communication
- **ASGI Application**: A2A server is an ASGI app (runs with uvicorn)

### Comparison: Lecture 03 vs. Lecture 05

| Aspect | Lecture 03 (Agent-as-Tool) | Lecture 05 (A2A Protocol) |
|--------|---------------------------|---------------------------|
| Pattern | Direct code integration | HTTP protocol communication |
| Communication | In-process function call | HTTP requests to A2A server |
| Protocol | None | Google's A2A standard |
| Agent Location | Same process | Separate service/server |
| Interoperability | Framework-specific | Cross-framework/vendor |
| Message Format | Python objects | A2A protocol JSON |
| Deployment | Single application | Distributed services |
| Scalability | Limited to process | Horizontally scalable |

### When to Use Each Pattern

**Use Agent-as-Tool (Lecture 03) when:**
- Simple, in-process delegation
- All agents in same codebase
- Single application deployment
- No need for service separation

**Use A2A Protocol (Lecture 05) when:**
- Need agent interoperability
- Distributed agent architecture
- Agents from different vendors/frameworks
- Service-oriented architecture
- Want to follow industry standards
- Need horizontal scalability

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

- **Lecture 06**: Parallel agent execution and coordination
- **Lecture 07**: Error handling and retry strategies
- **Lecture 08**: Performance optimization and scaling

Each lecture builds upon the previous ones, demonstrating increasingly sophisticated agent architectures and communication patterns.

## Communication Patterns Summary

| Pattern | Lecture | Key Concept | Best For |
|---------|---------|-------------|----------|
| Simple Agent | 01, 02 | Single agent with tools | Straightforward tasks |
| Agent-as-Tool | 03 | Wrap agent as tool | Simple in-process delegation |
| Workflow | 04 | Sequential agent orchestration | Multi-step processes |
| A2A Protocol | 05 | HTTP-based standardized communication | Distributed agents, interoperability |
