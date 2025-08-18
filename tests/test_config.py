"""Tests for configuration management."""

import os
from unittest.mock import patch

import pytest

from common.config import AppConfig, get_config


def test_config_from_env_defaults():
    """Test configuration with default values."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "OPENAI_API_KEY": "test_openai_key",
        },
        clear=True,
    ):
        config = get_config()
        
        assert config.tavily.api_key == "test_key"
        assert config.tavily.max_results == 10
        assert config.tavily.search_depth == "advanced"
        
        assert config.agent.model_name == "openai:gpt-4o"
        assert config.agent.temperature == 0.1
        assert config.agent.max_retries == 3
        
        assert config.debug is False
        assert config.log_level == "INFO"


def test_config_from_env_custom():
    """Test configuration with custom values."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "custom_key",
            "TAVILY_MAX_RESULTS": "20",
            "TAVILY_SEARCH_DEPTH": "basic",
            "AGENT_MODEL": "anthropic:claude-3-sonnet",
            "AGENT_TEMPERATURE": "0.5",
            "AGENT_MAX_RETRIES": "5",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "ANTHROPIC_API_KEY": "test_anthropic_key",
        },
        clear=True,
    ):
        config = get_config()
        
        assert config.tavily.api_key == "custom_key"
        assert config.tavily.max_results == 20
        assert config.tavily.search_depth == "basic"
        
        assert config.agent.model_name == "anthropic:claude-3-sonnet"
        assert config.agent.temperature == 0.5
        assert config.agent.max_retries == 5
        
        assert config.debug is True
        assert config.log_level == "DEBUG"


def test_config_validation():
    """Test configuration validation."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "AGENT_TEMPERATURE": "3.0",  # Invalid: > 2.0
            "OPENAI_API_KEY": "test_key",
        },
        clear=True,
    ):
        with pytest.raises(ValueError):
            get_config()


def test_config_missing_api_key():
    """Test configuration with missing API key."""
    with patch.dict(os.environ, {}, clear=True):
        config = get_config()
        # Should still create config but with empty API key
        assert config.tavily.api_key == ""


def test_config_invalid_numeric_values():
    """Test configuration with invalid numeric values."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "TAVILY_MAX_RESULTS": "invalid",  # Invalid: not a number
            "OPENAI_API_KEY": "test_key",
        },
        clear=True,
    ):
        with pytest.raises(ValueError):
            get_config()


def test_config_negative_temperature():
    """Test configuration with negative temperature."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "AGENT_TEMPERATURE": "-0.1",  # Invalid: < 0.0
            "OPENAI_API_KEY": "test_key",
        },
        clear=True,
    ):
        with pytest.raises(ValueError):
            get_config()


def test_config_zero_retries():
    """Test configuration with zero retries."""
    with patch.dict(
        os.environ,
        {
            "TAVILY_API_KEY": "test_key",
            "AGENT_MAX_RETRIES": "0",  # Invalid: < 1
            "OPENAI_API_KEY": "test_key",
        },
        clear=True,
    ):
        with pytest.raises(ValueError):
            get_config()


def test_tavily_config_direct():
    """Test TavilyConfig creation directly."""
    from common.config import TavilyConfig
    
    config = TavilyConfig(api_key="test_key")
    assert config.api_key == "test_key"
    assert config.max_results == 10
    assert config.search_depth == "advanced"


def test_agent_config_direct():
    """Test AgentConfig creation directly."""
    from common.config import AgentConfig
    
    config = AgentConfig()
    assert config.model_name == "openai:gpt-4o"
    assert config.temperature == 0.1
    assert config.max_retries == 3


def test_app_config_direct():
    """Test AppConfig creation directly."""
    from common.config import TavilyConfig, AgentConfig, AppConfig
    
    tavily_config = TavilyConfig(api_key="test_key")
    agent_config = AgentConfig()
    
    app_config = AppConfig(tavily=tavily_config, agent=agent_config)
    assert app_config.debug is False
    assert app_config.log_level == "INFO"