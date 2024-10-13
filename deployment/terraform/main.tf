# Google Provider Configuration
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable necessary APIs
resource "google_project_service" "run" {
  project = var.project_id
  service = "run.googleapis.com"
}

resource "google_project_service" "cloud_build" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "storage" {
  project = var.project_id
  service = "storage.googleapis.com"
}

resource "google_project_service" "container_registry" {
  project = var.project_id
  service = "containerregistry.googleapis.com"
}

# Google Cloud Storage (GCS) bucket for data storage
resource "google_storage_bucket" "geotech_data_bucket" {
  name     = "${var.project_id}-geotech-data"
  location = var.region
}

# IAM binding to allow Cloud Run to access the GCS bucket
resource "google_storage_bucket_iam_binding" "bucket_permission" {
  bucket = google_storage_bucket.geotech_data_bucket.name
  role   = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.cloud_run_sa.email}"
  ]
}

# Create a service account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}

# Assign necessary roles to the service account
resource "google_project_iam_binding" "run_permission" {
  project = var.project_id
  role    = "roles/run.admin"
  members = [
    "serviceAccount:${google_service_account.cloud_run_sa.email}"
  ]
}

# Cloud Run service for the API
resource "google_cloud_run_service" "geotech_api" {
  name     = "geotech-api"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/geotech-api"
        ports {
          container_port = 8080
        }
      }
      service_account_name = google_service_account.cloud_run_sa.email
    }
  }

  autogenerate_revision_name = true

  metadata {
    annotations = {
      "autoscaling.knative.dev/maxScale" = "5"  # Scale limit
    }
  }
}

# Allow unauthenticated invocations for the Cloud Run service
resource "google_cloud_run_service_iam_binding" "invoker_binding" {
  service = google_cloud_run_service.geotech_api.name
  location = var.region
  role = "roles/run.invoker"
  members = ["allUsers"]
}

# Cloud Build trigger for continuous deployment
resource "google_cloudbuild_trigger" "api_deploy_trigger" {
  name = "geotech-api-deploy"

  trigger_template {
    branch_name = "main"
    project     = var.project_id
    repo_name   = "your-repo-name"  # Replace with your repo name
  }

  build {
    step {
      name = "gcr.io/cloud-builders/docker"
      args = [
        "build", "-t", "gcr.io/${var.project_id}/geotech-api", "."
      ]
    }

    step {
      name = "gcr.io/cloud-builders/docker"
      args = [
        "push", "gcr.io/${var.project_id}/geotech-api"
      ]
    }

    step {
      name = "gcr.io/cloud-builders/gcloud"
      args = [
        "run", "deploy", "geotech-api",
        "--image", "gcr.io/${var.project_id}/geotech-api",
        "--region", var.region,
        "--platform", "managed",
        "--allow-unauthenticated"
      ]
    }
  }
}

# Terraform Variables
variable "project_id" {
  description = "The GCP project ID."
}

variable "region" {
  description = "The region to deploy resources in."
  default     = "us-central1"
}

output "bucket_name" {
  value = google_storage_bucket.geotech_data_bucket.name
}

output "cloud_run_url" {
  value = google_cloud_run_service.geotech_api.status[0].url
}
