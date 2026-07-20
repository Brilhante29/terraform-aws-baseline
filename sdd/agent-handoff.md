# Agent Handoff

Project: 27 - terraform-aws-baseline

## Principal Agent Summary

- Objective: Build a small local-first Terraform baseline with replaceable cloud adapters.
- Portfolio program: delivery-observability-infra.
- Public proof claim: Terraform modules can be validated and planned without AWS credentials.
- Primary benchmark: provision_time_seconds.
- Default runnable path: Docker validate, then the versioned local fixture benchmark.

## Subagent Decisions

| Role | Decision | Evidence Path | Status |
|---|---|---|---|
| program-planner | delivery-observability-infra | project.yaml | complete |
| architecture-selector | hexagonal module composition | sdd/architecture-decision.md | complete |
| engineering-principles-reviewer | dependency inversion at adapter boundary | sdd/technical-decision.md | complete |
| stack-decision-agent | Terraform plus Python stdlib | project.yaml, sdd/technical-decision.md | complete |
| api-style-agent | CLI and Terraform variable/output contracts | tests/test_contracts.py | complete |
| cloud-local-first-agent | terraform_data mock; AWS opt-in; Kumo reference only | README.md, sdd/technical-decision.md | complete |
| messaging-agent | none | sdd/technical-decision.md | complete |
| language-profile-agent | Terraform primary, Python harness | project.yaml | complete |
| benchmark-harness-agent | repeated validate and plan JSON | sdd/benchmark-plan.md, benchmarks/results/ | complete |
| design-system-agent | README graph and benchmark table | README.md | complete |
| security-reuse-reviewer | no secret default; IAM excluded from local path | REFERENCES.md, sdd/release-checklist.md | complete |
| release-ci-publisher | Docker, CI, strict validation and diff check | Dockerfile, .github/workflows/ci.yml | complete |

## Local-First Runtime

- Docker command: docker run --rm terraform-aws-baseline
- Local services: none
- Kumo services, if any: none; the local reference is recorded without invented APIs
- Real cloud adapter target, if any: AWS in adapters/aws
- Config switch: choose root local adapter or terraform -chdir=adapters/aws
- Default path requires paid secret: no

## Architecture Boundaries

- Domain boundaries: network, service and observability contracts
- Use-case boundaries: root composition and benchmark runner
- Ports: module variables and outputs
- Adapters: adapters/local and adapters/aws
- Dependency direction rule: root depends on module outputs; AWS provider is isolated in the real adapter

## Benchmark Handoff

- Metric: provision_time_seconds
- Unit: seconds
- Higher or lower is better: lower
- Command: python benchmarks/benchmark.py --repeat 3 --output benchmarks/results/27-local-first.json
- Result path: benchmarks/results/27-local-first.json
- Dataset or fixture: fixtures/local-baseline.auto.tfvars.json

## Open Risks

- AWS adapter has public subnets and requires an existing ECS execution role; review before apply.
- Local fixture is not an AWS emulator and has no resource side effects.
- Terraform provider cache or binary availability can affect timing.

## Publication Gates

- [x] Docker path works
- [x] benchmark result exists
- [x] README starts with number and claim
- [x] references are documented
- [x] no secret in files or git remote
- [x] validation passes
