# API Testing Commands

## Quick Setup

1. **Start the API server:**
```bash
uv run uvicorn challenge.api:app --reload --host 0.0.0.0 --port 8000
```


2. **Test in another terminal** (while server is running):

## Health Check

```bash
curl -X GET "http://localhost:8000/health" | jq
```

Expected response:
```json
{
  "status": "OK",
  "model_loaded": false,
  "model_version": null,
  "timestamp": "2026-08-14T18:24:51.370000"
}
```

## Prediction Request

### Valid Flight Data
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "OPERA": "Aerolineas Argentinas",
        "TIPOVUELO": "N",
        "MES": 3
      },
      {
        "OPERA": "Grupo LATAM",
        "TIPOVUELO": "I", 
        "MES": 7
      }
    ]
  }' | jq
```

Expected response:
```json
{
  "predict": [0, 0]
}
```

### Invalid Data (should return 400)
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "flights": [
      {
        "OPERA": "Invalid Airline",
        "TIPOVUELO": "X",
        "MES": 13
      }
    ]
  }' | jq
```

Expected response (400 error):
```json
{
  "detail": "Validation Error"
}
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Using Python Requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Prediction
flight_data = {
    "flights": [
        {
            "OPERA": "Aerolineas Argentinas",
            "TIPOVUELO": "N",
            "MES": 3
        }
    ]
}

response = requests.post(
    "http://localhost:8000/predict",
    json=flight_data
)
print(response.json())
```

## Valid Airlines List

The API accepts these airline names:
- Aerolineas Argentinas
- Grupo LATAM
- Sky Airline
- Copa Air
- Latin American Wings
- American Airlines
- United Airlines
- Delta Air Lines
- Air Canada
- British Airways
- Lufthansa
- Air France
- KLM
- Iberia
- Avianca
- LATAM Airlines

## Flight Types
- `N` = National flight
- `I` = International flight

## Months
- Valid range: 1-12 (January to December)