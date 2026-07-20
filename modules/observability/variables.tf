variable "name" {
  type        = string
  description = "Observability contract name."
}

variable "service_id" {
  type        = string
  description = "Service contract identifier."
}

variable "log_retention_days" {
  type        = number
  description = "Requested log retention."
}

variable "tags" {
  type        = map(string)
  description = "Observability metadata."
}
