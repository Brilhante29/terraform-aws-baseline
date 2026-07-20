from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BaselineContractTests(unittest.TestCase):
    def test_local_module_graph_is_complete(self) -> None:
        for module in ("network", "service", "observability"):
            module_dir = ROOT / "modules" / module
            self.assertTrue((module_dir / "main.tf").is_file())
            self.assertTrue((module_dir / "variables.tf").is_file())
            self.assertTrue((module_dir / "outputs.tf").is_file())
            self.assertIn("terraform_data", (module_dir / "main.tf").read_text())

    def test_local_adapter_wires_all_capabilities(self) -> None:
        main = (ROOT / "adapters/local/main.tf").read_text()
        self.assertIn('source = "../../modules/network"', main)
        self.assertIn('source = "../../modules/service"', main)
        self.assertIn('source = "../../modules/observability"', main)

    def test_aws_provider_is_outside_the_default_root(self) -> None:
        self.assertNotIn("hashicorp/aws", (ROOT / "versions.tf").read_text())
        self.assertIn("hashicorp/aws", (ROOT / "adapters/aws/versions.tf").read_text())
        self.assertIn('value       = "local"', (ROOT / "outputs.tf").read_text())

    def test_fixture_is_non_secret_and_deterministic(self) -> None:
        fixture = json.loads((ROOT / "fixtures/local-baseline.auto.tfvars.json").read_text())
        self.assertEqual(fixture["baseline_name"], "fixture-baseline")
        self.assertEqual(fixture["availability_zones"], ["local-a", "local-b"])
        self.assertNotIn("access_key", json.dumps(fixture).lower())
        self.assertNotIn("secret_key", json.dumps(fixture).lower())

    def test_benchmark_contract_is_versioned(self) -> None:
        result = json.loads((ROOT / "benchmarks/results/27-local-first.json").read_text())
        self.assertEqual(result["project"], "27-terraform-aws-baseline")
        self.assertEqual(result["metric"], "provision_time_seconds")
        self.assertIn("schema_version", result)
        self.assertIn("fixture_version", result)
        self.assertIn("environment", result)


if __name__ == "__main__":
    unittest.main()
