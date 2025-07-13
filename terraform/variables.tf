variable "aiven_api_token" {
  description = "API token for AIVEN."
  sensitive = true
  type =  string
}

variable "aiven_pg_user_username" {
  description = "Username of the Admin DB User"
  sensitive = true
  type = string
}
variable "aiven_pg_user_password" {
  description = "Password of the Admin DB User"
  sensitive = true
  type = string
}

variable "gcp_rfx_project_id" {
  description = "Project ID of the RuneFX Project"
  sensitive = true
  type = string
}

variable "cloudflare_api_token" {
  default = "API token for cloudflare provider"
  type = string
  sensitive = true
}
variable "cloudflare_zone_id" {
  default = "Zone ID for the cloudflare domain"
  type = string
  sensitive = true
}