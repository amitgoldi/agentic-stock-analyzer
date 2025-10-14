"""
Lecture 05: Agent-to-Agent (A2A) Protocol Communication

This module demonstrates the Agent-to-Agent (A2A) protocol - an open standard
introduced by Google that enables communication between AI agents.

The A2A protocol allows agents to communicate over HTTP following a standardized
format, enabling true agent interoperability regardless of framework or vendor.

In this example:
- The stock analysis agent (lecture02) is exposed as an A2A server
- The financial assistant agent communicates with it via HTTP using the A2A protocol
- This demonstrates true inter-agent communication following the A2A standard

Key concepts:
- Tasks: Complete execution of an agent (one request/response cycle)
- Context: Conversation threads that span multiple tasks
- Protocol-based: Standardized communication format for agent interoperability

Reference: https://ai.pydantic.dev/a2a/
"""
