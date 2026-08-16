#!/bin/bash

# Test script for Workload Identity configuration
# Run this after Terraform apply to verify the setup

set -e

echo "🔍 Testing Workload Identity Configuration"
echo "========================================"

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

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "")
if [ -z "$PROJECT_ID" ]; then
    print_error "No GCP project set. Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi
print_success "GCP project: $PROJECT_ID"

# Get Terraform outputs
echo ""
echo "📋 Getting Terraform outputs..."
cd terraform

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    print_error "terraform.tfvars not found. Please run terraform apply first."
    exit 1
fi

# Get outputs
SERVICE_ACCOUNT=$(terraform output -raw service_account_email 2>/dev/null || echo "")
WORKLOAD_IDENTITY_PROVIDER=$(terraform output -raw workload_identity_provider 2>/dev/null || echo "")

if [ -z "$SERVICE_ACCOUNT" ] || [ -z "$WORKLOAD_IDENTITY_PROVIDER" ]; then
    print_error "Could not get Terraform outputs. Please run terraform apply first."
    exit 1
fi

print_success "Service account: $SERVICE_ACCOUNT"
print_success "Workload identity provider: $WORKLOAD_IDENTITY_PROVIDER"

# Test 1: Check if service account exists
echo ""
echo "🔍 Test 1: Checking service account..."
if gcloud iam service-accounts describe "$SERVICE_ACCOUNT" --project="$PROJECT_ID" &>/dev/null; then
    print_success "Service account exists"
else
    print_error "Service account not found"
    exit 1
fi

# Test 2: Check workload identity pool
echo ""
echo "🔍 Test 2: Checking workload identity pool..."
POOL_ID=$(echo "$WORKLOAD_IDENTITY_PROVIDER" | cut -d'/' -f6)
if gcloud iam workload-identity-pools describe "$POOL_ID" --location=global --project="$PROJECT_ID" &>/dev/null; then
    print_success "Workload identity pool exists"
else
    print_error "Workload identity pool not found"
    exit 1
fi

# Test 3: Check workload identity provider
echo ""
echo "🔍 Test 3: Checking workload identity provider..."
PROVIDER_ID=$(echo "$WORKLOAD_IDENTITY_PROVIDER" | cut -d'/' -f8)
if gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
    --workload-identity-pool="$POOL_ID" --location=global --project="$PROJECT_ID" &>/dev/null; then
    print_success "Workload identity provider exists"
else
    print_error "Workload identity provider not found"
    exit 1
fi

# Test 4: Check IAM policy on service account
echo ""
echo "🔍 Test 4: Checking service account IAM policy..."
IAM_POLICY=$(gcloud iam service-accounts get-iam-policy "$SERVICE_ACCOUNT" \
    --project="$PROJECT_ID" --format=json 2>/dev/null)

if echo "$IAM_POLICY" | grep -q "roles/iam.workloadIdentityUser"; then
    print_success "Service account has workloadIdentityUser role"
else
    print_error "Service account missing workloadIdentityUser role"
    exit 1
fi

# Test 5: Try to impersonate the service account (requires gcloud auth login)
echo ""
echo "🔍 Test 5: Testing service account impersonation..."
echo "   (This requires you to be authenticated with gcloud)"
if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    if gcloud iam service-accounts impersonate-service-account "$SERVICE_ACCOUNT" \
        --project="$PROJECT_ID" -- \
        gcloud projects list --format="value(projectId)" | grep -q "$PROJECT_ID"; then
        print_success "Service account impersonation works"
    else
        print_error "Service account impersonation failed"
        exit 1
    fi
else
    print_warning "Skipping impersonation test - not authenticated with gcloud"
    echo "   Run 'gcloud auth login' to test impersonation"
fi

# Summary
echo ""
echo "🎉 All tests passed!"
echo ""
echo "Next steps:"
echo "1. Add these secrets to your GitHub repository:"
echo "   GCP_PROJECT_ID=$PROJECT_ID"
echo "   GCP_WORKLOAD_IDENTITY_PROVIDER=$WORKLOAD_IDENTITY_PROVIDER"
echo "   GCP_SERVICE_ACCOUNT_EMAIL=$SERVICE_ACCOUNT"
echo ""
echo "2. Configure GitHub repository permissions:"
echo "   Settings > Actions > General > Workflow permissions"
echo "   - Read and write permissions"
echo "   - Allow GitHub Actions to create and approve pull requests"
echo "   - Allow GitHub Actions to run approved pull requests from forks"