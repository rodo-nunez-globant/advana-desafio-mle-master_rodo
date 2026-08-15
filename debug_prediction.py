#!/usr/bin/env python3
"""
Debug script to explore the trained model and make predictions.
Run this with your debugger to step through the process.
"""

import pandas as pd
import joblib
import sys
from pathlib import Path

# Add the challenge directory to the path
sys.path.append(str(Path(__file__).parent / 'challenge'))

from model import DelayModel

def explore_trained_model():
    """Explore the trained model structure."""
    print("=" * 60)
    print("🔍 EXPLORING TRAINED MODEL")
    print("=" * 60)
    
    # Load the trained model
    model_path = "models/delay_model.pkl"
    if not Path(model_path).exists():
        print(f"❌ Model not found at {model_path}")
        print("Run: uv run python challenge/train_model.py")
        return None
    
    model = joblib.load(model_path)
    
    print(f"✅ Model loaded from {model_path}")
    print(f"   Model type: {type(model)}")
    print(f"   Trained model: {type(model._model)}")
    print(f"   Model trained: {model._model is not None}")
    
    if model._model is not None:
        print(f"   Expected features: {model._model.n_features_in_}")
        print(f"   Feature names: {list(model._model.feature_names_in_)}")
        print(f"   Classes: {model._model.classes_}")
        print(f"   Coefficients shape: {model._model.coef_.shape}")
    
    print(f"\n   Required columns for training: {model._required_columns}")
    print(f"   Feature columns: {model._features_cols}")
    print(f"   Target column: {model._target_col}")
    print(f"   Delay threshold: {model._delay_threshold} minutes")
    
    return model

def test_prediction_scenarios(model):
    """Test different prediction scenarios."""
    print("\n" + "=" * 60)
    print("🧪 TESTING PREDICTION SCENARIOS")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "name": "Known airline - Grupo LATAM",
            "data": {
                "OPERA": ["Grupo LATAM"],
                "MES": [7],
                "TIPOVUELO": ["I"]
            }
        },
        {
            "name": "Known airline - Sky Airline",
            "data": {
                "OPERA": ["Sky Airline"],
                "MES": [12],
                "TIPOVUELO": ["N"]
            }
        },
        {
            "name": "Unknown airline - American Airlines",
            "data": {
                "OPERA": ["American Airlines"],
                "MES": [3],
                "TIPOVUELO": ["N"]
            }
        },
        {
            "name": "Multiple flights batch",
            "data": {
                "OPERA": ["Grupo LATAM", "Sky Airline", "Copa Air"],
                "MES": [7, 12, 10],
                "TIPOVUELO": ["I", "N", "I"]
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        
        # Create DataFrame
        df = pd.DataFrame(test_case['data'])
        print(f"Input data:\n{df}")
        
        # Step 1: Preprocess
        print("\n📊 Step 1: Preprocessing...")
        try:
            features = model.preprocess(df)
            print(f"✅ Preprocessing successful")
            print(f"   Features shape: {features.shape}")
            print(f"   Features columns: {list(features.columns)}")
            print(f"   Features values:\n{features}")
        except Exception as e:
            print(f"❌ Preprocessing failed: {e}")
            continue
        
        # Step 2: Predict
        print("\n🔮 Step 2: Making prediction...")
        try:
            predictions = model.predict(features)
            print(f"✅ Prediction successful")
            print(f"   Predictions: {predictions}")
            
            # Interpret predictions
            for j, pred in enumerate(predictions):
                status = "🔴 DELAY (>15 min)" if pred == 1 else "🟢 ON-TIME"
                print(f"   Flight {j+1}: {status}")
                
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            continue
        
        # Step 3: Show model internals (if available)
        if model._model is not None:
            print("\n🔬 Step 3: Model internals...")
            try:
                # Get probability predictions
                if hasattr(model._model, 'predict_proba'):
                    probabilities = model._model.predict_proba(features)
                    print(f"   Probabilities: {probabilities}")
                    print(f"   Delay probability: {probabilities[:, 1]}")
                
                # Show feature contributions
                if hasattr(model._model, 'coef_'):
                    coef_df = pd.DataFrame({
                        'feature': features.columns,
                        'coefficient': model._model.coef_[0]
                    })
                    print(f"   Top features contributing to delay:")
                    top_features = coef_df.reindex(
                        coef_df['coefficient'].abs().sort_values(ascending=False).index
                    ).head(5)
                    for _, row in top_features.iterrows():
                        sign = "➕" if row['coefficient'] > 0 else "➖"
                        print(f"     {sign} {row['feature']}: {row['coefficient']:.4f}")
                        
            except Exception as e:
                print(f"   Could not access model internals: {e}")

def compare_with_training_data(model):
    """Compare prediction features with training data features."""
    print("\n" + "=" * 60)
    print("📈 COMPARING WITH TRAINING DATA")
    print("=" * 60)
    
    # Load a sample of training data
    try:
        df_train = pd.read_csv("data/data.csv", nrows=100)
        print(f"Loaded {len(df_train)} sample training rows")
        
        # Preprocess training data
        features_train, target_train = model.preprocess(df_train, target_column="delay")
        print(f"Training features shape: {features_train.shape}")
        print(f"Training target distribution: {target_train['delay'].value_counts().to_dict()}")
        
        # Compare with a prediction
        df_pred = pd.DataFrame({
            "OPERA": ["Grupo LATAM"],
            "MES": [7],
            "TIPOVUELO": ["I"]
        })
        features_pred = model.preprocess(df_pred)
        
        print(f"\nPrediction features shape: {features_pred.shape}")
        print(f"Feature columns match: {list(features_train.columns) == list(features_pred.columns)}")
        
        # Show feature comparison
        print(f"\nFeature comparison (first 5 features):")
        for col in list(features_train.columns)[:5]:
            train_val = features_train[col].iloc[0] if len(features_train) > 0 else "N/A"
            pred_val = features_pred[col].iloc[0]
            print(f"  {col}: train={train_val}, pred={pred_val}")
            
    except Exception as e:
        print(f"❌ Could not compare with training data: {e}")

def main():
    """Main debug function."""
    print("🐛 MODEL PREDICTION DEBUG SCRIPT")
    print("Run this with your debugger to explore step by step")
    print("\nBreakpoints you might want to set:")
    print("  - Line ~75: After preprocessing to see features")
    print("  - Line ~85: After prediction to see results")
    print("  - Line ~95: To explore model internals")
    
    # Load and explore model
    model = explore_trained_model()
    if model is None:
        return
    
    # Test predictions
    test_prediction_scenarios(model)
    
    # Compare with training data
    compare_with_training_data(model)
    
    print("\n" + "=" * 60)
    print("✅ Debug exploration complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()