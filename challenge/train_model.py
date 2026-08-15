#!/usr/bin/env python3
"""
Simple training script that uses the existing DelayModel class.
This script trains the model and saves it for the API to use.
"""

import pandas as pd
import joblib
from pathlib import Path
import sys

# Import using the same path the API uses
from challenge.model import DelayModel

def main():
    """Train the model using existing DelayModel class."""
    
    # Load the data
    print("Loading flight data...")
    df = pd.read_csv("data/data.csv")
    print(f"Loaded {len(df)} flights")
    
    # Initialize the model (using existing class)
    model = DelayModel()
    
    # Preprocess the data (using existing method)
    print("Preprocessing data...")
    features, target = model.preprocess(df, target_column="delay")
    
    # Train the model (using existing method)
    print("Training model...")
    model.fit(features, target)
    
    # Save the trained model
    print("Saving model...")
    Path("models").mkdir(exist_ok=True)
    joblib.dump(model, "models/delay_model.pkl")
    
    print("✅ Model training complete!")
    print(f"Model saved to: models/delay_model.pkl")
    
    # Test the model
    print("\nTesting model...")
    test_predictions = model.predict(features.head(5))
    print(f"Sample predictions: {test_predictions}")

if __name__ == "__main__":
    main()