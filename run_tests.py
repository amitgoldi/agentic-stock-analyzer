#!/usr/bin/env python3
"""Comprehensive test runner for the agentic stock analyzer."""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def run_unit_tests() -> bool:
    """Run unit tests."""
    return run_command([
        "python", "-m", "pytest", 
        "tests/test_models.py",
        "tests/test_config.py", 
        "tests/test_utils.py",
        "-v", "--tb=short"
    ], "Unit Tests")


def run_integration_tests() -> bool:
    """Run integration tests."""
    return run_command([
        "python", "-m", "pytest",
        "tests/test_agent_integration.py",
        "-v", "--tb=short"
    ], "Integration Tests")


def run_e2e_tests() -> bool:
    """Run end-to-end tests."""
    return run_command([
        "python", "-m", "pytest",
        "tests/test_end_to_end.py",
        "-v", "--tb=short"
    ], "End-to-End Tests")


def run_all_tests() -> bool:
    """Run all tests with coverage."""
    return run_command([
        "python", "-m", "pytest",
        "tests/",
        "-v", "--tb=short",
        "--cov=common",
        "--cov=lecture01",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov"
    ], "All Tests with Coverage")


def run_fast_tests() -> bool:
    """Run fast tests only (exclude slow/e2e tests)."""
    return run_command([
        "python", "-m", "pytest",
        "tests/",
        "-v", "--tb=short",
        "-m", "not slow"
    ], "Fast Tests Only")


def run_type_checking() -> bool:
    """Run type checking with mypy."""
    return run_command([
        "python", "-m", "mypy",
        "common/",
        "lecture01/",
        "--ignore-missing-imports"
    ], "Type Checking")


def run_code_formatting_check() -> bool:
    """Check code formatting with black."""
    return run_command([
        "python", "-m", "black",
        "--check",
        "--diff",
        "common/",
        "lecture01/",
        "tests/"
    ], "Code Formatting Check")


def run_import_sorting_check() -> bool:
    """Check import sorting with isort."""
    return run_command([
        "python", "-m", "isort",
        "--check-only",
        "--diff",
        "common/",
        "lecture01/",
        "tests/"
    ], "Import Sorting Check")


def run_quality_checks() -> bool:
    """Run all code quality checks."""
    print("\n🔍 Running Code Quality Checks...")
    
    checks = [
        ("Type Checking", run_type_checking),
        ("Code Formatting", run_code_formatting_check),
        ("Import Sorting", run_import_sorting_check),
    ]
    
    results = []
    for name, check_func in checks:
        results.append(check_func())
    
    return all(results)


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for agentic stock analyzer")
    parser.add_argument(
        "test_type",
        choices=["unit", "integration", "e2e", "all", "fast", "quality", "full"],
        nargs="?",
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    print("🧪 Agentic Stock Analyzer Test Runner")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Error: pyproject.toml not found. Please run from project root.")
        sys.exit(1)
    
    # Check if dependencies are installed
    try:
        import pytest
        import pytest_asyncio
    except ImportError:
        print("❌ Error: Test dependencies not installed.")
        print("Please run: uv add --dev pytest pytest-asyncio pytest-cov pytest-mock")
        sys.exit(1)
    
    success = True
    
    if args.test_type == "unit":
        success = run_unit_tests()
    elif args.test_type == "integration":
        success = run_integration_tests()
    elif args.test_type == "e2e":
        success = run_e2e_tests()
    elif args.test_type == "fast":
        success = run_fast_tests()
    elif args.test_type == "quality":
        success = run_quality_checks()
    elif args.test_type == "all":
        success = run_all_tests()
    elif args.test_type == "full":
        # Run everything: quality checks + all tests
        print("\n🚀 Running Full Test Suite...")
        quality_success = run_quality_checks()
        test_success = run_all_tests()
        success = quality_success and test_success
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("✅ All tests completed successfully!")
        print("\n📊 Coverage report generated in htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
        print("\n💡 Tips:")
        print("  - Check the error messages above")
        print("  - Run with --verbose for more details")
        print("  - Run specific test types: unit, integration, e2e")
    print('='*60)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()