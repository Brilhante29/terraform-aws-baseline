output "adapter" {
  description = "Adapter selected by this root module."
  value       = "local"
}

output "network_id" {
  description = "Stable local network contract identifier."
  value       = module.local_adapter.network_id
}

output "private_subnet_ids" {
  description = "Stable local subnet contract identifiers."
  value       = module.local_adapter.private_subnet_ids
}

output "service_id" {
  description = "Stable local service contract identifier."
  value       = module.local_adapter.service_id
}

output "log_group_name" {
  description = "Stable local log group contract name."
  value       = module.local_adapter.log_group_name
}
