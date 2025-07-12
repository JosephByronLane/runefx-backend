terraform {
  required_providers {
    aiven = {
      source = "aiven/aiven"
      version = ">= 4.0.0, < 5.0.0"
    }
  }
}

//postgres db in aiven
provider "aiven" {
  api_token = var.aiven_api_token
}


//backend service in gcp run