output "artifact_bucket" {
  value = aws_s3_bucket.artifacts.id
}

output "event_topic_arn" {
  value = aws_sns_topic.events.arn
}

output "state_table" {
  value = aws_dynamodb_table.state.name
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.service.name
}
