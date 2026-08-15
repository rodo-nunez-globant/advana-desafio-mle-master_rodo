# FastAPI Deployment Design

## Architecture Overview

### API Architecture
```
FastAPI Application
├── Startup Lifecycle
│   ├── Load Configuration
│   ├── Initialize DelayModel
│   ├── Load Pre-trained Model
│   └── Health Check Ready
├── Request Processing
│   ├── Pydantic Validation
│   ├── Data Preprocessing
│   ├── Model Prediction
│   └── Response Enhancement
└── Error Handling
    ├── Input Validation Errors
    ├── Model Prediction Errors
    └── System Errors
```

### Component Relationships
- **FastAPI**: Web framework and routing
- **Pydantic**: Request/response validation and serialization
- **DelayModel**: Machine learning model integration
- **Configuration**: Environment and model management
- **Logging**: Audit trail and monitoring

## Detailed Design

### API Application Structure

#### Main Application (api.py)
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from challenge.model import DelayModel
from challenge.schemas import PredictionRequest, PredictionResponse
import logging

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API for predicting flight delays using ML model",
    version="1.0.0"
)

# Global model instance
model = DelayModel()

@app.on_event("startup")
async def startup_event():
    # Load pre-trained model
    pass

@app.get("/health")
async def health_check():
    # Enhanced health check with model status
    pass

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Main prediction endpoint
    pass
```

#### Pydantic Schemas (schemas.py)
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class FlightData(BaseModel):
    OPERA: str = Field(..., description="Airline name")
    TIPOVUELO: str = Field(..., description="Flight type (N/I)")
    MES: int = Field(..., ge=1, le=12, description="Month number")
    
    @validator('OPERA')
    def validate_airline(cls, v):
        valid_airlines = [...]  # From training data
        if v not in valid_airlines:
            raise ValueError(f"Invalid airline: {v}")
        return v
    
    @validator('TIPOVUELO')
    def validate_flight_type(cls, v):
        if v not in ['N', 'I']:
            raise ValueError("Flight type must be 'N' or 'I'")
        return v

class PredictionRequest(BaseModel):
    flights: List[FlightData] = Field(..., max_items=1000)
    
    @validator('flights')
    def validate_flights_not_empty(cls, v):
        if not v:
            raise ValueError("Flights list cannot be empty")
        return v

class PredictionMetadata(BaseModel):
    model_version: str
    predictions_count: int
    timestamp: datetime
    processing_time_ms: float

class PredictionResponse(BaseModel):
    predict: List[int]
    metadata: Optional[PredictionMetadata] = None
```

#### Configuration Management (config.py)
```python
from pydantic import BaseSettings
from typing import Optional

class APISettings(BaseSettings):
    model_path: str = "models/delay_model.pkl"
    model_version: str = "1.0.0"
    log_level: str = "INFO"
    max_batch_size: int = 1000
    
    class Config:
        env_file = ".env"
        env_prefix = "API_"

settings = APISettings()
```

### Model Integration Strategy

#### Pre-trained Model Approach
```python
import joblib
import os
from pathlib import Path

class ModelManager:
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model = None
        self.model_version = None
        
    def load_model(self):
        """Load pre-trained model from file"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        try:
            self.model = joblib.load(self.model_path)
            self.model_version = self._extract_model_version()
            logging.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise
            
    def _extract_model_version(self) -> str:
        """Extract model version from model metadata"""
        # Implementation depends on model saving format
        return "1.0.0"
```

#### Prediction Pipeline
```python
import pandas as pd
import time
from typing import List

class PredictionService:
    def __init__(self, model: DelayModel):
        self.model = model
        
    def predict_flights(self, flights_data: List[dict]) -> tuple:
        """Process flight predictions with timing"""
        start_time = time.time()
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(flights_data)
            
            # Preprocess features
            features = self.model.preprocess(df)
            
            # Make predictions
            predictions = self.model.predict(features)
            
            # Calculate processing time
            processing_time = (time.time() - start_time) * 1000
            
            return predictions, processing_time
            
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise
```

### Error Handling Design

#### Error Response Structure
```python
from fastapi import HTTPException
from typing import Dict, Any

class APIError(Exception):
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

def create_error_response(
    error_type: str,
    message: str,
    field: str = None,
    value: Any = None,
    valid_values: List[str] = None
) -> Dict[str, Any]:
    """Create standardized error response"""
    error_detail = {
        "error": error_type,
        "message": message
    }
    
    if field:
        error_detail["field"] = field
    if value is not None:
        error_detail["value"] = value
    if valid_values:
        error_detail["valid_values"] = valid_values
        
    return {"detail": error_detail}
```

