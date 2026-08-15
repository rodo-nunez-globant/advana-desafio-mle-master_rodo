from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class FlightData(BaseModel):
    """Schema for individual flight data with validation."""
    
    OPERA: str = Field(..., description="Airline name")
    TIPOVUELO: str = Field(..., description="Flight type (N=National, I=International)")
    MES: int = Field(..., ge=1, le=12, description="Month number (1-12)")
    
    @field_validator('OPERA')
    @classmethod
    def validate_airline(cls, v):
        """Validate airline name against known airlines."""
        valid_airlines = [
            "Aerolineas Argentinas", "Grupo LATAM", "Sky Airline", "Copa Air",
            "Latin American Wings", "American Airlines", "United Airlines",
            "Delta Air Lines", "Air Canada", "British Airways", "Lufthansa",
            "Air France", "KLM", "Iberia", "Avianca", "LATAM Airlines"
        ]
        if v not in valid_airlines:
            raise ValueError(
                f"Invalid airline: {v}. Valid airlines are: {', '.join(valid_airlines)}"
            )
        return v
    
    @field_validator('TIPOVUELO')
    @classmethod
    def validate_flight_type(cls, v):
        """Validate flight type is either N (National) or I (International)."""
        if v not in ['N', 'I']:
            raise ValueError("Flight type must be 'N' (National) or 'I' (International)")
        return v


class PredictionRequest(BaseModel):
    """Schema for prediction request with batch flight data."""
    
    flights: List[FlightData] = Field(..., max_length=1000, description="List of flights to predict")
    
    @field_validator('flights')
    @classmethod
    def validate_flights_not_empty(cls, v):
        """Validate that flights list is not empty."""
        if not v:
            raise ValueError("Flights list cannot be empty")
        return v


class PredictionMetadata(BaseModel):
    """Schema for prediction response metadata."""
    
    model_version: str = Field(..., description="Model version used for prediction")
    predictions_count: int = Field(..., description="Number of predictions made")
    timestamp: datetime = Field(..., description="Prediction timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class PredictionResponse(BaseModel):
    """Schema for prediction response with predictions and optional metadata."""
    
    predict: List[int] = Field(..., description="List of delay predictions (0=no delay, 1=delay)")
    metadata: Optional[PredictionMetadata] = Field(None, description="Optional prediction metadata")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_version: Optional[str] = Field(None, description="Model version if loaded")
    timestamp: str = Field(..., description="Current timestamp")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    detail: dict = Field(..., description="Error details with message and context")