provider "aws" {
  region                      = var.aws_region
  access_key                  = "local"
  secret_key                  = "local"
  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true

  endpoints {
    cloudwatchlogs = var.endpoint_url
    dynamodb       = var.endpoint_url
    s3             = var.endpoint_url
    sns            = var.endpoint_url
  }
}
