# Challenge Model Implementation Tasks

## Priority 1: Core Infrastructure (Must Complete First)

### Task 1.1: Setup and Validation
- [ ] **Create constants class attributes**
  - Define REQUIRED_COLUMNS list
  - Define FEATURES_COLS list (exact 10 features from tests)
  - Define TARGET_COL and DELAY_THRESHOLD constants
  - **Estimated time**: 30 minutes
  - **Dependencies**: None

- [ ] **Add input validation to preprocess method**
  - Check for required columns in input DataFrame
  - Validate DataFrame is not empty
  - Add meaningful error messages
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 1.1

### Task 1.2: Basic Method Skeletons
- [ ] **Implement method signatures with type hints**
  - Ensure preprocess() returns correct types
  - Ensure fit() has correct parameters
  - Ensure predict() returns List[int]
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 1.1

## Priority 2: Data Preprocessing Implementation

### Task 2.1: Date Processing
- [ ] **Implement date conversion logic**
  - Convert Fecha-I and Fecha-O to datetime
  - Handle date parsing errors gracefully
  - Calculate min_diff between dates
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 1.2

- [ ] **Create delay target column**
  - Implement delay calculation (min_diff > 15)
  - Return target DataFrame when target_column provided
  - Ensure correct column name and type
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 2.1

### Task 2.2: Feature Engineering
- [ ] **Implement one-hot encoding for OPERA**
  - Create binary columns for each airline
  - Keep only required airlines in FEATURES_COLS
  - Handle unknown airlines gracefully
  - **Estimated time**: 1.5 hours
  - **Dependencies**: Task 1.2

- [ ] **Implement one-hot encoding for MES**
  - Create binary columns for months 4, 7, 10, 11, 12
  - Ensure correct column naming (MES_X format)
  - Handle missing months
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 2.2

- [ ] **Implement one-hot encoding for TIPOVUELO**
  - Create TIPOVUELO_I column
  - Handle both 'I' and 'N' values
  - Ensure correct binary encoding
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 2.2

### Task 2.3: Feature Selection
- [ ] **Implement feature selection logic**
  - Select exactly the 10 features from FEATURES_COLS
  - Ensure consistent column ordering
  - Handle missing features gracefully
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 2.2, Task 2.3

- [ ] **Complete preprocess method**
  - Combine all preprocessing steps
  - Return correct format (features, target) or features
  - Add comprehensive error handling
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 2.3

## Priority 3: Model Training Implementation

### Task 3.1: Model Initialization
- [ ] **Initialize Logistic Regression model**
  - Use class_weight='balanced' for class imbalance
  - Set random_state for reproducibility
  - Configure max_iter for convergence
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 2.3

### Task 3.2: Training Logic
- [ ] **Implement fit method**
  - Train model on provided features and target
  - Handle edge cases (empty data, single class)
  - Store trained model in self._model
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 3.1

- [ ] **Add training validation**
  - Validate input shapes match
  - Check for NaN values
  - Add training success confirmation
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 3.2

## Priority 4: Prediction Implementation

### Task 4.1: Prediction Logic
- [ ] **Implement predict method**
  - Check if model is trained
  - Validate input features match training
  - Return list of integers (0/1)
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 3.2

### Task 4.2: Prediction Validation
- [ ] **Add comprehensive error handling**
  - Model not trained error
  - Feature mismatch error
  - Empty input handling
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 4.1

## Priority 5: Testing and Refinement

### Task 5.1: Unit Testing
- [ ] **Run provided test suite**
  - Execute `make model-test`
  - Identify failing tests
  - Document specific failures
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 4.2

- [ ] **Fix test failures**
  - Debug and fix preprocessing issues
  - Correct feature selection problems
  - Ensure correct return types
  - **Estimated time**: 2-3 hours
  - **Dependencies**: Task 5.1

### Task 5.2: Integration Testing
- [ ] **Test with real data**
  - Load data/data.csv
  - Test full preprocessing pipeline
  - Verify training and prediction flow
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 5.1

- [ ] **Performance validation**
  - Test training time on full dataset
  - Verify memory usage is reasonable
  - Check prediction speed
  - **Estimated time**: 45 minutes
  - **Dependencies**: Task 5.2

### Task 5.3: Code Quality
- [ ] **Add comprehensive docstrings**
  - Document all methods
  - Add parameter descriptions
  - Include return type documentation
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 5.1

- [ ] **Code style compliance**
  - Run black formatter
  - Fix any flake8 issues
  - Ensure PEP 8 compliance
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 5.3

## Priority 6: Final Validation

### Task 6.1: Complete Test Suite
- [ ] **Ensure all tests pass**
  - Run full test suite multiple times
  - Test on different data subsets
  - Verify edge cases handled
  - **Estimated time**: 1 hour
  - **Dependencies**: Task 5.3

### Task 6.2: Documentation
- [ ] **Update README if needed**
  - Document any special requirements
  - Add usage examples
  - Note any limitations
  - **Estimated time**: 30 minutes
  - **Dependencies**: Task 6.1

## Dependencies Summary

```
Phase 1 (Infrastructure): Tasks 1.1 → 1.2
Phase 2 (Preprocessing): Tasks 1.2 → 2.1 → 2.2 → 2.3
Phase 3 (Training): Tasks 2.3 → 3.1 → 3.2
Phase 4 (Prediction): Tasks 3.2 → 4.1 → 4.2
Phase 5 (Testing): Tasks 4.2 → 5.1 → 5.2 → 5.3
Phase 6 (Validation): Tasks 5.3 → 6.1 → 6.2
```

## Total Estimated Time: 18-22 hours

## Critical Path
1. Constants and validation (Task 1.1)
2. Preprocessing implementation (Tasks 2.1-2.3)
3. Model training (Tasks 3.1-3.2)
4. Prediction (Tasks 4.1-4.2)
5. Test compliance (Task 5.1)

## Risk Mitigation Tasks
- **High Risk**: Task 5.1 (Test failures) - allocate extra time
- **Medium Risk**: Task 2.2 (Feature engineering) - complex logic
- **Low Risk**: Tasks 1.1-1.2 (Infrastructure) - straightforward

## Success Criteria
- [ ] All tests in `tests/model/test_model.py` pass
- [ ] Model uses exactly 10 specified features
- [ ] Class balancing implemented
- [ ] Code follows constitutional boundaries
- [ ] No test data or model artifacts committed