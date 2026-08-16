variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "service_account_id" {
  description = "Service account ID"
  type        = string
  default     = "github-actions"
}

variable "service_account_display_name" {
  description = "Service account display name"
  type        = string
  default     = "GitHub Actions Service Account"
}

variable "service_account_description" {
  description = "Service account description"
  type        = string
  default     = "Service account for CI/CD deployments via GitHub Actions"
}