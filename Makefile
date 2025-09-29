# Makefile for Tikal Lecture Communication Patterns
# Simple setup for a lecture repository with linting, formatting, and type checking

.PHONY: help setup install format lint type-check check clean all

# Default target
all: setup format lint type-check

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Install dependencies and set up pre-commit hooks
	@echo "🔧 Setting up development environment..."
	uv sync --extra dev
	uv run pre-commit install
	@echo "✅ Setup complete!"

install: setup ## Alias for setup

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	uv run black .
	uv run isort .
	@echo "✅ Code formatted!"

lint: ## Run linting with ruff
	@echo "🔍 Running linter..."
	uv run ruff check . --fix
	uv run ruff format --check .
	@echo "✅ Linting complete!"

type-check: ## Run type checking with mypy
	@echo "🔎 Running type checker..."
	uv run mypy . --ignore-missing-imports --no-strict-optional
	@echo "✅ Type checking complete!"

check: format lint type-check ## Run all checks (format, lint, type-check)
	@echo "✅ All checks passed!"

clean: ## Clean up cache files and temporary files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "✅ Cleanup complete!"

# Demo targets
demo-lecture01: ## Run lecture01 demo (simple financial assistant)
	@echo "🚀 Running Lecture 01 demo..."
	uv run lecture01 --demo

demo-lecture02: ## Run lecture02 demo with AAPL
	@echo "🚀 Running Lecture 02 demo..."
	uv run lecture02 AAPL

demo-lecture03: ## Run lecture03 demo
	@echo "🚀 Running Lecture 03 demo..."
	uv run lecture03

# Development workflow
dev: setup ## Set up development environment and run checks
	@echo "🚀 Development setup complete!"
	@echo "Run 'make check' to validate your changes"
	@echo "Run 'make demo-lecture01', 'make demo-lecture02', or 'make demo-lecture03' to test the demos"
