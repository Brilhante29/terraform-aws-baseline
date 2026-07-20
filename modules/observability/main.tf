resource "terraform_data" "observability" {
  input = {
    name               = var.name
    service_id         = var.service_id
    log_retention_days = var.log_retention_days
    tags               = var.tags
  }
}

locals {
  log_group_name = "/local/${var.name}"
}
