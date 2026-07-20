resource "terraform_data" "service" {
  input = {
    name        = var.name
    image       = var.image
    replicas    = var.replicas
    network_id  = var.network_id
    subnet_ids  = var.subnet_ids
    environment = var.environment
    tags        = var.tags
  }
}

locals {
  service_id = "local-service-${var.name}-${substr(sha1(jsonencode(terraform_data.service.input)), 0, 10)}"
}
