# Reuse Map: #27 terraform-aws-baseline

## Kit Inputs

| Concern | Source of truth | Project use |
|---|---|---|
| Agent skills | `.codex/skills/` and `.claude/skills/` | select by problem and language |
| Architecture | `decision-brain/` | record the module composition in SDD |
| Stack and libraries | `.portfolio/decision-brain/` | justify Terraform and stdlib against benchmark |
| Local-first cloud | `.portfolio/decision-brain/cloud-matrix.yaml` | keep local provider-free and AWS adapter replaceable |
| API style | `decision-brain/api-style-matrix.yaml` | use CLI and Terraform contracts |
| Messaging | `decision-brain/messaging-matrix.yaml` | none until measured need |
| Benchmark contract | `contracts/benchmark-result.schema.json` | emit machine-readable evidence |

## Project Delta

| Delta | Why it is project-specific or reusable | Action |
|---|---|---|
| Explicit plan-only provisioning mode and provider-free Terraform adapter | Useful distinction for future IaC benchmarks; implementation stays project-specific. | backlog in sdd/reuse-improvement-review.md |
| Kumo boundary without invented API claims | Project follows cloud rule while current scope has no emulated AWS operation. | reject for this project |

## Coupling Rule

Domain and local contract code must not depend on infrastructure adapters, providers, brokers, HTTP frameworks or vendors. Dependencies point inward through stable module variables and outputs.
