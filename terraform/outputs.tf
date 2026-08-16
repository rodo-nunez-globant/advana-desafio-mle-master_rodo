output "service_account_email" {
  description = "Email of the GitHub Actions service account"
  value       = module.service-account.email
}

output "service_account_name" {
  description = "Full name of the GitHub Actions service account"
  value       = module.service-account.name
}

output "workload_identity_provider" {
  description = "Workload identity provider resource name"
  value       = module.workload-identity.provider_name
}

output "workload_identity_pool" {
  description = "Workload identity pool resource name"
  value       = module.workload-identity.pool_name
}

output "github_secrets" {
  description = "GitHub secrets configuration for setup"
  value = {
    GCP_PROJECT_ID                 = var.project_id
    GCP_WORKLOAD_IDENTITY_PROVIDER = module.workload-identity.provider_name
    GCP_SERVICE_ACCOUNT_EMAIL      = module.service-account.email
  }
  sensitive = true
}

output "iam_bindings" {
  description = "IAM bindings applied to the service account"
  value = {
    run_admin            = module.iam.run_admin_binding
    cloudbuild_editor    = module.iam.cloudbuild_editor_binding
    service_account_user = module.iam.service_account_user_binding
  }
}

output "setup_commands" {
  description = "Commands to set up GitHub repository"
  value = [
    "echo '=== GitHub Repository Setup ==='",
    "echo '1. Add these secrets to your GitHub repository:'",
    "echo '   GCP_PROJECT_ID: ${var.project_id}'",
    "echo '   GCP_WORKLOAD_IDENTITY_PROVIDER: ${module.workload-identity.provider_name}'",
    "echo '   GCP_SERVICE_ACCOUNT_EMAIL: ${module.service-account.email}'",
    "",
    "echo '2. Configure GitHub repository permissions:'",
    "echo '   Settings > Actions > General > Workflow permissions'",
    "echo '   - Read and write permissions'",
    "echo '   - Allow GitHub Actions to create and approve pull requests'",
    "echo '   - Allow GitHub Actions to run approved pull requests from forks'",
    "",
    "echo '3. Verify the workload identity provider:'",
    "echo '   gcloud iam workload-identity-pools providers describe ${module.workload-identity.provider_id}'",
    "echo '     --workload-identity-pool=${module.workload-identity.pool_id}'",
    "echo '     --location=global --project=${var.project_id}'",
    "",
    "echo '4. Test the configuration:'",
    "echo '   gcloud iam service-accounts impersonate-service-account ${module.service-account.email}'",
    "echo '     --project=${var.project_id} -- gcloud projects list'"
  ]
}