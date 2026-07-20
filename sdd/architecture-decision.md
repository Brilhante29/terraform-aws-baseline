# Architecture Decision

## Status

Accepted

## Context

Project: #27 terraform-aws-baseline
Claim: local-first Terraform baseline with an explicit AWS adapter
Benchmark: provision_time_seconds

Problem forces:

- Domain complexity: low
- Integration pressure: medium
- UI state complexity: none
- Data/ML reproducibility: low
- Auditability/event history: medium
- Throughput/async pressure: low
- Independent deployability need: medium

## Decision

Chosen architecture: hexagonal module composition.

The root module is the composition boundary. The local adapter exposes the same capability outputs as the AWS adapter, while network, service and observability are separate modules with small variable and output contracts. The default root uses only Terraform builtin terraform_data, so static validation and plan are local and deterministic.

Dependency rule:

The root depends on module contracts. The local modules do not import cloud SDKs. The AWS provider and real resources exist only under adapters/aws and are never required by the default root.

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| serverless | No function or event requirement exists. |
| microservices | The artifact is one baseline, not a distributed runtime. |
| Kumo-first emulation | It would add an unneeded provider surface without a claimed AWS operation. |

## Folder Layout

~~~text
modules/{network,service,observability}/
adapters/local/
adapters/aws/
fixtures/
tests/
benchmarks/
tools/
~~~

## Testing Strategy

- Unit and contract tests: Python stdlib checks module files, adapter wiring, fixture shape and benchmark contract.
- Terraform validation: fmt, init with backend disabled and validate on the root local adapter.
- Integration boundary: AWS adapter is statically inspectable and only runs after explicit provider init.
- Benchmark: repeated validate and plan timings with no refresh and no apply.

## Consequences

Positive:

- Default path is offline after the Terraform binary is available.
- Module responsibilities are visible and independently replaceable.
- AWS credentials cannot be accidentally required by root validation.

Tradeoffs:

- terraform_data is a contract mock, not AWS emulation.
- AWS adapter needs an existing ECS execution role and real environment review.
- No remote state, IAM composition, ALB or NAT is included.

Migration path:

Add a module contract test against a pinned Kumo operation only when a concrete AWS capability is added, then keep that client behind the same adapter boundary.
