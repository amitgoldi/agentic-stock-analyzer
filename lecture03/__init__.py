"""Lecture 03: Agent Delegation Pattern

This module demonstrates the Agent Delegation communication pattern where
a primary agent (StockRecommender) delegates specific tasks to specialized
agents (StockAnalysisAgent) through tool calls.
"""

from .agent import StockRecommender

__all__ = ["StockRecommender"]
