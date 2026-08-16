# Terraform Infrastructure Design

## Architecture Overview

This design document outlines the technical architecture for implementing Infrastructure as Code using Terraform to manage GCP resources for the Flight Delay Prediction API deployment. The solution focuses on secure, automated infrastructure provisioning with GitHub Actions integration.

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Terraform      │    │   GCP           │
│   Actions       │───▶│   Cloud          │───▶│   Resources     │
│                 │    │                  │    │                 │
│ - Plan/Apply    │    │ - State Mgmt     │    │ - Service Acct   │
│ - OIDC Auth     │    │ - Validation     │    │ - IAM Roles     │
│ - CI/CD         │    │ - Modules        │    │ - Cloud Run     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   GCS Bucket     │
                       │ (State Storage)  │
                       │                  │
                       │ - terraform/     │
                       │   state/         │
                       │ - versioning     │
                       │ - locking        │
                       └──────────────────┘
```

## Detailed Design

### 1. Authentication Architecture

#### Workload Identity Federation Flow
```
GitHub Actions ──► OIDC Token ──► GCP STS ──► Federated Token ──► GCP APIs
     │                                                           │
     │                                                           ▼
     │                                                   Service Account
     │                                                           │
     └───────────────────────────────────────────────────────┘
                              (Impersonation)
```

**Key Design Decisions:**
- **No Service Account Keys**: Eliminates risk of key leakage
- **Short-lived Tokens**: OIDC tokens expire after 1 hour
- **Repository-scoped Access**: Only specific repo can impersonate
- **Attribute-based Mapping**: Uses GitHub repository and actor attributes

### 2. Terraform Module Architecture

#### Module Structure
```
terraform/
├── main.tf                    # Root module
├── variables.tf               # Input variables
├── outputs.tf                # Output values
├── providers.tf              # Provider configuration
├── backend.tf                # State backend
├── modules/
│   ├── service-account/      # SA management
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── workload-identity/     # Workload identity
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── iam/                  # IAM bindings
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

#### Module Dependencies
```
main.tf
├── module.service-account
├── module.workload-identity (depends on service-account)
└── module.iam (depends on service-account)
```

### 3. State Management Design

#### Remote State Configuration
```hcl
terraform {
  backend "gcs" {
    bucket = "rodo-nunez-challenge-latam-data"
    prefix = "terraform/state"
  }
}
```

**State Protection Features:**
- **Versioning**: All state versions preserved
- **Locking**: Prevents concurrent state modifications
- **Encryption**: Server-side encryption at rest
- **Access Control**: IAM permissions on state bucket

#### State Structure
```
gs://rodo-nunez-challenge-latam-data/terraform/state/
├── default.tflock          # State lock file
├── terraform.tfstate       # Current state
└── versions/               # State history
    ├── 1640000000.tfstate
    ├── 1640000100.tfstate
    └── ...
```

### 4. Resource Design

#### Service Account Design
```hcl
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions Service Account"
  description  = "For CI/CD deployments via GitHub Actions"
  
  # Ensure consistent naming
  depends_on = [time_sleep.wait_for_project_id]
}
```

**Design Considerations:**
- **Descriptive Naming**: Clear purpose identification
- **Documentation**: Comprehensive descriptions
- **Dependencies**: Handle project propagation delays

#### Workload Identity Pool Design
```hcl
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-pool"
  display_name            = "GitHub Actions Pool"
  
  # Attribute mapping for GitHub integration
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }
}
```

**Attribute Mapping Strategy:**
- **subject**: GitHub actor (user or workflow)
- **actor**: GitHub user who triggered action
- **repository**: Specific repository for scoping

#### IAM Binding Design
```hcl
# Minimal required roles
resource "google_project_iam_binding" "run_admin" {
  role    = "roles/run.admin"
  members = [local.service_account_member]
}

resource "google_project_iam_binding" "cloudbuild_editor" {
  role    = "roles/cloudbuild.builds.editor"
  members = [local.service_account_member]
}
```

**Role Selection Rationale:**
- **run.admin**: Required for Cloud Run deployment
- **cloudbuild.builds.editor**: Required for Cloud Build
- **serviceAccountUser**: Required for impersonation
- **No excess permissions**: Principle of least privilege

### 5. CI/CD Integration Design

#### GitHub Actions Workflow
```yaml
name: Terraform

on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
      - uses: hashicorp/setup-terraform@v3
      - run: terraform plan
  
  apply:
    if: github.ref == 'refs/heads/main'
    needs: plan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
      - uses: hashicorp/setup-terraform@v3
      - run: terraform apply -auto-approve
```

**Workflow Design Features:**
- **Path-based Triggers**: Only runs on Terraform changes
- **Plan on PR**: Shows changes before merge
- **Apply on Main**: Automatic deployment after approval
- **Dependency Chain**: Plan must pass before apply

### 6. Security Design

#### Authentication Flow
```
1. GitHub Action starts
2. GitHub generates OIDC token
3. Action exchanges token for GCP access token
4. GCP validates token against workload identity pool
5. Action impersonates service account
6. Action accesses GCP resources with SA permissions
```

