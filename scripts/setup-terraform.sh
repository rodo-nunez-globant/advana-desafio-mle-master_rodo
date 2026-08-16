#!/bin/bash

# Terraform Setup Script for Flight Delay Prediction API
# This script helps set up the Terraform infrastructure

set -e

echo "🚀 Terraform Setup for Flight Delay Prediction API"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo ""
echo "📋 Checking prerequisites..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi
print_success "gcloud CLI is installed"

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    print_error "Terraform is not installed. Please install it first:"
    echo "   https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli"
    exit 1
fi
print_success "Terraform is installed"

# Check if user is authenticated with gcloud
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_error "Not authenticated with gcloud. Please run:"
    echo "   gcloud auth login"
    exit 1
fi
print_success "Authenticated with gcloud"

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
if [ -z "$PROJECT_ID" ]; then
    print_error "No GCP project set. Please run:"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi
print_success "GCP project: $PROJECT_ID"

# Check if bucket exists
BUCKET_NAME="rodo-nunez-challenge-latam-data"
if ! gsutil ls "gs://$BUCKET_NAME" &> /dev/null; then
    print_warning "Bucket $BUCKET_NAME not found. Creating it..."
    gsutil mb -p $PROJECT_ID "gs://$BUCKET_NAME" || {
        print_error "Failed to create bucket. Please create it manually:"
        echo "   gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME"
        exit 1
    }
    print_success "Bucket created: gs://$BUCKET_NAME"
else
    print_success "Bucket exists: gs://$BUCKET_NAME"
fi

# Navigate to terraform directory
cd terraform

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    print_warning "terraform.tfvars not found. Creating from example..."
    cp terraform.tfvars.example terraform.tfvars
    
    # Update with current project
    sed -i.bak "s/project_id = \".*\"/project_id = \"$PROJECT_ID\"/" terraform.tfvars
    rm -f terraform.tfvars.bak
    
    print_warning "Please edit terraform.tfvars and update the github_repo value"
    echo "   Current value: $(grep github_repo terraform.tfvars)"
fi

# Initialize Terraform
echo ""
echo "🔧 Initializing Terraform..."
terraform init

# Validate configuration
echo ""
echo "✅ Validating Terraform configuration..."
terraform validate

# Show plan
echo ""
echo "📋 Showing execution plan..."
echo "   This will create the following resources:"
echo "   - Service account for GitHub Actions"
echo "   - Workload Identity Pool and Provider"
echo "   - IAM role bindings"
echo "   - Enable required GCP APIs"
echo ""
terraform plan

echo ""
echo "🎯 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review the plan above"
echo "2. If everything looks good, run:"
echo "   terraform apply"
echo ""
echo "3. After apply, get the GitHub secrets:"
echo "   terraform output github_secrets"
echo ""
echo "4. Add these secrets to your GitHub repository:"
echo "   - GCP_PROJECT_ID"
echo "   - GCP_WORKLOAD_IDENTITY_PROVIDER"
echo "   - GCP_SERVICE_ACCOUNT_EMAIL"
echo ""
echo "5. Configure GitHub repository permissions:"
echo "   Settings → Actions → General → Workflow permissions"
echo "   - Read and write permissions"
echo "   - Allow GitHub Actions to create and approve pull requests"
echo "   - Allow GitHub Actions to run approved pull requests from forks"