"""Additional tests to achieve 100% coverage for DelayModel"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from challenge.model import DelayModel


class TestModelCoverage:
    """Test edge cases and error paths for complete coverage"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.model = DelayModel()
        
        # Create minimal test data
        self.test_data = pd.DataFrame({
            'Fecha-I': ['2017-01-01 10:00:00'] * 10,
            'Fecha-O': ['2017-01-01 10:30:00'] * 10,
            'OPERA': ['Grupo LATAM'] * 5 + ['Sky Airline'] * 5,
            'MES': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'TIPOVUELO': ['I'] * 5 + ['N'] * 5,
            'Vlo-I': ['100'] * 10,
            'Vlo-O': ['100'] * 10
        })
        
        # Add required airlines and months for features
        extended_data = []
        for i, airline in enumerate(['Latin American Wings', 'Grupo LATAM', 'Sky Airline', 'Copa Air']):
            for month in [4, 7, 10, 11, 12]:
                for flight_type in ['I', 'N']:
                    # Create some flights with delays and some without
                    if i % 2 == 0:
                        # Delayed flight (30 min difference)
                        extended_data.append({
                            'Fecha-I': f'2017-{month:02d}-01 10:00:00',
                            'Fecha-O': f'2017-{month:02d}-01 10:30:00',
                            'OPERA': airline,
                            'MES': month,
                            'TIPOVUELO': flight_type,
                            'Vlo-I': '100',
                            'Vlo-O': '100'
                        })
                    else:
                        # Non-delayed flight (5 min difference)
                        extended_data.append({
                            'Fecha-I': f'2017-{month:02d}-01 10:00:00',
                            'Fecha-O': f'2017-{month:02d}-01 10:05:00',
                            'OPERA': airline,
                            'MES': month,
                            'TIPOVUELO': flight_type,
                            'Vlo-I': '100',
                            'Vlo-O': '100'
                        })
        self.full_test_data = pd.DataFrame(extended_data)
    
    def test_preprocess_empty_dataframe(self):
        """Test preprocess with empty dataframe"""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="Input data is empty"):
            self.model.preprocess(data=empty_df)
    
    def test_preprocess_missing_columns(self):
        """Test preprocess with missing required columns"""
        incomplete_data = pd.DataFrame({
            'Fecha-I': ['2017-01-01 10:00:00'],
            'Fecha-O': ['2017-01-01 10:30:00']
            # Missing OPERA, MES, TIPOVUELO
        })
        with pytest.raises(ValueError, match="Missing required columns"):
            self.model.preprocess(data=incomplete_data)
    
    def test_preprocess_invalid_date_format(self):
        """Test preprocess with invalid date format"""
        invalid_data = pd.DataFrame({
            'Fecha-I': ['invalid-date'],
            'Fecha-O': ['2017-01-01 10:30:00'],
            'OPERA': ['Grupo LATAM'],
            'MES': [1],
            'TIPOVUELO': ['I']
        })
        with pytest.raises(ValueError, match="Error parsing date columns"):
            self.model.preprocess(data=invalid_data)
    
    def test_preprocess_invalid_target_column(self):
        """Test preprocess with invalid target column name"""
        with pytest.raises(ValueError, match="Invalid target_column"):
            self.model.preprocess(data=self.full_test_data, target_column="invalid_target")
    
    def test_preprocess_missing_features(self):
        """Test preprocess when data doesn't contain all required feature categories"""
        # Data with only one airline and month - will miss required features
        limited_data = pd.DataFrame({
            'Fecha-I': ['2017-01-01 10:00:00'],
            'Fecha-O': ['2017-01-01 10:30:00'],
            'OPERA': ['Unknown Airline'],  # Not in required features
            'MES': [1],  # Not in required months
            'TIPOVUELO': ['I']
        })
        with pytest.raises(ValueError, match="Missing required feature columns"):
            self.model.preprocess(data=limited_data)
    
    def test_fit_empty_features(self):
        """Test fit with empty features dataframe"""
        empty_features = pd.DataFrame()
        target = pd.DataFrame({'delay': [0, 1]})
        with pytest.raises(ValueError, match="Features dataframe is empty"):
            self.model.fit(features=empty_features, target=target)
    
    def test_fit_empty_target(self):
        """Test fit with empty target dataframe"""
        features = pd.DataFrame({'feature1': [1, 2]})
        empty_target = pd.DataFrame()
        with pytest.raises(ValueError, match="Target dataframe is empty"):
            self.model.fit(features=features, target=empty_target)
    
    def test_fit_mismatched_lengths(self):
        """Test fit with features and target of different lengths"""
        features = pd.DataFrame({'feature1': [1, 2]})
        target = pd.DataFrame({'delay': [0]})  # Different length
        with pytest.raises(ValueError, match="Features and target must have the same length"):
            self.model.fit(features=features, target=target)
    
    def test_predict_model_not_trained(self):
        """Test predict when model is not yet trained"""
        features = pd.DataFrame({'feature1': [1, 2]})
        with pytest.raises(ValueError, match="Model must be trained before making predictions"):
            self.model.predict(features=features)
    
    def test_predict_empty_features(self):
        """Test predict with empty features dataframe"""
        # First train the model
        features, target = self.model.preprocess(data=self.full_test_data, target_column="delay")
        self.model.fit(features, target)
        
        # Then try to predict with empty features
        empty_features = pd.DataFrame()
        with pytest.raises(ValueError, match="Features dataframe is empty"):
            self.model.predict(features=empty_features)
    
    def test_predict_feature_mismatch(self):
        """Test predict with features that don't match training columns"""
        # First train the model
        features, target = self.model.preprocess(data=self.full_test_data, target_column="delay")
        self.model.fit(features, target)
        
        # Try to predict with wrong features
        wrong_features = pd.DataFrame({'wrong_feature': [1, 2]})
        with pytest.raises(ValueError, match="Feature columns do not match training data"):
            self.model.predict(features=wrong_features)
    
    def test_main_block_execution(self):
        """Test the if __name__ == '__main__' block"""
        # Import the module and run the main block directly
        import subprocess
        import sys
        
        # Run the model.py script as a subprocess
        result = subprocess.run(
            [sys.executable, 'challenge/model.py'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        
        # Check that it ran without errors
        assert result.returncode == 0
        assert "Starting Flight Delay Prediction Pipeline" in result.stdout
        assert "Pipeline completed successfully" in result.stdout