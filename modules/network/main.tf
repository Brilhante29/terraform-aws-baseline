resource "terraform_data" "network" {
  input = {
    name               = var.name
    cidr_block         = var.cidr_block
    availability_zones = var.availability_zones
    tags               = var.tags
  }
}

locals {
  contract_suffix = substr(sha1(jsonencode(terraform_data.network.input)), 0, 10)
  network_id      = "local-network-${var.name}-${local.contract_suffix}"
  subnet_ids = [
    for index, zone in var.availability_zones :
    "local-subnet-${var.name}-${index + 1}-${replace(zone, "-", "")}"
  ]
}
