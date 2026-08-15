#!/usr/bin/env python3
"""
Test the API with the full dataset using batch processing.
Validates that predictions have a reasonable distribution of delays (1s) and on-time (0s).
"""

import pandas as pd
import requests
import json
import time
from datetime import datetime
import numpy as np
from pathlib import Path
import sys

# Add the challenge directory to the path (from sandbox folder)
sys.path.append(str(Path(__file__).parent.parent / 'challenge'))

from model import DelayModel

def load_and_prepare_test_data():
    """Load the full dataset and prepare it for batch testing."""
    print("📊 Loading and preparing test data...")
    
    # Load the full dataset (from sandbox folder)
    df = pd.read_csv("../data/data.csv")
    print(f"   Loaded {len(df):,} flights")
    
    # Filter to only airlines that the model knows
    known_airlines = ['Latin American Wings', 'Grupo LATAM', 'Sky Airline', 'Copa Air']
    df_filtered = df[df['OPERA'].isin(known_airlines)].copy()
    print(f"   Filtered to {len(df_filtered):,} flights with known airlines")
    
    # Create a sample for batch testing (use a subset for faster testing)
    # You can change this to use the full dataset
    sample_size = min(5000, len(df_filtered))  # Use 5000 or all if less
    df_sample = df_filtered.sample(n=sample_size, random_state=42).reset_index(drop=True)
    
    print(f"   Using sample of {len(df_sample):,} flights for testing")
    
    # Prepare data for API (only need OPERA, MES, TIPOVUELO)
    batch_data = []
    for _, row in df_sample.iterrows():
        batch_data.append({
            "OPERA": row["OPERA"],
            "MES": int(row["MES"]),  # Convert to Python int to avoid JSON serialization issues
            "TIPOVUELO": row["TIPOVUELO"]
        })
    
    return df_sample, batch_data

def test_direct_model_predictions(df_sample):
    """Test predictions directly using the model (bypass API)."""
    print("\n🔬 Testing direct model predictions...")
    
    # Load the trained model
    import joblib
    model = joblib.load("../models/delay_model.pkl")
    
    # Prepare data for model
    model_data = df_sample[["OPERA", "MES", "TIPOVUELO"]].copy()
    
    # Make predictions
    start_time = time.time()
    features = model.preprocess(model_data)
    predictions = model.predict(features)
    prediction_time = time.time() - start_time
    
    # Calculate distribution
    predictions = np.array(predictions)
    delay_count = np.sum(predictions == 1)
    ontime_count = np.sum(predictions == 0)
    delay_rate = delay_count / len(predictions)
    
    print(f"   ✅ Direct model predictions completed in {prediction_time:.3f}s")
    print(f"   Total predictions: {len(predictions):,}")
    print(f"   Delays (1s): {delay_count:,} ({delay_rate:.1%})")
    print(f"   On-time (0s): {ontime_count:,} ({1-delay_rate:.1%})")
    
    return predictions, delay_rate

def test_api_batch_predictions(batch_data, batch_size=100):
    """Test predictions through the API with batch processing."""
    print(f"\n🌐 Testing API batch predictions (batch size: {batch_size})...")
    
    base_url = "http://localhost:8000"
    
    # Check if API is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code != 200:
            print("   ❌ API is not responding correctly")
            return None, None
    except requests.exceptions.RequestException:
        print("   ❌ API is not running. Start with: uv run uvicorn challenge.api:app --reload")
        return None, None
    
    # Process in batches
    all_predictions = []
    total_batches = (len(batch_data) + batch_size - 1) // batch_size
    
    start_time = time.time()
    
    for i in range(0, len(batch_data), batch_size):
        batch_num = i // batch_size + 1
        batch = batch_data[i:i + batch_size]
        
        print(f"   Processing batch {batch_num}/{total_batches} ({len(batch)} flights)...")
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                json={"flights": batch},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                batch_predictions = result.get("predict", [])
                all_predictions.extend(batch_predictions)
                
                # Show progress
                delay_count = sum(batch_predictions)
                print(f"      ✅ Batch {batch_num}: {delay_count}/{len(batch)} delays")
                
            else:
                print(f"      ❌ Batch {batch_num} failed: {response.status_code}")
                print(f"         Response: {response.text}")
                
        except Exception as e:
            print(f"      ❌ Batch {batch_num} error: {e}")
    
    total_time = time.time() - start_time
    
    if all_predictions:
        # Calculate distribution
        predictions = np.array(all_predictions)
        delay_count = np.sum(predictions == 1)
        ontime_count = np.sum(predictions == 0)
        delay_rate = delay_count / len(predictions)
        
        print(f"\n   ✅ API batch predictions completed in {total_time:.3f}s")
        print(f"   Total predictions: {len(predictions):,}")
        print(f"   Average time per prediction: {(total_time/len(predictions)*1000):.2f}ms")
        print(f"   Delays (1s): {delay_count:,} ({delay_rate:.1%})")
        print(f"   On-time (0s): {ontime_count:,} ({1-delay_rate:.1%})")
        
        return predictions, delay_rate
    else:
        print("   ❌ No successful predictions from API")
        return None, None

