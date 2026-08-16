# Software Engineer (ML & LLMs) Challenge

## Overview

Welcome to the **Software Engineer (ML & LLMs)** Application Challenge. In this, you will have the opportunity to get closer to a part of the reality of the role, and demonstrate your skills and knowledge in machine learning and cloud.

## SDD Methodology

This project follows **Spec-Driven Development (SDD)** methodology. The project constitution is located in `.sdd/constitution.md` and defines all technical decisions, boundaries, and requirements.

### Project Structure

The project has been enhanced with SDD-compliant structure while preserving the original challenge folders:

```
├── .sdd/                    # SDD methodology files
│   ├── constitution.md      # Project constitution and boundaries
│   └── README.md           # SDD documentation
├── challenge/               # Original challenge code (preserved)
│   ├── api.py              # FastAPI implementation
│   ├── model.py            # Model implementation
│   └── exploration.qmd     # Exploratory analysis
├── src/                    # SDD source code modules
│   ├── data/              # Data processing modules
│   ├── features/          # Feature engineering
│   ├── models/            # Model definitions
│   ├── evaluation/        # Model evaluation
│   └── utils/             # Utility functions
├── pipeline/              # Pipeline orchestration
│   ├── dags/             # Airflow DAGs (future)
│   ├── scripts/          # Pipeline scripts
│   └── config/           # Pipeline configurations
├── config/               # YAML configurations
│   ├── global/           # Global settings
│   ├── dev/              # Development settings
│   ├── stage/            # Staging settings
│   └── prod/             # Production settings
├── tests/                # Test suites
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── data/             # Test fixtures
├── data/                 # Data directories
│   ├── raw/              # Raw input data
│   ├── processed/        # Processed data
│   └── external/         # External data references
├── docs/                 # Documentation
│   └── adr/              # Architecture Decision Records
├── notebooks/            # Quarto notebooks
├── models/               # Saved models
├── outputs/              # Analysis outputs
└── scripts/              # Standalone scripts
```

### Key SDD Principles

- **Constitution-Driven**: All decisions follow the constitution boundaries
- **YAML Configuration**: Hierarchical config overrides (global → env → runtime)
- **Debug Mode**: All pipelines support `--debug-mode` for fast testing
- **No Output Commits**: Only source code is versioned
- **Modular Design**: SOLID principles for all code

## Problem

A jupyter notebook (training.ipynb) has been provided with the work of a Data Scientist (from now on, the DS). The DS, trained a model to predict the probability of **delay** for a flight taking off or landing at SCL airport. The model was trained with public and real data, below we provide you with the description of the dataset:

|Column|Description|
|-----|-----------|
|`Fecha-I`|Scheduled date and time of the flight.|
|`Vlo-I`|Scheduled flight number.|
|`Ori-I`|Programmed origin city code.|
|`Des-I`|Programmed destination city code.|
|`Emp-I`|Scheduled flight airline code.|
|`Fecha-O`|Date and time of flight operation.|
|`Vlo-O`|Flight operation number of the flight.|
|`Ori-O`|Operation origin city code.|
|`Des-O`|Operation destination city code.|
|`Emp-O`|Airline code of the operated flight.|
|`DIA`|Day of the month of flight operation.|
|`MES`|Number of the month of operation of the flight.|
|`AÑO`|Year of flight operation.|
|`DIANOM`|Day of the week of flight operation.|
|`TIPOVUELO`|Type of flight, I =International, N =National.|
|`OPERA`|Name of the airline that operates.|
|`SIGLAORI`|Name city of origin.|
|`SIGLADES`|Destination city name.|

In addition, the DS considered relevant the creation of the following columns:

|Column|Description|
|-----|-----------|
|`high_season`|1 if `Date-I` is between Dec-15 and Mar-3, or Jul-15 and Jul-31, or Sep-11 and Sep-30, 0 otherwise.|
|`min_diff`|difference in minutes between `Date-O` and `Date-I`|
|`period_day`|morning (between 5:00 and 11:59), afternoon (between 12:00 and 18:59) and night (between 19:00 and 4:59), based on `Date-I`.|
|`delay`|1 if `min_diff` > 15, 0 if not.|

## Challenge

### Instructions

1. Create a repository in **github** and copy all the challenge content into it. Remember that the repository must be **public**.

2. Use the **main** branch for any official release that we should review. It is highly recommended to use [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) development practices. **NOTE: do not delete your development branches.**
   
3. Please, do not change the structure of the challenge (names of folders and files).
   
4. All the documentation and explanations that you have to give us must go in the `challenge.md` file inside `docs` folder.

5. To send your challenge, you must do a `POST` request to:
    `https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer`
    This is an example of the `body` you must send:
    ```json
    {
      "name": "Juan Perez",
      "mail": "juan.perez@example.com",
      "github_url": "https://github.com/juanperez/latam-challenge.git",
      "api_url": "https://juan-perez.api"
    }
    ```

***NOTE: We recommend to send the challenge even if you didn't manage to finish all the parts.***

### Context:

We need to operationalize the data science work for the airport team. For this, we have decided to enable an `API` in which they can consult the delay prediction of a flight.

*We recommend reading the entire challenge (all its parts) before you start developing.*

### Part I

In order to operationalize the model, transcribe the `.ipynb` file into the `model.py` file:

- If you find any bug, fix it.
- The DS proposed a few models in the end. Choose the best model at your discretion, argue why. **It is not necessary to make improvements to the model.**
- Apply all the good programming practices that you consider necessary in this item.
- The model should pass the tests by running `make model-test`.

