resource "cloudflare_record" "cloudflare_rfx_site_www_record" {
  zone_id = var.cloudflare_zone_id
  name    = "api"
  type = "CNAME"
  content = replace(google_cloud_run_v2_service.gcp_rfx_cloud_run.uri, "https://", "") //uri returns url with https
  proxied = true
  ttl     = 1

  depends_on = [ google_cloud_run_v2_service.gcp_rfx_cloud_run ]
}