variable "baseline_name" {
  description = "Stable prefix shared by every baseline resource."
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,31}$", var.baseline_name))
    error_message = "baseline_name must contain 3-32 lowercase letters, digits, or hyphens."
  }
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention period."
  type        = number

  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90], var.log_retention_days)
    error_message = "log_retention_days must use a supported CloudWatch retention value."
  }
}

variable "tags" {
  description = "Non-secret metadata applied to every resource."
  type        = map(string)
}
