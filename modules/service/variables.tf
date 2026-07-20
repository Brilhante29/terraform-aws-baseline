variable "name" {
  type        = string
  description = "Service contract name."
}

variable "image" {
  type        = string
  description = "Container image recorded by the service contract."
}

variable "replicas" {
  type        = number
  description = "Desired replica count."
}

variable "network_id" {
  type        = string
  description = "Network contract identifier."
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet contract identifiers."
}

variable "environment" {
  type        = map(string)
  description = "Non-secret service environment."
}

variable "tags" {
  type        = map(string)
  description = "Service metadata."
}
