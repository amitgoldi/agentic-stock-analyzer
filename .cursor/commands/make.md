# Make Command

Run `make` and automatically fix all issues that arise.

## Command

```bash
make
```

## What This Command Does

1. **Verifies virtual environment** - Ensures the command is running in an active Python virtual environment
2. **Runs the full build pipeline** including:
   - Pre-commit hooks (formatting, linting, type checking)
   - Unit tests
   - Coverage reporting
3. **Automatically fixes common issues**:
   - Code formatting (ruff, black)
   - Trailing whitespace
   - Import sorting
   - Type hints
4. **Performs semantic analysis** on changed files:
   - Verifies all imports are absolute imports
   - Checks for unnecessary inline imports
5. **Runs until all issues are resolved**

## Usage

Simply run this command in your terminal:

```bash
make
```

## Virtual Environment Check

The command will first verify you're in an active virtual environment:

```bash
# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Error: Not running in a virtual environment"
    echo "Please activate your virtual environment first:"
    echo "  source venv/bin/activate  # or equivalent"
    exit 1
fi

echo "✅ Virtual environment detected: $VIRTUAL_ENV"
```

## Semantic Analysis

The command performs semantic analysis on all changed files to ensure code quality and consistency:

### Import Verification

1. **Absolute Imports Check**:
   - Scans all changed Python files for import statements
   - Verifies that all imports use absolute paths (e.g., `from src.module import function`)
   - Flags any relative imports (e.g., `from .module import function` or `from ..module import function`)

2. **Inline Import Detection**:
   - Identifies imports placed inside functions, methods, or conditional blocks
   - Flags unnecessary inline imports that should be moved to the top of the file
   - Allows exceptions only for truly necessary cases (e.g., conditional imports for optional dependencies)

### Analysis Process

```bash
# Example of what the semantic analysis checks:
# ✅ Good: Absolute import at top of file
from src.tasks.service import TaskService

# ❌ Bad: Relative import
from .service import TaskService

# ❌ Bad: Inline import (unless absolutely necessary)
def some_function():
    from src.tasks.service import TaskService  # Should be at top
```

### Fixing Import Issues

When import issues are detected:
1. **Relative imports** are automatically converted to absolute imports
2. **Inline imports** are moved to the top of the file (unless flagged as necessary)
3. **Import organization** follows the standard: standard library → third-party → local imports

## Expected Output

The command will:
- Verify virtual environment is active
- Show progress of each build step
- Automatically fix formatting issues
- Perform semantic analysis on changed files
- Verify absolute imports and fix relative imports
- Move inline imports to top of files (where appropriate)
- Run tests and show results
- Display coverage information
- Exit with success (0) when all issues are resolved

## Troubleshooting

If you encounter persistent issues:

1. **Check virtual environment**: Ensure you're in an active venv
   ```bash
   source venv/bin/activate
   ```

2. **Check Docker**: Ensure MongoDB container is running
   ```bash
   docker compose up --detach
   ```

3. **Clean environment**: Remove cached files
   ```bash
   make clean
   ```

4. **Manual fixes**: If automatic fixes fail, manually address the specific error messages

## Notes

- This command follows the project's build pipeline defined in `Makefile`
- Pre-commit hooks will automatically format code before running tests
- Semantic analysis ensures import consistency across the codebase
- All tests must pass for the build to succeed
- Coverage requirements must be met (currently 55%)
- Make is running also in CI, if make did not pass this branch cannot be pushed to CI
- You must fix all errors even if they are not relevant directly to the current task
