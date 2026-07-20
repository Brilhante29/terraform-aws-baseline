output "service_id" {
  description = "Deterministic local service identifier."
  value       = local.service_id
}

output "contract" {
  description = "Service contract captured by the local adapter."
  value       = terraform_data.service.input
}
