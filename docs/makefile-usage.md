# Makefile Usage Guide

This project uses a smart Makefile that automatically detects whether you have `uv` installed and adapts accordingly.

## Automatic Detection

The Makefile automatically detects if `uv` is available:
- **If uv is installed**: Uses `uv` commands (faster)
- **If uv is NOT installed**: Falls back to `pip` and `venv` (works everywhere)

## Quick Start

```bash
# Check if you have uv installed (optional)
make check-uv

# Install all dependencies
make install-dev

# Run tests
make api-test
make model-test

# Start the API server
make api

# Deploy to GCP
make deploy
```

## Available Commands

### Environment Setup
- `make check-uv` - Check if uv is installed
- `make venv` - Create virtual environment
- `make install` - Install production dependencies
- `make install-dev` - Install development dependencies

### Testing
- `make test` - Run all tests
- `make api-test` - Run API tests with coverage
- `make model-test` - Run model tests with coverage
- `make stress-test` - Run stress tests (requires deployed API)

### Development
- `make lint` - Run code linting
- `make format` - Format code with ruff
- `make train` - Train the model
- `make api` - Start the API server locally

### Deployment
- `make docker-build` - Build Docker image
- `make docker-test` - Test Docker container locally
- `make deploy` - Deploy to GCP Cloud Run

### Utilities
- `make build` - Build Python wheel package
- `make clean` - Clean up all generated files

## Installing uv (Optional but Recommended)

If you don't have uv installed, you can install it for faster dependency management:

```bash
# macOS
brew install uv

# Linux/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python (any platform)
pip install uv
```

## Benefits of uv

- **10-100x faster** than pip
- **Better dependency resolution**
- **Built-in virtual environment management**
- **Lock file support** (uv.lock)

## Without uv

The Makefile will still work perfectly with just pip and venv:
- Uses standard Python virtual environments
- Installs from pyproject.toml
- All commands work the same way

## Notes

- The Makefile automatically creates a virtual environment if it doesn't exist
- All commands activate the virtual environment automatically
- The `STRESS_URL` in the Makefile should be updated after deployment to GCP