variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "service_account_email" {
  description = "Email of the service account"
  type        = string
}

variable "service_account_member" {
  description = "Service account member format for IAM bindings"
  type        = string
}

variable "enable_cloud_run_admin" {
  description = "Whether to grant Cloud Run admin role"
  type        = bool
  default     = true
}

variable "enable_cloudbuild_editor" {
  description = "Whether to grant Cloud Build editor role"
  type        = bool
  default     = true
}

variable "enable_storage_access" {
  description = "Whether to grant Storage Object Viewer role for Terraform state access"
  type        = bool
  default     = true
}

variable "enable_service_account_user" {
  description = "Whether to grant service account user role (DANGEROUS - allows impersonation)"
  type        = bool
  default     = false
}

variable "enable_self_impersonation" {
  description = "Whether to grant self-impersonation role for Workload Identity (required for Terraform state access)"
  type        = bool
  default     = true
}

variable "additional_roles" {
  description = "Additional IAM roles to grant"
  type = map(object({
    role    = string
    members = list(string)
  }))
  default = {}
}