> **Note:**
> - **You cannot** remove or change the name or arguments of **provided** methods.
> - **You can** change/complete the implementation of the provided methods.
> - **You can** create the extra classes and methods you deem necessary.

### Part II

Deploy the model in an `API` with `FastAPI` using the `api.py` file.

- The `API` should pass the tests by running `make api-test`.

> **Note:** 
> - **You cannot** use other framework.

### Part III

Deploy the `API` in your favorite cloud provider (we recomend to use GCP).

- Put the `API`'s url in the `Makefile` (`line 26`).
- The `API` should pass the tests by running `make stress-test`.

> **Note:** 
> - **It is important that the API is deployed until we review the tests.**

### Part IV

We are looking for a proper `CI/CD` implementation for this development.

- Create a new folder called `.github` and copy the `workflows` folder that we provided inside it.
- Complete both `ci.yml` and `cd.yml`(consider what you did in the previous parts).

## Complete Setup and Testing Guide

This guide walks you through setting up the environment and testing all parts of the challenge.

### Prerequisites

- Python 3.13 (required)
- Git
- Google Cloud Account (for Part III)
- Docker (optional, for container testing)

### 1. Environment Setup

#### Install uv (recommended for faster dependency management)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

#### Clone and setup the project
```bash
git clone <your-repo-url>
cd advana-desafio-mle-master_rodo

# Install all dependencies (recommended for developers)
uv sync --all-extras

# Or install minimal dependencies (for just running the API)
uv sync
```

### 2. Part I: Model Implementation

#### Train the model
```bash
# Train the model using the existing script
uv run python challenge/train_model.py
```
This will:
- Load data from `data/data.csv`
- Train the model using the `DelayModel` class
- Save the trained model to `models/delay_model.pkl`

#### Test the model
```bash
# Run model tests
make model-test

# View test coverage report
open reports/html/index.html
```

### 3. Part II: Local API Testing

#### Start the API locally
```bash
# Development mode with auto-reload
uv run uvicorn challenge.api:app --reload --port 8000

# Or use the Makefile
make run
```

#### Test the API endpoints
```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "I", "MES": 7}]}'

# Run API tests
make api-test
```

### 4. Docker Testing (Optional but Recommended)

#### Build and test locally
```bash
# Build the Docker image
docker build -t flight-delay-api:test .

# Run the container
docker run -p 8080:8080 flight-delay-api:test

# Test the containerized API
curl http://localhost:8080/health
```

### 5. Part III: GCP Cloud Run Deployment

#### Setup GCP Project
```bash
# Install gcloud CLI if not already installed
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Replace YOUR_PROJECT_ID in deploy/gcp-deploy.sh
# Edit the file and change PROJECT_ID="your-gcp-project-id"
```

#### Deploy to Cloud Run
```bash
# Deploy using the automated script
make deploy

# Or manually
./deploy/gcp-deploy.sh
```

The deployment script will:
- Enable required GCP APIs (Cloud Build, Cloud Run)
- Build the Docker image on Google Cloud Build
- Deploy to Cloud Run
- Update the Makefile with the deployed URL

#### Test the deployed API
```bash
# The deployment script updates this automatically
make health-check

# Run stress tests against deployed API
make stress-test

# View stress test report
open reports/stress-test.html
```

### 6. Part IV: CI/CD Setup

#### GitHub Actions Setup
```bash
# The workflows are already in place
# Just push to GitHub to trigger CI/CD

git add .
git commit -m "Complete implementation"
git push origin main
```

#### CI/CD Pipeline
- **CI** (`ci.yml`): Runs on every push, tests code quality and functionality
- **CD** (`cd.yml`): Deploys to Cloud Run on merges to main

### 7. Troubleshooting

#### Common Issues

**uv command not found**
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Permission denied on gcloud**
```bash
# Authenticate with GCP
gcloud auth login
gcloud auth application-default login
```

**Docker build fails with data not found**
```bash
# Check .gcloudignore doesn't exclude data/
cat .gcloudignore
# Ensure data/ is not excluded
```

**Stress test fails with locust not found**
```bash
# Install test dependencies
uv sync --extra test
# The Makefile now does this automatically
```

### 8. Quick Commands Reference

```bash
# Development
make run              # Start API locally
make test             # Run all tests
make model-test       # Test model only
make api-test         # Test API only
make lint             # Code quality checks

# Deployment
make deploy           # Deploy to GCP Cloud Run
make health-check     # Check deployed API
make stress-test      # Load test deployed API

# Docker
docker build -t flight-delay-api .
docker run -p 8080:8080 flight-delay-api
```

### 9. Submitting Your Challenge

Once all parts are complete and tested:

1. Ensure your API is deployed and passing stress tests
2. Update the submission details:
   ```json
   {
     "name": "Your Name",
     "mail": "your.email@example.com",
     "github_url": "https://github.com/yourusername/your-repo.git",
     "api_url": "https://your-deployed-api-url.a.run.app"
   }
   ```
3. Submit to: `https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer`

### 10. Project Structure for Reviewers

```
├── challenge/           # Core implementation
│   ├── model.py       # Part I: Model implementation
│   ├── api.py         # Part II: FastAPI implementation
│   └── train_model.py # Model training script
├── data/              # Training data
├── models/            # Trained model (.pkl files)
├── tests/             # All test suites
├── deploy/            # Deployment scripts
├── .github/workflows/ # CI/CD configuration
└── Makefile          # All commands and URLs
```

The Makefile contains all necessary commands and will be updated with your deployed API URL after running `make deploy`.