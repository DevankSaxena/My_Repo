# Google Cloud Project ID
variable "project_id" {
  description = "The ID of the GCP project where resources will be deployed."
  type        = string
}

# Google Cloud region for deployment
variable "region" {
  description = "The region where resources will be deployed."
  type        = string
  default     = "us-central1"  # You can change this to your preferred region
}

# Cloud Run service name
variable "cloud_run_service_name" {
  description = "The name of the Cloud Run service."
  type        = string
  default     = "geotech-api"
}

# Storage bucket name suffix
variable "storage_bucket_suffix" {
  description = "Suffix to add to the storage bucket name."
  type        = string
  default     = "geotech-data"
}

# Maximum number of instances for the Cloud Run service
variable "max_scale" {
  description = "Maximum number of instances to scale the Cloud Run service."
  type        = number
  default     = 5
}

# Docker image tag for Cloud Run
variable "docker_image_tag" {
  description = "Docker image tag to deploy on Cloud Run."
  type        = string
  default     = "latest"
}

# Cloud Build Trigger Repository Name
variable "repo_name" {
  description = "The repository name where the Cloud Build trigger will be set up."
  type        = string
}

# Cloud Build Trigger Branch Name
variable "branch_name" {
  description = "The branch name to monitor for Cloud Build deployments."
  type        = string
  default     = "main"
}
