"""
Lecture 04: Workflow Communication Pattern

This module demonstrates the workflow pattern where a single tool orchestrates
multiple specialized agents in sequence to accomplish a complex task.

In this example, the stock_report_tool implements a workflow that:
1. Calls a stock analysis agent to gather all information except recommendation
2. Calls a recommendation agent to generate investment advice based on the analysis
3. Combines both results into a complete StockReport

This pattern is useful when a task can be broken down into sequential steps
where each step's output feeds into the next step.
"""
