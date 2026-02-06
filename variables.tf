variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "ccs6344-a2-library"
}

variable "db_username" {
  type    = string
  default = "adminuser"
}

variable "db_password" {
  type      = string
  sensitive = true
}
