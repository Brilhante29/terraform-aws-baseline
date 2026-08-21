# Architecture decision: shared module with provider adapters

## Status

Accepted

## Context

The original implementation used `terraform_data` as a local fake and duplicated AWS resources in a separate root. It validated quickly but did not prove provisioning, Kumo usage, or behavioral substitutability.

## Decision

Use a hexagonal infrastructure boundary:

- `modules/application-baseline` is the stable port and owns every resource declaration.
- `adapters/kumo` configures the AWS provider for local Kumo endpoints.
- `adapters/aws` configures the same provider for real AWS.
- `benchmarks/benchmark.py` is the lifecycle harness and asserts resource parity.

Dependencies point inward from adapters to the module. No Kumo endpoint, fake credential, benchmark concern, or environment policy appears in the shared module.

## SOLID and simplicity

- SRP: module intent, local provider, real provider, and evidence have distinct owners.
- OCP: another AWS-compatible adapter can reuse the module without changing its resources.
- LSP: both adapters expose `adapter`, bucket, topic, table, and log-group outputs.
- ISP: the module accepts only name, retention, and tags.
- DIP: environment details depend on the module contract, not the reverse.
- KISS/YAGNI: four capabilities are enough; remote state and landing-zone concerns remain outside scope.

## Consequences

The local path now downloads the AWS provider and the image is larger, but it proves real provider calls. Kumo gaps must be documented rather than hidden. AWS apply remains an explicit, reviewed operation.

## Rejected alternatives

| Alternative | Reason |
|---|---|
| `terraform_data` local fake | Does not exercise provider APIs or Kumo. |
| Duplicated Kumo/AWS modules | Creates drift and weakens substitution evidence. |
| LocalStack | Conflicts with the portfolio's selected Kumo-first standard. |
| Full landing zone | Too broad for one reproducible benchmark and requires account policy decisions. |
