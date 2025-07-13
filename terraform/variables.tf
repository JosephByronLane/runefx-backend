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