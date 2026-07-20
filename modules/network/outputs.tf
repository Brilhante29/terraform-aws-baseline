output "network_id" {
  description = "Deterministic local network identifier."
  value       = local.network_id
}

output "private_subnet_ids" {
  description = "Deterministic local subnet identifiers."
  value       = local.subnet_ids
}

output "contract" {
  description = "Network contract captured by the local adapter."
  value       = terraform_data.network.input
}
