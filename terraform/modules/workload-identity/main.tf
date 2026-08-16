# Create workload identity pool for GitHub
resource "google_iam_workload_identity_pool" "github" {
  provider                  = google
  workload_identity_pool_id = var.workload_identity_pool_id
  display_name             = var.workload_identity_pool_display_name
  description              = var.workload_identity_pool_description
  
  # Enable the pool
  disabled = false
}

# Create workload identity provider for GitHub
resource "google_iam_workload_identity_pool_provider" "github" {
  provider                           = google
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = var.workload_identity_provider_id
  display_name                       = var.workload_identity_provider_display_name
  description                        = var.workload_identity_provider_description
  
  # OIDC configuration for GitHub
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
  
  # Attribute mapping from GitHub OIDC token to GCP attributes
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }
  
  # Restrict authentication to specific repository and branch
  # Only allow main branch and pull requests
  attribute_condition = "attribute.repository == '${var.github_repo}' && (attribute.ref == 'refs/heads/main' || attribute.ref.startsWith('refs/pull/'))"
  
  # Enable the provider
  disabled = false
}

# Allow the GitHub repository to impersonate the service account
resource "google_service_account_iam_binding" "workload_identity_user" {
  service_account_id = "projects/${var.project_id}/serviceAccounts/${var.service_account_email}"
  role               = "roles/iam.workloadIdentityUser"
  
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_repo}"
  ]
}