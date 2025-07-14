
output "gcp_wif_provider_id" {
  description = "ID of the Workload Identity Federation provider. Output is used to auth into gcp during CI."
  value = google_iam_workload_identity_pool_provider.gcp_rfx_wif_pool_gh.id
  sensitive = true
}


output "gcp_project_id" {
  description = "ID of the project hosted on GCP. Output is used to auth into gcp during CI."
  value = var.gcp_rfx_project_id
  sensitive = true
}