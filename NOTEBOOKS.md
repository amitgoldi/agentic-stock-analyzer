# Jupyter Notebooks Guide

This project includes Jupyter notebooks for each lecture, providing an interactive way to learn about AI agent communication patterns.

## Setup

The notebooks are already configured to work with the project's dependencies. All you need to do is:

### Option 1: Use the installed kernel (Recommended)

1. Open any notebook (e.g., `lecture01.ipynb`) in your IDE or Jupyter
2. Select the **"tikal-lecture"** kernel from the kernel selector
3. Run the cells!

### Option 2: Use `uv run` directly

```bash
# Start Jupyter Notebook
uv run jupyter notebook

# Or start Jupyter Lab
uv run jupyter lab

# Then open any lecture notebook (lecture01.ipynb, lecture02.ipynb, etc.)
```

### Option 3: Run notebooks from command line

```bash
# Run a specific notebook non-interactively
uv run jupyter nbconvert --to notebook --execute lecture01.ipynb
```

## Available Notebooks

- **lecture01.ipynb**: Simple Financial Assistant
  - Basic agent with web search
  - Simple text-based Q&A

- **lecture02.ipynb**: Single Agent Stock Analysis
  - Structured output with `StockReport`
  - Web search for stock data

- **lecture03.ipynb**: Tool Delegation Pattern
  - Enhanced agent with `stock_report_tool`
  - Delegates to lecture02 agent

- **lecture04.ipynb**: Workflow Pattern
  - Multi-agent orchestration
  - Sequential agent execution

- **lecture05.ipynb**: A2A Protocol
  - Agent-to-Agent communication over HTTP
  - Requires A2A server running (see below)

## Special Note for Lecture 05

Before running `lecture05.ipynb`, you need to start the A2A server:

```bash
# In a separate terminal
uvicorn lecture05.stock_a2a_server:app --host 0.0.0.0 --port 8001
```

Then run the notebook cells.

## Troubleshooting

### Import Errors

If you get import errors, make sure dependencies are installed:

```bash
uv sync
```

### Kernel Not Found

If the "tikal-lecture" kernel isn't available, reinstall it:

```bash
uv run python -m ipykernel install --user --name=tikal-lecture
```

### Environment Variables

Make sure you have a `.env` file with required API keys:

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required keys:
- `TAVILY_API_KEY`: For web search functionality
- `LITELLM_BASE_URL` and `LITELLM_API_KEY`: For LLM access
- `LOGFIRE_API_KEY` (optional): For observability

## Benefits of Notebooks vs CLI

- **Interactive Learning**: Run code step-by-step
- **Immediate Feedback**: See results inline
- **Easy Experimentation**: Modify prompts and see results
- **Clear Agent Creation**: See how agents are built
- **No CLI Complexity**: Just create agents and run prompts
