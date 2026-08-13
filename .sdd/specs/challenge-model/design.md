# Challenge Model Design

## Architecture Overview

The challenge model follows a simple, monolithic design pattern with a single `DelayModel` class encapsulating all functionality. This design prioritizes simplicity and test compliance over scalability, as required by the challenge constraints.

### Component Architecture
```
DelayModel
├── _model: LogisticRegression (private)
├── preprocess()
├── fit()
└── predict()
```

### Data Flow Architecture
```
Raw CSV → Preprocess → Feature Engineering → Feature Selection → Training/Prediction
```

## Detailed Design

### Data Structures and Schemas

#### Input Schema
```python
# Raw data columns (from CSV)
required_columns = [
    'Fecha-I',      # Scheduled datetime (string)
    'Fecha-O',      # Operation datetime (string)
    'OPERA',        # Airline name (string)
    'MES',          # Month number (int 1-12)
    'TIPOVUELO',     # Flight type (string: 'I' or 'N')
    # ... other columns ignored
]
```

#### Feature Schema
```python
# Output features (exactly 10 as required by tests)
feature_columns = [
    'OPERA_Latin American Wings',  # One-hot encoded airline
    'MES_7',                       # One-hot encoded month
    'MES_10',                      # One-hot encoded month
    'OPERA_Grupo LATAM',           # One-hot encoded airline
    'MES_12',                      # One-hot encoded month
    'TIPOVUELO_I',                 # One-hot encoded flight type
    'MES_4',                       # One-hot encoded month
    'MES_11',                      # One-hot encoded month
    'OPERA_Sky Airline',           # One-hot encoded airline
    'OPERA_Copa Air'               # One-hot encoded airline
]
```

#### Target Schema
```python
# Target variable
target_column = 'delay'  # Binary: 1 if delayed, 0 otherwise
```

### Processing Algorithms and Workflows

#### Preprocessing Algorithm
```python
def preprocess(data, target_column=None):
    """
    1. Input Validation
       - Check required columns exist
       - Validate data types
    
    2. Date Processing
       - Convert Fecha-I and Fecha-O to datetime
       - Calculate min_diff = Fecha-O - Fecha-I
    
    3. Target Creation (if training)
       - Create delay column: 1 if min_diff > 15, else 0
    
    4. Feature Engineering
       - One-hot encode OPERA (create binary columns for each airline)
       - One-hot encode MES (create binary columns for each month)
       - One-hot encode TIPOVUELO (create binary for 'I')
    
    5. Feature Selection
       - Select only the 10 required features
       - Ensure consistent column order
    
    6. Return
       - Training: (features_df, target_df)
       - Prediction: features_df
    """
```

#### Training Algorithm
```python
def fit(features, target):
    """
    1. Model Initialization
       - LogisticRegression(class_weight='balanced')
       - Random state for reproducibility
    
    2. Training
       - Fit model on features and target
       - Handle class imbalance automatically
    
    3. Model Storage
       - Save trained model in self._model
    """
```

#### Prediction Algorithm
```python
def predict(features):
    """
    1. Validation
       - Check if model is trained
       - Validate feature columns
    
    2. Prediction
       - Use model.predict() on features
       - Convert to list of integers
    
    3. Return
       - List of 0/1 predictions
    """
```

### Model Architecture and Training Procedures

#### Model Configuration
```python
model = LogisticRegression(
    class_weight='balanced',  # Handle class imbalance
    random_state=42,          # Reproducibility
    max_iter=1000            # Ensure convergence
)
```

#### Training Procedure
1. **Data Preparation**: Features and target from preprocessing
2. **Model Fitting**: Standard scikit-learn fit procedure
3. **Validation**: Internal validation (optional, not required by tests)
4. **Storage**: Save model instance for prediction

### Error Handling and Edge Cases

#### Input Validation
```python
# Missing columns
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"Missing required columns: {missing_columns}")

# Empty data
if data.empty:
    raise ValueError("Input data is empty")

# Invalid dates
try:
    data['Fecha-I'] = pd.to_datetime(data['Fecha-I'])
    data['Fecha-O'] = pd.to_datetime(data['Fecha-O'])
except Exception as e:
    raise ValueError(f"Invalid date format: {e}")
```

