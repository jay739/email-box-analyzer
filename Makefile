# Makefile for Email Box Analyzer

.PHONY: help install test lint format clean build-windows build-macos build-linux run

# Default target
help:
	@echo "Email Box Analyzer - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run the application"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo ""
	@echo "Building:"
	@echo "  build-windows - Build Windows executable"
	@echo "  build-macos   - Build macOS DMG"
	@echo "  build-linux   - Build Linux DEB package"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       - Clean build artifacts"
	@echo "  help        - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .

# Run the application
run:
	@echo "Running Email Box Analyzer..."
	python src/main.py

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

# Run linting
lint:
	@echo "Running linting checks..."
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	mypy src/ --ignore-missing-imports

# Format code
format:
	@echo "Formatting code..."
	black src/
	isort src/

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf *.deb
	rm -rf *.dmg
	rm -rf *.exe
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build Windows executable
build-windows:
	@echo "Building Windows executable..."
	python scripts/build_windows.py

# Build macOS DMG
build-macos:
	@echo "Building macOS DMG..."
	python scripts/build_macos.py

# Build Linux DEB package
build-linux:
	@echo "Building Linux DEB package..."
	python scripts/build_linux.py

# Build all platforms
build-all: build-windows build-macos build-linux

# Create source distribution
sdist:
	@echo "Creating source distribution..."
	python setup.py sdist

# Create wheel distribution
wheel:
	@echo "Creating wheel distribution..."
	python setup.py bdist_wheel

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-qt pytest-cov black flake8 mypy isort pre-commit

# Setup pre-commit hooks
setup-hooks:
	@echo "Setting up pre-commit hooks..."
	pre-commit install

# Run pre-commit on all files
pre-commit-all:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

# Security check
security:
	@echo "Running security checks..."
	pip install bandit safety
	bandit -r src/ -f json -o bandit-report.json || true
	safety check --json --output safety-report.json || true

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  # On Linux/macOS"
	@echo "  venv\\Scripts\\activate     # On Windows"

# Install in development mode
install-dev-mode:
	@echo "Installing in development mode..."
	pip install -e .[dev]

# Run specific test file
test-file:
	@echo "Usage: make test-file FILE=tests/unit/test_config_manager.py"
	@if [ -z "$(FILE)" ]; then echo "Please specify FILE parameter"; exit 1; fi
	pytest $(FILE) -v

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage report..."
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

# Check code quality
quality: lint format test

# Full development setup
setup: venv install-dev setup-hooks
	@echo "Development environment setup complete!"
	@echo "Activate virtual environment and run 'make run' to start the application" 