# Terraform Infrastructure Specification

## Overview
This specification defines the Infrastructure as Code (IaC) implementation for automating GCP resource creation and management for the Flight Delay Prediction API deployment. The solution uses Terraform to create all necessary GCP resources, configure secure authentication via Workload Identity Federation, and integrate with GitHub Actions for CI/CD automation.

## Scope
- Create and manage GCP service accounts for GitHub Actions
- Configure Workload Identity Federation for secure authentication
- Set up IAM policies and bindings with principle of least privilege
- Integrate with existing GCS bucket `rodo-nunez-challenge-latam-data`
- Provide Terraform configuration for Cloud Run deployment
- Enable easy resource cleanup after challenge completion

## Requirements

### Functional Requirements
1. **Service Account Management**
   - Create dedicated service account for GitHub Actions
   - Assign minimum required IAM roles
   - Enable service account to impersonate via Workload Identity

2. **Workload Identity Federation**
   - Create workload identity pool for GitHub
   - Configure GitHub provider with proper attribute mapping
   - Link GitHub repository to service account

3. **IAM Configuration**
   - Grant `roles/run.admin` for Cloud Run management
   - Grant `roles/cloudbuild.builds.editor` for Cloud Build
   - Grant `roles/iam.serviceAccountUser` for service account impersonation

4. **State Management**
   - Use existing GCS bucket for Terraform state storage
   - Enable state locking and versioning
   - Configure remote backend properly

5. **CI/CD Integration**
   - Terraform plan as pull request check
   - Terraform apply on main branch merge
   - Automatic resource updates

### Non-Functional Requirements
1. **Security**
   - No service account keys stored in GitHub Secrets
   - Use Workload Identity Federation exclusively
   - Follow principle of least privilege
   - All changes audited in Cloud Audit Logs

2. **Maintainability**
   - Modular Terraform structure
   - Clear documentation and comments
   - Version controlled infrastructure
   - Easy to understand and modify

3. **Reproducibility**
   - Same configuration works in new projects
   - All resources defined in code
   - No manual setup required

4. **Cleanup**
   - Single command to destroy all resources
   - No orphaned resources left behind
   - Clear dependency mapping

## Data Flow

### Input Configuration
```yaml
# terraform.tfvars
project_id = "rodo-nunez-challenge-latam"
region = "us-central1"
github_repo = "rodo-nunez-globant/advana-desafio-mle-master_rodo"
```

### Resource Creation Flow
1. Terraform reads configuration from variables
2. Creates service account with specified permissions
3. Sets up workload identity pool and provider
4. Configures IAM bindings
5. Stores state in GCS bucket
6. Outputs resource identifiers for GitHub Actions

### Output Values
- Service account email
- Workload identity provider
- IAM role bindings
- Resource dependencies

## Implementation Specifications

### File Structure
```
terraform/
├── main.tf              # Main configuration
├── variables.tf         # Input variables
├── outputs.tf          # Output values
├── providers.tf        # Provider configuration
├── backend.tf          # Remote state configuration
├── modules/
│   ├── service-account/  # Service account module
│   ├── workload-identity/ # Workload identity module
│   └── iam/              # IAM bindings module
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

### Core Components

#### 1. Provider Configuration
```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "rodo-nunez-challenge-latam-data"
    prefix = "terraform/state"
  }
}
```

#### 2. Service Account Module
```hcl
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions Service Account"
  description  = "Service account for CI/CD deployments via GitHub Actions"
}
```

#### 3. Workload Identity Module
```hcl
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-pool"
  display_name            = "GitHub Actions Pool"
  description             = "Workload identity pool for GitHub Actions authentication"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Provider"
  description                        = "Workload identity provider for GitHub"
  
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }
  
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}
```

#### 4. IAM Bindings Module
```hcl
resource "google_project_iam_binding" "run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  members = [
    "serviceAccount:${google_service_account.github_actions.email}"
  ]
}

resource "google_project_iam_binding" "cloudbuild_editor" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.editor"
  members = [
    "serviceAccount:${google_service_account.github_actions.email}"
  ]
}
```

### Variables Definition
```hcl
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "github_repo" {
  description = "GitHub repository in format owner/repo"
  type        = string
}
```

### Outputs Definition
```hcl
output "service_account_email" {
  description = "Email of the GitHub Actions service account"
  value       = google_service_account.github_actions.email
}

output "workload_identity_provider" {
  description = "Workload identity provider resource name"
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "github_secrets" {
  description = "GitHub secrets configuration"
  value = {
    GCP_PROJECT_ID              = var.project_id
    GCP_WORKLOAD_IDENTITY_PROVIDER = google_iam_workload_identity_pool_provider.github.name
    GCP_SERVICE_ACCOUNT_EMAIL   = google_service_account.github_actions.email
  }
  sensitive = true
}
```

## Integration Points

### 1. GitHub Actions Workflow
- Terraform configuration stored in `.github/workflows/terraform.yml`
- Plan runs on pull requests
- Apply runs on main branch merge
- Uses OIDC authentication

### 2. Existing Makefile
- Add `terraform-init`, `terraform-plan`, `terraform-apply` targets
- Complement existing deployment targets
- Maintain backward compatibility

### 3. CI/CD Pipeline
- Terraform plan as required check
- Automatic deployment after successful apply
- Integration with existing test workflows

## Quality Standards

### Testing Requirements
1. **Terraform Validation**
   - `terraform validate` in CI
   - `terraform fmt -check` for formatting
   - `tflint` for best practices

2. **Security Scanning**
   - Checkov for security scanning
   - tfsec for vulnerability detection
   - No secrets in configuration

3. **Integration Testing**
   - Test resource creation in dev environment
   - Verify IAM permissions
   - Validate GitHub Actions integration

### Documentation Requirements
1. **Code Comments**
   - All resources documented
   - Variable descriptions complete
   - Output values explained

2. **README Updates**
   - Terraform setup instructions
   - Prerequisites and requirements
   - Troubleshooting guide

3. **Architecture Diagrams**
   - Resource relationship diagram
   - Authentication flow diagram
   - CI/CD integration flow

### Success Criteria
1. All resources created successfully
2. GitHub Actions can authenticate without keys
3. CI/CD pipeline deploys to Cloud Run
4. Resources can be destroyed cleanly
5. No security vulnerabilities
6. All tests pass

## Constraints and Boundaries

### Constitutional Compliance
- Must use GCP as specified in constitution
- Cannot modify existing challenge structure
- Must follow security best practices (no secrets in code)
- Must complement existing Makefile targets

### Technical Constraints
- Terraform version compatibility
- GCP API limitations
- GitHub Actions permissions
- Resource naming conventions

### Security Constraints
- No service account keys
- Minimum privilege principle
- All changes audited
- State protection enabled