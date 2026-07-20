variable "baseline_name" {
  description = "Stable name used by every module in the baseline."
  type        = string
  default     = "baseline"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,31}$", var.baseline_name))
    error_message = "baseline_name must be 3-32 lowercase letters, digits, or hyphens."
  }
}

variable "cidr_block" {
  description = "Network CIDR used by the local contract and AWS adapter."
  type        = string
  default     = "10.42.0.0/16"
}

variable "availability_zones" {
  description = "Logical zones for the network module. Local mode does not create subnets."
  type        = list(string)
  default     = ["local-a", "local-b"]

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least two availability zones are required."
  }
}

variable "service_image" {
  description = "Container image recorded by the service contract."
  type        = string
  default     = "example/service:1.0.0"
}

variable "service_replicas" {
  description = "Desired service replica count."
  type        = number
  default     = 2

  validation {
    condition     = var.service_replicas >= 1 && floor(var.service_replicas) == var.service_replicas
    error_message = "service_replicas must be a positive whole number."
  }
}

variable "service_environment" {
  description = "Non-secret environment values passed to the service contract."
  type        = map(string)
  default = {
    MODE = "local"
  }
}

variable "log_retention_days" {
  description = "Retention requested by the observability module."
  type        = number
  default     = 7

  validation {
    condition     = var.log_retention_days >= 1 && floor(var.log_retention_days) == var.log_retention_days
    error_message = "log_retention_days must be a positive whole number."
  }
}

variable "tags" {
  description = "Common metadata for the local contract and AWS adapter."
  type        = map(string)
  default = {
    project    = "27-terraform-aws-baseline"
    managed_by = "terraform"
  }
}
