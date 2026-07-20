module "network" {
  source = "../../modules/network"

  name               = var.baseline_name
  cidr_block         = var.cidr_block
  availability_zones = var.availability_zones
  tags               = var.tags
}

module "service" {
  source = "../../modules/service"

  name        = var.baseline_name
  image       = var.service_image
  replicas    = var.service_replicas
  network_id  = module.network.network_id
  subnet_ids  = module.network.private_subnet_ids
  environment = var.service_environment
  tags        = var.tags
}

module "observability" {
  source = "../../modules/observability"

  name               = var.baseline_name
  service_id         = module.service.service_id
  log_retention_days = var.log_retention_days
  tags               = var.tags
}
