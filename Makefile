# ENTROPIA Makefile
# Thermodynamic Framework for Information Systems

.PHONY: help install install-dev clean test lint format type-check docs serve-docs build publish docker docker-run benchmark shell

# Variables
PYTHON := python3
PIP := pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy
DOCKER_IMAGE := entropia:latest
DOCKER_CONTAINER := entropia

# Colors
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(GREEN)ENTROPIA Makefile Commands:$(NC)"
	@echo "  make install     - Install production dependencies"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make type-check  - Run type checking"
	@echo "  make docs        - Build documentation"
	@echo "  make serve-docs  - Serve documentation locally"
	@echo "  make build       - Build package"
	@echo "  make publish     - Publish to PyPI"
	@echo "  make docker      - Build Docker image"
	@echo "  make docker-run  - Run Docker container"
	@echo "  make benchmark   - Run benchmarks"
	@echo "  make shell       - Start Python shell with ENTROPIA"

install:
	@echo "$(GREEN)Installing production dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev:
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e ".[dev]"
	pre-commit install

clean:
	@echo "$(GREEN)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .benchmarks/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(PYTEST) tests/ -v --cov=entropia --cov-report=term-missing

test-slow:
	@echo "$(GREEN)Running slow tests...$(NC)"
	$(PYTEST) tests/ -v -m slow --cov=entropia

test-simulation:
	@echo "$(GREEN)Running simulation tests...$(NC)"
	entropia test --env E-ENV-01 --nodes 1000 --duration 60
	entropia test --env E-ENV-02 --nodes 10000 --duration 120

lint:
	@echo "$(GREEN)Running linters...$(NC)"
	$(FLAKE8) src/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	$(MYPY) src/ --ignore-missing-imports

format:
	@echo "$(GREEN)Formatting code...$(NC)"
	$(BLACK) src/ tests/ --line-length=88
	$(ISORT) src/ tests/ --profile=black --line-length=88

type-check:
	@echo "$(GREEN)Running type checker...$(NC)"
	$(MYPY) src/ --strict --ignore-missing-imports

docs:
	@echo "$(GREEN)Building documentation...$(NC)"
	cd docs && make html

serve-docs:
	@echo "$(GREEN)Serving documentation at http://localhost:8000$(NC)"
	cd docs/build/html && $(PYTHON) -m http.server 8000

build:
	@echo "$(GREEN)Building package...$(NC)"
	rm -rf dist/
	$(PYTHON) -m build
	@echo "$(GREEN)Package built in dist/$(NC)"

publish-test:
	@echo "$(GREEN)Publishing to TestPyPI...$(NC)"
	$(PYTHON) -m twine upload --repository testpypi dist/*

publish:
	@echo "$(GREEN)Publishing to PyPI...$(NC)"
	$(PYTHON) -m twine upload dist/*

docker:
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t $(DOCKER_IMAGE) .

docker-run:
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 8080:8080 --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)

docker-stop:
	@echo "$(GREEN)Stopping Docker container...$(NC)"
	docker stop $(DOCKER_CONTAINER) || true
	docker rm $(DOCKER_CONTAINER) || true

benchmark:
	@echo "$(GREEN)Running benchmarks...$(NC)"
	$(PYTEST) tests/benchmarks/ --benchmark-only --benchmark-json=benchmark.json

shell:
	@echo "$(GREEN)Starting Python shell...$(NC)"
	$(PYTHON) -c "import entropia; print(f'ENTROPIA v{entropia.__version__} loaded'); import IPython; IPython.embed()"

dashboard:
	@echo "$(GREEN)Starting Ψ-Dashboard...$(NC)"
	entropia dashboard --port 8080

simulate:
	@echo "$(GREEN)Running simulation...$(NC)"
	entropia simulate --env $(ENV) --nodes $(NODES) --duration $(DURATION)

analyze:
	@echo "$(GREEN)Analyzing outage data...$(NC)"
	entropia analyze --outage $(OUTAGE) --data $(DATA)

health:
	@echo "$(GREEN)Health check...$(NC)"
	entropia health-check

version:
	@echo "$(GREEN)ENTROPIA version:$(NC)"
	entropia --version

all: clean install-dev lint type-check test build
	@echo "$(GREEN)All tasks completed!$(NC)"
