resource "google_cloud_run_v2_service" "gcp_rfx_cloud_run" {
  name     = "rfx-backend"
  location = "us-central1"
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" //gets overwritten once the ci pipeline runs
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}

resource "google_service_account" "gcp_rfx_cloud_run_sa" {
  account_id = "cloud-run-admin"
  display_name = "Cloud Run Admin"
}

resource "google_project_iam_binding" "gcp_rfx_cloud_run_iam_binding" {
  project = var.gcp_rfx_project_id
  role = "roles/run.admin"
  members = [
    "serviceAccount:${google_service_account.gcp_rfx_cloud_run_sa.email}"
  ]
}

resource "google_iam_workload_identity_pool" "gcp_rfx_wif_pool" {
  workload_identity_pool_id = "rfx-wif-pool-prod"
  display_name = "rfx-wif-pool-prod"
}

resource "google_iam_workload_identity_pool_provider" "gcp_rfx_wif_pool_gh" {
  workload_identity_pool_id = google_iam_workload_identity_pool.gcp_rfx_wif_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "gh-provider"
  display_name = "Github Provider"
  attribute_mapping = {
    "google.subject" = "assertion.sub"
  }
  attribute_condition = "assertion.repository_id == ${var.github_repository}"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

}