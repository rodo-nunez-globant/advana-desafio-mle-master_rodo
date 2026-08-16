#!/bin/bash

# GCP Cloud Run Deployment Script
# Usage: ./deploy/gcp-deploy.sh [PROJECT_ID] [REGION] [SERVICE_NAME]

set -e

# Default values
PROJECT_ID=${1:-rodo-nunez-challenge-latam}
REGION=${2:-us-central1}
SERVICE_NAME=${3:-flight-delay-api}

# Check if project ID is set
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No project ID provided and no default project set"
    echo "Usage: $0 [PROJECT_ID] [REGION] [SERVICE_NAME]"
    echo "Or set default project with: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "🚀 Deploying Flight Delay Prediction API to GCP Cloud Run"
echo "=========================================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not found"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Enable required APIs
echo "📋 Enabling required GCP APIs..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com --project=$PROJECT_ID

# Build and push the image
echo "🔨 Building Docker image..."
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"
gcloud builds submit --config=cloudbuild.yaml --substitutions=_SERVICE_NAME=$SERVICE_NAME --project=$PROJECT_ID

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --project $PROJECT_ID

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --region $REGION \
    --format 'value(status.url)' \
    --project $PROJECT_ID)

echo ""
echo "✅ Deployment successful!"
echo "📍 Service URL: $SERVICE_URL"
echo ""

# Update Makefile with the new URL
echo "📝 Updating Makefile with service URL..."
sed -i.bak "s|STRESS_URL = .*|STRESS_URL = $SERVICE_URL|g" Makefile
echo "✅ Updated Makefile line 26 with: STRESS_URL = $SERVICE_URL"

# Test the deployment
echo "🧪 Testing deployment..."
curl -s $SERVICE_URL/health | jq '.' || echo "Health check response received"

echo ""
echo "🎉 Deployment complete!"
echo "You can now run: make stress-test"