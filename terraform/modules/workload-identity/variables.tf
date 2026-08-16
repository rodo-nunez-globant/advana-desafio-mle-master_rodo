variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "workload_identity_pool_id" {
  description = "Workload identity pool ID"
  type        = string
  default     = "github-pool"
}

variable "workload_identity_pool_display_name" {
  description = "Workload identity pool display name"
  type        = string
  default     = "GitHub Actions Pool"
}

variable "workload_identity_pool_description" {
  description = "Workload identity pool description"
  type        = string
  default     = "Workload identity pool for GitHub Actions authentication"
}

variable "workload_identity_provider_id" {
  description = "Workload identity provider ID"
  type        = string
  default     = "github-provider"
}

variable "workload_identity_provider_display_name" {
  description = "Workload identity provider display name"
  type        = string
  default     = "GitHub Provider"
}

variable "workload_identity_provider_description" {
  description = "Workload identity provider description"
  type        = string
  default     = "Workload identity provider for GitHub"
}

variable "github_repo" {
  description = "GitHub repository in format owner/repo"
  type        = string
}

variable "github_owner" {
  description = "GitHub owner/organization"
  type        = string
  default     = ""
}

variable "service_account_email" {
  description = "Email of the service account to link"
  type        = string
}