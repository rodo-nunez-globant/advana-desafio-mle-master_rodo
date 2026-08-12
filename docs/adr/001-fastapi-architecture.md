# ADR-001: FastAPI Architecture for Flight Delay Prediction

## Status
Accepted

## Context
The challenge requires deploying a machine learning model for flight delay prediction as an API service. The existing codebase includes a basic FastAPI structure with health and prediction endpoints. We need to architect a production-ready API that serves the flight delay model while maintaining compatibility with existing tests.

## Decision
Adopt FastAPI as the web framework for serving flight delay predictions with the following architectural principles:

1. **Separation of Concerns**: Model logic remains in the `challenge/model.py` as required by tests, FastAPI handles HTTP concerns in `challenge/api.py`
2. **ASynchronous Processing**: FastAPI's async support enables concurrent request handling
3. **Automatic Documentation**: FastAPI generates OpenAPI/Swagger documentation automatically
4. **Type Safety**: Use Python type hints for request/response validation
5. **Dependency Injection**: Leverage FastAPI's DI for shared services

## Consequences

### Positive
- High performance async request handling
- Automatic API documentation generation
- Built-in request/response validation
- Easy testing with TestClient (already used in existing tests)
- Type safety for better development experience
- Good integration with existing challenge structure

### Negative
- Additional complexity over simple Flask/other frameworks
- Learning curve for async patterns (minimal for this use case)
- Requires understanding of FastAPI's dependency injection

### Neutral
- Follows challenge requirement of using FastAPI (no alternative choice)
- Requires maintaining compatibility with existing test structure

## Implementation Details

- Maintain existing endpoint signatures required by tests
- Support the 10 specified features from the model
- Implement proper error handling and validation
- Include health check endpoint as required
- Ensure request format matches test expectations

## Alternatives Considered (by the AI analysis, I would just stick to FastAPI becuse of the challenge restrictions and to save time)
- Flask: Simpler but less performant and no async support
- Django REST: Overkill for single-model API
- FastAPI with different structure: Would break existing tests

## References
- README.md Challenge Requirements
- Constitution.md Technical Stack section
- Existing tests/api/test_api.py structure