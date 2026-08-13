import pandas as pd
from sklearn.linear_model import LogisticRegression

from typing import Tuple, Union, List

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self._required_columns = [
            'Fecha-I',      # Scheduled datetime
            'Fecha-O',      # Operation datetime
            'OPERA',        # Airline name
            'MES',          # Month number
            'TIPOVUELO'     # Flight type
        ]
        self._features_cols = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        self._target_col = "delay"
        self._delay_threshold = 15  # minutes

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        # Input validation
        if data.empty:
            raise ValueError("Input data is empty")
        
        missing_columns = [col for col in self._required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Make a copy to avoid modifying original data
        data = data.copy()
        
        # Convert date columns to datetime
        try:
            data['Fecha-I'] = pd.to_datetime(data['Fecha-I'])
            data['Fecha-O'] = pd.to_datetime(data['Fecha-O'])
        except Exception as e:
            raise ValueError(f"Error parsing date columns: {e}")
        
        # Calculate min_diff in minutes
        data['min_diff'] = (data['Fecha-O'] - data['Fecha-I']).dt.total_seconds() / 60
        
        # Create target column if requested
        if target_column is not None:
            if target_column == self._target_col:
                data[self._target_col] = (data['min_diff'] > self._delay_threshold).astype(int)
            else:
                raise ValueError(f"Invalid target_column: {target_column}")
        
        # One-hot encode categorical variables
        # OPERA (airline)
        opera_dummies = pd.get_dummies(data['OPERA'], prefix='OPERA')
        
        # MES (month)
        mes_dummies = pd.get_dummies(data['MES'], prefix='MES')
        
        # TIPOVUELO (flight type)
        tipo_vuelo_dummies = pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO')
        
        # Combine all features
        features = pd.concat([opera_dummies, mes_dummies, tipo_vuelo_dummies], axis=1)
        
        # Select only the required features
        missing_features = [col for col in self._features_cols if col not in features.columns]
        if missing_features:
            # Add missing features as zeros
            for col in missing_features:
                features[col] = 0
        
        # Ensure consistent column order
        features = features[self._features_cols]
        
        # Return based on whether target was requested
        if target_column is not None:
            target = data[[self._target_col]]
            return features, target
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        # Input validation
        if features.empty:
            raise ValueError("Features dataframe is empty")
        if target.empty:
            raise ValueError("Target dataframe is empty")
        if len(features) != len(target):
            raise ValueError("Features and target must have the same length")
        
        # Initialize and train the model
        self._model = LogisticRegression(
            class_weight='balanced',
            random_state=42,
            max_iter=1000
        )
        
        # Fit the model
        self._model.fit(features, target.values.ravel())

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        # Check if model is trained
        if self._model is None:
            raise ValueError("Model must be trained before making predictions")
        
        # Input validation
        if features.empty:
            raise ValueError("Features dataframe is empty")
        
        # Check feature columns match training
        if set(features.columns) != set(self._features_cols):
            raise ValueError(f"Feature columns do not match training data. Expected: {self._features_cols}")
        
        # Make predictions
        predictions = self._model.predict(features)
        
        # Return as list of integers
        return predictions.tolist()

if __name__=="__main__":
    delay = DelayModel()
    