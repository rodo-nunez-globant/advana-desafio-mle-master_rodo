locals {
  # Ensure we have the correct member format
  service_account_member = var.service_account_member != "" ? var.service_account_member : "serviceAccount:${var.service_account_email}"
}

# Grant Cloud Run admin role to manage Cloud Run services
resource "google_project_iam_binding" "run_admin" {
  count = var.enable_cloud_run_admin ? 1 : 0
  
  project = var.project_id
  role    = "roles/run.admin"
  
  members = [
    local.service_account_member
  ]
  
  # Add condition to restrict to specific resources if needed
  # condition {
  #   title       = "Cloud Run management"
  #   description = "Allow management of Cloud Run services"
  #   expression  = "resource.name.startsWith('projects/_/services/')"
  # }
}

# Grant Cloud Build editor role to build and push images
resource "google_project_iam_binding" "cloudbuild_editor" {
  count = var.enable_cloudbuild_editor ? 1 : 0
  
  project = var.project_id
  role    = "roles/cloudbuild.builds.editor"
  
  members = [
    local.service_account_member
  ]
}

# Grant service account user role for impersonation (RESTRICTED)
# Note: This role is disabled by default for security reasons.
# Only enable if absolutely necessary and consider using service account-specific
# bindings instead of project-level bindings.
resource "google_project_iam_binding" "service_account_user" {
  count = var.enable_service_account_user ? 1 : 0
  
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  
  members = [
    local.service_account_member
  ]
  
  # Add condition to restrict to specific service accounts if needed
  # condition {
  #   title       = "Restricted service account access"
  #   description = "Only allow impersonation of specific service accounts"
  #   expression  = "resource.name.startsWith('projects/-/serviceAccounts/') && resource.name.endsWith('@my-project.iam.gserviceaccount.com')"
  # }
}

# Additional IAM roles if specified
resource "google_project_iam_binding" "additional" {
  for_each = var.additional_roles
  
  project = var.project_id
  role    = each.value.role
  
  members = each.value.members
}