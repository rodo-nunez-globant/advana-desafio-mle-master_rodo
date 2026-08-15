.ONESHELL:

# Check if uv is available, otherwise use pip
UV_AVAILABLE := $(shell command -v uv 2> /dev/null)
ifeq ($(UV_AVAILABLE),)
    PYTHON_CMD := python
    PIP_CMD := pip
    VENV_CMD := python3 -m venv
    ACTIVATE := source .venv/bin/activate &&
    INSTALL_DEV := $(PIP_CMD) install -e ".[dev,test]"
    INSTALL := $(PIP_CMD) install -e .
    PYTEST := pytest
    RUFF := ruff
    UVICORN := uvicorn
else
    PYTHON_CMD := uv run python
    PIP_CMD := uv pip
    VENV_CMD := uv venv
    ACTIVATE :=
    INSTALL_DEV := uv sync --dev
    INSTALL := uv sync
    PYTEST := uv run pytest
    RUFF := uv run ruff
    UVICORN := uv run uvicorn
endif

.PHONY: help
help:            	## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep
	@if [ -z "$(UV_AVAILABLE)" ]; then \
		echo ""; \
		echo "Note: Using pip/venv (uv not found)"; \
		echo "Install uv for faster dependency management: https://docs.astral.sh/uv/"; \
	else \
		echo ""; \
		echo "Using uv for fast dependency management"; \
	fi

.PHONY: check-uv
check-uv:			## Check if uv is installed
	@if [ -z "$(UV_AVAILABLE)" ]; then \
		echo "❌ uv not found. Install it from: https://docs.astral.sh/uv/"; \
		echo "Or continue with pip/venv (slower but works)"; \
	else \
		echo "✅ uv is installed and ready to use"; \
	fi

.PHONY: venv
venv:				## Create a virtual environment
	@echo "Creating virtual environment..."
	@rm -rf .venv
	$(VENV_CMD)
	@echo
	@echo "Virtual environment created!"
	@if [ -z "$(UV_AVAILABLE)" ]; then \
		echo "Run 'source .venv/bin/activate' to enable"; \
	else \
		echo "Run 'source .venv/bin/activate' or 'uv shell' to enable"; \
	fi

.PHONY: install
install:			## Install dependencies
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment first..."; \
		$(MAKE) venv; \
	fi
	@echo "Installing dependencies..."
	$(ACTIVATE) $(INSTALL)

.PHONY: install-dev
install-dev:		## Install development dependencies
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment first..."; \
		$(MAKE) venv; \
	fi
	@echo "Installing development dependencies..."
	$(ACTIVATE) $(INSTALL_DEV)

STRESS_URL = http://127.0.0.1:8000 
.PHONY: stress-test
stress-test:			## Run stress tests (change stress url to your deployed app)
	mkdir reports || true
	$(ACTIVATE) locust -f tests/stress/api_stress.py --print-stats --html reports/stress-test.html --run-time 60s --headless --users 100 --spawn-rate 1 -H $(STRESS_URL)

.PHONY: model-test
model-test:			## Run model tests and coverage
	mkdir reports || true
	$(ACTIVATE) $(PYTEST) --cov-config=.coveragerc --cov-report term --cov-report html:reports/html --cov-report xml:reports/coverage.xml --junitxml=reports/junit.xml --cov=challenge tests/model

.PHONY: api-test
api-test:			## Run API tests and coverage
	mkdir reports || true
	$(ACTIVATE) $(PYTEST) --cov-config=.coveragerc --cov-report term --cov-report html:reports/html --cov-report xml:reports/coverage.xml --junitxml=reports/junit.xml --cov=challenge tests/api

.PHONY: test
test:				## Run all tests
	mkdir reports || true
	$(ACTIVATE) $(PYTEST) --cov-config=.coveragerc --cov-report term --cov-report html:reports/html --cov-report xml:reports/coverage.xml --junitxml=reports/junit.xml --cov=challenge tests/

.PHONY: lint
lint:				## Run linting
	$(ACTIVATE) $(RUFF) check || echo "⚠️  Ruff not installed. Install with: pip install ruff or uv add ruff"

.PHONY: format
format:			## Format code
	$(ACTIVATE) $(RUFF) format || echo "⚠️  Ruff not installed. Install with: pip install ruff or uv add ruff"

.PHONY: build
build:				## Build locally the python artifact
	$(ACTIVATE) $(PYTHON_CMD) setup.py bdist_wheel

.PHONY: train
train:				## Train the model
	$(ACTIVATE) $(PYTHON_CMD) challenge/train_model.py

.PHONY: api
api:				## Start the API server
	$(ACTIVATE) $(UVICORN) challenge.api:app --reload

.PHONY: docker-build
docker-build:		## Build Docker image
	docker build -t flight-delay-api:latest .

.PHONY: docker-test
docker-test:			## Test Docker container locally
	./deploy/test-local.sh

.PHONY: deploy
deploy:				## Deploy to GCP Cloud Run
	./deploy/gcp-deploy.sh

.PHONY: clean
clean:				## Clean up generated files
	rm -rf .venv
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf reports/
	rm -rf .coverage
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete