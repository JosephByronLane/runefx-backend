resource "google_cloud_run_v2_service" "gcp_rfx_cloud_run" {
  name     = "rfx-backend"
  location = "us-central1"
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 1
      min_instance_count = 0
    }
    containers {
      image = "docker.io/${var.dockerhub_username}/${var.dockerhub_repository}:latest" //gets overwritten by the newest once the ci pipeline runs
      name = "runefx-backend-1"
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }
    }
  }
}

resource "google_project_iam_binding" "gcp_rfx_cloud_run_iam_binding_cradmin" {
  project = var.gcp_rfx_project_id
  role    = "roles/run.admin"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gcp_rfx_wif_pool.name}/attribute.repository/${var.github_repository}"
  ]
  depends_on = [ google_iam_workload_identity_pool.gcp_rfx_wif_pool ]
}


resource "google_project_iam_binding" "gcp_rfx_cloud_run_iam_binding_satokenc" {
  project = var.gcp_rfx_project_id
  role = "roles/iam.serviceAccountTokenCreator"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gcp_rfx_wif_pool.name}/attribute.repository/${var.github_repository}"
  ]
  depends_on = [ google_iam_workload_identity_pool.gcp_rfx_wif_pool ]
}

resource "google_project_iam_binding" "gcp_rfx_cloud_run_iam_binding_sauser" {
  project = var.gcp_rfx_project_id
  role = "roles/iam.serviceAccountUser"
  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gcp_rfx_wif_pool.name}/attribute.repository/${var.github_repository}"
  ]
  depends_on = [ google_iam_workload_identity_pool.gcp_rfx_wif_pool ]
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
    "attribute.environment" = "assertion.environment"
    "attribute.repository" = "assertion.repository"
  }
  attribute_condition = "assertion.repository == '${var.github_repository}'"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
  depends_on = [ google_iam_workload_identity_pool.gcp_rfx_wif_pool ]
}


resource "google_cloud_run_domain_mapping" "gcp_rfx_run_domain_mapping" {
  location = "us-central1"
  name = "api.runefx.org"
  metadata {
    namespace = var.gcp_rfx_project_id
  }
  spec {
    route_name = google_cloud_run_v2_service.gcp_rfx_cloud_run.name
  }
}