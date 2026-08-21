output "adapter" {
  value = "kumo"
}

output "artifact_bucket" {
  value = module.baseline.artifact_bucket
}

output "event_topic_arn" {
  value = module.baseline.event_topic_arn
}

output "state_table" {
  value = module.baseline.state_table
}

output "log_group_name" {
  value = module.baseline.log_group_name
}
