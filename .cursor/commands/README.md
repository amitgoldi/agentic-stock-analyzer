# Cursor Commands

This directory contains custom commands for the chat-service project. These commands are designed to streamline common development workflows.

## Available Commands

### commit-and-pr
Automatically commits changes and creates a pull request with proper formatting.

**Usage:**
```bash
make commit-and-pr                    # Normal execution
make commit-and-pr-dry-run           # Dry run mode
# or
./.cursor/commands/commit-and-pr [--dry-run] [--help]
```

**Features:**
- Extracts story ID from branch name (CN-XXXX format)
- Stages all changes automatically
- Creates properly formatted commit messages
- Generates comprehensive PR descriptions
- Supports dry-run mode for testing
- Validates branch naming conventions

**Requirements:**
- Branch must follow format: `CN-XXXX-feature-description`
- GitHub CLI (gh) must be installed and authenticated
- Must be run from within the git repository

See [commit-and-pr.md](./commit-and-pr.md) for detailed documentation.

## Adding New Commands

To add a new command:

1. Create the executable script in this directory
2. Make it executable: `chmod +x command-name`
3. Add documentation in a corresponding `.md` file
4. Optionally add a Makefile target for easy access
5. Update this README

## Command Conventions

- All commands should include `--help` and `--dry-run` options where applicable
- Use colored output for better user experience
- Include proper error handling and validation
- Follow the project's coding standards
- Document all options and usage patterns
