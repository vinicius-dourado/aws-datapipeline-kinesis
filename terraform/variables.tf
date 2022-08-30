variable "region" {
  description = "aws region"
  default     = "us-east-1"
}

variable "account_id" {
  default = 304816653859
}

variable "environment" {
  default = "dev"
}

variable "prefix" {
  description = "objects prefix"
  default     = "trips"
}

# Prefix configuration and project common tags
locals {
  prefix = var.prefix
  common_tags = {
    Environment = "dev"
    Project     = "aws-trips"
  }
}

variable "bucket_names" {
  description = "s3 bucket names"
  type        = list(string)
  default = [
    "landing-zone",
    "processed-layer",
    "presentation-layer",
    "kinesis",
    "scripts"
  ]
}
