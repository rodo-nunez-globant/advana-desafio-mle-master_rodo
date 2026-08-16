terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0.0"
    }
    time = {
      source  = "hashicorp/time"
      version = ">= 0.9.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  
  # Default tags for all resources
  default_tags {
    tags = {
      project     = "flight-delay-prediction"
      managed-by  = "terraform"
      environment = "production"
    }
  }
}

provider "time" {
  # Configuration for time resource
}