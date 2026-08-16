# Create service account for GitHub Actions
resource "google_service_account" "github_actions" {
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
  description  = var.service_account_description
  
  project = var.project_id
  
  # Ensure consistent naming and avoid conflicts
  depends_on = [time_sleep.wait_for_project_id]
}

# Wait a bit to ensure project is fully initialized
# This helps with propagation delays in GCP
resource "time_sleep" "wait_for_project_id" {
  depends_on = [null_resource.project_check]
  
  create_duration = "30s"
}

# Check if project exists and is accessible
resource "null_resource" "project_check" {
  provisioner "local-exec" {
    command = "gcloud projects describe ${var.project_id} --format='value(projectId)'"
  }
}