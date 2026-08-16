#!/bin/bash

# Debug GCP Cloud Build
# This script helps debug what's happening during the GCP build

set -e

PROJECT_ID=${1:-rodo-nunez-challenge-latam}
SERVICE_NAME=${2:-flight-delay-api}

echo "🔍 Debugging GCP Cloud Build for $SERVICE_NAME"
echo "=========================================="
echo ""

# First, let's see what files are being sent to Cloud Build
echo "📦 Creating a tar archive to check what's being sent..."
tar -czf /tmp/build-context.tar.gz --exclude='.git' --exclude='.dockerignore' .
echo "✅ Build context created at /tmp/build-context.tar.gz"

# List the contents
echo ""
echo "📋 Contents of the build context:"
tar -tzf /tmp/build-context.tar.gz | head -20
echo "..."
echo ""

# Check if data directory is included
echo "🔍 Checking if data directory is in build context:"
if tar -tzf /tmp/build-context.tar.gz | grep -q "^data/"; then
    echo "✅ data/ directory found in build context"
    echo "Files in data/:"
    tar -tzf /tmp/build-context.tar.gz | grep "^data/" | head -10
else
    echo "❌ data/ directory NOT found in build context"
    echo "This might be excluded by .dockerignore"
fi

echo ""
echo "📄 .dockerignore contents:"
cat .dockerignore

echo ""
echo "💡 To manually test the Cloud Build locally:"
echo "docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:debug ."
echo "docker run --rm gcr.io/$PROJECT_ID/$SERVICE_NAME:debug ls -la data/"

# Clean up
rm -f /tmp/build-context.tar.gz