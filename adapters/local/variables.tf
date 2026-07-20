variable "baseline_name" {
  type = string
}

variable "cidr_block" {
  type = string
}

variable "availability_zones" {
  type = list(string)
}

variable "service_image" {
  type = string
}

variable "service_replicas" {
  type = number
}

variable "service_environment" {
  type = map(string)
}

variable "log_retention_days" {
  type = number
}

variable "tags" {
  type = map(string)
}
