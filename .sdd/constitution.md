# Project Constitution: Software Engineer (ML & LLMs) Challenge - Rodo

## Project Identity
- **Name**: Software Engineer (ML & LLMs) Challenge - Rodo
- **Problem**: Operationalize a flight delay prediction model to help airports and airlines manage expected operational delays
- **Domain**: Aviation/Travel/Transportation
- **Data Science Type**: Binary Classification
- **End Users**: Airport operations teams
- **Project Type**: Adding SDD to existing codebase

## Technical Decisions

### Model & Performance
- **Problem Type**: Binary classification (delay vs no delay)
- **Primary Metric**: F-3 score (F-beta with beta=3) - gives 3x weight to recall over precision
- **Secondary Metrics**: Recall for delayed flights prioritized
- **Data Volume**: 9MB total dataset (very small)
- **Latency**: No strict requirements for this challenge

### Technology Stack
- **Language**: Python
- **Frameworks**: scikit-learn and XGBoost (as indicated in notebook, to be analyzed further)
- **Data Processing**: pandas initially, may test polars later for performance comparison
- **Environment**: uv for virtual environment management
- **Notebooks**: Quarto (.qmd) notebooks preferred over Jupyter
- **Containerization**: Dockerfile required for deployment

### Architecture
- **Deployment**: GCP (Google Cloud Platform) - per challenge requirements
- **Data**: No existing system integration (standalone API)
- **Latency**: Real-time API predictions needed
- **Deployment Frequency**: Monthly (model updates)
- **Monitoring**: Basic monitoring initially, no drift detection (challenge constraints)

### Configuration & Debugging
- **Configuration**: YAML files in config/ folder with hierarchical overrides
- **Environments**: dev, stage, prod
- **Debug Mode**: Mandatory for pipelines, optional for modules/scripts
- **Debug Strategy**: Synthetic dummy data for fast testing (<1 minute)

## Technical Decision Boundaries

### Always Do

**Project Structure & Standards**
- Preserve existing challenge folder structure and test files
- Maintain existing class/method signatures as required by tests
- Use exactly the top 10 features specified in tests
- Use uv for environment management
- Include Dockerfile for containerization
- Implement data leakage prevention (train/test split before transformations)
- Create modular scripts (.py, .sh, .r) instead of Jupyter notebooks
- Use Quarto notebooks (.qmd) when notebook format needed
- Follow SOLID principles for OOP design

**Data Science Standards**
- Prioritize recall for delayed flights (F-3 score metric)
- Use SHAP for model interpretability
- Implement proper logging and monitoring
- Include comprehensive testing (unit, integration, stress)
- Follow reproducible research principles
- Version source code only, reconstruct outputs through pipeline execution

**Security & Governance**
- Version source code only (.gitignore all outputs: .ipynb, .html, .pdf, .csv, model files)
- Never commit API keys, passwords, or secrets
- Never commit datasets or large data files
- Implement full audit trails for model decisions
- Use server-side validation (never client-side)

**Git Workflow**
- Use Git Flow framework with prod (protected default), dev, stage as permanent branches
- Use feature branches from dev for development (Git Flow pattern)
- Require PR approval for all merges to permanent branches
- Only project owner can merge to prod and stage
- Comprehensive testing before deployment

**Debug & Configuration**
- Use YAML configuration with hierarchical overrides (global → env → runtime)
- Implement --debug-mode flag for fast testing
- Debug mode mandatory for pipelines in pipeline/ folder
- Debug mode uses sandbox environments, not production
- Log execution times and alert when debug mode exceeds 1 minute

### Ask First

**Model & Architecture Changes**
- Modifying the top 10 features specification
- Changing model selection (XGBoost vs Logistic Regression)
- Adding new features beyond the specified 10
- Changing data preprocessing logic
- Modifying API endpoints or request/response format

**Infrastructure & Deployment**
- Changing cloud provider from GCP
- Modifying container configuration
- Changing deployment frequency strategy
- Adding external integrations beyond standalone API

**Testing & Quality**
- Modifying test requirements or expectations
- Changing performance metrics thresholds
- Altering monitoring strategy
- Modifying debug mode implementation

**Workflow Changes**
- Changing git workflow structure
- Modifying PR approval requirements
- Changing CI/CD platform from GitHub Actions
- Modifying merge permissions

### Never Do

**Project Integrity**
- Never modify existing test files or test class/method names
- Never change the existing challenge folder structure
- Never remove or modify provided class/method signatures
- Never break backward compatibility with existing API contract
- Never commit model artifacts or datasets to repository

**Security & Data**
- Never mix train/test information before proper split
- Never store credentials or sensitive data in code
- Never commit any output files (.html, .pdf, .csv, model files)
- Never ignore security vulnerability alerts
- Never skip data validation steps

**Production Safety**
- Never deploy to prod without passing all tests
- Never push directly to prod branch
- Never modify production configuration without review
- Never disable audit logging
- Never expose internal debugging endpoints in production

## Implementation Constraints

### Challenge-Specific Rules
- Must respect existing challenge folder structure
- Cannot modify provided class/method signatures
- Must implement the exact 10 features expected by tests
- Must pass all existing tests for model and API
- Must achieve performance thresholds as specified in tests

### SDD Integration Rules
- All SDD artifacts must not interfere with existing challenge structure
- Documentation must preserve existing conventions
- New workflows must complement, not replace, existing Makefile targets
- Configuration must not break existing setup

## Success Criteria

1. **Technical Success**: All existing tests pass with improved model implementation
2. **SDD Success**: Constitution followed throughout development
3. **Deployment Success**: API deployed to GCP with proper monitoring
4. **Challenge Success**: All 4 parts completed according to requirements

## Governance

This constitution serves as the immutable boundary system for this project. Any deviation from these rules requires explicit constitution amendment and team approval.

---
*Constitution Version: 1.0*
*Last Updated: 2026-07-10*
*Project: Software Engineer (ML & LLMs) Challenge - Rodo*