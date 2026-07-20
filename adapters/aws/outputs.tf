output "adapter" {
  description = "Adapter selected by this configuration."
  value       = "aws"
}

output "network_id" {
  description = "AWS VPC identifier."
  value       = aws_vpc.baseline.id
}

output "subnet_ids" {
  description = "AWS subnet identifiers."
  value       = [for subnet in aws_subnet.public : subnet.id]
}

output "service_id" {
  description = "AWS ECS service identifier."
  value       = aws_ecs_service.service.id
}

output "log_group_name" {
  description = "AWS CloudWatch log group name."
  value       = aws_cloudwatch_log_group.service.name
}
