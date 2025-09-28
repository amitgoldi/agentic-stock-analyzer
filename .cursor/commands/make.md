# Make Command

Run `make` to set up the development environment and run all code quality checks.

## Command

```bash
make
```

## What This Command Does

1. **Sets up the development environment**:
   - Installs all dependencies including dev tools
   - Sets up pre-commit hooks automatically
2. **Runs code quality checks**:
   - **Formatting**: Black and isort for consistent code style
   - **Linting**: Ruff for fast, comprehensive linting
   - **Type checking**: MyPy for static type analysis
3. **Automatically fixes common issues**:
   - Code formatting with Black
   - Import sorting with isort
   - Auto-fixable linting issues with Ruff
   - Trailing whitespace and file endings

## Usage

Simply run this command in your terminal:

```bash
make
```

## Available Make Targets

```bash
make            # Default: setup + format + lint + type-check
make setup      # Install dependencies and set up pre-commit hooks
make format     # Format code with black and isort
make lint       # Run linting with ruff
make type-check # Run type checking with mypy
make check      # Run format + lint + type-check
make clean      # Clean up cache files
make help       # Show all available commands
```

## Demo Commands

```bash
make demo-lecture02  # Run lecture02 demo with AAPL
make demo-lecture03  # Run lecture03 demo
```

## Code Quality Tools

The make command uses modern Python tooling for code quality:

### Formatting Tools
- **Black**: Uncompromising Python code formatter
- **isort**: Sorts and organizes imports consistently

### Linting Tools
- **Ruff**: Fast Python linter that replaces flake8, pylint, and more
  - Checks for code style issues
  - Identifies potential bugs
  - Enforces best practices
  - Auto-fixes many issues

### Type Checking
- **MyPy**: Static type checker for Python
  - Validates type hints
  - Catches type-related errors
  - Improves code reliability

## Expected Output

The command will:
- Install dependencies and set up pre-commit hooks
- Show progress of each step
- Automatically fix formatting issues with Black and isort
- Run Ruff linting with auto-fixes where possible
- Perform type checking with MyPy
- Display results for each step
- Exit with success (0) when all checks pass

## Pre-commit Integration

After running `make setup`, pre-commit hooks are automatically installed and will run on every commit:
- Prevents commits with formatting issues
- Catches linting problems before they reach the repository
- Ensures consistent code quality across all contributions

## Troubleshooting

If you encounter issues:

1. **Clean environment**: Remove cached files
   ```bash
   make clean
   ```

2. **Reinstall dependencies**:
   ```bash
   make setup
   ```

3. **Run individual checks**:
   ```bash
   make format     # Fix formatting
   make lint       # Check linting
   make type-check # Check types
   ```

4. **Manual fixes**: Address specific error messages shown by the tools

## Notes

- This is a simplified setup for a lecture repository (no unit tests)
- Pre-commit hooks ensure code quality on every commit
- All tools are configured to work together harmoniously
- The setup uses modern Python tooling (Ruff, Black, MyPy)
- Use `make help` to see all available commands
