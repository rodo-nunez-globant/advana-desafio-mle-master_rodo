# Remote state configuration using GCS bucket
# This bucket should already exist: rodo-nunez-challenge-latam-data
terraform {
  backend "gcs" {
    bucket = "rodo-nunez-challenge-latam-data"
    prefix = "terraform/state"
    
    # Optional: Enable state locking
    # Note: This requires the Cloud Storage API to be enabled
  }
}

# Note: Make sure the GCS bucket has the following:
# 1. Versioning enabled (for state history)
# 2. Uniform bucket-level access
# 3. Appropriate IAM permissions for the user running Terraform