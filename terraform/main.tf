# Extract GitHub owner from repository if not provided
locals {
  github_owner = var.github_owner != "" ? var.github_owner : split("/", var.github_repo)[0]
  github_repo_name = split("/", var.github_repo)[1]
}

# Call service account module
module "service-account" {
  source = "./modules/service-account"
  
  project_id                    = var.project_id
  service_account_id           = var.service_account_id
  service_account_display_name = "GitHub Actions Service Account"
  service_account_description  = "Service account for CI/CD deployments via GitHub Actions for ${var.github_repo}"
}

# Call workload identity module
module "workload-identity" {
  source = "./modules/workload-identity"
  
  project_id                           = var.project_id
  workload_identity_pool_id            = var.workload_identity_pool_id
  workload_identity_pool_display_name  = "GitHub Actions Pool"
  workload_identity_pool_description   = "Workload identity pool for GitHub Actions authentication"
  workload_identity_provider_id        = var.workload_identity_provider_id
  workload_identity_provider_display_name = "GitHub Provider"
  workload_identity_provider_description = "Workload identity provider for GitHub"
  
  github_repo           = var.github_repo
  github_owner         = local.github_owner
  service_account_email = module.service-account.email
  
  depends_on = [module.service-account]
}

# Call IAM module
module "iam" {
  source = "./modules/iam"
  
  project_id             = var.project_id
  service_account_email  = module.service-account.email
  service_account_member = module.service-account.member
  
  enable_cloud_run_admin     = true
  enable_cloudbuild_editor   = true
  enable_service_account_user = true
  
  depends_on = [module.service-account]
}

# Enable required APIs for the project
resource "google_project_service" "iam" {
  project = var.project_id
  service = "iam.googleapis.com"
  
  disable_on_destroy = false
}

resource "google_project_service" "run" {
  project = var.project_id
  service = "run.googleapis.com"
  
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
  
  disable_on_destroy = false
}

resource "google_project_service" "storage" {
  project = var.project_id
  service = "storage-component.googleapis.com"
  
  disable_on_destroy = false
}