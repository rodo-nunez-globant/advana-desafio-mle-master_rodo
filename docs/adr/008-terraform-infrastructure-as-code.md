# ADR 008: Terraform Infrastructure as Code for GCP Deployment

## Status
Proposed

## Context
For Part IV of the challenge, we need to implement CI/CD with automated deployment to GCP Cloud Run. The current manual setup for GCP authentication and service accounts is error-prone and difficult to reproduce. We need an Infrastructure as Code solution that:

1. **Automates GCP resource creation** - Service accounts, IAM bindings, and permissions
2. **Uses secure authentication** - Workload Identity Federation instead of service account keys
3. **Integrates with CI/CD** - Terraform plan/apply in GitHub Actions
4. **Enables easy cleanup** - Destroy all resources when challenge is complete
5. **References existing resources** - Uses the already created bucket `rodo-nunez-challenge-latam-data`

## Decision
Adopt Terraform for managing all GCP infrastructure with the following approach:

### 1. **Terraform Structure**
- Separate modules for different resource types
- Remote state storage in GCS bucket
- Environment-specific configurations
- Integration with GitHub Actions

### 2. **Authentication Strategy**
- Use Workload Identity Federation for secure GitHub Actions authentication
- No service account keys stored in GitHub Secrets
- Principle of least privilege for all IAM roles

### 3. **Resource Management**
- Service account for GitHub Actions
- IAM policies and bindings
- Cloud Run service configuration
- Integration with existing GCS bucket

### 4. **CI/CD Integration**
- Terraform plan as a pull request check
- Terraform apply on merge to main
- Automatic resource updates

## Consequences

### Positive
- **Reproducible Infrastructure** - Easy to setup in new projects
- **Version Controlled** - All infrastructure changes tracked in Git
- **Secure Authentication** - No long-lived credentials
- **Easy Cleanup** - Single command to destroy all resources
- **Documentation** - Infrastructure code serves as documentation
- **Compliance** - Follows IaC best practices

### Negative
- **Additional Complexity** - Learning curve for Terraform
- **Initial Setup Time** - Requires understanding of Terraform concepts
- **State Management** - Need to manage Terraform state file
- **Dependency on Terraform** - New tool in the toolchain

### Neutral
- **Infrastructure as Code** - Shift from manual to automated setup
- **GitOps Approach** - Infrastructure changes through PRs
- **Modular Design** - Reusable Terraform modules

## Implementation Details

### 1. **Terraform Configuration**
```hcl
# Main configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# Remote state backend
terraform {
  backend "gcs" {
    bucket = "rodo-nunez-challenge-latam-data"
    prefix = "terraform/state"
  }
}
```

### 2. **Service Account Module**
```hcl
# GitHub Actions service account
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions Service Account"
}

# Workload Identity Pool
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-pool"
  display_name            = "GitHub pool"
}
```

### 3. **IAM Bindings**
```hcl
# Required roles for deployment
resource "google_project_iam_binding" "run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  members = [
    "serviceAccount:${google_service_account.github_actions.email}"
  ]
}
```

### 4. **GitHub Actions Integration**
```yaml
- name: Terraform Plan
  uses: hashicorp/setup-terraform@v3
  with:
    terraform_version: "latest"
    
- name: Terraform Apply
  if: github.ref == 'refs/heads/main'
  run: terraform apply -auto-approve
```

## Alternatives Considered

### 1. **Manual Setup**
- **Pros**: No additional tools
- **Cons**: Error-prone, not reproducible, security risks with keys

### 2. **gcloud CLI Scripts**
- **Pros**: Uses familiar gcloud commands
- **Cons**: Less structured, no state management, harder to version

### 3. **Pulumi**
- **Pros**: Code-based infrastructure
- **Cons**: Additional tool, less adoption than Terraform

### 4. **Deployment Manager**
- **Pros**: Native GCP solution
- **Cons**: Less flexible, smaller community

## Security Considerations

1. **Workload Identity** - No service account keys in GitHub
2. **Least Privilege** - Minimum required IAM roles
3. **State Protection** - GCS bucket with versioning
4. **Audit Logging** - All changes tracked in Cloud Audit Logs

## Migration Strategy

1. **Initial Setup** - Create Terraform configuration
2. **Import Existing Resources** - Import bucket if needed
3. **Update CI/CD** - Add Terraform steps to workflows
4. **Test and Validate** - Ensure deployment works
5. **Cleanup Manual Setup** - Remove manually created resources

## Future Considerations

- **Multi-environment Support** - dev/staging/prod environments
- **Module Registry** - Publish reusable modules
- **Policy as Code** - Add OPA/Conftest for policy validation
- **Cost Monitoring** - Budget alerts and cost optimization

---

*Decision Date: 2026-08-15*  
*Status: Proposed*  
*Implementation: Pending Review*