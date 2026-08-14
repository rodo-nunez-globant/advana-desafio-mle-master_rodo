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
            raise ValueError(
                f"Missing required feature columns: {missing_features}. "
                f"Required features: {self._features_cols}. "
                f"This may be due to missing categories in the data. "
                f"Ensure your data contains all necessary airline (OPERA), month (MES), "
                f"and flight type (TIPOVUELO) combinations."
            )
        
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
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
    
    print("Starting Flight Delay Prediction Pipeline...")
    print("=" * 50)
    
    # Initialize model
    model = DelayModel()
    
    # Load data
    print("Loading data...")
    data = pd.read_csv(filepath_or_buffer="data/data.csv")
    print(f"Data shape: {data.shape}")
    
    # Preprocess data
    print("\nPreprocessing data...")
    features, target = model.preprocess(data=data, target_column="delay")
    print(f"Features shape: {features.shape}")
    print(f"Target shape: {target.shape}")
    print(f"Class distribution: {target.value_counts().to_dict()}")
    
    # Train model
    print("\nTraining model...")
    model.fit(features=features, target=target)
    print("Model trained successfully!")
    
    # Make predictions on training data (for demonstration)
    print("\nMaking predictions...")
    predictions = model.predict(features=features)
    
    # Evaluate model
    print("\nModel Evaluation:")
    print("-" * 30)
    print(f"Accuracy: {accuracy_score(target, predictions):.4f}")
    print("\nClassification Report:")
    print(classification_report(target, predictions))
    print("\nConfusion Matrix:")
    print(confusion_matrix(target, predictions))

    print("\nPipeline completed successfully!")
    