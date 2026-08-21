resource "aws_s3_bucket" "artifacts" {
  bucket        = "${var.baseline_name}-artifacts"
  force_destroy = true
}

resource "aws_sns_topic" "events" {
  name = "${var.baseline_name}-events"
  tags = var.tags
}

resource "aws_dynamodb_table" "state" {
  name         = "${var.baseline_name}-state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  tags         = var.tags

  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_cloudwatch_log_group" "service" {
  name              = "/portfolio/${var.baseline_name}"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}
