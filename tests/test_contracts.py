from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BaselineContractTests(unittest.TestCase):
    def test_shared_module_owns_every_cloud_resource(self) -> None:
        module = (ROOT / "modules/application-baseline/main.tf").read_text()
        for resource in (
            "aws_s3_bucket",
            "aws_sns_topic",
            "aws_dynamodb_table",
            "aws_cloudwatch_log_group",
        ):
            self.assertIn(resource, module)

    def test_both_adapters_depend_on_the_same_module(self) -> None:
        source = 'source = "../../modules/application-baseline"'
        self.assertIn(source, (ROOT / "adapters/kumo/main.tf").read_text())
        self.assertIn(source, (ROOT / "adapters/aws/main.tf").read_text())

    def test_kumo_is_default_without_leaking_into_aws(self) -> None:
        kumo = (ROOT / "adapters/kumo/provider.tf").read_text()
        aws = (ROOT / "adapters/aws/versions.tf").read_text()
        self.assertIn("endpoints {", kumo)
        self.assertIn("skip_credentials_validation = true", kumo)
        self.assertNotIn("endpoint_url", aws)
        self.assertNotIn('access_key = "local"', aws)

    def test_fixture_is_non_secret_and_deterministic(self) -> None:
        fixture = json.loads((ROOT / "fixtures/kumo-baseline.tfvars.json").read_text())
        self.assertEqual(fixture["baseline_name"], "fixture-baseline")
        serialized = json.dumps(fixture).lower()
        self.assertNotIn("access_key", serialized)
        self.assertNotIn("secret_key", serialized)

    def test_runtime_and_provider_versions_are_pinned(self) -> None:
        dockerfile = (ROOT / "Dockerfile").read_text()
        versions = (ROOT / "adapters/kumo/versions.tf").read_text()
        self.assertIn("kumo:0.28.1@sha256:", dockerfile)
        self.assertIn("hashicorp/terraform:1.15.8", dockerfile)
        self.assertIn('version = "5.100.0"', versions)


if __name__ == "__main__":
    unittest.main()
