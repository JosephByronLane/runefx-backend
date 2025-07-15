//aiven
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


//gcp
variable "gcp_rfx_project_id" {
  description = "Project ID of the RuneFX Project"
  sensitive = true
  type = string
}



//cloudflare
variable "cloudflare_api_token" {
  description = "API token for cloudflare provider"
  type = string
  sensitive = true
}
variable "cloudflare_zone_id" {
  description = "Zone ID for the cloudflare domain"
  type = string
  sensitive = true
}



//gh
variable "github_repository" {
  description = "Repository in github with format owner-name/repository-name"
  type = string
}


///docker
variable "dockerhub_username" {
  description = "Username of the dockerhub account where the iamge is hosted"
  type = string
}

variable "dockerhub_repository" {
  description = "Name of the repository where the docker image is hosted"
  type = string
}