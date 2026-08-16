#!/bin/bash

# Terraform Validation Script
# This script validates the Terraform configuration

set -e

echo "🔍 Validating Terraform Configuration"
echo "===================================="

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install Terraform >= 1.5.0"
    exit 1
fi

# Check Terraform version
TERRAFORM_VERSION=$(terraform version -json | jq -r '.terraform_version')
REQUIRED_VERSION="1.5.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$TERRAFORM_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Terraform version $TERRAFORM_VERSION is too old. Required: >= $REQUIRED_VERSION"
    exit 1
fi

echo "✅ Terraform version: $TERRAFORM_VERSION"

# Initialize Terraform
echo ""
echo "📦 Initializing Terraform..."
terraform init -input=false

# Validate configuration
echo ""
echo "✅ Validating configuration..."
terraform validate

# Check formatting
echo ""
echo "📝 Checking formatting..."
if ! terraform fmt -check -recursive; then
    echo "❌ Code is not properly formatted. Run 'terraform fmt' to fix."
    exit 1
fi

echo "✅ Code is properly formatted"

# Plan (dry run)
echo ""
echo "📋 Planning changes (dry run)..."
terraform plan -out=tfplan

# Show plan summary
echo ""
echo "📊 Plan Summary:"
terraform show -json tfplan | jq -r '
  {
    "add": .planned_values.root_module.resources | map(select(.mode == "managed" and .actions == ["create"])) | length,
    "change": .planned_values.root_module.resources | map(select(.mode == "managed" and (.actions | length) > 1 and .actions != ["create"])) | length,
    "destroy": .planned_values.root_module.resources | map(select(.mode == "managed" and .actions == ["delete"])) | length
  } |
  "Resources to add: \(.add)\nResources to change: \(.change)\nResources to destroy: \(.destroy)"
'

# Clean up
rm -f tfplan

echo ""
echo "✅ All validations passed!"
echo ""
echo "Next steps:"
echo "1. Review the plan output above"
echo "2. Run 'terraform apply' to create resources"
echo "3. Configure GitHub secrets with the outputs"