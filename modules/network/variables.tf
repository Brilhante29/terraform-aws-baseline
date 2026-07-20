variable "name" {
  type        = string
  description = "Network contract name."
}

variable "cidr_block" {
  type        = string
  description = "Network CIDR recorded in the contract."
}

variable "availability_zones" {
  type        = list(string)
  description = "Logical or provider availability zones."
}

variable "tags" {
  type        = map(string)
  description = "Network metadata."
}
