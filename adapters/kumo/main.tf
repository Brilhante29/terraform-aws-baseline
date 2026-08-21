module "baseline" {
  source = "../../modules/application-baseline"

  baseline_name      = var.baseline_name
  log_retention_days = var.log_retention_days
  tags               = var.tags
}
