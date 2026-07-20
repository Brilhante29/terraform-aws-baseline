variable "aws_region" {
  description = "AWS region used only by the opt-in adapter."
  type        = string
  default     = "us-east-1"
}

variable "baseline_name" {
  description = "Name prefix for AWS resources."
  type        = string
  default     = "baseline"
}

variable "cidr_block" {
  description = "VPC CIDR."
  type        = string
  default     = "10.42.0.0/16"
}

variable "availability_zones" {
  description = "At least two AWS availability zones."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least two availability zones are required."
  }
}

variable "service_image" {
  description = "Container image for the ECS service."
  type        = string
  default     = "public.ecr.aws/docker/library/nginx:1.27-alpine"
}

variable "service_replicas" {
  description = "Desired ECS service count."
  type        = number
  default     = 2
}

variable "service_environment" {
  description = "Non-secret container environment."
  type        = map(string)
  default     = {}
}

variable "log_retention_days" {
  description = "CloudWatch log retention."
  type        = number
  default     = 7
}

variable "execution_role_arn" {
  description = "Existing ECS task execution role ARN. The adapter does not create IAM."
  type        = string
}

variable "tags" {
  description = "Common AWS resource tags."
  type        = map(string)
  default = {
    project    = "27-terraform-aws-baseline"
    managed_by = "terraform"
  }
}