def compare_distributions(direct_preds, api_preds, df_sample):
    """Compare prediction distributions between direct model and API."""
    print("\n📊 Comparing prediction distributions...")
    
    if direct_preds is None or api_preds is None:
        print("   ❌ Cannot compare - missing predictions")
        return
    
    # Calculate actual delays from data (if available)
    if 'Fecha-I' in df_sample.columns and 'Fecha-O' in df_sample.columns:
        df_sample['Fecha-I'] = pd.to_datetime(df_sample['Fecha-I'])
        df_sample['Fecha-O'] = pd.to_datetime(df_sample['Fecha-O'])
        df_sample['min_diff'] = (df_sample['Fecha-O'] - df_sample['Fecha-I']).dt.total_seconds() / 60
        actual_delays = (df_sample['min_diff'] > 15).astype(int)
        actual_delay_rate = actual_delays.mean()
        
        print(f"   Actual delay rate (from data): {actual_delay_rate:.1%}")
    
    # Compare distributions
    direct_delay_rate = np.mean(direct_preds)
    api_delay_rate = np.mean(api_preds)
    
    print(f"   Direct model delay rate: {direct_delay_rate:.1%}")
    print(f"   API delay rate: {api_delay_rate:.1%}")
    
    # Check if predictions match
    if np.array_equal(direct_preds, api_preds):
        print("   ✅ API and direct model predictions are IDENTICAL")
    else:
        diff_count = np.sum(direct_preds != api_preds)
        diff_rate = diff_count / len(direct_preds)
        print(f"   ⚠️  Predictions differ: {diff_count:,} ({diff_rate:.1%}) cases")
        
        # Show some differences
        diff_indices = np.where(direct_preds != api_preds)[0][:5]  # First 5 differences
        for idx in diff_indices:
            print(f"      Index {idx}: direct={direct_preds[idx]}, api={api_preds[idx]}")

def analyze_by_categories(df_sample, predictions):
    """Analyze prediction rates by airline, month, and flight type."""
    print("\n📈 Analyzing predictions by categories...")
    
    df_analysis = df_sample.copy()
    df_analysis['prediction'] = predictions
    
    # By airline
    print("\n   By Airline:")
    airline_stats = df_analysis.groupby('OPERA')['prediction'].agg(['count', 'mean']).round(3)
    airline_stats.columns = ['flights', 'delay_rate']
    airline_stats = airline_stats.sort_values('delay_rate', ascending=False)
    for airline, stats in airline_stats.head(10).iterrows():
        print(f"      {airline:20s}: {int(stats['flights']):4d} flights, {stats['delay_rate']:.1%} delay rate")
    
    # By month
    print("\n   By Month:")
    month_stats = df_analysis.groupby('MES')['prediction'].agg(['count', 'mean']).round(3)
    month_stats.columns = ['flights', 'delay_rate']
    for month, stats in month_stats.iterrows():
        month_name = pd.to_datetime(month, format='%m').strftime('%B')
        print(f"      {month_name:10s}: {int(stats['flights']):4d} flights, {stats['delay_rate']:.1%} delay rate")
    
    # By flight type
    print("\n   By Flight Type:")
    type_stats = df_analysis.groupby('TIPOVUELO')['prediction'].agg(['count', 'mean']).round(3)
    type_stats.columns = ['flights', 'delay_rate']
    for flight_type, stats in type_stats.iterrows():
        type_name = "International" if flight_type == 'I' else "National"
        print(f"      {type_name:12s}: {int(stats['flights']):4d} flights, {stats['delay_rate']:.1%} delay rate")

def main():
    """Main test function."""
    print("🧪 BATCH PREDICTION VALIDATION TEST")
    print("=" * 60)
    print("This script tests the API with batch processing to validate")
    print("that predictions have a reasonable distribution of delays.")
    print("=" * 60)
    
    # Load test data
    df_sample, batch_data = load_and_prepare_test_data()
    
    # Test direct model predictions
    direct_preds, direct_rate = test_direct_model_predictions(df_sample)
    
    # Test API batch predictions
    api_preds, api_rate = test_api_batch_predictions(batch_data, batch_size=100)
    
    # Compare distributions
    compare_distributions(direct_preds, api_preds, df_sample)
    
    # Analyze by categories (using API predictions if available, otherwise direct)
    predictions_to_analyze = api_preds if api_preds is not None else direct_preds
    if predictions_to_analyze is not None:
        analyze_by_categories(df_sample, predictions_to_analyze)
    
    print("\n" + "=" * 60)
    print("✅ Batch prediction validation complete!")
    print("=" * 60)
    
    # Summary
    if api_rate is not None:
        print(f"\n📋 SUMMARY:")
        print(f"   API delay rate: {api_rate:.1%}")
        print(f"   Reasonable range: 10% - 30% (based on training data)")
        
        if 0.10 <= api_rate <= 0.30:
            print("   ✅ Delay rate is within reasonable range")
        else:
            print("   ⚠️  Delay rate may be unusual - investigate further")

if __name__ == "__main__":
    main()