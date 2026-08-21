variable "aws_region" {
  description = "AWS region used only by the opt-in real-cloud adapter."
  type        = string
  default     = "us-east-1"
}

variable "baseline_name" {
  description = "Stable prefix shared by every baseline resource."
  type        = string
  default     = "portfolio-baseline"
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention period."
  type        = number
  default     = 7
}

variable "tags" {
  description = "Common AWS resource tags."
  type        = map(string)
  default = {
    project    = "terraform-aws-baseline"
    managed_by = "terraform"
    runtime    = "aws"
  }
}
