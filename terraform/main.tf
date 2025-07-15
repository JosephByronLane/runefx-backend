terraform {
  required_providers {
    aiven = {
      source = "aiven/aiven"
      version = ">= 4.0.0, < 5.0.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~>4.25"
    }
  }
}

//postgres db in aiven free tier
provider "aiven" {
  api_token = var.aiven_api_token
}


//backend service in gcp run
provider "google" {
  project     = var.gcp_rfx_project_id //we need an org to be able to create projects dynamically, as we dont, we gotta create it manualy
  region      = "us-central1"
}

//cf for dns
provider "cloudflare" {
  api_token = var.cloudflare_api_token  
}