#### Exception Handlers
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=400,
        content=create_error_response(
            "Validation Error",
            exc.message,
            exc.field,
            exc.value
        )
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=create_error_response(
            "Value Error",
            str(exc)
        )
    )
```

### Performance Optimization

#### Request Processing Optimization
```python
from functools import lru_cache
import asyncio

class OptimizedPredictionService:
    def __init__(self, model: DelayModel):
        self.model = model
        self._prediction_cache = {}
        
    @lru_cache(maxsize=128)
    def _get_valid_airlines(self) -> tuple:
        """Cache valid airlines list"""
        # Return tuple for hashability
        return tuple(self.model.get_valid_airlines())
    
    async def predict_batch_async(self, flights: List[FlightData]) -> List[int]:
        """Async batch prediction for better performance"""
        # Process in chunks if batch is large
        chunk_size = 100
        if len(flights) <= chunk_size:
            return await self._predict_chunk(flights)
        
        # Process chunks concurrently
        chunks = [flights[i:i+chunk_size] for i in range(0, len(flights), chunk_size)]
        results = await asyncio.gather(*[
            self._predict_chunk(chunk) for chunk in chunks
        ])
        return [pred for chunk_result in results for pred in chunk_result]
```

### Monitoring and Logging

#### Structured Logging
```python
import structlog
from datetime import datetime

logger = structlog.get_logger()

class RequestLogger:
    def __init__(self):
        self.logger = logger
        
    def log_request(self, request_data: dict, response_data: dict, processing_time: float):
        """Log prediction request with structured data"""
        self.logger.info(
            "prediction_request",
            timestamp=datetime.utcnow().isoformat(),
            request_size=len(request_data.get('flights', [])),
            prediction_count=len(response_data.get('predict', [])),
            processing_time_ms=processing_time,
            model_version=response_data.get('metadata', {}).get('model_version')
        )
```

#### Health Check Enhancement
```python
@app.get("/health")
async def health_check():
    """Enhanced health check with detailed status"""
    try:
        model_status = {
            "loaded": model._model is not None,
            "version": model.model_version if hasattr(model, 'model_version') else None,
            "features_count": len(model._features_cols) if hasattr(model, '_features_cols') else None
        }
        
        return {
            "status": "OK",
            "timestamp": datetime.utcnow().isoformat(),
            "model": model_status,
            "api": {
                "version": "1.0.0",
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
```

## Implementation Strategy

### Development Phases

#### Phase 1: Core API Implementation (Priority 1)
1. Create Pydantic schemas for request/response validation
2. Implement basic FastAPI application structure
3. Integrate DelayModel with pre-trained model loading
4. Implement prediction endpoint with basic functionality
5. Add enhanced health check endpoint

#### Phase 2: Validation and Error Handling (Priority 1)
1. Implement comprehensive input validation
2. Add detailed error responses
3. Create exception handlers
4. Add request/response logging
5. Ensure backward compatibility with tests

#### Phase 3: Performance and Monitoring (Priority 2)
1. Optimize prediction performance
2. Add structured logging
3. Implement request timing
4. Add model status monitoring
5. Performance testing and optimization

#### Phase 4: Production Readiness (Priority 3)
1. Add configuration management
2. Implement rate limiting considerations
3. Add API documentation
4. Security hardening
5. Load testing

### Risk Mitigation

#### Technical Risks
- **Model Loading Failures**: Graceful degradation and retry logic
- **Performance Issues**: Async processing and caching strategies
- **Memory Leaks**: Proper resource management and monitoring

#### Integration Risks
- **Test Compatibility**: Maintain exact test response format
- **Model Versioning**: Clear version management strategy
- **Configuration**: Environment-specific configuration management

### Technology Choices

#### FastAPI
- **Rationale**: Required by challenge, high performance, automatic documentation
- **Benefits**: Type hints, automatic validation, async support
- **Features Used**: Pydantic integration, dependency injection, middleware

#### Pydantic
- **Rationale**: Built-in FastAPI integration, robust validation
- **Benefits**: Type safety, automatic error messages, performance
- **Implementation**: Request/response models, validation logic

#### Structured Logging
- **Choice**: structlog library for structured JSON logging
- **Rationale**: Better observability and debugging capabilities
- **Benefits**: Searchable logs, correlation IDs, performance metrics