module "local_adapter" {
  source = "./adapters/local"

  baseline_name       = var.baseline_name
  cidr_block          = var.cidr_block
  availability_zones  = var.availability_zones
  service_image       = var.service_image
  service_replicas    = var.service_replicas
  service_environment = var.service_environment
  log_retention_days  = var.log_retention_days
  tags                = var.tags
}
