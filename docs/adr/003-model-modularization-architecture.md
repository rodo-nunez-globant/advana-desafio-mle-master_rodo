# ADR 003: Model Modularization Architecture

## Status
Accepted

## Context
We need to modularize the flight delay prediction model from `challenge/exploration.qmd` into two implementations:
1. A simple challenge solution in `challenge/model.py`
2. A robust, scalable pipeline using scikit-learn's Pipeline library

The exploration notebook contains all the data analysis, feature engineering, and model training logic that needs to be extracted into maintainable, production-ready code.

## Decision

### 1. Challenge Solution (Simple Implementation)

**Location**: `challenge/model.py`
**Purpose**: Meet challenge requirements while respecting existing constraints

**Approach**:
- Use exact same features and preprocessing from `exploration.qmd`
- Implement Logistic Regression with feature engineering and class balancing
- Respect existing method signatures in `challenge/model.py`
- Keep it simple and self-contained

**Features to Implement** (from exploration.qmd):
- `high_season` feature (1 if date in high season periods)
- `min_diff` feature (difference in minutes between Fecha-O and Fecha-I)
- `period_day` feature (morning/afternoon/night based on Fecha-I)
- Other features as identified in the exploration
- Class balancing for the binary classification

### 2. Robust Pipeline Solution (Production Implementation)

There are a lot of ways to create pipelines. We could use a simple script importation, we could use Pipeline from scikit learn, we could create an Airflow DAG for batch processes, we could create a KubeFlow pipeline to later upload to Vertex AI, etc. There are intinite ways to create modularized pipelines. Here I want to propose one idea simple enought, but with some ideas I like to implement, like a debug mode. We can talk more about this during the technical interview.

**Structure**:
```
src/data/preprocess.py          # Custom transformers for feature engineering
src/models/train.py             # Model training logic
src/evaluation/predict.py       # Model prediction logic
pipeline/pipeline.py            # Pipeline orchestrator
src/data/synthetic_generator.py # Synthetic data generator
```

**Technical Approach**:

#### Custom Transformers (`src/data/preprocess.py`)
- Create custom transformer classes inheriting from `BaseEstimator` and `TransformerMixin`
- Transformers for:
  - Date parsing and feature extraction
  - High season calculation
  - Period of day calculation
  - Min difference calculation
  - Categorical encoding
  - Feature scaling

#### Training Module (`src/models/train.py`)
- Encapsulate model training logic
- Support for Logistic Regression with class balancing
- Hyperparameter configuration
- Model validation and metrics calculation

#### Prediction Module (`src/evaluation/predict.py`)
- Model loading and prediction logic
- Batch and single prediction support
- Prediction confidence scoring

#### Pipeline Orchestrator (`pipeline/pipeline.py`)
- Use scikit-learn's `Pipeline` class
- Debug mode with `--debug` flag
- End-to-end execution with proper error handling
- Configuration management

#### Synthetic Data Generator (`src/data/synthetic_generator.py`)
- Generate synthetic data matching the real data schema
- 1000 rows for fast debugging
- Target execution time: <10 seconds in debug mode

### 3. Model Persistence
- Use `joblib` for fast model serialization
- Save models to `models/` directory
- Version model artifacts with timestamps

### 4. Debug Mode Implementation
- `--debug` flag in pipeline script
- Synthetic data generation for fast testing
- Independent of real data size
- Target execution: <10 seconds end-to-end

## Rationale

### Why Two Implementations?
1. **Challenge Requirements**: The challenge has specific constraints (existing method signatures, simple structure) that must be respected
2. **Production Readiness**: The robust pipeline provides scalability, maintainability, and follows SDD methodology
3. **Learning Opportunity**: Shows evolution from simple to production-ready code

### Why Scikit-learn Pipeline?
- Standard, well-documented approach
- Easy to save/load entire preprocessing + model pipeline
- Prevents data leakage through proper fit/transform separation
- Supports hyperparameter tuning

### Why Custom Transformers?
- Full control over feature engineering logic
- Reusable components
- Easy to test individual components
- Consistent with production ML best practices

### Why Synthetic Data for Debug?
- Fast execution regardless of real data size
- Reproducible testing environment
- No dependency on data availability
- Meets constitution requirement for <1 minute debug execution

## Consequences

### Positive
- Clear separation of concerns
- Maintainable and testable code
- Follows SDD methodology
- Meets both challenge and production requirements
- Fast debugging capability

### Negative
- More complex than simple script
- Requires understanding of scikit-learn Pipeline API
- Additional code to maintain

### Risks
- Custom transformers might have bugs not caught in exploration
- Synthetic data might not represent real data edge cases
- Pipeline complexity could hide issues

## Implementation Plan

1. **Phase 1**: Implement challenge solution in `challenge/model.py`
2. **Phase 2**: Create custom transformers in `src/data/preprocess.py`
3. **Phase 3**: Implement training and prediction modules
4. **Phase 4**: Build pipeline orchestrator with debug mode
5. **Phase 5**: Add synthetic data generator
6. **Phase 6**: Integration testing and documentation

## Related Decisions
- [ADR 001: FastAPI Architecture](001-fastapi-architecture.md)
- [ADR 002: SDD Methodology Adoption](002-sdd-methodology-adoption.md)

## Notes
- All implementations must follow the constitution boundaries
- Model performance targets (F-3 score) must be met
- Code must pass existing tests
- Documentation should be updated as modules are implemented