resource "aiven_organization" "aiven_runefx_org" {
  name = "RuneFX"
}

resource "aiven_project" "aiven_runefx_project" {
  project = "runefx-backend-project"
  parent_id = aiven_organization.aiven_runefx_org.id
}

resource "aiven_pg" "aiven_runefx_pg" {
  project = aiven_project.aiven_runefx_project.id
  plan = "free-1-1gb"
  service_name = "rfx-pg"
  
  cloud_name = "upcloud-us-nyc"

  pg_user_config {
    admin_password = var.aiven_pg_user_password
    admin_username = var.aiven_pg_user_username
  }
}

