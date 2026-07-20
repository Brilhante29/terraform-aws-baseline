output "log_group_name" {
  description = "Deterministic local log group name."
  value       = local.log_group_name
}

output "contract" {
  description = "Observability contract captured by the local adapter."
  value       = terraform_data.observability.input
}
