output "network_id" {
  value = module.network.network_id
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}

output "service_id" {
  value = module.service.service_id
}

output "log_group_name" {
  value = module.observability.log_group_name
}
