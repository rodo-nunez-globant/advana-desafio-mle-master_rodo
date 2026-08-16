output "pool_name" {
  description = "Full name of the workload identity pool"
  value       = google_iam_workload_identity_pool.github.name
}

output "pool_id" {
  description = "ID of the workload identity pool"
  value       = google_iam_workload_identity_pool.github.workload_identity_pool_id
}

output "provider_name" {
  description = "Full name of the workload identity provider"
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "provider_id" {
  description = "ID of the workload identity provider"
  value       = google_iam_workload_identity_pool_provider.github.workload_identity_pool_provider_id
}

output "issuer_uri" {
  description = "OIDC issuer URI"
  value       = google_iam_workload_identity_pool_provider.github.oidc[0].issuer_uri
}

output "attribute_mapping" {
  description = "Attribute mapping configuration"
  value       = google_iam_workload_identity_pool_provider.github.attribute_mapping
}

output "attribute_condition" {
  description = "Attribute condition for repository scoping"
  value       = google_iam_workload_identity_pool_provider.github.attribute_condition
}