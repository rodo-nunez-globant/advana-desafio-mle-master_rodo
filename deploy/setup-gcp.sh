#!/bin/bash

# GCP Setup Script for Flight Delay Prediction API
# Sets up gcloud with the correct project and enables required APIs

set -e

PROJECT_ID="rodo-nunez-challenge-latam"
REGION="us-central1"

echo "🔧 Setting up GCP for Flight Delay Prediction API"
echo "=============================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not found"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Authenticate if not already authenticated
echo "🔐 Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "Please run: gcloud auth login"
    echo "And then: gcloud auth application-default login"
    exit 1
fi

echo "✅ Authentication OK"

# Set the project
echo "📋 Setting project..."
gcloud config set project $PROJECT_ID
echo "✅ Project set to: $PROJECT_ID"

# Enable required APIs
echo "📋 Enabling required GCP APIs..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com --project=$PROJECT_ID
echo "✅ APIs enabled"

# Show project info
echo ""
echo "📊 Project Information:"
gcloud projects describe $PROJECT_ID --format="table(projectId,projectNumber,createTime, lifecycleState)"

# Show available regions for Cloud Run
echo ""
echo "🌍 Available Cloud Run regions:"
gcloud run regions list --format="table(name)" --filter="name~us-"

echo ""
echo "✅ GCP setup complete!"
echo ""
echo "Next steps:"
echo "1. Test Docker locally: ./deploy/test-local.sh"
echo "2. Deploy to GCP: ./deploy/gcp-deploy.sh"
echo "3. Run stress tests: make stress-test"