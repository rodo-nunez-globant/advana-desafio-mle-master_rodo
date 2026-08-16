output "email" {
  description = "Email of the service account"
  value       = google_service_account.github_actions.email
}

output "name" {
  description = "Full name of the service account"
  value       = google_service_account.github_actions.name
}

output "id" {
  description = "ID of the service account"
  value       = google_service_account.github_actions.id
}

output "member" {
  description = "Service account member format for IAM bindings"
  value       = "serviceAccount:${google_service_account.github_actions.email}"
}

output "unique_id" {
  description = "Unique ID of the service account"
  value       = google_service_account.github_actions.unique_id
}