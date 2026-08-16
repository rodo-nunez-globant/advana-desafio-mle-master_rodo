#!/bin/bash

# Test the Docker container locally before deploying to GCP

set -e

echo "🐳 Testing Docker container locally"
echo "===================================="

# Build the image
echo "🔨 Building Docker image..."
docker build -t flight-delay-api:test .

# Run the container
echo "🚀 Starting container..."
docker run -d --name flight-delay-test -p 8080:8080 flight-delay-api:test

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 10

# Test health endpoint
echo "🧪 Testing health endpoint..."
curl -s http://localhost:8080/health | jq '.' || echo "Health check response"

# Test prediction endpoint
echo "🔮 Testing prediction endpoint..."
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"flights": [{"OPERA": "Grupo LATAM", "TIPOVUELO": "I", "MES": 7}]}' | jq '.' || echo "Prediction response"

# Clean up
echo "🧹 Cleaning up..."
docker stop flight-delay-test
docker rm flight-delay-test
docker rmi flight-delay-api:test

echo ""
echo "✅ Local test complete!"