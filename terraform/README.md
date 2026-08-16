# Terraform Infrastructure for Flight Delay Prediction API

This directory contains Terraform configuration for managing GCP infrastructure required for deploying the Flight Delay Prediction API to Cloud Run with secure GitHub Actions integration.

## Overview

The Terraform configuration creates:
- Service account for GitHub Actions
- Workload Identity Federation for secure authentication
- Required IAM roles and permissions
- Integration with GitHub Actions CI/CD

## Prerequisites

1. **GCP Project**: Ensure you have a GCP project with billing enabled
2. **gcloud CLI**: Install and authenticate with `gcloud auth login`
3. **Terraform**: Install Terraform >= 1.5.0
4. **GCS Bucket**: The bucket `rodo-nunez-challenge-latam-data` must exist

## Quick Start

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Configure Variables

Copy the example variables file:
```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your project and repository details:
```hcl
project_id = "your-gcp-project-id"
github_repo = "your-username/your-repo"
```

### 3. Plan and Apply

```bash
# Review the changes
terraform plan

# Apply the changes
terraform apply
```

### 4. Configure GitHub Secrets

After successful apply, Terraform will output the required GitHub secrets:

```bash
terraform output -json | jq -r '.github_secrets.value | to_entries[] | "\(.key)=\(.value)"'
```

Add these secrets to your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add each secret:
   - `GCP_PROJECT_ID`
   - `GCP_WORKLOAD_IDENTITY_PROVIDER`
   - `GCP_SERVICE_ACCOUNT_EMAIL`

### 5. Configure GitHub Repository

In your GitHub repository settings:
1. Go to Settings → Actions → General
2. Under "Workflow permissions":
   - Select "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"
   - Check "Allow GitHub Actions to run approved pull requests from forks"

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Terraform      │    │   GCP           │
│   Actions       │───▶│   Cloud          │───▶│   Resources     │
│                 │    │                  │    │                 │
│ - OIDC Auth     │    │ - State Mgmt     │    │ - Service Acct   │
│ - CI/CD         │    │ - Modules        │    │ - IAM Roles     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   GCS Bucket     │
                       │ (State Storage)  │
                       └──────────────────┘
```

## Modules

### service-account
Creates a service account for GitHub Actions with proper configuration.

### workload-identity
Sets up Workload Identity Federation for secure authentication without service account keys.

### iam
Manages IAM role bindings for the service account following the principle of least privilege.

## Variables

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| project_id | GCP project ID | string | - |
| region | GCP region | string | us-central1 |
| github_repo | GitHub repository (owner/repo) | string | - |
| service_account_id | Service account ID | string | github-actions |
| workload_identity_pool_id | Workload identity pool ID | string | github-pool |

## Outputs

| Output | Description |
|--------|-------------|
| service_account_email | Email of the GitHub Actions service account |
| workload_identity_provider | Workload identity provider resource name |
| github_secrets | GitHub secrets configuration (sensitive) |
| setup_commands | Commands for GitHub setup |

## Security Features

- **No Service Account Keys**: Uses Workload Identity Federation
- **Least Privilege**: Only required IAM roles granted
- **Repository Scoping**: Only specific repository can authenticate
- **Audit Logging**: All actions logged in Cloud Audit Logs
- **State Protection**: Remote state with versioning and locking

## Common Commands

```bash
# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy all resources
terraform destroy

# Import existing resources (if needed)
terraform import google_service_account.github_actions projects/PROJECT_ID/serviceAccounts/SA_EMAIL

# Validate configuration
terraform validate

# Format code
terraform fmt

# Show state
terraform show

# List resources
terraform state list
```

## Troubleshooting

### Permission Denied
Ensure you have the following roles in the GCP project:
- `roles/owner` or `roles/resourcemanager.projectIamAdmin`
- `roles/iam.serviceAccountAdmin`
- `roles/iam.workloadIdentityPoolAdmin`

### State Lock Issues
If Terraform state is locked:
```bash
# Force unlock (use with caution)
terraform force-unlock LOCK_ID
```

### API Not Enabled
If you get API not enabled errors:
```bash
# Enable required APIs
gcloud services enable iam.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage-component.googleapis.com
```

### Workload Identity Issues
1. Verify the GitHub repository name matches exactly
2. Check the attribute condition in the provider
3. Ensure GitHub Actions permissions are configured correctly

## Cleanup

To remove all created resources:
```bash
terraform destroy
```

This will remove:
- Service account
- Workload identity pool and provider
- IAM bindings
- Enabled APIs (will remain enabled)

## Integration with CI/CD

The GitHub Actions workflow (`.github/workflows/terraform.yml`) uses this configuration to:
1. Plan changes on pull requests
2. Apply changes on main branch merges
3. Authenticate using Workload Identity Federation
4. Deploy to Cloud Run after successful apply

## Support

For issues:
1. Check the troubleshooting section
2. Review Terraform logs
3. Verify GCP project permissions
4. Check GitHub Actions workflow logs