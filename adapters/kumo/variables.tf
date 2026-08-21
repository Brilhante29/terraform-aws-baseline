variable "endpoint_url" {
  description = "Kumo AWS-compatible endpoint."
  type        = string
  default     = "http://127.0.0.1:4566"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "baseline_name" {
  type    = string
  default = "portfolio-baseline"
}

variable "log_retention_days" {
  type    = number
  default = 7
}

variable "tags" {
  type = map(string)
  default = {
    project    = "terraform-aws-baseline"
    managed_by = "terraform"
    runtime    = "kumo"
  }
}