#### Prediction Validation
```python
# Model not trained
if self._model is None:
    raise ValueError("Model must be trained before prediction")

# Feature mismatch
if set(features.columns) != set(self.FEATURES_COLS):
    raise ValueError("Feature columns do not match training data")
```

#### Edge Cases
- **Single row prediction**: Handle DataFrame with one row
- **Duplicate columns**: Ensure no duplicate feature names
- **NaN values**: Handle or fill appropriately
- **Unknown categories**: Handle unseen airlines/months

### Performance Optimization Strategies

#### Memory Optimization
- Use efficient data types (category for categorical variables)
- Drop unnecessary columns early
- Avoid copying large DataFrames

#### Computation Optimization
- Vectorized operations with pandas/numpy
- Efficient one-hot encoding
- Minimal model complexity

#### Code Optimization
- Precompute feature mappings
- Cache model state
- Avoid redundant computations

## Implementation Strategy

### Development Phases

#### Phase 1: Basic Structure
1. Implement class skeleton with required methods
2. Add basic input validation
3. Create placeholder implementations

#### Phase 2: Preprocessing
1. Implement date processing
2. Add one-hot encoding
3. Implement feature selection
4. Test with sample data

#### Phase 3: Model Training
1. Implement Logistic Regression training
2. Add class balancing
3. Store model properly
4. Validate training works

#### Phase 4: Prediction
1. Implement prediction method
2. Add validation checks
3. Ensure correct output format
4. Test end-to-end

#### Phase 5: Testing and Refinement
1. Run all unit tests
2. Fix any failing tests
3. Optimize performance
4. Add error handling

### Risk Mitigation Approaches

#### Technical Risks
- **Feature Mismatch**: Validate feature names match tests exactly
- **Data Type Issues**: Ensure consistent data types throughout
- **Model Convergence**: Use appropriate max_iter and random_state

#### Compliance Risks
- **Test Failure**: Continuously test against provided test suite
- **Signature Changes**: Never modify method signatures
- **Feature Drift**: Use exactly the 10 features specified

#### Performance Risks
- **Memory Issues**: Process data efficiently
- **Training Time**: Use appropriate model complexity
- **Prediction Speed**: Optimize for fast inference

### Technology Choices Aligned with Constitution

#### Framework Selection
- **scikit-learn**: Approved framework for ML models
- **pandas**: Approved for data processing
- **numpy**: Implicit dependency for numerical operations

#### Design Patterns
- **Single Class Pattern**: Simple, meets challenge requirements
- **Immutable Features**: Feature set fixed by tests
- **Stateful Model**: Model stored as instance variable

### Integration and Testing Approach

#### Integration Points
- **Test Suite**: Must integrate with `tests/model/test_model.py`
- **Data Source**: Reads from `data/data.csv`
- **API Integration**: Model will be used by FastAPI endpoint

#### Testing Strategy
1. **Unit Tests**: Provided test suite must pass
2. **Integration Tests**: Test with real data
3. **Edge Case Tests**: Handle unusual inputs
4. **Performance Tests**: Ensure reasonable speed

#### Validation Approach
1. **Feature Validation**: Ensure exactly 10 features
2. **Type Validation**: Correct return types
3. **Shape Validation**: Correct DataFrame shapes
4. **Value Validation**: Binary predictions only

## Implementation Notes

### Constants and Configuration
```python
class DelayModel:
    REQUIRED_COLUMNS = ['Fecha-I', 'Fecha-O', 'OPERA', 'MES', 'TIPOVUELO']
    FEATURES_COLS = [
        "OPERA_Latin American Wings", "MES_7", "MES_10",
        "OPERA_Grupo LATAM", "MES_12", "TIPOVUELO_I",
        "MES_4", "MES_11", "OPERA_Sky Airline", "OPERA_Copa Air"
    ]
    TARGET_COL = "delay"
    DELAY_THRESHOLD = 15  # minutes
```

### Dependencies
- pandas: Data manipulation
- scikit-learn: Logistic Regression
- typing: Type hints
- No external dependencies beyond requirements.txt

### Performance Considerations
- One-hot encoding creates sparse features
- Class balancing affects training time
- Memory usage scales with data size