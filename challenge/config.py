from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os


class APISettings(BaseSettings):
    """API configuration settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="API_",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Model configuration
    model_path: str = "models/delay_model.pkl"
    model_version: str = "1.0.0"
    
    # API configuration
    api_title: str = "Flight Delay Prediction API"
    api_description: str = "API for predicting flight delays using ML model"
    api_version: str = "1.0.0"
    
    # Performance settings
    max_batch_size: int = 1000
    request_timeout: int = 30
    
    # Logging configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Environment settings
    environment: str = "development"
    debug: bool = False
    
    # CORS settings
    cors_origins: list = ["*"]
    cors_methods: list = ["GET", "POST"]
    cors_headers: list = ["*"]


class ModelSettings(BaseSettings):
    """Model-specific configuration settings."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_prefix="MODEL_",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Feature columns (must match model training)
    feature_columns: list = [
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
    
    # Valid airlines for validation
    valid_airlines: list = [
        "Aerolineas Argentinas", "Grupo LATAM", "Sky Airline", "Copa Air",
        "Latin American Wings", "American Airlines", "United Airlines",
        "Delta Air Lines", "Air Canada", "British Airways", "Lufthansa",
        "Air France", "KLM", "Iberia", "Avianca", "LATAM Airlines"
    ]
    
    # Prediction settings
    delay_threshold: int = 15  # minutes
    prediction_threshold: float = 0.5  # probability threshold for binary classification


# Global settings instances
api_settings = APISettings()
model_settings = ModelSettings()


def get_settings() -> tuple[APISettings, ModelSettings]:
    """Get API and model settings instances."""
    return api_settings, model_settings


def is_development() -> bool:
    """Check if running in development environment."""
    return api_settings.environment.lower() == "development"


def is_production() -> bool:
    """Check if running in production environment."""
    return api_settings.environment.lower() == "production"