#!/usr/bin/env python3
"""
Simple debug script for stepping through predictions with a debugger.
Set breakpoints at the marked lines to explore the model.
"""

import pandas as pd
import joblib
import sys
from pathlib import Path

# Add the challenge directory to the path
sys.path.append(str(Path(__file__).parent / 'challenge'))

from model import DelayModel

def main():
    """Simple debug function with clear breakpoints."""
    
    # === BREAKPOINT 1: Model Loading ===
    # Load the trained model
    model = joblib.load("models/delay_model.pkl")
    print(f"Model loaded: {type(model._model)}")
    print(f"Expected features: {model._features_cols}")
    
    # Create test data
    test_data = pd.DataFrame({
        "OPERA": ["Grupo LATAM"],
        "MES": [7],
        "TIPOVUELO": ["I"]
    })
    print(f"\nTest data:\n{test_data}")
    
    # === BREAKPOINT 2: After Preprocessing ===
    # Preprocess the data
    features = model.preprocess(test_data)
    print(f"\nFeatures after preprocessing:")
    print(f"Shape: {features.shape}")
    print(f"Columns: {list(features.columns)}")
    print(f"Values:\n{features}")
    
    # === BREAKPOINT 3: Before Prediction ===
    # Check model state
    print(f"\nModel coefficients: {model._model.coef_}")
    print(f"Model intercept: {model._model.intercept_}")
    
    # === BREAKPOINT 4: After Prediction ===
    # Make prediction
    prediction = model.predict(features)
    print(f"\nPrediction: {prediction}")
    
    # Get probabilities if available
    if hasattr(model._model, 'predict_proba'):
        probabilities = model._model.predict_proba(features)
        print(f"Probabilities: {probabilities}")
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()