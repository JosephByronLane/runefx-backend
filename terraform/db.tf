resource "aiven_organization" "aiven_runefx_org" {
  name = "RuneFX"
}

resource "aiven_project" "aiven_runefx_project" {
  project = "runefx-backend-project"
  parent_id = aiven_organization.aiven_runefx_org.id
}