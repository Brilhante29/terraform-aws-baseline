# Portfolio Control: #27 terraform-aws-baseline

## Identity

- **Program:** delivery-observability-infra
- **Status:** benchmarked
- **Proves:** local-first Terraform baseline with an explicit AWS adapter
- **Primary benchmark:** `provision_time_seconds`

## Evidence Map

| Evidence | Location | State |
|---|---|---|
| Specification | `sdd/spec.md` | complete |
| Architecture decision | `sdd/architecture-decision.md` | complete |
| Benchmark plan | `sdd/benchmark-plan.md` | complete |
| Benchmark result | `benchmarks/results/27-local-first.json` | complete |
| OpenSpec verification | `openspec/artifacts/verification.md` | complete |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |
| Docker and CI | `Dockerfile`, `.github/workflows/ci.yml` | complete |

This inventory preserves the project-level control contract and points to the implemented proof artifacts.
