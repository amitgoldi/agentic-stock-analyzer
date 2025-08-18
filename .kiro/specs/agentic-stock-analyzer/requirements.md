# Requirements Document

## Introduction

This feature implements a demo repository for teaching agentic communication patterns through a stock analysis system. The system will demonstrate different communication patterns starting with a simple ReACT (Reasoning and Acting) loop using a single agent. The agent will analyze stocks and provide financial advice to investors using pydantic-ai and the Tavily research tool.

## Requirements

### Requirement 1

**User Story:** As a lecture attendee, I want to see a working example of a single agent using ReACT pattern, so that I can understand the basic agentic communication flow.

#### Acceptance Criteria

1. WHEN the system is provided with a list of stock symbols THEN the agent SHALL process each stock individually using a ReACT loop
2. WHEN the agent processes a stock THEN it SHALL use the Tavily tool to research current information about the stock
3. WHEN the agent completes research THEN it SHALL generate a comprehensive stock report including financial analysis
4. WHEN the agent generates a report THEN it SHALL provide specific investment advice based on the research findings
5. IF the agent encounters an error during research THEN it SHALL handle the error gracefully and continue with available information

### Requirement 2

**User Story:** As a developer following the lecture, I want a clear project structure with separate directories for each lecture, so that I can easily navigate and understand different communication patterns.

#### Acceptance Criteria

1. WHEN the project is initialized THEN it SHALL have a lecture01 directory for the single agent ReACT pattern
2. WHEN the project is structured THEN it SHALL have a common directory for shared utilities and models
3. WHEN each lecture directory is created THEN it SHALL contain its own main script and configuration
4. WHEN the project uses external dependencies THEN it SHALL use uv as the build system with Python 3.12

### Requirement 3

**User Story:** As a lecture instructor, I want the system to use pydantic-ai for agent implementation, so that students can learn modern Python AI patterns with proper type safety.

#### Acceptance Criteria

1. WHEN the agent is implemented THEN it SHALL use pydantic-ai framework for agent definition
2. WHEN data models are defined THEN they SHALL use Pydantic for validation and serialization
3. WHEN the agent processes data THEN it SHALL maintain type safety throughout the pipeline
4. WHEN the system handles stock data THEN it SHALL validate input using Pydantic models

### Requirement 4

**User Story:** As a system user, I want the agent to integrate with Tavily for research capabilities, so that it can access real-time financial information.

#### Acceptance Criteria

1. WHEN the system starts THEN it SHALL load the Tavily API key from a .env file
2. WHEN the agent needs to research a stock THEN it SHALL use Tavily to search for current financial information
3. WHEN Tavily returns search results THEN the agent SHALL process and synthesize the information
4. IF the Tavily API is unavailable THEN the system SHALL provide appropriate error handling and fallback behavior

### Requirement 5

**User Story:** As a potential investor, I want to receive detailed stock reports with actionable investment advice, so that I can make informed investment decisions.

#### Acceptance Criteria

1. WHEN a stock analysis is completed THEN the report SHALL include company overview and current financial status
2. WHEN a stock analysis is completed THEN the report SHALL include recent news and market sentiment analysis
3. WHEN a stock analysis is completed THEN the report SHALL include specific investment recommendation (buy/hold/sell)
4. WHEN a stock analysis is completed THEN the report SHALL include risk assessment and reasoning for the recommendation
5. WHEN multiple stocks are analyzed THEN each SHALL receive an individual comprehensive report

### Requirement 6

**User Story:** As a developer, I want the system to be easily extensible for future lectures, so that additional communication patterns can be added without major refactoring.

#### Acceptance Criteria

1. WHEN the base system is implemented THEN it SHALL have a modular architecture supporting multiple communication patterns
2. WHEN common functionality is implemented THEN it SHALL be reusable across different lecture implementations
3. WHEN new lecture patterns are added THEN they SHALL integrate with the existing common utilities
4. WHEN the system is extended THEN it SHALL maintain consistent interfaces and data models