#### Security Controls
- **No Long-lived Credentials**: Only temporary tokens
- **Repository Scoping**: Only specific repo can authenticate
- **Role Minimization**: Minimum required permissions only
- **Audit Logging**: All actions logged in Cloud Audit
- **State Encryption**: Terraform state encrypted at rest

### 7. Error Handling Design

#### Common Error Scenarios
1. **Service Account Creation Delays**
   - Solution: Add `time_sleep` resource
   - Retry logic in GitHub Actions

2. **State Lock Conflicts**
   - Solution: Automatic lock acquisition
   - Manual unlock procedure documented

3. **Permission Errors**
   - Solution: Clear error messages
   - IAM binding verification

4. **Resource Dependencies**
   - Solution: Explicit depends_on
   - Resource graph validation

#### Monitoring and Alerting
```hcl
# Example monitoring configuration
resource "google_monitoring_alert_policy" "terraform_failures" {
  display_name = "Terraform Deployment Failures"
  condition {
    filter = 'metric.type="workflows.googleapis.com/workflow/failed"'
  }
}
```

### 8. Performance Optimization

#### Terraform Optimization
- **Parallel Resource Creation**: Independent resources created concurrently
- **State Caching**: Local state cache for faster operations
- **Dependency Graph**: Optimized resource dependencies

#### CI/CD Optimization
- **Conditional Execution**: Only runs on relevant changes
- **Parallel Jobs**: Plan and validation run in parallel
- **Caching**: Terraform binary and provider caching

### 9. Disaster Recovery

#### State Recovery
```bash
# List state versions
gsutil ls gs://bucket/terraform/state/

# Restore specific version
gsutil cp gs://bucket/terraform/state/versions/1640000000.tfstate terraform.tfstate
```

#### Resource Recreation
```bash
# Import existing resources
terraform import google_service_account.github_actions projects/PROJECT_ID/serviceAccounts/SA_EMAIL

# Recreate from state
terraform apply -replace=google_service_account.github_actions
```

### 10. Migration Strategy

#### Phase 1: Initial Setup
1. Create Terraform configuration
2. Initialize remote state
3. Create service account and workload identity
4. Configure GitHub Actions

#### Phase 2: Migration
1. Import existing resources (if any)
2. Update GitHub Secrets with outputs
3. Test authentication flow
4. Validate deployment pipeline

#### Phase 3: Cleanup
1. Remove manually created resources
2. Verify all resources managed by Terraform
3. Document maintenance procedures

## Implementation Strategy

### Development Phases

#### Phase 1: Core Infrastructure (Priority 1)
- Create basic Terraform structure
- Implement service account module
- Set up remote state backend
- Basic GitHub Actions workflow

#### Phase 2: Security Integration (Priority 2)
- Implement workload identity federation
- Configure IAM bindings
- Add security scanning
- Test authentication flow

#### Phase 3: CI/CD Integration (Priority 3)
- Complete GitHub Actions workflow
- Add plan/apply automation
- Integrate with existing CI/CD
- Add monitoring and alerting

#### Phase 4: Optimization (Priority 4)
- Performance tuning
- Advanced security features
- Documentation completion
- Testing automation

### Risk Mitigation

#### Technical Risks
1. **State Corruption**
   - Mitigation: Versioning and backups
   - Recovery: State restoration procedures

2. **Permission Issues**
   - Mitigation: Principle of least privilege
   - Recovery: Manual permission verification

3. **Resource Conflicts**
   - Mitigation: Clear naming conventions
   - Recovery: Resource import procedures

#### Operational Risks
1. **Team Knowledge Gap**
   - Mitigation: Comprehensive documentation
   - Training: Terraform best practices

2. **Workflow Disruption**
   - Mitigation: Gradual migration
   - Rollback: Manual deployment procedures

## Technology Choices

### Terraform Version
- **Version**: 1.5+
- **Rationale**: Latest features and security patches
- **Compatibility**: Works with all required providers

### Provider Selection
- **Google Provider**: Official GCP provider
- **Version**: Latest stable
- **Features**: Full GCP resource support

### Module Sources
- **Local Modules**: Custom logic for project
- **Registry Modules**: Reusable components
- **Version Pinning**: Prevent unexpected changes

## Integration Considerations

### Existing Makefile Integration
```makefile
terraform-init:
	@echo "Initializing Terraform..."
	cd terraform && terraform init

terraform-plan:
	@echo "Planning Terraform changes..."
	cd terraform && terraform plan

terraform-apply:
	@echo "Applying Terraform changes..."
	cd terraform && terraform apply -auto-approve

terraform-destroy:
	@echo "Destroying Terraform resources..."
	cd terraform && terraform destroy -auto-approve
```

### CI/CD Pipeline Integration
- **Pre-deployment**: Terraform plan validation
- **Deployment**: Terraform apply after tests
- **Post-deployment**: Health checks and monitoring

### Monitoring Integration
- **Cloud Monitoring**: Resource metrics
- **Cloud Logging**: Audit logs
- **GitHub Actions**: Workflow status