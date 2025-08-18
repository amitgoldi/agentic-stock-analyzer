"""Pytest configuration and shared fixtures."""

import os
import pytest
from unittest.mock import patch
from typing import Generator

# Set test environment variables
os.environ["TAVILY_API_KEY"] = "test_tavily_key"
os.environ["OPENAI_API_KEY"] = "test_openai_key"
os.environ["ANTHROPIC_API_KEY"] = "test_anthropic_key"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """Set up test environment variables and configuration."""
    # Ensure we're in test mode
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "ERROR"  # Reduce log noise during tests
    
    yield
    
    # Cleanup after tests
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


@pytest.fixture(autouse=True)
def mock_external_apis():
    """Mock external API calls by default to prevent actual network requests."""
    with patch('common.utils.TavilyClient') as mock_tavily:
        # Configure default mock behavior
        mock_client = mock_tavily.return_value
        mock_client.search.return_value = {"results": []}
        
        yield mock_tavily


@pytest.fixture
def disable_api_mocking():
    """Fixture to disable API mocking for specific tests."""
    # This fixture can be used when you want to test with real API calls
    # Usage: def test_real_api(disable_api_mocking): ...
    pass


# Pytest markers for test categorization
pytest_plugins = ["pytest_asyncio"]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file names
        if "test_models" in item.nodeid or "test_config" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_utils" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_agent_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_end_to_end" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
            item.add_marker(pytest.mark.slow)


@pytest.fixture
def temp_env_vars():
    """Fixture to temporarily set environment variables for testing."""
    original_env = os.environ.copy()
    
    def set_env(**kwargs):
        for key, value in kwargs.items():
            os.environ[key] = str(value)
    
    yield set_env
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# Import fixtures from fixtures.py
from tests.fixtures import *