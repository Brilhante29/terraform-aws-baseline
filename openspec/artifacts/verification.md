# Verification: #27 terraform-aws-baseline

## Evidence

- Terraform root uses only the builtin terraform_data resource.
- Local adapter composes network, service and observability modules.
- AWS provider is isolated under adapters/aws.
- Fixture is versioned at fixtures/local-baseline.auto.tfvars.json.
- Benchmark result is benchmarks/results/27-local-first.json.
- Docker and CI commands are documented.

## Required checks

- [x] README opens with #27 and states the measured artifact.
- [x] project.yaml contains the selected program, architecture, cloud mode and metric.
- [x] SDD records scope, rejected alternatives, coupling and testability.
- [x] Contract tests cover module graph, adapter split, fixture and benchmark schema.
- [x] Default path requires no AWS credentials.
- [x] Kumo is referenced without invented APIs or conformance claims.
- [x] Real AWS instructions are explicit and opt-in.
- [x] Reuse review records patch-now, backlog or reject decisions.
- [x] Benchmark JSON is versioned and includes metadata.
