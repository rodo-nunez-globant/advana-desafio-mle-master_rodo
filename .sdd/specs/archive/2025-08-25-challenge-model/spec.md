# Challenge Model Specification

## Overview
Implement a simple flight delay prediction model for the challenge requirements. This specification covers the implementation of the `DelayModel` class in `challenge/model.py` that meets all test requirements while following constitutional boundaries.

## Requirements

### Functional Requirements
1. **Model Class**: Implement `DelayModel` class with three required methods:
   - `preprocess()`: Prepare raw data for training/prediction
   - `fit()`: Train the model with preprocessed data
   - `predict()`: Predict delays for new flights

2. **Feature Engineering**: Create exactly the 10 features required by tests:
   - `OPERA_Latin American Wings`
   - `MES_7`
   - `MES_10`
   - `OPERA_Grupo LATAM`
   - `MES_12`
   - `TIPOVUELO_I`
   - `MES_4`
   - `MES_11`
   - `OPERA_Sky Airline`
   - `OPERA_Copa Air`

3. **Target Variable**: Binary classification for `delay` column (1 if delayed, 0 otherwise)

4. **Model Algorithm**: Use Logistic Regression with class balancing

### Data Processing Requirements
1. **Input Data**: Raw flight data from CSV with columns:
   - `Fecha-I`: Scheduled date and time
   - `Fecha-O`: Operation date and time
   - `OPERA`: Airline name
   - `MES`: Month number
   - `TIPOVUELO`: Flight type (I=International, N=National)
   - Other columns as provided in dataset

2. **Feature Transformations**:
   - One-hot encoding for categorical variables (OPERA, MES, TIPOVUELO)
   - Select only the 10 required features
   - Handle missing values appropriately

3. **Target Processing**:
   - Create `delay` column: 1 if min_diff > 15, 0 otherwise
   - Return as DataFrame with single column

### Performance Requirements
1. **Primary Metric**: F-3 score (beta=3) - prioritize recall for delayed flights
2. **Secondary Metrics**: Recall for delayed flights
3. **Data Volume**: Handle 9MB dataset efficiently
4. **Latency**: No strict requirements for challenge

### Integration Requirements
1. **Test Compatibility**: Must pass all tests in `tests/model/test_model.py`
2. **Method Signatures**: Cannot change existing method signatures
3. **Return Types**: Must return exact types expected by tests
4. **Dependencies**: Use only approved frameworks (scikit-learn, pandas)

## Data Flow

### Input
```
Raw CSV Data (data/data.csv)
├── Fecha-I: Scheduled datetime
├── Fecha-O: Operation datetime
├── OPERA: Airline name
├── MES: Month (1-12)
├── TIPOVUELO: Flight type (I/N)
└── Other columns...
```

### Preprocessing Flow
```
Raw Data → Feature Engineering → Feature Selection → Output
```

1. **Feature Engineering**:
   - Calculate `min_diff` = Fecha-O - Fecha-I
   - Create `delay` target if target_column provided
   - One-hot encode categorical variables

2. **Feature Selection**:
   - Select exactly 10 features specified in tests
   - Ensure consistent column ordering

3. **Output**:
   - Training mode: (features_df, target_df)
   - Prediction mode: features_df

### Training Flow
```
Features + Target → Logistic Regression → Trained Model
```

### Prediction Flow
```
New Data → Preprocess → Trained Model → Predictions (0/1)
```

## Implementation Specifications

### File Structure
```
challenge/
└── model.py  # Complete implementation
```

### Class Structure
```python
class DelayModel:
    def __init__(self):
        self._model = None  # Trained model storage
        
    def preprocess(self, data, target_column=None):
        # Feature engineering and selection
        # Returns (features, target) or features
        
    def fit(self, features, target):
        # Train Logistic Regression with class balancing
        # Store model in self._model
        
    def predict(self, features):
        # Return list of 0/1 predictions
```

### Key Implementation Details

#### Preprocessing Method
1. **Input Validation**: Check for required columns
2. **Date Processing**: Convert Fecha-I and Fecha-O to datetime
3. **Feature Creation**:
   - One-hot encode OPERA (keep only specified airlines)
   - One-hot encode MES (keep only specified months)
   - One-hot encode TIPOVUELO (keep only 'I')
4. **Target Creation**: If target_column provided, create delay column
5. **Feature Selection**: Return only the 10 required features

#### Fit Method
1. **Model Selection**: LogisticRegression with class_weight='balanced'
2. **Training**: Fit model on provided features and target
3. **Storage**: Save trained model in self._model

#### Predict Method
1. **Validation**: Ensure model is trained
2. **Prediction**: Use model to predict on features
3. **Output**: Return list of integers (0 or 1)

### Error Handling
- Handle missing columns gracefully
- Validate input data types
- Check model state before prediction
- Provide meaningful error messages

## Quality Standards

### Testing Requirements
- Must pass all unit tests in `tests/model/test_model.py`
- Achieve reasonable F-3 score on validation data
- Handle edge cases (empty data, missing columns)

### Code Quality
- Follow PEP 8 style guidelines
- Include docstrings for all methods
- Type hints for all function signatures
- No hardcoded values (use constants)

### Performance Standards
- Efficient memory usage for 9MB dataset
- Reasonable training time (<1 minute)
- Fast prediction for single instances

## Constitutional Compliance

### Always Do
- ✅ Preserve existing challenge folder structure
- ✅ Maintain existing class/method signatures
- ✅ Use exactly the top 10 features from tests
- ✅ Use uv for environment management
- ✅ Follow SOLID principles

### Ask First (Already Addressed)
- ✅ Model selection: Logistic Regression
- ✅ Class balancing: Implemented
- ✅ Feature selection: Exact 10 features

### Never Do
- ❌ Modify existing test files
- ❌ Change method signatures
- ❌ Break backward compatibility
- ❌ Commit model artifacts

## Success Criteria
1. All tests pass (`make model-test`)
2. Model achieves reasonable F-3 score
3. Code follows constitutional boundaries
4. Implementation is maintainable and documented