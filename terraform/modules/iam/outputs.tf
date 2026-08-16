output "run_admin_binding" {
  description = "Cloud Run admin IAM binding"
  value = var.enable_cloud_run_admin ? {
    role    = "roles/run.admin"
    members = [local.service_account_member]
  } : null
}

output "cloudbuild_editor_binding" {
  description = "Cloud Build editor IAM binding"
  value = var.enable_cloudbuild_editor ? {
    role    = "roles/cloudbuild.builds.editor"
    members = [local.service_account_member]
  } : null
}

output "service_account_user_binding" {
  description = "Service account user IAM binding"
  value = var.enable_service_account_user ? {
    role    = "roles/iam.serviceAccountUser"
    members = [local.service_account_member]
  } : null
}

output "additional_bindings" {
  description = "Additional IAM bindings"
  value = {
    for k, v in google_project_iam_binding.additional : k => {
      role    = v.role
      members = v.members
    }
  }
}

output "service_account_member" {
  description = "Service account member format used"
  value       = local.service_account_member
}