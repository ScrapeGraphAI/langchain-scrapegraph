# Makefile for Project Automation

.PHONY: install lint type-check test docs serve-docs build all clean

# Variables
PACKAGE_NAME = langchain_scrapegraph
TEST_DIR = tests

# Default target
all: lint type-check test docs

# Install project dependencies
install:
	poetry install

# Linting and Formatting Checks
lint:
	poetry run ruff check $(PACKAGE_NAME) $(TEST_DIR) examples
	poetry run black --check $(PACKAGE_NAME) $(TEST_DIR) examples
	poetry run isort --check-only $(PACKAGE_NAME) $(TEST_DIR) examples

# Auto-format code
format:
	poetry run ruff check --fix $(PACKAGE_NAME) $(TEST_DIR) examples
	poetry run black $(PACKAGE_NAME) $(TEST_DIR) examples
	poetry run isort $(PACKAGE_NAME) $(TEST_DIR) examples

# Type Checking with MyPy
type-check:
	poetry run mypy $(PACKAGE_NAME) $(TEST_DIR)

# Run Tests
test:
	poetry run pytest --disable-socket --allow-unix-socket --asyncio-mode=auto $(TEST_DIR)/unit_tests
	poetry run pytest --asyncio-mode=auto $(TEST_DIR)/integration_tests

# Build Documentation using MkDocs
docs:
	poetry run mkdocs build

# Serve Documentation Locally
serve-docs:
	poetry run mkdocs serve

# Run Pre-Commit Hooks
pre-commit:
	poetry run pre-commit run --all-files

# Clean Up Generated Files
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf site/

# Build the Package
build:
	poetry build
