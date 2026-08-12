# Model Definition Modules

This directory contains model definitions, training logic, and model management.

## Expected Modules
- Model classes (XGBoost, Logistic Regression as per constitution)
- Training pipelines
- Model serialization/deserialization
- Model versioning utilities

Models should prioritize recall for delayed flights (F-3 score metric) and include SHAP for interpretability.