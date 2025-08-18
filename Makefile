.PHONY: help setup run1 test lint format clean install-dev check-env

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup     - Setup the project (install dependencies, create .env)"
	@echo "  make run1      - Run lecture 1 (Single Agent ReACT Pattern)"
	@echo "  make test      - Run all tests"
	@echo "  make test-fast - Run fast tests (exclude slow/e2e)"
	@echo "  make test-unit - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-e2e  - Run end-to-end tests only"
	@echo "  make test-quality - Run quality checks"
	@echo "  make test-full - Run full test suite"
	@echo "  make lint      - Run linting (mypy, black --check, isort --check)"
	@echo "  make format    - Format code (black, isort)"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make check-env - Check if required environment variables are set"

# Setup the project
setup:
	@echo "🚀 Setting up the project..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp .env.template .env; \
		echo "⚠️  Please edit .env file and add your API keys!"; \
	else \
		echo "✅ .env file already exists"; \
	fi
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Project setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env file and add your API keys"
	@echo "2. Run 'make check-env' to verify configuration"
	@echo "3. Run 'make run1' to start lecture 1"

# Run lecture 1
run1: check-env
	@echo "🎓 Running Lecture 1: Single Agent ReACT Pattern..."
	uv run python -m lecture01.main

# Run tests
test:
	@echo "🧪 Running all tests..."
	uv run python run_tests.py all

# Run fast tests (exclude slow/e2e tests)
test-fast:
	@echo "🧪 Running fast tests..."
	uv run python run_tests.py fast

# Run unit tests only
test-unit:
	@echo "🧪 Running unit tests..."
	uv run python run_tests.py unit

# Run integration tests only
test-integration:
	@echo "🧪 Running integration tests..."
	uv run python run_tests.py integration

# Run end-to-end tests only
test-e2e:
	@echo "🧪 Running end-to-end tests..."
	uv run python run_tests.py e2e

# Run quality checks (type checking, formatting, etc.)
test-quality:
	@echo "🔍 Running quality checks..."
	uv run python run_tests.py quality

# Run full test suite (quality + all tests)
test-full:
	@echo "🚀 Running full test suite..."
	uv run python run_tests.py full

# Lint code
lint:
	@echo "🔍 Running linting..."
	uv run mypy common/ lecture01/
	uv run black --check common/ lecture01/
	uv run isort --check-only common/ lecture01/

# Format code
format:
	@echo "🎨 Formatting code..."
	uv run black common/ lecture01/
	uv run isort common/ lecture01/

# Install development dependencies
install-dev:
	@echo "🛠️  Installing development dependencies..."
	uv sync --extra dev

# Check environment variables
check-env:
	@uv run python -m common.check_env

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"